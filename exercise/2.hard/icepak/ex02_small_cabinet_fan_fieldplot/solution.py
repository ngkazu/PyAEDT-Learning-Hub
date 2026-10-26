"""演習2: 小型筐体のファン冷却解析（温度フィールドプロット・モニタ）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

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

# 3. PCB基板を作成する
ipk.modeler.create_box(origin=[15, 5, 5], sizes=[70, 70, 1.6], name="Box5", material="fr4_epoxy")

# 4. 発熱部品を作成する
ipk.modeler.create_box(origin=[50, 40, 6.6], sizes=[20, 20, 4], name="Box6", material="ceramic_material")

# 5. 発熱部品に温度ポイントモニタを割り当てる
ipk.assign_point_monitor_in_object(name="Box6", monitor_type="Temperature", monitor_name="Monitor_Box6")

# 6. 発熱部品上面にダイアタッチ割り当て用のシートを作成する
ipk.modeler.create_rectangle(
    orientation="XY",
    origin=[50, 40, 10.6],
    sizes=[20, 20],
    name="Box6_ObjectFromFace1",
)

# 7. ヒートシンクを作成する（ベース+フィン8枚）
ipk.modeler.create_box(origin=[40, 30, 10.6], sizes=[40, 40, 5], name="Box7", material="al-extruded")
ipk.modeler.create_box(origin=[40, 30, 15.6], sizes=[40, 1.5, 15], name="Box8", material="al-extruded")
_, fin_clone_names = ipk.modeler.duplicate_along_line(assignment="Box8", vector=[0, 5.5, 0], clones=8)

# 8. 解析領域（Region）を作り直す（Icepakデザイン作成時の既定Regionを削除してから作成する）
# create_fan()が許容するradiusの上限は、作成時点で存在するRegion／モデル形状全体の
# バウンディングボックスのサイズに依存する（小さいモデルのままFanを作成すると、10mm程度の
# radiusでもネイティブコンポーネント挿入に失敗する）。そのためRegionをFanより先に作る。
ipk.modeler["Region"].delete()
ipk.modeler.create_region(pad_value=[58, 58, 48, 48, 28, 28], pad_type="Absolute Offset")

# 9. 送風機（Fanコンポーネント）を配置する
# Radius/HubRadiusは作成後に変更すると、Fanのケース形状と流路形状の寸法が食い違い
# 「Case and Passage intersect」の検証エラーになるため、ここでは変更しない。
fan = ipk.create_fan(name="Fan1", shape="Circular", cross_section="YZ", radius="10mm", hub_radius="5mm", origin=[0, 60, 20])
fan_provider = fan.props["NativeComponentDefinitionProvider"]
fan_provider["DimUnits"] = ["m3_per_s", "pascal"]
fan_provider["X"] = ["0", "0.005", "0.01", "0.015"]
fan_provider["Y"] = ["50", "40", "20", "0"]
fan.update()

# 10. 発熱部品に総発熱量10Wを割り当てる
ipk.assign_solid_block(object_name="Box6", power_assignment="10W", boundary_name="Block1")

# 11. ダイアタッチ層（伝導板）を割り当てる
ipk.assign_conducting_plate_with_thickness(
    obj_plate="Box6_ObjectFromFace1",
    boundary_name="ConductingPlate1",
    total_power="0W",
    thickness="0.02mm",
    solid_material="Die_attach_material",
)

# 12. Regionの±X面に圧力開口を割り当てる
region = ipk.modeler["Region"]
xmin, ymin, zmin, xmax, ymax, zmax = region.bounding_box
yc, zc = (ymin + ymax) / 2, (zmin + zmax) / 2
face_xmax = ipk.modeler.get_faceid_from_position([xmax, yc, zc], assignment="Region")
face_xmin = ipk.modeler.get_faceid_from_position([xmin, yc, zc], assignment="Region")
ipk.assign_pressure_free_opening(
    assignment=[face_xmax, face_xmin],
    boundary_name="Opening1",
    no_reverse_flow=False,
)

# 13. セットアップを作成する
setup = ipk.create_setup(name="Setup1")
setup.props["Flow Regime"] = "Turbulent"
setup.props["Include Temperature"] = True
setup.props["Include Flow"] = True
setup.props["Include Gravity"] = False
setup.props["Radiation Model"] = "Off"
setup.props["Convergence Criteria - Max Iterations"] = 500
setup.update()

# 14. 解析を実行する
setup.analyze()

# 15. ヒートシンク表面（ベース+フィン8枚）の温度フィールドプロットを作成する
setup_sweep = f"{setup.name} : {ipk.solution_type}"
ipk.post.create_fieldplot_surface(
    assignment=["Box7", "Box8"] + fin_clone_names,
    quantity="Temperature",
    setup=setup_sweep,
    plot_name="HeatsinkTemperature",
)

# 16. 保存して終了する
ipk.save_project()
ipk.release_desktop(close_projects=True, close_desktop=True)
