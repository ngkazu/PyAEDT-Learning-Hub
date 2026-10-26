"""演習1: RLCローパスフィルタのSパラメータ解析（AEDT内ポスト処理）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
"""

from ansys.aedt.core import Circuit
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False


def left_right(component):
    """部品のピンを X 座標でソートし、(左ピン座標, 右ピン座標) を返す。"""
    pins = sorted(component.pins, key=lambda p: p.location[0])
    return pins[0].location, pins[-1].location


# 1. Circuit を起動する
cir = Circuit(
    design="RLC_LowpassFilter",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
sch = cir.modeler.schematic

# 2. RLC ローパス用に R/L/C を配置する（R=50ohm, L=10nH, C=1nF → カットオフ ~2.4GHz）
# TODO: create_resistor([0.02,0]) / create_inductor([0.04,0]) / create_capacitor([0.06,0])
r = ...
l = ...
c = ...
r_left, r_right = left_right(r)
l_left, l_right = left_right(l)
c_left, c_right = left_right(c)

# R→L を直列に配線（L の右端が出力ノード）
# TODO: sch.create_wire([r_right, l_left])

# 3. 入出力インターフェースポートを配置する
# TODO: sch.create_interface_port(name="Port1", location=[0.0, 0.0])
#       sch.create_interface_port(name="Port2", location=[0.08, 0.0])
p1 = ...
p2 = ...

# 4. 接地を配置する
# TODO: sch.create_gnd(location=[0.06, -0.03])
gnd = ...
g = gnd.pins[0].location

# 5. 配線する（Port1→R左、L右→C左、L右→Port2、C右→GND）
# TODO: create_wire を4本
#       [p1.pins[0].location, r_left]
#       [l_right, c_left]
#       [l_right, p2.pins[0].location]
#       [c_right, [c_right[0], -0.03], g]

# 6. 周波数ドメイン（LNA）セットアップと周波数スイープを作成する
# TODO: cir.create_setup(name="LNA", setup_type="NexximLNA") を作成し、
#       setup.add_sweep_count(sweep_variable="Freq", start=0.01, stop=5, count=401,
#                             units="GHz", count_type="Linear") を呼ぶ
setup = ...

# 7. 解析を実行する
# TODO: setup.analyze()

# 8. AEDT内ポスト処理: S21・S11 のレポートを作成する
# TODO: cir.post.create_report(expressions="dB(S(Port2,Port1))", setup_sweep_name="LNA",
#                              domain="Sweep", plot_name="S21_InsertionLoss")
#       cir.post.create_report(expressions="dB(S(Port1,Port1))", setup_sweep_name="LNA",
#                              domain="Sweep", plot_name="S11_ReturnLoss")

# 9. 保存して終了する
cir.save_project()
cir.release_desktop(close_projects=True, close_desktop=True)
