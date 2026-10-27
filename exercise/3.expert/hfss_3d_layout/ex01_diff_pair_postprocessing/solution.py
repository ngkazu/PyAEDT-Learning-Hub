"""演習1: 差動ペア伝送線路 Sパラメータの Python 後処理（CSV入出力・matplotlib・Touchstone出力）。

hard（差動Sパラメータ解析）と同じモデル・解析に、以下の Python 後処理を追加する:
  - Sdd21（差動挿入損失）データを取得して CSV に保存する
  - 伝送線路の実用帯域（Sdd21 が DC 値から −3dB 下がる周波数）を Python で算出する
  - matplotlib（headless）で Sdd21・Sdd11 特性を画像（PNG）に保存する
  - 差動Sパラメータを Touchstone（.s4p）にエクスポートする

注意: この課題は CPython 実行環境で動かす（matplotlib を使うため）。
"""

import csv
import os

from pyedb import Edb

from ansys.aedt.core import Hfss3dLayout
from ansys.aedt.core.generic.settings import settings

# matplotlib は headless 構成（pyplot を使わず Figure + Agg キャンバス）で使う
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 出力先（このスクリプトと同じフォルダ）
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
AEDB_PATH = os.path.join(OUTPUT_DIR, "diff_pair.aedb")

LENGTH = 0.040  # 線路長 40mm
GAP = 0.0005  # 差動2本の中心間隔 0.5mm
WIDTH = 0.0002  # 線路幅 0.2mm

# ---------------------------------------------------------------------------
# モデル作成 + 差動Sパラメータ解析（hard と同じ。各課題は自己完結させる）
# ---------------------------------------------------------------------------
import shutil

if os.path.isdir(AEDB_PATH):
    shutil.rmtree(AEDB_PATH, ignore_errors=True)

edb = Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)

edb.stackup.add_layer(
    "GND_TOP", layer_type="signal", material="copper", thickness="35um"
)
edb.stackup.add_layer(
    "Diel_1",
    base_layer="GND_TOP",
    method="add_on_top",
    layer_type="dielectric",
    material="FR4_epoxy",
    thickness="0.2mm",
)
edb.stackup.add_layer(
    "SIG",
    base_layer="Diel_1",
    method="add_on_top",
    layer_type="signal",
    material="copper",
    thickness="35um",
)
edb.stackup.add_layer(
    "Diel_2",
    base_layer="SIG",
    method="add_on_top",
    layer_type="dielectric",
    material="FR4_epoxy",
    thickness="0.2mm",
)
edb.stackup.add_layer(
    "GND_BOT",
    base_layer="Diel_2",
    method="add_on_top",
    layer_type="signal",
    material="copper",
    thickness="35um",
)

trace_p = edb.modeler.create_trace(
    [[0, GAP / 2], [LENGTH, GAP / 2]], layer_name="SIG", width=WIDTH, net_name="DIFF_P"
)
trace_n = edb.modeler.create_trace(
    [[0, -GAP / 2], [LENGTH, -GAP / 2]],
    layer_name="SIG",
    width=WIDTH,
    net_name="DIFF_N",
)
edb.modeler.create_rectangle(
    "GND_TOP",
    net_name="GND",
    lower_left_point=[-0.005, -0.005],
    upper_right_point=[0.045, 0.005],
)
edb.modeler.create_rectangle(
    "GND_BOT",
    net_name="GND",
    lower_left_point=[-0.005, -0.005],
    upper_right_point=[0.045, 0.005],
)

edb.source_excitation.create_edge_port_vertical(
    prim_id=trace_p.id,
    point_on_edge=[0, GAP / 2],
    port_name="P_in",
    reference_layer="GND_TOP",
    hfss_type="Gap",
)
edb.source_excitation.create_edge_port_vertical(
    prim_id=trace_p.id,
    point_on_edge=[LENGTH, GAP / 2],
    port_name="P_out",
    reference_layer="GND_TOP",
    hfss_type="Gap",
)
edb.source_excitation.create_edge_port_vertical(
    prim_id=trace_n.id,
    point_on_edge=[0, -GAP / 2],
    port_name="N_in",
    reference_layer="GND_TOP",
    hfss_type="Gap",
)
edb.source_excitation.create_edge_port_vertical(
    prim_id=trace_n.id,
    point_on_edge=[LENGTH, -GAP / 2],
    port_name="N_out",
    reference_layer="GND_TOP",
    hfss_type="Gap",
)

edb.save()
edb.close()

h3d = Hfss3dLayout(
    project=AEDB_PATH,
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

setup = h3d.create_setup(name="MySetup")
sweep = h3d.create_linear_count_sweep(
    setup=setup.name,
    unit="GHz",
    start_frequency=0,
    stop_frequency=20,
    num_of_freq_points=201,
    sweep_type="Interpolating",
)
setup_sweep = f"{setup.name} : {sweep.name}"

h3d.set_differential_pair(
    assignment="P_in",
    reference="N_in",
    differential_mode="Diff_In",
    common_mode="Comm_In",
    differential_reference=100,
    common_reference=25,
)
h3d.set_differential_pair(
    assignment="P_out",
    reference="N_out",
    differential_mode="Diff_Out",
    common_mode="Comm_Out",
    differential_reference=100,
    common_reference=25,
)

h3d.analyze_setup(name="MySetup")

# ---------------------------------------------------------------------------
# Python 後処理
# ---------------------------------------------------------------------------
# 1) Sdd21（差動挿入損失）・Sdd11（差動反射）データを取得する
#    【重要】差動Sパラメータは context="Differential Pairs" を指定しないと
#    データが取得できない（AEDT内レポートと同じ注意点）。
data_sdd21 = h3d.post.get_solution_data(
    expressions="dB(S(Diff_Out,Diff_In))",
    setup_sweep_name=setup_sweep,
    context="Differential Pairs",
)
freq_ghz, sdd21_db = data_sdd21.get_expression_data("dB(S(Diff_Out,Diff_In))")

data_sdd11 = h3d.post.get_solution_data(
    expressions="dB(S(Diff_In,Diff_In))",
    setup_sweep_name=setup_sweep,
    context="Differential Pairs",
)
_, sdd11_db = data_sdd11.get_expression_data("dB(S(Diff_In,Diff_In))")

# 2) CSV に保存する
csv_path = os.path.join(OUTPUT_DIR, "sdd_parameters.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Freq_GHz", "Sdd21_dB", "Sdd11_dB"])
    for fq, s21, s11 in zip(freq_ghz, sdd21_db, sdd11_db):
        writer.writerow([float(fq), float(s21), float(s11)])

# 3) 実用帯域（Sdd21 が DC 値から −3dB 下がる周波数）を算出する
#    伝送線路は低域でほぼ無損失（Sdd21 ≈ 0dB）から単調に減衰していくため、
#    RLCフィルタのカットオフと同様に「DC値 − 3dB」をしきい値としたクロス点を探す。
sdd21_dc = float(sdd21_db[0])
threshold = sdd21_dc - 3.0
cutoff_ghz = None
for i in range(1, len(freq_ghz)):
    if sdd21_db[i] <= threshold:
        f0, f1 = float(freq_ghz[i - 1]), float(freq_ghz[i])
        y0, y1 = float(sdd21_db[i - 1]), float(sdd21_db[i])
        cutoff_ghz = f0 + (threshold - y0) * (f1 - f0) / (y1 - y0)
        break

# 4) matplotlib（headless）で Sdd21・Sdd11 特性を画像に保存する
fig = Figure(figsize=(8, 5))
FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.plot(freq_ghz, sdd21_db, label="Sdd21 (Insertion Loss)")
ax.plot(freq_ghz, sdd11_db, label="Sdd11 (Return Loss)")
ax.axhline(threshold, color="r", linestyle="--", label=f"-3dB ({threshold:.2f} dB)")
if cutoff_ghz is not None:
    ax.axvline(
        cutoff_ghz, color="g", linestyle="--", label=f"f(-3dB) = {cutoff_ghz:.2f} GHz"
    )
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Differential S-parameters (dB)")
ax.set_title("Differential Pair Transmission Line - Sdd21 / Sdd11")
ax.grid(True)
ax.legend()
png_path = os.path.join(OUTPUT_DIR, "sdd_parameters.png")
fig.savefig(png_path, dpi=150)

# 5) 差動Sパラメータを Touchstone（.s4p）にエクスポートする
snp_path = os.path.join(OUTPUT_DIR, "diff_pair.s4p")
h3d.export_touchstone(setup="MySetup", sweep=sweep.name, output_file=snp_path)

print(f"Sdd21 DC value : {sdd21_dc:.4f} dB")
if cutoff_ghz is not None:
    print(f"-3dB point     : {cutoff_ghz:.2f} GHz")
else:
    print("-3dB point     : not reached within sweep range")
print(f"CSV  : {csv_path}")
print(f"PNG  : {png_path}")
print(f"s4p  : {snp_path}")

# ---------------------------------------------------------------------------
# 保存して終了する
# ---------------------------------------------------------------------------
h3d.save_project()
h3d.release_desktop(close_projects=True, close_desktop=True)
