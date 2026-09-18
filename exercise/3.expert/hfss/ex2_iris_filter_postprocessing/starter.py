"""演習2: 導波管インダクティブアイリスフィルタ S/フィールドデータの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

import numpy as np
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

WG_WIDTH = 22.86  # WG16 (WR-90) 内寸 [mm]
WG_HEIGHT = 10.16  # WG16 (WR-90) 内寸 [mm]

# TODO: 1. conditions.csv を読み込み、wg_length / iris_thickness / iris_aperture を取得する

# TODO: 2. 2.hard/hfss/ex2_iris_filter/solution.py と同じ手順でモデルを作成・解析する
#          （寸法はCSVから読み込んだ値を使う）
hfss = None


def create_iris(z_position_expr: str, name: str):
    """導波管内寸全体を覆う銅板を作り、中央の開口部をくり抜いてインダクティブアイリスを作る。"""
    return None


# TODO: 3. hfss.excitation_names から励振名を取得し、S11・S21の SolutionData を取得する
#          （get_solution_data(expressions=[...], setup_sweep_name=hfss.nominal_sweep,
#          report_category="Modal Solution Data")）

# TODO: 4. get_expression_data(formula="db20") で周波数・S11[dB]・S21[dB]の配列を取得する

# TODO: 5. S11・S21の結果をCSVファイル（results_s_parameters.csv）に出力する

# TODO: 6. modeler.create_plane() + post.create_fieldplot_cutplane() で
#          導波管中心を通るXZ平面の電界分布（Mag_E）のフィールドプロットを作成する

# TODO: 7. post.plot_field_from_fieldplot(plot_name=..., project_path=..., image_format="png",
#          view="xz", show=False) で、PyVistaによる画像を出力する

# TODO: 8. post.plot_field_from_fieldplot(plot_name=..., view="xz", show=True)（project_pathは渡さない）で、
#          同じフィールドプロットをインタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する

# TODO: 9. 保存して終了する
