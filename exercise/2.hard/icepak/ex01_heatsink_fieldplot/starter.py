"""演習1: ヒートシンク熱解析（温度フィールドプロット・モニタ）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Icepak を SteadyState ソリューションで起動し、modeler.model_units = "mm" を設定する
ipk = None

# TODO: 2. edit_design_settings(ambient_temperature="20cel", gravity_dir=2) で
#          周囲温度20℃・重力方向-Zを設定する

# TODO: 3. ベース("base")を origin=[0, -50, -50], sizes=[10, 100, 100],
#          material="Al-Extruded" で作成する

# TODO: 4. assign_point_monitor_in_object(name="base", monitor_type="Temperature",
#          monitor_name="Monitor_base") でベースに温度ポイントモニタを割り当てる
#          （モニタは解析実行前に割り当てること）

# TODO: 5. フィン1枚目("fin")を origin=[10, -50, -50], sizes=[40, 5, 100],
#          material="Al-Extruded" で作成し、_ok, fin_clone_names =
#          duplicate_along_line(assignment="fin", vector=[0, 9.5, 0], clones=11) で
#          Y方向にピッチ9.5mmで11枚に複製する。fin_names = ["fin"] + fin_clone_names
#          としてフィン名の一覧を保持しておく（手順14で使う）

# TODO: 6. 発熱面シート("Rectangle1")を create_rectangle(orientation="YZ",
#          origin=[0, -50, -50], sizes=[100, 100]) で作成する

# TODO: 7. 解析領域("Region")を create_region(pad_value=[25, 25, 50, 50, 50, 50],
#          pad_type="Absolute Offset") で作成する

# TODO: 8. assign_source(assignment="Rectangle1", thermal_condition="Total Power",
#          assignment_value="20W", boundary_name="Source1", radiate=False) で
#          発熱面に総発熱量20Wの熱源を割り当てる

# TODO: 9. Regionの6面（±X, ±Y, ±Z）の中心座標から get_faceid_from_position() で
#          面IDを特定する

# TODO: 10. Regionの+Z面に assign_pressure_free_opening(assignment=[+Z面],
#           boundary_name="Opening1", no_reverse_flow=True)、-Z面に
#           assign_pressure_free_opening(assignment=[-Z面], boundary_name="Opening2",
#           no_reverse_flow=False) で圧力開口を割り当てる

# TODO: 11. Regionの±X, ±Y面（4面）に assign_stationary_wall(geometry=[4面],
#           boundary_condition="Temperature", name="StationaryWall1",
#           temperature="AmbientTemp", material="Al-Extruded", radiate=True) で
#           固定温度壁を割り当てる

# TODO: 12. セットアップ "Setup1" を作成し、Flow Regime="Laminar"、
#           Include Gravity=True、最大反復500を設定する

# TODO: 13. 解析を実行する

# TODO: 14. post.create_fieldplot_surface(assignment=["base"] + fin_names,
#           quantity="Temperature", setup=f"{setup.name} : {ipk.solution_type}",
#           plot_name="HeatsinkTemperature") で、ヒートシンク表面（base+フィン11枚）の
#           温度フィールドプロットを作成する

# TODO: 15. 保存して終了する
