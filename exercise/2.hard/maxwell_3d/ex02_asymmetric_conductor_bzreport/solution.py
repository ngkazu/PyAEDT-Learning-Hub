"""演習2: TEAM7非対称導体（$B_z$ラインレポート）。"""

from math import sqrt

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Maxwell3d を EddyCurrent ソリューションで起動する
m3d = Maxwell3d(
    design="TEAM_7_Asymmetric_Conductor",
    solution_type="EddyCurrent",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 2. セットアップを作成する（normalの200Hzに加え、実測値比較用の50Hzをスイープ点として追加する）
setup = m3d.create_setup(name="Setup1")
setup.props["Frequency"] = "200Hz"
setup.props["HasSweepSetup"] = True
setup.add_eddy_current_sweep(sweep_type="SinglePoints", start_frequency=50, units="Hz", clear=True)

# 3. コイルの寸法を定義する（TEAM7図面の値）
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

# 4. コイルの4分の1形状をポリラインで描画し、ローカル座標系を基準に90度回転複製して全体を作る
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

# 5. コイルに銅を割り当て、内部にも電磁界解を求めるよう設定する
m3d.assign_material(assignment="Coil", material="Copper")
m3d.solve_inside("Coil")

# 6. コイルの断面を半分に切り、ターミナル（電流励振面）を作る
m3d.modeler.section(assignment="Coil", plane="YZ")
m3d.modeler.separate_bodies(assignment="Coil_Section1")
m3d.modeler.delete(assignment="Coil_Section1_Separate1")

# 7. コイルに電流励振を割り当てる（巻数込みのアンペア・ターンを変数化）
Coil_Excitation = 2742
m3d["Coil_Excitation"] = str(Coil_Excitation) + "A"
m3d.assign_current(assignment="Coil_Section1", amplitude="Coil_Excitation", solid=False)
m3d.modeler.set_working_coordinate_system("Global")

# 8. アルミ板用の専用材料を追加する
mat = m3d.materials.add_material("team7_aluminium")
mat.conductivity = 3.526e7

# 9. 中央に矩形の穴が開いたアルミ板を作成する
plate = m3d.modeler.create_box(origin=[0, 0, 0], sizes=[294, 294, 19], name="Plate", material="team7_aluminium")
m3d.modeler.fit_all()
hole = m3d.modeler.create_box(origin=[18, 18, 0], sizes=[108, 108, 19], name="Hole")
m3d.modeler.subtract(blank_list="Plate", tool_list=["Hole"], keep_originals=False)

# 10. 解析領域（Region）を作成する
m3d.modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=100)

# 11. 渦電流・変位電流の有無を設定する（コイルは渦電流なし、板は変位電流なし）
m3d.eddy_effects_on(assignment=["Coil"], enable_eddy_effects=False)
m3d.eddy_effects_on(assignment=["Plate"], enable_displacement_current=False)

# 12. 解析を実行する
setup.analyze()

# 13. $B_z$（磁束密度Z成分、Gauss換算）を評価するFields Calculator式を定義する
# 生のベクトル成分（Bx/By/Bz）はFields Calculatorで式を登録しないとレポートの式として使えないため必須。
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

# 14. 板の上に、$B_z$を評価するための2本のラインを作成する（局所的なメッシュ細分化の円柱も添える）
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

# 15. 各ラインに沿った$|B_z|$のレポートを作成する（50Hz/200Hzの両方、位相0度）
variations = {"Distance": ["All"], "Freq": ["All"], "Phase": ["0deg"]}
for line_name in lines:
    m3d.post.create_report(
        expressions="mag(Bz)",
        variations=variations,
        primary_sweep_variable="Distance",
        report_category="Fields",
        context=line_name,
        plot_name=f"mag(Bz) Along {line_name}",
    )

# 16. 板表面のB磁束密度（Mag_B）のフィールドプロットを作成する
m3d.post.create_fieldplot_surface(
    assignment=plate.name,
    quantity="Mag_B",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": "200Hz", "Phase": "0deg"},
    plot_name="PlateMagB",
)

# 17. 保存して終了する
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)
