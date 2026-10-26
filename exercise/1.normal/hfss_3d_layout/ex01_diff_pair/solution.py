"""演習1: 差動ペア伝送線路（HFSS 3D Layout, モデル作成〜解析実行）。

PyEDB でストリップライン・スタックアップと差動ペアを作り、各信号線の端に
vertical gap ポートを配置してから、HFSS 3D Layout で開いて周波数スイープ付き
セットアップを作成し、解析を実行する。

他の課題と異なり、ジオメトリは PyEDB（`pyedb`）で作る（レイヤー/ECAD の操作に向くため）。
生成した .aedb をこのスクリプトと同じフォルダに作り、それを HFSS 3D Layout で開く。
"""

import os
import shutil

from pyedb import Edb

from ansys.aedt.core import Hfss3dLayout
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# このスクリプトと同じフォルダに .aedb を作る
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
AEDB_PATH = os.path.join(WORK_DIR, "diff_pair.aedb")

# 差動ペアの寸法（m 単位。PyEDB の座標はメートル）
LENGTH = 0.040  # 線路長 40mm
GAP = 0.0005  # 差動2本の中心間隔 0.5mm
WIDTH = 0.0002  # 線路幅 0.2mm

# ---------------------------------------------------------------------------
# 1. PyEDB で EDB を作る（既存があれば消してクリーンに）
# ---------------------------------------------------------------------------
if os.path.isdir(AEDB_PATH):
    shutil.rmtree(AEDB_PATH, ignore_errors=True)

edb = Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)

# 2. スタックアップ（ストリップライン: GND / 誘電体 / 信号 / 誘電体 / GND）
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

# 3. 差動ペア 2本（SIG 層に平行配置）
trace_p = edb.modeler.create_trace(
    [[0, GAP / 2], [LENGTH, GAP / 2]],
    layer_name="SIG",
    width=WIDTH,
    net_name="DIFF_P",
)
trace_n = edb.modeler.create_trace(
    [[0, -GAP / 2], [LENGTH, -GAP / 2]],
    layer_name="SIG",
    width=WIDTH,
    net_name="DIFF_N",
)

# 4. 上下層に GND プレーン（リファレンス）
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

# 5. 両端に vertical gap ポート（各信号線の端に1つずつ、計4ポート）
#
# 【重要】ストリップライン構造（GND/誘電体/信号/誘電体/GND）では、信号線の
# "端" に wave port を置くのは不向き。wave port は内部で同軸(coax)ポート扱いに
# なり、ポート領域内に via か bondwire が必要になる。本課題は via の無い平面
# トレースなので、wave port だとメッシュ生成が失敗する
# （"could not find suitable geometry to form the terminal of the coax port"）。
#
# 正解は create_edge_port_vertical の "Gap" タイプ。信号線の端のエッジと
# リファレンス層（GND）との間にギャップ励振を作るため via 不要で、
# ストリップライン端に適する。P/N それぞれ入力側・出力側に1つずつ置く。
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

# 6. 保存して閉じる
edb.save()
edb.close()

# ---------------------------------------------------------------------------
# 7. HFSS 3D Layout で開いてセットアップ・スイープ・解析
# ---------------------------------------------------------------------------
h3d = Hfss3dLayout(
    project=AEDB_PATH,
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

setup = h3d.create_setup(name="MySetup")

# 周波数スイープ（0〜20GHz, 201点, Interpolating）。引数は unit（units ではない）
h3d.create_linear_count_sweep(
    setup=setup.name,
    unit="GHz",
    start_frequency=0,
    stop_frequency=20,
    num_of_freq_points=201,
    sweep_type="Interpolating",
)

# 8. 解析を実行する
#
# メッシュ生成 → 適応解析 → 周波数スイープ まで走るため数分かかる。
# blocking=True（既定）なので、解析が完了するまでこの呼び出しは戻らない。
# もしここで "mesh generation" エラーが出る場合、ほとんどはポートの作り方が
# モデル構造に合っていない（例: ストリップラインに wave port を使った）こと
# が原因。上記 5. のとおり vertical gap port を使えば回避できる。
h3d.analyze_setup(name="MySetup")

# 9. 保存して終了する（normal は解析実行までで終了。ポスト処理は hard 以降）
h3d.save_project()
h3d.release_desktop(close_projects=True, close_desktop=True)
