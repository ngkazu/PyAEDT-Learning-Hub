"""演習1: ヒートシンク熱解析 温度データのPython後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# TODO: 1. conditions.csv を読み込み、"power_w" の値を float として取得する

# TODO: 2. Icepak を SteadyState ソリューションで起動し、modeler.model_units = "mm" を設定する
ipk = None

# TODO: 3. edit_design_settings(ambient_temperature="20cel", gravity_dir=2) で
#          周囲温度20℃・重力方向-Zを設定する

# TODO: 4. ベース("base")を origin=[0, -50, -50], sizes=[10, 100, 100],
#          material="Al-Extruded" で作成する

# TODO: 5. assign_point_monitor_in_object(name="base", monitor_type="Temperature",
#          monitor_name="Monitor_base") でベースに温度ポイントモニタを割り当てる

# TODO: 6. フィン1枚目("fin")を origin=[10, -50, -50], sizes=[40, 5, 100],
#          material="Al-Extruded" で作成し、_ok, fin_clone_names =
#          duplicate_along_line(assignment="fin", vector=[0, 9.5, 0], clones=11) で
#          Y方向にピッチ9.5mmで11枚に複製する

# TODO: 7. 発熱面シート("Rectangle1")を create_rectangle(orientation="YZ",
#          origin=[0, -50, -50], sizes=[100, 100]) で作成する

# TODO: 8. 解析領域("Region")を create_region(pad_value=[25, 25, 50, 50, 50, 50],
#          pad_type="Absolute Offset") で作成する

# TODO: 9. assign_source(assignment="Rectangle1", thermal_condition="Total Power",
#          assignment_value=f"{power_w}W", boundary_name="Source1", radiate=False) で、
#          CSVから読み込んだ発熱量を発熱面に割り当てる

# TODO: 10. Regionの6面（±X, ±Y, ±Z）の中心座標から get_faceid_from_position() で
#           面IDを特定する

# TODO: 11. Regionの+Z面に assign_pressure_free_opening(assignment=[+Z面],
#           boundary_name="Opening1", no_reverse_flow=True)、-Z面に
#           assign_pressure_free_opening(assignment=[-Z面], boundary_name="Opening2",
#           no_reverse_flow=False) で圧力開口を割り当てる

# TODO: 12. Regionの±X, ±Y面（4面）に assign_stationary_wall(geometry=[4面],
#           boundary_condition="Temperature", name="StationaryWall1",
#           temperature="AmbientTemp", material="Al-Extruded", radiate=True) で
#           固定温度壁を割り当てる

# TODO: 13. セットアップ "Setup1" を作成し、Flow Regime="Laminar"、
#           Include Gravity=True、最大反復500を設定する

# TODO: 14. 解析を実行する。setup_sweep = f"{setup.name} : {ipk.solution_type}" を
#           作っておく（以降の手順で使う）

# TODO: 15. ipk.post.evaluate_monitor_quantity(monitor="Monitor_base",
#           quantity="Temperature", setup_name=setup_sweep) で、ベースの
#           温度モニタ値（Min/Max/Mean/Stdev/Unit）を取得する

# TODO: 16. power_w・モニタ最大温度・温度単位を results_thermal.csv に書き出す

# TODO: 17. post.create_fieldplot_surface(assignment=["base"] + fin_names,
#           quantity="Temperature", setup=setup_sweep, plot_name="HeatsinkTemperature")
#           で、ヒートシンク表面の温度フィールドプロットを作成する

# TODO: 18. post.plot_field_from_fieldplot(plot_name="HeatsinkTemperature",
#           project_path=str(script_dir), image_format="png", view="isometric",
#           log_scale=False, show=False) で、フィールドプロットをPNG画像として出力する

# TODO: 19. post.plot_field_from_fieldplot(plot_name="HeatsinkTemperature",
#           view="isometric", log_scale=False, show=True) で、同じフィールドプロットを
#           インタラクティブなPyVistaウィンドウで表示する

# TODO: 20. 保存して終了する
