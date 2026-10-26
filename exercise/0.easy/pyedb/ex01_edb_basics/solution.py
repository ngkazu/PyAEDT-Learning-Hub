"""演習1: EDB の基本構造（スタックアップ → ネット → トレース → ビア）。

HFSS 3D Layout（レイヤー/ECAD 構造）のジオメトリは PyEDB（`from pyedb import Edb`）で作る。
この easy 課題では解析は行わず、EDB で PCB の基本構造を組み立てる手順だけを学ぶ:

  1. スタックアップ（層の積み重ね）
  2. ネット（配線の論理名）
  3. トレース（信号配線）と GND プレーン
  4. パッドスタック定義とビア（層をまたぐ縦の接続）

生成した .aedb をこのスクリプトと同じフォルダに作って保存する（解析はしない）。
"""

import os
import shutil

from pyedb import Edb

AEDT_VERSION = "2026.1"

# このスクリプトと同じフォルダに .aedb を作る
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
AEDB_PATH = os.path.join(WORK_DIR, "edb_basics.aedb")

# 寸法（m 単位。PyEDB の座標はメートル）
TRACE_LEN = 0.010  # トレース長 10mm
TRACE_WIDTH = 0.0002  # トレース幅 0.2mm

# ---------------------------------------------------------------------------
# 1. EDB を作る（既存があれば消してクリーンに）
# ---------------------------------------------------------------------------
if os.path.isdir(AEDB_PATH):
    shutil.rmtree(AEDB_PATH, ignore_errors=True)

edb = Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)

# ---------------------------------------------------------------------------
# 2. スタックアップ（2層基板: TOP / 誘電体 / BOTTOM）
# ---------------------------------------------------------------------------
# 最初の層は base_layer なしで作る。2層目以降は base_layer と method で
# 「どの層の上に積むか」を指定する（add_on_top = 直前の層の上に積む）。
edb.stackup.add_layer("TOP", layer_type="signal", material="copper", thickness="35um")
edb.stackup.add_layer(
    "Diel",
    base_layer="TOP",
    method="add_on_top",
    layer_type="dielectric",
    material="FR4_epoxy",
    thickness="0.2mm",
)
edb.stackup.add_layer(
    "BOTTOM",
    base_layer="Diel",
    method="add_on_top",
    layer_type="signal",
    material="copper",
    thickness="35um",
)

# ---------------------------------------------------------------------------
# 3. ネットを作る（配線の論理名。トレースやプレーンはこのネットに属させる）
# ---------------------------------------------------------------------------
edb.nets.find_or_create_net(net_name="SIG")
edb.nets.find_or_create_net(net_name="GND")

# ---------------------------------------------------------------------------
# 4. TOP 層に信号トレース、BOTTOM 層に GND プレーン
# ---------------------------------------------------------------------------
# create_trace の座標は [[x0, y0], [x1, y1]] の列（メートル）。
edb.modeler.create_trace(
    [[0, 0], [TRACE_LEN, 0]],
    layer_name="TOP",
    width=TRACE_WIDTH,
    net_name="SIG",
)
edb.modeler.create_rectangle(
    "BOTTOM",
    net_name="GND",
    lower_left_point=[-0.002, -0.002],
    upper_right_point=[0.012, 0.002],
)

# ---------------------------------------------------------------------------
# 5. パッドスタック定義 → ビアを配置（TOP から BOTTOM へ層をまたぐ縦の接続）
# ---------------------------------------------------------------------------
# ビアはまず「パッドスタック定義」（穴径・パッド径・アンチパッド径・貫通範囲）を
# 作ってから、その定義を使って place で位置に配置する。
edb.padstacks.create(
    padstackname="VIA_SIG",
    holediam="0.2mm",  # ドリル穴径
    paddiam="0.4mm",  # パッド径
    antipaddiam="0.6mm",  # アンチパッド径（プレーン層のクリアランス）
    start_layer="TOP",
    stop_layer="BOTTOM",
)
edb.padstacks.place(
    position=[TRACE_LEN, 0],  # トレース終端にビアを置く
    definition_name="VIA_SIG",
    net_name="SIG",
)

# ---------------------------------------------------------------------------
# 6. 保存して閉じる（easy は EDB の構造作成までで終了。解析は normal 以降）
# ---------------------------------------------------------------------------
edb.save()
edb.close()

print("EDB を作成しました:", AEDB_PATH)
