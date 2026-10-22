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

# TODO: 2. セットアップ "Setup1" を作成し、setup.props["Frequency"] = "200Hz" を設定したうえで、
#          setup.props["HasSweepSetup"] = True と
#          setup.add_eddy_current_sweep(sweep_type="SinglePoints", start_frequency=50, units="Hz",
#          clear=True) で、実測値比較用の50Hzをスイープ点として追加する
setup = None

# 3. コイルの寸法を定義する（TEAM7図面の値。変更不要）
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

# TODO: 12. 解析を実行する

# TODO: 13. $B_z$（磁束密度Z成分、Gauss換算）を評価するFields Calculator式(bz)を定義し、
#           post.fields_calculator.add_expression(bz, None) で登録する
#           （README.mdの式の内容を参照。生のベクトル成分はCalculatorなしではレポートの式に使えない）

# TODO: 14. 板の上に、$B_z$を評価するための2本のライン("Line_A1_B1", "Line_A2_B2")と、
#           局所的なメッシュ細分化用の円柱を、どちらも create_polyline(..., non_model=True) で作成する
#           （どちらもレポート・メッシュヒント用の補助形状であり、ソリッドの解析モデル自体には含めないため）。
#           円柱には set_crosssection_properties(section="Circle", width="2mm") で断面を設定する

# TODO: 15. 各ラインに沿った$|B_z|$のレポートを作成する
#           post.create_report(expressions="mag(Bz)", variations={"Distance": ["All"], "Freq": ["All"],
#           "Phase": ["0deg"]}, primary_sweep_variable="Distance", report_category="Fields",
#           context=line_name, plot_name=...) をラインごとに呼ぶ

# TODO: 16. post.create_fieldplot_surface(assignment=plate.name, quantity="Mag_B",
#           setup=f"{setup.name} : LastAdaptive", intrinsics={"Freq": "200Hz", "Phase": "0deg"},
#           plot_name="PlateMagB") で板表面のフィールドプロットを作成する

# TODO: 17. 保存して終了する

# TODO: 16. 保存して終了する
