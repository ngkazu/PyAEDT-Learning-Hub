"""演習2: 小型筐体のファン冷却解析（モデル作成〜解析実行）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Icepak を SteadyState ソリューションで起動し、modeler.model_units = "mm" を設定する
ipk = None

# TODO: 2. edit_design_settings(ambient_temperature="20cel", gravity_dir=2) で
#          周囲温度20℃・重力方向-Zを設定する

# TODO: 3. PCB基板("Box5")を origin=[15, 5, 5], sizes=[70, 70, 1.6],
#          material="fr4_epoxy" で作成する

# TODO: 4. 発熱部品("Box6")を origin=[50, 40, 6.6], sizes=[20, 20, 4],
#          material="ceramic_material" で作成する

# TODO: 5. 発熱部品上面（Z=10.6）に、ダイアタッチ割り当て用の20x20mmシート
#          ("Box6_ObjectFromFace1")を create_rectangle(orientation="XY",
#          origin=[50, 40, 10.6], sizes=[20, 20]) で作成する

# TODO: 6. ヒートシンクを作成する
#          "Box7"（ベース）: origin=[40, 30, 10.6], sizes=[40, 40, 5], material="al-extruded"
#          "Box8"（フィン1枚目）: origin=[40, 30, 15.6], sizes=[40, 1.5, 15],
#          material="al-extruded"。duplicate_along_line(assignment="Box8",
#          vector=[0, 5.5, 0], clones=8) でY方向に8枚複製する

# TODO: 7. 解析領域("Region")を作り直す。Icepakデザイン作成時に自動生成される
#          既定の"Region"を ipk.modeler["Region"].delete() で削除してから、
#          create_region(pad_value=[58, 58, 48, 48, 28, 28], pad_type="Absolute Offset")
#          で作成する（create_fan()が許容するradius上限はRegion／モデル全体のサイズに
#          依存するため、Regionは必ずFanより先に作ること）

# TODO: 8. 送風機（Fanコンポーネント）を配置する。create_fan(name="Fan1",
#          shape="Circular", cross_section="YZ", radius="10mm", hub_radius="5mm",
#          origin=[0, 60, 20]) で作成する。その後、
#          fan.props["NativeComponentDefinitionProvider"] の "DimUnits"、"X"、"Y"を
#          書き換えて流量圧力カーブを設定し、fan.update() で適用する
#          （Radius/HubRadiusは作成後に変えないこと。変えるとケース形状と流路形状の
#          寸法が食い違う検証エラーになる）

# TODO: 9. assign_solid_block(object_name="Box6", power_assignment="10W",
#          boundary_name="Block1") で発熱部品に総発熱量10Wを割り当てる

# TODO: 10. assign_conducting_plate_with_thickness(obj_plate="Box6_ObjectFromFace1",
#           boundary_name="ConductingPlate1", total_power="0W", thickness="0.02mm",
#           solid_material="Die_attach_material") でダイアタッチ層を割り当てる

# TODO: 11. Regionの±X面を get_faceid_from_position() で特定し、
#           assign_pressure_free_opening(assignment=[+X面, -X面],
#           boundary_name="Opening1", no_reverse_flow=False) で圧力開口を割り当てる

# TODO: 12. セットアップ "Setup1" を作成し、Flow Regime="Turbulent"、
#           Include Gravity=False、Radiation Model="Off"、最大反復500を設定する

# TODO: 13. 解析を実行する

# TODO: 14. 保存して終了する（normalはここまで。ポスト処理は行わない）
