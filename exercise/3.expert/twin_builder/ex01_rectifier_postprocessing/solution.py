"""演習1: ブリッジ整流回路+コンデンサフィルタの Python 後処理（CSV入出力・matplotlib・リプル率算出）。

hard（波形ポスト処理）と同じモデル・解析に、以下の Python 後処理を追加する:
  - 入力交流電圧・出力DC電圧の波形データを取得して CSV に保存する
  - 出力DC電圧の平均値・リプル率（脈動の割合）を Python で算出する
  - matplotlib（headless）で入出力波形を画像（PNG）に保存する

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

# 出力先（このスクリプトと同じフォルダ）
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# モデル作成 + 過渡解析（hard と同じ。各課題は自己完結させる）
# ---------------------------------------------------------------------------
tb = TwinBuilder(
    design="RectifierPostprocessing",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

tb["V_AMPL"] = "100V"
tb["AC_FREQ"] = "50Hz"
tb["C_FILTER"] = "1uF"
tb["R_LOAD"] = "100kohm"

sch = tb.modeler.schematic
G = 0.00254

source = sch.create_voltage_source(
    "V_AC", "ESINE", "V_AMPL", "AC_FREQ", location=[-1 * G, 0]
)
diode1 = sch.create_diode(name="D1", location=[10 * G, 6 * G], angle=270)
diode2 = sch.create_diode(name="D2", location=[20 * G, 6 * G], angle=270)
diode3 = sch.create_diode(name="D3", location=[10 * G, -4 * G], angle=270)
diode4 = sch.create_diode(name="D4", location=[20 * G, -4 * G], angle=270)
capacitor = sch.create_capacitor(
    name="C_FILT", value="C_FILTER", location=[29 * G, -10 * G]
)
resistor = sch.create_resistor(name="RL", value="R_LOAD", location=[39 * G, -10 * G])
gnd = sch.create_gnd(location=[5 * G, -16 * G])

sch.create_wire(points=[diode1.pins[0].location, diode3.pins[0].location])
sch.create_wire(points=[diode2.pins[1].location, diode4.pins[1].location])
sch.create_wire(points=[diode1.pins[1].location, diode2.pins[0].location])
sch.create_wire(points=[diode3.pins[1].location, diode4.pins[0].location])
sch.create_wire(
    points=[source.pins[1].location, [0, 10 * G], [15 * G, 10 * G], [15 * G, 5 * G]]
)
sch.create_wire(
    points=[source.pins[0].location, [0, -10 * G], [15 * G, -10 * G], [15 * G, -5 * G]]
)
sch.create_wire(points=[resistor.pins[0].location, [40 * G, 0], [22 * G, 0]])
sch.create_wire(points=[capacitor.pins[0].location, [30 * G, 0]])
sch.create_wire(
    points=[resistor.pins[1].location, [40 * G, -15 * G], gnd.pins[0].location]
)
sch.create_wire(points=[capacitor.pins[1].location, [30 * G, -15 * G]])
sch.create_wire(points=[gnd.pins[0].location, [5 * G, 0], [8 * G, 0]])

tb.modeler.zoom_to_fit()
tb.set_end_time("100ms")
tb.analyze_setup("TR")

# ---------------------------------------------------------------------------
# Python 後処理
# ---------------------------------------------------------------------------
# 1) 入力交流電圧・出力DC電圧の波形データを取得する
#    【重要】report_category="Standard" を指定しないとデータが取得できない。
#    【重要】Time の単位は ns（ミリ秒ではない）。CSV・グラフに出す前に ms へ変換する。
data_in = tb.post.get_solution_data(
    expressions="V_AC.V",
    setup_sweep_name="TR",
    domain="Time",
    report_category="Standard",
)
time_ns, v_in = data_in.intrinsics["Time"], data_in.get_expression_data("V_AC.V")[1]

data_out = tb.post.get_solution_data(
    expressions="RL.V", setup_sweep_name="TR", domain="Time", report_category="Standard"
)
_, v_out = data_out.intrinsics["Time"], data_out.get_expression_data("RL.V")[1]

time_ms = [float(t) / 1.0e6 for t in time_ns]  # ns -> ms

# 2) CSV に保存する
csv_path = os.path.join(OUTPUT_DIR, "rectifier_waveforms.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time_ms", "V_AC_V", "V_RL_V"])
    for t, vi, vo in zip(time_ms, v_in, v_out):
        writer.writerow([t, float(vi), float(vo)])

# 3) 出力DC電圧の平均値・リプル率を算出する
#    起動直後の過渡応答を避けるため、後半50%（定常状態）だけを評価に使う。
n = len(v_out)
steady = v_out[n // 2 :]
v_max = float(max(steady))
v_min = float(min(steady))
v_mean = float(sum(steady) / len(steady))
ripple_pct = (v_max - v_min) / v_mean * 100 if v_mean else None

# 4) matplotlib（headless）で入出力波形を画像に保存する
fig = Figure(figsize=(8, 5))
FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.plot(time_ms, v_in, label="V_AC (input)", alpha=0.6)
ax.plot(time_ms, v_out, label="V_RL (rectified+filtered output)")
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Voltage (V)")
ax.set_title("Bridge Rectifier with Capacitor Filter")
ax.grid(True)
ax.legend()
png_path = os.path.join(OUTPUT_DIR, "rectifier_waveforms.png")
fig.savefig(png_path, dpi=150)

print(f"Steady-state V_RL mean : {v_mean:.2f} V")
print(f"Steady-state V_RL range: {v_min:.2f} V - {v_max:.2f} V")
if ripple_pct is not None:
    print(f"Ripple                 : {ripple_pct:.2f} %")
print(f"CSV : {csv_path}")
print(f"PNG : {png_path}")

# ---------------------------------------------------------------------------
# 保存して終了する
# ---------------------------------------------------------------------------
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
