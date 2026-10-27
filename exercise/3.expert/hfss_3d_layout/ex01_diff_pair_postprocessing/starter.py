"""演習1: 差動ペア伝送線路 Sパラメータの Python 後処理（CSV入出力・matplotlib・Touchstone出力）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
モデル作成・差動ペア設定・解析部分は hard 課題と同じなので、埋め方に迷ったら
`2.hard/hfss_3d_layout/ex01_diff_pair_sparams/solution.py` を参考にしてよい。

注意: この課題は CPython 実行環境で動かす（matplotlib を使うため）。
"""

import csv
import os
import shutil

from pyedb import Edb

from ansys.aedt.core import Hfss3dLayout
from ansys.aedt.core.generic.settings import settings

# matplotlib は headless 構成（pyplot を使わず Figure + Agg キャンバス）で使う
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
AEDB_PATH = os.path.join(OUTPUT_DIR, "diff_pair.aedb")

LENGTH = 0.040  # 線路長 40mm
GAP = 0.0005  # 差動2本の中心間隔 0.5mm
WIDTH = 0.0002  # 線路幅 0.2mm

# ---------------------------------------------------------------------------
# モデル作成 + 差動Sパラメータ解析（hard と同じ）
# ---------------------------------------------------------------------------
if os.path.isdir(AEDB_PATH):
    shutil.rmtree(AEDB_PATH, ignore_errors=True)
edb = Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)

# TODO: hard課題と同じ手順でスタックアップ・差動ペア2本・GNDプレーン・
#       vertical gap ポート4つ（P_in, P_out, N_in, N_out）を作る
trace_p = ...
trace_n = ...

edb.save()
edb.close()

h3d = Hfss3dLayout(
    project=AEDB_PATH,
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# TODO: setup = h3d.create_setup(name="MySetup")
#       sweep = h3d.create_linear_count_sweep(setup=setup.name, unit="GHz", start_frequency=0,
#           stop_frequency=20, num_of_freq_points=201, sweep_type="Interpolating")
#       setup_sweep = f"{setup.name} : {sweep.name}"
setup = ...
sweep = ...
setup_sweep = ...

# TODO: h3d.set_differential_pair() で Diff_In（P_in/N_in）と Diff_Out（P_out/N_out）を設定する

# TODO: h3d.analyze_setup(name="MySetup")

# ---------------------------------------------------------------------------
# Python 後処理
# ---------------------------------------------------------------------------
# 1) Sdd21・Sdd11 データを取得する
# TODO: data_sdd21 = h3d.post.get_solution_data(expressions="dB(S(Diff_Out,Diff_In))",
#         setup_sweep_name=setup_sweep, context="Differential Pairs")
#       freq_ghz, sdd21_db = data_sdd21.get_expression_data("dB(S(Diff_Out,Diff_In))")
#       同様に Sdd11（dB(S(Diff_In,Diff_In))）も取得する
freq_ghz = ...
sdd21_db = ...
sdd11_db = ...

# 2) CSV に保存する
# TODO: csv.writer で Freq_GHz, Sdd21_dB, Sdd11_dB の3列を書き出す
csv_path = os.path.join(OUTPUT_DIR, "sdd_parameters.csv")

# 3) 実用帯域（Sdd21 が DC 値から −3dB 下がる周波数）を算出する
# TODO: sdd21_db[0] を基準に threshold = DC値 - 3.0 を求め、
#       隣接する点の線形補間でしきい値クロス点 cutoff_ghz を求める
#       （RLCフィルタのカットオフ算出 `3.expert/circuit/ex01_rlc_filter_postprocessing/` と同じやり方）
cutoff_ghz = None

# 4) matplotlib（headless）で Sdd21・Sdd11 特性を画像に保存する
# TODO: Figure + FigureCanvasAgg で Sdd21・Sdd11 を1枚のグラフに重ねてプロットし、
#       -3dBのしきい値線・cutoff_ghzの縦線も描いて PNG 保存する
png_path = os.path.join(OUTPUT_DIR, "sdd_parameters.png")

# 5) 差動Sパラメータを Touchstone（.s4p）にエクスポートする
# TODO: h3d.export_touchstone(setup="MySetup", sweep=sweep.name, output_file=...)
snp_path = os.path.join(OUTPUT_DIR, "diff_pair.s4p")

# ---------------------------------------------------------------------------
# 保存して終了する
# ---------------------------------------------------------------------------
h3d.save_project()
h3d.release_desktop(close_projects=True, close_desktop=True)
