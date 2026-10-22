"""演習3: コイル・コア電磁石（インダクタンスレポート、Bフィールドプロット）。"""

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modules.boundary.maxwell_boundary import MatrixMagnetostatic, SourceMagnetostatic

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Maxwell3d を Magnetostatic ソリューションで起動する
m3d = Maxwell3d(
    design="coil_core_electromagnet",
    solution_type="Magnetostatic",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 2. コア用の磁性材料を作る（比透磁率1000の線形材料として簡略化）
core_steel = m3d.materials.add_material(name="core_steel")
core_steel.conductivity = 2000000
core_steel.permeability.value = 1000

# 3. 寸法をデザイン変数として定義する
m3d["core_r"] = "10mm"
m3d["core_h"] = "40mm"
m3d["coil_ri"] = "15mm"
m3d["coil_ro"] = "25mm"
m3d["coil_h"] = "20mm"
m3d["amp_turns"] = "1000A"

# 4. コア（Z軸中心の円柱）を作成する
m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-core_h/2"],
    radius="core_r",
    height="core_h",
    name="Core",
    material=core_steel.name,
)

# 5. コイル（外円柱から内円柱をsubtractして円環にする）を作成する
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

# 6. 解析領域（Region）を作成する
m3d.modeler.create_region(pad_value=[100, 100, 100, 100, 100, 100], pad_type="Percentage Offset", name="Region")

# 7. コイルをZX平面で断面切断し、片側だけを残して電流を流す断面を作る
m3d.modeler.section(assignment="Coil", plane="ZX")
m3d.modeler.separate_bodies(["Coil_Section1"])
m3d.modeler.delete("Coil_Section1_Separate1")

# 8. 断面にコイルターミナルを割り当てる
m3d.assign_coil(assignment=["Coil_Section1"], conductors_number=1, polarity="Positive", name="CoilTerminal")

# 9. Windingを作成し、コイルターミナルを紐付ける
m3d.assign_winding(assignment=None, winding_type="Current", is_solid=True, current="amp_turns", name="Winding1")
m3d.add_winding_coils(assignment="Winding1", coils=["CoilTerminal"])

# 10. インダクタンス計算のためにMatrixをWindingに割り当てる
sources = [SourceMagnetostatic(name="Winding1")]
matrix_args = MatrixMagnetostatic(signal_sources=sources, group_sources=[], matrix_name="Matrix1")
m3d.assign_matrix(matrix_args)

# 11. セットアップを作成する
setup = m3d.create_setup(name="MySetup")
setup.props["MaximumPasses"] = 6
setup.props["MinimumPasses"] = 2
setup.props["MinimumConvergedPasses"] = 1
setup.props["PercentError"] = 1
setup.props["PercentRefinement"] = 30

# 12. 解析を実行する
setup.analyze()

# 13. 自己インダクタンス Matrix1.L(Winding1,Winding1) をデータテーブルレポートとして作成する
m3d.post.create_report(
    expressions=["Matrix1.L(Winding1,Winding1)"],
    plot_type="Data Table",
    plot_name="Inductance",
)

# 14. コア表面のB磁束密度（Mag_B）のフィールドプロットを作成する
m3d.post.create_fieldplot_surface(
    assignment="Core",
    quantity="Mag_B",
    setup=f"{setup.name} : LastAdaptive",
    plot_name="CoreMagB",
)

# 15. 保存して終了する
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)
