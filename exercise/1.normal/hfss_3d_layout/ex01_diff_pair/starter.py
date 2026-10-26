"""演習1: 差動ペア伝送線路（HFSS 3D Layout, モデル作成〜解析実行）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
"""

import os
import shutil

from pyedb import Edb

from ansys.aedt.core import Hfss3dLayout
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
AEDB_PATH = os.path.join(WORK_DIR, "diff_pair.aedb")

LENGTH = 0.040  # 線路長 40mm
GAP = 0.0005  # 差動2本の中心間隔 0.5mm
WIDTH = 0.0002  # 線路幅 0.2mm

# 1. PyEDB で EDB を作る（既存があれば消す）
if os.path.isdir(AEDB_PATH):
    shutil.rmtree(AEDB_PATH, ignore_errors=True)
edb = Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)

# 2. スタックアップ（GND / 誘電体 / 信号 / 誘電体 / GND）
# TODO: edb.stackup.add_layer(...) を5回呼んで次の積層を作る:
#   GND_TOP(signal,copper,35um) / Diel_1(dielectric,FR4_epoxy,0.2mm) /
#   SIG(signal,copper,35um) / Diel_2(dielectric,FR4_epoxy,0.2mm) / GND_BOT(signal,copper,35um)
#   2層目以降は base_layer="直前の層", method="add_on_top" を指定する

# 3. 差動ペア 2本（SIG 層）
# TODO: edb.modeler.create_trace([[0, GAP/2],[LENGTH, GAP/2]], layer_name="SIG",
#       width=WIDTH, net_name="DIFF_P") と、-GAP/2 側の "DIFF_N" を作る
trace_p = ...
trace_n = ...

# 4. 上下層に GND プレーン
# TODO: edb.modeler.create_rectangle("GND_TOP"/"GND_BOT", net_name="GND",
#       lower_left_point=[-0.005,-0.005], upper_right_point=[0.045,0.005]) を2枚

# 5. 両端に vertical gap ポート（各信号線の端に1つずつ、計4ポート）
# 【重要】ストリップライン端に wave port は不向き（coax 扱いになり via が必要になって
#         メッシュ生成が失敗する）。via 不要の vertical gap port を使う。
# TODO: edb.source_excitation.create_edge_port_vertical(
#         prim_id=trace_p.id, point_on_edge=[x, GAP/2], port_name=...,
#         reference_layer="GND_TOP", hfss_type="Gap")
#       を P 側（trace_p, +GAP/2）と N 側（trace_n, -GAP/2）それぞれ x=0 と x=LENGTH の
#       計4回呼ぶ（例: P_in, P_out, N_in, N_out）

# 6. 保存して閉じる
edb.save()
edb.close()

# 7. HFSS 3D Layout で開く
h3d = Hfss3dLayout(
    project=AEDB_PATH,
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# 8. セットアップと周波数スイープを作成する
# TODO: setup = h3d.create_setup(name="MySetup")
#       h3d.create_linear_count_sweep(setup=setup.name, unit="GHz", start_frequency=0,
#           stop_frequency=20, num_of_freq_points=201, sweep_type="Interpolating")
#       （引数は units ではなく unit なので注意）
setup = ...

# 9. 解析を実行する
# TODO: h3d.analyze_setup(name="MySetup")

# 10. 保存して終了する
h3d.save_project()
h3d.release_desktop(close_projects=True, close_desktop=True)
