"""演習3: PCB表面実装部品の熱解析（温度フィールドプロット・モニタ）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modules.mesh_icepak import MeshRegion

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Icepak を SteadyState ソリューションで起動する
ipk = Icepak(
    design="IcepakDesign1",
    solution_type="SteadyState",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
ipk.modeler.model_units = "mm"

# 2. 周囲温度・重力方向を設定する
ipk.edit_design_settings(ambient_temperature="20cel", gravity_dir=2)

# 3. PCB基板とその上の層を下から順に積み重ねて作成する
ipk.modeler.create_box(origin=[0, 0, 0], sizes=[50, 50, 1.6], name="Box1", material="fr4_epoxy")
ipk.modeler.create_box(origin=[0, 0, 0], sizes=[50, 50, 0.035], name="Box2", material="copper")
ipk.modeler.create_box(origin=[24.5, 0, 1.565], sizes=[1, 24.5, 0.035], name="Box3", material="copper")
ipk.modeler.create_box(origin=[24.5, 25.5, 1.565], sizes=[1, 24.5, 0.035], name="Box4", material="copper")
ipk.modeler.create_box(origin=[24.5, 24, 1.6], sizes=[1, 0.5, 0.05], name="Box5", material="solder")
ipk.modeler.create_box(origin=[24.5, 25.5, 1.6], sizes=[1, 0.5, 0.05], name="Box6", material="solder")
ipk.modeler.create_box(origin=[24.5, 24, 1.65], sizes=[1, 2, 0.5], name="Box7", material="ceramic_material")
ipk.modeler.create_box(origin=[24.7, 24.5, 1.9], sizes=[0.6, 1, 0.02], name="Box8", material="si-typical_ref")

# 4. Siダイに温度ポイントモニタを割り当てる
ipk.assign_point_monitor_in_object(name="Box8", monitor_type="Temperature", monitor_name="Monitor_Box8")

# 5. メッシュリージョンを作成する（Regionより先に作る。Regionのパーセントオフセットは
#    メッシュリージョンのSubRegionを含むモデル全体のbboxを基準に計算されるため）

# MeshRegion1: PCB(Box1)を内包、パディング0（Box1のbboxに一致）。2Dマルチレベルメッシュ（XY面）を使う
mesh_region1 = MeshRegion(ipk, ["Box1"], "MeshRegion1")
mesh_region1.assignment.padding_types = ["Absolute Offset"] * 6
mesh_region1.assignment.padding_values = ["0"] * 6
mesh_region1.manual_settings = True
mesh_region1.settings["MaxElementSizeX"] = "1mm"
mesh_region1.settings["MaxElementSizeY"] = "1mm"
mesh_region1.settings["MaxElementSizeZ"] = "1mm"
mesh_region1.settings["MaxLevels"] = "1"
mesh_region1.settings["EnforeMLMType"] = "2D"
mesh_region1.settings["2DMLMType"] = "2DMLM_XY"
mesh_region1.update()

# MeshRegion2: 部品群（Box5-8）を内包、±0.4mmパディング（底面のみ0）
mesh_region2 = MeshRegion(ipk, ["Box5", "Box6", "Box7", "Box8"], "MeshRegion2")
mesh_region2.assignment.padding_types = ["Absolute Offset"] * 6
mesh_region2.assignment.padding_values = ["0.4", "0.4", "0.4", "0.4", "0.4", "0"]
mesh_region2.manual_settings = True
mesh_region2.settings["MaxElementSizeX"] = "0.2mm"
mesh_region2.settings["MaxElementSizeY"] = "0.2mm"
mesh_region2.settings["MaxElementSizeZ"] = "0.2mm"
mesh_region2.settings["MaxLevels"] = "3"
mesh_region2.update()

# MeshRegion3: PCB+部品全体（Box1-8）を内包、4mmパディング（+Zのみ4.4mm）
mesh_region3 = MeshRegion(ipk, ["Box1", "Box2", "Box3", "Box4", "Box5", "Box6", "Box7", "Box8"], "MeshRegion3")
mesh_region3.assignment.padding_types = ["Absolute Offset"] * 6
mesh_region3.assignment.padding_values = ["4", "4", "4", "4", "4.4", "4"]
mesh_region3.manual_settings = True
mesh_region3.settings["MaxElementSizeX"] = "1mm"
mesh_region3.settings["MaxElementSizeY"] = "1mm"
mesh_region3.settings["MaxElementSizeZ"] = "1mm"
mesh_region3.settings["MaxLevels"] = "1"
mesh_region3.update()

# 6. 解析領域（Region）を、面ごとに異なるパディング種別で作成する
ipk.modeler["Region"].delete()
ipk.modeler.create_region(
    pad_type=[
        "Absolute Offset",
        "Absolute Offset",
        "Absolute Offset",
        "Absolute Offset",
        "Absolute Offset",
        "Absolute Offset",
    ],
    pad_value=["25mm", "25mm", "25mm", "25mm", "50mm", "10mm"],
)

# 7. Siダイに総発熱量0.05Wを割り当てる
ipk.assign_solid_block(object_name="Box8", power_assignment="0.05W", boundary_name="Block1")

# 8. Regionの6面の中心座標から面IDを特定する
region = ipk.modeler["Region"]
xmin, ymin, zmin, xmax, ymax, zmax = region.bounding_box
xc, yc, zc = (xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2

face_zmax = ipk.modeler.get_faceid_from_position([xc, yc, zmax], assignment="Region")
face_zmin = ipk.modeler.get_faceid_from_position([xc, yc, zmin], assignment="Region")
face_xmax = ipk.modeler.get_faceid_from_position([xmax, yc, zc], assignment="Region")
face_xmin = ipk.modeler.get_faceid_from_position([xmin, yc, zc], assignment="Region")
face_ymax = ipk.modeler.get_faceid_from_position([xc, ymax, zc], assignment="Region")
face_ymin = ipk.modeler.get_faceid_from_position([xc, ymin, zc], assignment="Region")

# 9. Regionの+Z面に圧力開口を割り当てる
ipk.assign_pressure_free_opening(
    assignment=[face_zmax],
    boundary_name="Opening1",
    no_reverse_flow=True,
)

# 10. Regionの±X, ±Y面（4面）に圧力開口を割り当てる
ipk.assign_pressure_free_opening(
    assignment=[face_xmax, face_xmin, face_ymax, face_ymin],
    boundary_name="Opening2",
    no_reverse_flow=False,
)

# 11. Regionの-Z面にHTC壁面境界条件を割り当てる
ipk.assign_stationary_wall_with_htc(
    geometry=face_zmin,
    name="StationaryWall1",
    thickness="30mm",
    material="Epoxy Resin-JSME",
    htc="10w_per_m2kel",
    ref_temperature="AmbientTemp",
    shell_conduction=True,
)

# 12. セットアップを作成する
setup = ipk.create_setup(name="Setup1")
setup.props["Flow Regime"] = "Laminar"
setup.props["Include Temperature"] = True
setup.props["Include Flow"] = True
setup.props["Include Gravity"] = True
setup.props["Radiation Model"] = "Discrete Ordinates Model"
setup.props["Convergence Criteria - Max Iterations"] = 500
setup.props["Convergence Criteria - Flow"] = "0.001"
setup.props["Convergence Criteria - Energy"] = "1e-07"
setup.props["Linear Solver Type - Pressure"] = "V"
setup.update()

# 13. 解析を実行する
setup.analyze()

# 14. PCB・部品本体・Siダイ表面の温度フィールドプロットを作成する
setup_sweep = f"{setup.name} : {ipk.solution_type}"
ipk.post.create_fieldplot_surface(
    assignment=["Box1", "Box7", "Box8"],
    quantity="Temperature",
    setup=setup_sweep,
    plot_name="PcbTemperature",
)

# 15. 保存して終了する
ipk.save_project()
ipk.release_desktop(close_projects=True, close_desktop=True)
