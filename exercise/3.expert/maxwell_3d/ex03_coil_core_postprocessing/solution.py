"""演習3: コイル・コア電磁石 インダクタンスデータのPython後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modules.boundary.maxwell_boundary import MatrixMagnetostatic, SourceMagnetostatic

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 条件CSV（conditions.csv）を読み込む
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
amp_turns = float(condition["amp_turns"])
core_r_mm = float(condition["core_r_mm"])

# 2. Maxwell3d を Magnetostatic ソリューションで起動する
m3d = Maxwell3d(
    design="coil_core_electromagnet",
    solution_type="Magnetostatic",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 3. コア用の磁性材料を作る（hard/normalと同じモデル。巻数相当の起磁力・コア半径はCSVから取得）
core_steel = m3d.materials.add_material(name="core_steel")
core_steel.conductivity = 2000000
core_steel.permeability.value = 1000

m3d["core_r"] = f"{core_r_mm}mm"
m3d["core_h"] = "40mm"
m3d["coil_ri"] = "15mm"
m3d["coil_ro"] = "25mm"
m3d["coil_h"] = "20mm"
m3d["amp_turns"] = f"{amp_turns}A"

m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-core_h/2"],
    radius="core_r",
    height="core_h",
    name="Core",
    material=core_steel.name,
)

m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-coil_h/2"],
    radius="coil_ro",
    height="coil_h",
    name="Coil",
    material="copper",
)
m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-coil_h/2"],
    radius="coil_ri",
    height="coil_h",
    name="Coil_hole",
    material="copper",
)
m3d.modeler.subtract(blank_list=["Coil"], tool_list=["Coil_hole"], keep_originals=False)

m3d.modeler.create_region(pad_value=[100, 100, 100, 100, 100, 100], pad_type="Percentage Offset", name="Region")

m3d.modeler.section(assignment="Coil", plane="ZX")
m3d.modeler.separate_bodies(["Coil_Section1"])
m3d.modeler.delete("Coil_Section1_Separate1")

m3d.assign_coil(assignment=["Coil_Section1"], conductors_number=1, polarity="Positive", name="CoilTerminal")

m3d.assign_winding(assignment=None, winding_type="Current", is_solid=True, current="amp_turns", name="Winding1")
m3d.add_winding_coils(assignment="Winding1", coils=["CoilTerminal"])

sources = [SourceMagnetostatic(name="Winding1")]
matrix_args = MatrixMagnetostatic(signal_sources=sources, group_sources=[], matrix_name="Matrix1")
m3d.assign_matrix(matrix_args)

# 4. セットアップを作成する
setup = m3d.create_setup(name="MySetup")
setup.props["MaximumPasses"] = 6
setup.props["MinimumPasses"] = 2
setup.props["MinimumConvergedPasses"] = 1
setup.props["PercentError"] = 1
setup.props["PercentRefinement"] = 30

# 5. 解析を実行する
setup.analyze()

# 6. 自己インダクタンスのSolutionDataを取得する
solution_data = m3d.post.get_solution_data(
    expressions=["Matrix1.L(Winding1,Winding1)"],
)
_, inductance_h = solution_data.get_expression_data(expression="Matrix1.L(Winding1,Winding1)", formula="real")

# 7. 条件・インダクタンスの値をCSVファイルに出力する
with open(script_dir / "results_inductance.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["amp_turns", "core_r_mm", "inductance_h"])
    writer.writerow([amp_turns, core_r_mm, inductance_h[0]])

# 8. コア表面のB磁束密度（Mag_B）のフィールドプロットを作成する
m3d.post.create_fieldplot_surface(
    assignment="Core",
    quantity="Mag_B",
    setup=f"{setup.name} : LastAdaptive",
    plot_name="CoreMagB",
)

# 9. フィールドプロットを PyVista で画像出力する
m3d.post.plot_field_from_fieldplot(
    plot_name="CoreMagB",
    project_path=str(script_dir),
    image_format="png",
    view="isometric",
    log_scale=True,
    show=False,
)

# 10. 同じフィールドプロットをインタラクティブなPyVistaウィンドウで表示する
m3d.post.plot_field_from_fieldplot(
    plot_name="CoreMagB",
    view="isometric",
    log_scale=True,
    show=True,
)

# 11. 保存して終了する
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)
