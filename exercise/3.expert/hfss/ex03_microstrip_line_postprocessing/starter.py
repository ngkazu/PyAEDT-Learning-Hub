"""演習3: マイクロストリップ線路 S/フィールドデータの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

SUB_W = 6.0  # 基板の幅 [mm]（Y方向）
SUB_H = 1.0  # 基板の厚さ [mm]（Z方向）
AIR_H = 3.0  # 基板上部のエアボックス高さ [mm]

# TODO: 1. conditions.csv を読み込み、line_w_mm / line_l_mm を取得する

# TODO: 2. 1.normal/hfss/ex03_microstrip_line/solution.py と同じ手順でマイクロストリップ線路を作成し、
#          解析する（導体幅・長さはCSVから読み込んだ値を使う）
hfss = None

# TODO: 3. sorted(hfss.excitation_names) からポート名を取得し、
#          hfss.post.get_solution_data(expressions=[S11式, S21式], setup_sweep_name=hfss.nominal_sweep,
#          report_category="Terminal Solution Data") でS11・S21の SolutionData を取得する

# TODO: 4. get_expression_data(formula="db20") で周波数・S11[dB]・S21[dB]の配列を取得する

# TODO: 5. S11・S21の結果をCSVファイル（results_s_parameters.csv）に出力する

# TODO: 6. hfss.post.create_fieldplot_surface(assignment=[gnd.name, line.name], quantity="Mag_E",
#          setup="Setup1 : LastAdaptive", plot_name=...) でフィールドプロットを作成する

# TODO: 7. hfss.post.plot_field_from_fieldplot(plot_name=..., project_path=..., image_format="png",
#          view="isometric", log_scale=True, show=False) で、PyVistaによる画像を出力する

# TODO: 8. project_pathを渡さずshow=Trueで同じplot_field_from_fieldplot()を呼び、
#          インタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する

# TODO: 9. 保存して終了する
