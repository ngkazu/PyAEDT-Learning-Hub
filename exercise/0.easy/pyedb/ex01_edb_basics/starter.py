"""演習1: EDB の基本構造（スタックアップ → ネット → トレース → ビア）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す（解析はしない）。
"""

import os
import shutil

from pyedb import Edb

AEDT_VERSION = "2026.1"

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
AEDB_PATH = os.path.join(WORK_DIR, "edb_basics.aedb")

TRACE_LEN = 0.010  # トレース長 10mm
TRACE_WIDTH = 0.0002  # トレース幅 0.2mm

# 1. EDB を作る（既存があれば消す）
if os.path.isdir(AEDB_PATH):
    shutil.rmtree(AEDB_PATH, ignore_errors=True)
edb = Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)

# 2. スタックアップ（2層基板: TOP / 誘電体 / BOTTOM）
# TODO: edb.stackup.add_layer(...) を3回呼んで次の積層を作る:
#   TOP(signal, copper, 35um)
#   Diel(dielectric, FR4_epoxy, 0.2mm, base_layer="TOP", method="add_on_top")
#   BOTTOM(signal, copper, 35um, base_layer="Diel", method="add_on_top")
#   ※最初の層(TOP)だけ base_layer / method を付けない

# 3. ネットを作る
# TODO: edb.nets.find_or_create_net(net_name="SIG") と "GND" を作る

# 4. TOP 層に信号トレース、BOTTOM 層に GND プレーン
# TODO: edb.modeler.create_trace([[0, 0], [TRACE_LEN, 0]], layer_name="TOP",
#         width=TRACE_WIDTH, net_name="SIG")
# TODO: edb.modeler.create_rectangle("BOTTOM", net_name="GND",
#         lower_left_point=[-0.002, -0.002], upper_right_point=[0.012, 0.002])

# 5. パッドスタック定義 → ビアを配置（TOP から BOTTOM へ貫通）
# TODO: edb.padstacks.create(padstackname="VIA_SIG", holediam="0.2mm",
#         paddiam="0.4mm", antipaddiam="0.6mm", start_layer="TOP", stop_layer="BOTTOM")
# TODO: edb.padstacks.place(position=[TRACE_LEN, 0], definition_name="VIA_SIG",
#         net_name="SIG")

# 6. 保存して閉じる
edb.save()
edb.close()

print("EDB を作成しました:", AEDB_PATH)
