"""演習2: TEAM7非対称導体 実測データとの比較（CSV入出力・PyVista可視化）。"""

import csv
from math import sqrt
from pathlib import Path

import numpy as np

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 公開実測データ（team7_measured_bz.csv）を読み込む
measured_distance_mm = []
measured_bz_a1b1 = []
measured_bz_a2b2 = []
with open(script_dir / "team7_measured_bz.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        measured_distance_mm.append(float(row["distance_mm"]))
        measured_bz_a1b1.append(float(row["bz_a1b1_gauss"]))
        measured_bz_a2b2.append(float(row["bz_a2b2_gauss"]))

# 2. Maxwell3d を EddyCurrent ソリューションで起動する（hardと同じモデル）
m3d = Maxwell3d(
    design="TEAM_7_Asymmetric_Conductor",
    solution_type="EddyCurrent",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 3. セットアップを作成する（200Hzに加え、50Hzもスイープ点として追加する）
setup = m3d.create_setup(name="Setup1")
setup.props["Frequency"] = "200Hz"
setup.props["HasSweepSetup"] = True
setup.add_eddy_current_sweep(sweep_type="SinglePoints", start_frequency=50, units="Hz", clear=True)

# 4. コイルの寸法を定義する（TEAM7図面の値）
coil_external = 150 + 25 + 25
coil_internal = 150
coil_r1 = 25
coil_r2 = 50
coil_thk = coil_r2 - coil_r1
coil_height = 100
coil_centre = [294 - 25 - 150 / 2, 25 + 150 / 2, 19 + 30 + 100 / 2]

dim1 = coil_internal / 2 + (coil_external - coil_internal) / 4
dim2 = coil_internal / 2 - coil_r1
dim3 = dim2 + sqrt(((coil_r1 + (coil_r2 - coil_r1) / 2) ** 2) / 2)

# 5. コイルの4分の1形状をポリラインで描画し、90度回転複製して全体を作る
P1 = [dim1, -dim2, 0]
P2 = [dim1, dim2, 0]
P3 = [dim3, dim3, 0]
P4 = [dim2, dim1, 0]

m3d.modeler.create_coordinate_system(origin=coil_centre, mode="view", view="XY", name="Coil_CS")

quarter_coil_centroid = m3d.modeler.create_polyline(
    points=[P1, P2, P3, P4],
    segment_type=["Line", "Arc"],
    name="Coil",
)
quarter_coil_centroid.set_crosssection_properties(section="Rectangle", width=coil_thk, height=coil_height)

m3d.modeler.duplicate_around_axis(
    assignment="Coil",
    axis="Global",
    angle=90,
    clones=4,
    create_new_objects=True,
    is_3d_comp=False,
)
m3d.modeler.unite("Coil, Coil_1, Coil_2")
m3d.modeler.unite("Coil, Coil_3")
m3d.modeler.fit_all()

m3d.assign_material(assignment="Coil", material="Copper")
m3d.solve_inside("Coil")

m3d.modeler.section(assignment="Coil", plane="YZ")
m3d.modeler.separate_bodies(assignment="Coil_Section1")
m3d.modeler.delete(assignment="Coil_Section1_Separate1")

Coil_Excitation = 2742
m3d["Coil_Excitation"] = str(Coil_Excitation) + "A"
m3d.assign_current(assignment="Coil_Section1", amplitude="Coil_Excitation", solid=False)
m3d.modeler.set_working_coordinate_system("Global")

mat = m3d.materials.add_material("team7_aluminium")
mat.conductivity = 3.526e7

plate = m3d.modeler.create_box(origin=[0, 0, 0], sizes=[294, 294, 19], name="Plate", material="team7_aluminium")
m3d.modeler.fit_all()
hole = m3d.modeler.create_box(origin=[18, 18, 0], sizes=[108, 108, 19], name="Hole")
m3d.modeler.subtract(blank_list="Plate", tool_list=["Hole"], keep_originals=False)

m3d.modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=100)

m3d.eddy_effects_on(assignment=["Coil"], enable_eddy_effects=False)
m3d.eddy_effects_on(assignment=["Plate"], enable_displacement_current=False)

# 6. 解析を実行する
setup.analyze()

# 7. $B_z$（磁束密度Z成分、Gauss換算）を評価するFields Calculator式を定義する
bz = {
    "name": "Bz",
    "description": "Z component of B in Gauss",
    "design_type": ["Maxwell 3D"],
    "fields_type": ["Fields"],
    "primary_sweep": "Distance",
    "assignment": "",
    "assignment_type": ["Line"],
    "operations": [
        "NameOfExpression('<Bx,By,Bz>')",
        "Operation('ScalarZ')",
        "Scalar_Function(FuncValue='Phase')",
        "Operation('AtPhase')",
        "Scalar_Constant(10000)",
        "Operation('*')",
        "Operation('Smooth')",
    ],
    "report": ["Field_3D"],
}
m3d.post.fields_calculator.add_expression(bz, None)

# 8. 評価用のラインを作成する（実測データと同じ2本）
lines = ["Line_A1_B1", "Line_A2_B2"]
mesh_diameter = "2mm"

line_points_1 = [["0mm", "72mm", "34mm"], ["288mm", "72mm", "34mm"]]
m3d.modeler.create_polyline(points=line_points_1, name=lines[0], non_model=True)
l1_mesh = m3d.modeler.create_polyline(points=line_points_1, name=lines[0] + "mesh", non_model=True)
l1_mesh.set_crosssection_properties(section="Circle", width=mesh_diameter)

line_points_2 = [["0mm", "144mm", "34mm"], ["288mm", "144mm", "34mm"]]
m3d.modeler.create_polyline(points=line_points_2, name=lines[1], non_model=True)
l2_mesh = m3d.modeler.create_polyline(points=line_points_2, name=lines[1] + "mesh", non_model=True)
l2_mesh.set_crosssection_properties(section="Circle", width=mesh_diameter)

# 9. 200Hz・位相0度における、各ラインに沿った$|B_z|$のSolutionDataを取得する
variations = {"Distance": ["All"], "Freq": ["200Hz"], "Phase": ["0deg"]}
solution_a1b1 = m3d.post.get_solution_data(
    expressions="mag(Bz)",
    variations=variations,
    primary_sweep_variable="Distance",
    report_category="Fields",
    context=lines[0],
)
solution_a2b2 = m3d.post.get_solution_data(
    expressions="mag(Bz)",
    variations=variations,
    primary_sweep_variable="Distance",
    report_category="Fields",
    context=lines[1],
)
sim_distance_a1b1, sim_bz_a1b1 = solution_a1b1.get_expression_data(expression="mag(Bz)", formula="real")
sim_distance_a2b2, sim_bz_a2b2 = solution_a2b2.get_expression_data(expression="mag(Bz)", formula="real")

# 10. シミュレーション結果（連続的な距離サンプル）を、実測データと同じ距離点に補間する
# 注意: AEDTが返すDistance軸の単位（m/mm）は実行環境・バージョンによって変わりうるため、
# 実行結果を確認し、必要なら measured_distance_mm の単位変換（mm<->m）を調整すること。
sim_bz_a1b1_at_measured = np.interp(measured_distance_mm, sim_distance_a1b1, sim_bz_a1b1)
sim_bz_a2b2_at_measured = np.interp(measured_distance_mm, sim_distance_a2b2, sim_bz_a2b2)

# 11. シミュレーション値・実測値・誤差をCSVファイルに出力する
with open(script_dir / "results_benchmark_comparison.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "distance_mm",
            "bz_a1b1_sim_gauss",
            "bz_a1b1_measured_gauss",
            "bz_a2b2_sim_gauss",
            "bz_a2b2_measured_gauss",
        ]
    )
    for row in zip(
        measured_distance_mm,
        sim_bz_a1b1_at_measured,
        measured_bz_a1b1,
        sim_bz_a2b2_at_measured,
        measured_bz_a2b2,
    ):
        writer.writerow(row)

# 12. シミュレーション結果と実測値をmatplotlibで重ね描きする
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(measured_distance_mm, sim_bz_a1b1_at_measured, "o-", label="Simulation")
axes[0].plot(measured_distance_mm, measured_bz_a1b1, "x--", label="Measured (TEAM7)")
axes[0].set_title("Bz along Line A1-B1")
axes[0].set_xlabel("Distance [mm]")
axes[0].set_ylabel("Bz [Gauss]")
axes[0].legend()

axes[1].plot(measured_distance_mm, sim_bz_a2b2_at_measured, "o-", label="Simulation")
axes[1].plot(measured_distance_mm, measured_bz_a2b2, "x--", label="Measured (TEAM7)")
axes[1].set_title("Bz along Line A2-B2")
axes[1].set_xlabel("Distance [mm]")
axes[1].legend()

fig.tight_layout()
fig.savefig(script_dir / "benchmark_comparison.png")

# 13. 板表面のB磁束密度（Mag_B）のフィールドプロットを作成し、PyVistaで表示する
m3d.post.create_fieldplot_surface(
    assignment=plate.name,
    quantity="Mag_B",
    setup="Setup1 : LastAdaptive",
    intrinsics={"Freq": "200Hz", "Phase": "0deg"},
    plot_name="PlateMagB",
)
m3d.post.plot_field_from_fieldplot(
    plot_name="PlateMagB",
    project_path=str(script_dir),
    image_format="png",
    view="isometric",
    log_scale=True,
    show=False,
)
m3d.post.plot_field_from_fieldplot(
    plot_name="PlateMagB",
    view="isometric",
    log_scale=True,
    show=True,
)

# 14. 保存して終了する
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)
