"""演習2: TEAM7非対称導体 実測データとの比較（CSV入出力・PyVista可視化）。"""

import csv
from math import sqrt
from pathlib import Path

import numpy as np

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# TODO: 1. team7_measured_bz.csv を読み込み、distance_mm / bz_a1b1_gauss / bz_a2b2_gauss の
#          リストを作る
measured_distance_mm = []
measured_bz_a1b1 = []
measured_bz_a2b2 = []

# TODO: 2. 2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/solution.py と同じ手順で
#          モデルを作成し、Setup作成・解析を行う（$B_z$計算式と評価ラインの定義も含む）
m3d = None

# TODO: 9. 200Hz・位相0度における、各ラインに沿った$|B_z|$のSolutionDataを
#          post.get_solution_data(expressions="mag(Bz)", variations={"Distance": ["All"],
#          "Freq": ["200Hz"], "Phase": ["0deg"]}, primary_sweep_variable="Distance",
#          report_category="Fields", context=line_name) で取得する

# TODO: 10. get_expression_data(expression="mag(Bz)", formula="real") で取得した
#           シミュレーション結果を、np.interp() で実測データと同じ距離点に補間する

# TODO: 11. シミュレーション値・実測値をCSVファイル（results_benchmark_comparison.csv）に出力する

# TODO: 12. シミュレーション結果と実測値をmatplotlibで重ね描きし、画像ファイルに保存する

# TODO: 13. post.create_fieldplot_surface(assignment=plate.name, quantity="Mag_B", ...) で
#           板表面のフィールドプロットを作成し、post.plot_field_from_fieldplot() で
#           画像出力（show=False）とインタラクティブ表示（show=True）の両方を行う

# TODO: 14. 保存して終了する
