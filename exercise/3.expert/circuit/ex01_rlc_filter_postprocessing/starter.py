"""演習1: RLCローパスフィルタ Sパラメータの Python 後処理（CSV入出力・matplotlib）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。

注意: この課題は CPython 実行環境で動かす（matplotlib を使うため）。
"""

import csv
import os

from ansys.aedt.core import Circuit
from ansys.aedt.core.generic.settings import settings

# matplotlib は headless 構成（pyplot を使わず Figure + Agg キャンバス）で使う
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def left_right(component):
    """部品のピンを X 座標でソートし、(左ピン座標, 右ピン座標) を返す。"""
    pins = sorted(component.pins, key=lambda p: p.location[0])
    return pins[0].location, pins[-1].location


# ---------------------------------------------------------------------------
# モデル作成 + Sパラメータ解析（hard と同じ。各課題は自己完結させる）
# ---------------------------------------------------------------------------
cir = Circuit(
    design="RLC_LowpassFilter",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
sch = cir.modeler.schematic

r = sch.create_resistor(name="R1", value=50, location=[0.02, 0.0])
l = sch.create_inductor(name="L1", value=10e-9, location=[0.04, 0.0])
c = sch.create_capacitor(name="C1", value=1e-9, location=[0.06, 0.0])
r_left, r_right = left_right(r)
l_left, l_right = left_right(l)
c_left, c_right = left_right(c)
sch.create_wire([r_right, l_left])

p1 = sch.create_interface_port(name="Port1", location=[0.0, 0.0])
p2 = sch.create_interface_port(name="Port2", location=[0.08, 0.0])
gnd = sch.create_gnd(location=[0.06, -0.03])
g = gnd.pins[0].location
sch.create_wire([p1.pins[0].location, r_left])
sch.create_wire([l_right, c_left])
sch.create_wire([l_right, p2.pins[0].location])
sch.create_wire([c_right, [c_right[0], -0.03], g])

setup = cir.create_setup(name="LNA", setup_type="NexximLNA")
setup.add_sweep_count(
    sweep_variable="Freq",
    start=0.01,
    stop=5,
    count=401,
    units="GHz",
    count_type="Linear",
)
setup.analyze()

# ---------------------------------------------------------------------------
# Python 後処理
# ---------------------------------------------------------------------------
# 1. S21 データを取得する
# TODO: cir.post.get_solution_data(expressions="dB(S(Port2,Port1))",
#       setup_sweep_name="LNA", domain="Sweep") を呼び、
#       data.get_expression_data("dB(S(Port2,Port1))") で (freq, s21) を取得する
freq_ghz, s21_db = ...

# 2. CSV に保存する
# TODO: OUTPUT_DIR に "s21.csv" を作り、ヘッダ ["Freq_GHz","S21_dB"] + 各行を書き出す
csv_path = os.path.join(OUTPUT_DIR, "s21.csv")
# ...

# 3. カットオフ周波数（S21 が DC 値から −3dB 下がる周波数）を算出する
# TODO: s21_dc = s21_db[0] を基準に threshold = s21_dc - 3.0 を定義し、
#       s21_db が threshold を下回る点を線形補間で求めて cutoff_ghz に入れる
cutoff_ghz = ...

# 4. matplotlib（headless: Figure + FigureCanvasAgg）で S21 特性を PNG 保存する
# TODO: Figure を作り、FigureCanvasAgg(fig) を関連付け、ax.plot(freq_ghz, s21_db) を描画し、
#       fig.savefig(os.path.join(OUTPUT_DIR, "s21.png"), dpi=150) で保存する
#       （plt.show()/plt.subplots() は使わない）

# 5. S パラメータを Touchstone（.s2p）にエクスポートする
# TODO: cir.export_touchstone(output_file=os.path.join(OUTPUT_DIR, "rlc_lowpass.s2p"))

# ---------------------------------------------------------------------------
# 保存して終了する
# ---------------------------------------------------------------------------
cir.save_project()
cir.release_desktop(close_projects=True, close_desktop=True)
