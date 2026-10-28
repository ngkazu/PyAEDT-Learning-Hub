"""演習1: 差動ペア伝送線路（HFSS 3D Layout, 差動Sパラメータ解析・AEDT内ポスト処理）。

normal（`1.normal/hfss_3d_layout/ex01_diff_pair/`）と同じストリップライン差動ペアモデルに、
以下を追加する:
  - 入出力それぞれの P/N ポートを差動ペア（Differential Pair）として設定する
  - 差動Sパラメータ（Sdd21: 挿入損失、Sdd11: 反射）の AEDT 内レポートを作成する

他の課題と異なり、ジオメトリは PyEDB（`pyedb`）で作る（レイヤー/ECAD の操作に向くため）。
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
# ストリップライン端には via 不要の vertical gap port を使う
# （wave port は coax 扱いになり via が必要になってメッシュ生成が失敗するため。詳細は
# normal課題の README / lecture/31_pyedb_basic.md §6 を参照）。
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

# 周波数スイープ（0〜20GHz, 201点, Interpolating）。戻り値を変数で受けて .name を使う
# （setup.sweeps[0] は再取得タイミングによって空になることがあるため、戻り値を直接使うのが確実）
sweep = h3d.create_linear_count_sweep(
    setup=setup.name,
    unit="GHz",
    start_frequency=0,
    stop_frequency=20,
    num_of_freq_points=201,
    sweep_type="Interpolating",
)
setup_sweep = f"{setup.name} : {sweep.name}"

# ---------------------------------------------------------------------------
# 8. 差動ペア（Differential Pair）を設定する
# ---------------------------------------------------------------------------
# 入力側（P_in/N_in）と出力側（P_out/N_out）それぞれを差動ペアとして登録する。
# これにより Sパラメータレポートで差動モード（Sdd）・コモンモード（Scc）の
# 式が使えるようになる。
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

# 9. 解析を実行する（メッシュ生成〜適応解析〜周波数スイープで数分かかる）
h3d.analyze_setup(name="MySetup")

# ---------------------------------------------------------------------------
# 10. AEDT内ポスト処理: 差動Sパラメータ（Sdd21・Sdd11）のレポートを作成する
# ---------------------------------------------------------------------------
# 【重要】差動Sパラメータのレポートは context="Differential Pairs" を指定しないと、
# 式の文法が正しくてもプロットが空になる。
h3d.post.create_report(
    expressions="dB(S(Diff_Out,Diff_In))",  # Sdd21: 差動挿入損失
    setup_sweep_name=setup_sweep,
    context="Differential Pairs",
    plot_name="Sdd21_InsertionLoss",
)
h3d.post.create_report(
    expressions="dB(S(Diff_In,Diff_In))",  # Sdd11: 差動反射（入力側）
    setup_sweep_name=setup_sweep,
    context="Differential Pairs",
    plot_name="Sdd11_ReturnLoss",
)

# 11. 保存して終了する
h3d.save_project()
h3d.release_desktop(close_projects=True, close_desktop=True)
