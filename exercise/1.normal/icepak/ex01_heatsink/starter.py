"""演習1: ヒートシンク熱解析（モデル作成〜解析実行）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Icepak を SteadyState ソリューションで起動し、modeler.model_units = "mm" を設定する
ipk = None

# TODO: 2. edit_design_settings(ambient_temperature="20cel", gravity_dir=2) で
#          周囲温度20℃・重力方向-Zを設定する

# TODO: 3. ベース("base")を create_box(origin=[0, -50, -50], sizes=[10, 100, 100],
#          material="Al-Extruded") で作成する

# TODO: 4. フィン1枚目("fin")を create_box(origin=[10, -50, -50], sizes=[40, 5, 100],
#          material="Al-Extruded") で作成し、
#          modeler.duplicate_along_line(assignment="fin", vector=[0, 9.5, 0], clones=11) で
#          Y方向に11枚になるよう複製する（戻り値は (成功フラグ, 複製名のリスト)）

# TODO: 5. 発熱面シート("Rectangle1")を create_rectangle(orientation="YZ",
#          origin=[0, -50, -50], sizes=[100, 100]) で作成する

# TODO: 6. 解析領域("Region")を create_region(pad_value=[25, 25, 50, 50, 50, 50],
#          pad_type="Absolute Offset") で作成する

# TODO: 7. assign_source(assignment="Rectangle1", thermal_condition="Total Power",
#          assignment_value="20W", boundary_name="Source1", radiate=False) で
#          発熱面に総発熱量20Wを割り当てる

# TODO: 8. modeler["Region"].bounding_box から6面（±X, ±Y, ±Z）それぞれの中心座標を計算し、
#          get_faceid_from_position() で各面の面IDを特定する

# TODO: 9. Regionの+Z面に assign_pressure_free_opening(boundary_name="Opening1",
#          no_reverse_flow=True)、-Z面に assign_pressure_free_opening(boundary_name="Opening2",
#          no_reverse_flow=False) で圧力開口を割り当てる

# TODO: 10. Regionの±X, ±Y面（4面まとめて）に assign_stationary_wall(geometry=...,
#           boundary_condition="Temperature", name="StationaryWall1",
#           temperature="AmbientTemp", material="Al-Extruded", radiate=True) で
#           固定温度壁を割り当てる

# TODO: 11. セットアップ "Setup1" を作成し、Flow Regime="Laminar"、
#           Include Temperature/Flow/Gravity=True、最大反復500を設定する

# TODO: 12. 解析を実行する

# TODO: 13. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
