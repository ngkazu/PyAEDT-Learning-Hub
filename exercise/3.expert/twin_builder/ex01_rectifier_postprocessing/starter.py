"""演習1: ブリッジ整流回路+コンデンサフィルタの Python 後処理（CSV入出力・matplotlib・リプル率算出）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
モデル作成・解析部分は hard 課題と同じなので、迷ったら
`2.hard/twin_builder/ex01_rectifier_waveforms/solution.py` を参考にしてよい。

注意: この課題は CPython 実行環境で動かす（matplotlib を使うため）。
"""

import csv
import os

from ansys.aedt.core import TwinBuilder
from ansys.aedt.core.generic.settings import settings

# matplotlib は headless 構成（pyplot を使わず Figure + Agg キャンバス）で使う
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# モデル作成 + 過渡解析（hard と同じ）
# ---------------------------------------------------------------------------
tb = TwinBuilder(
    design="RectifierPostprocessing",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# TODO: hard課題と同じ手順で設計変数4つ・回路（電源・ダイオード4個・コンデンサ・抵抗・GND）を作る

sch = tb.modeler.schematic
G = 0.00254

# TODO: tb.set_end_time("100ms") / tb.analyze_setup("TR") で過渡解析を実行する

# ---------------------------------------------------------------------------
# Python 後処理
# ---------------------------------------------------------------------------
# 1) 入力交流電圧・出力DC電圧の波形データを取得する
# TODO: data_in = tb.post.get_solution_data(expressions="V_AC.V", setup_sweep_name="TR",
#         domain="Time", report_category="Standard")
#       time_ns, v_in = data_in.intrinsics["Time"], data_in.get_expression_data("V_AC.V")[1]
#       同様に RL.V（出力DC電圧）も取得する
#       【重要】Time の単位は ns。ms に変換してから使うこと（time_ms = t / 1.0e6）
time_ms = ...
v_in = ...
v_out = ...

# 2) CSV に保存する
# TODO: csv.writer で Time_ms, V_AC_V, V_RL_V の3列を書き出す
csv_path = os.path.join(OUTPUT_DIR, "rectifier_waveforms.csv")

# 3) 出力DC電圧の平均値・リプル率を算出する
# TODO: v_out の後半50%（定常状態）から v_max, v_min, v_mean を求め、
#       ripple_pct = (v_max - v_min) / v_mean * 100 を計算する

# 4) matplotlib（headless）で入出力波形を画像に保存する
# TODO: Figure + FigureCanvasAgg で v_in・v_out を1枚のグラフに重ねてプロットし、PNG保存する
png_path = os.path.join(OUTPUT_DIR, "rectifier_waveforms.png")

# ---------------------------------------------------------------------------
# 保存して終了する
# ---------------------------------------------------------------------------
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
