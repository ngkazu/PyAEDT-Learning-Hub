"""演習1: RLCローパスフィルタ Sパラメータの Python 後処理（CSV入出力・matplotlib）。

hard（Sパラメータ解析）と同じモデル・解析に、以下の Python 後処理を追加する:
  - S21 データを取得して CSV に保存する
  - カットオフ周波数（S21 が −3dB になる周波数）を Python で算出する
  - matplotlib（headless）で S21 特性を画像（PNG）に保存する
  - S パラメータを Touchstone（.s2p）にエクスポートする

注意: この課題は CPython 実行環境で動かす（PyVista/matplotlib を使うため）。
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

# 出力先（このスクリプトと同じフォルダ）
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
# 1) S21（挿入損失）データを取得する
data = cir.post.get_solution_data(
    expressions="dB(S(Port2,Port1))",
    setup_sweep_name="LNA",
    domain="Sweep",
)
freq_ghz, s21_db = data.get_expression_data("dB(S(Port2,Port1))")

# 2) CSV に保存する
csv_path = os.path.join(OUTPUT_DIR, "s21.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Freq_GHz", "S21_dB"])
    for fq, s in zip(freq_ghz, s21_db):
        writer.writerow([float(fq), float(s)])

# 3) カットオフ周波数（S21 が DC 値から −3dB 下がる周波数）を算出する
s21_dc = float(s21_db[0])
threshold = s21_dc - 3.0
cutoff_ghz = None
for i in range(1, len(freq_ghz)):
    if s21_db[i] <= threshold:
        # 線形補間でしきい値クロス点を求める
        f0, f1 = float(freq_ghz[i - 1]), float(freq_ghz[i])
        y0, y1 = float(s21_db[i - 1]), float(s21_db[i])
        cutoff_ghz = f0 + (threshold - y0) * (f1 - f0) / (y1 - y0)
        break

# 4) matplotlib（headless）で S21 特性を画像に保存する
fig = Figure(figsize=(8, 5))
FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.plot(freq_ghz, s21_db, label="S21 (dB)")
ax.axhline(threshold, color="r", linestyle="--", label=f"-3dB ({threshold:.2f} dB)")
if cutoff_ghz is not None:
    ax.axvline(
        cutoff_ghz, color="g", linestyle="--", label=f"fc = {cutoff_ghz:.2f} GHz"
    )
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("dB(S21)")
ax.set_title("RLC Lowpass Filter - Insertion Loss")
ax.grid(True)
ax.legend()
png_path = os.path.join(OUTPUT_DIR, "s21.png")
fig.savefig(png_path, dpi=150)

# 5) S パラメータを Touchstone（.s2p）にエクスポートする
snp_path = os.path.join(OUTPUT_DIR, "rlc_lowpass.s2p")
cir.export_touchstone(output_file=snp_path)

print(f"S21 DC value : {s21_dc:.2f} dB")
if cutoff_ghz is not None:
    print(f"Cutoff (-3dB): {cutoff_ghz:.2f} GHz")
else:
    print("Cutoff (-3dB): not reached within sweep range")
print(f"CSV  : {csv_path}")
print(f"PNG  : {png_path}")
print(f"s2p  : {snp_path}")

# ---------------------------------------------------------------------------
# 保存して終了する
# ---------------------------------------------------------------------------
cir.save_project()
cir.release_desktop(close_projects=True, close_desktop=True)
