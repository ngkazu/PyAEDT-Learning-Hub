"""演習1: RLC直列回路の過渡解析（モデル作成〜解析実行）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
"""

from ansys.aedt.core import Circuit
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False


def left_right(component):
    """部品のピンを X 座標でソートし、(左ピン座標, 右ピン座標) を返す。

    Circuit の部品はピン名が種類ごとに異なる（抵抗=terminals_0/1、
    インダクタ=n1/n2、コンデンサ=positive/negative）。ピン名に依存せず
    位置で左右を判定することで、配線を部品種類に関わらず共通化する。
    """
    pins = sorted(component.pins, key=lambda p: p.location[0])
    return pins[0].location, pins[-1].location


# 1. Circuit を起動する
cir = Circuit(
    design="RLC_Transient",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
sch = cir.modeler.schematic

# 2. 直列 RLC を横一列に配置する（R=50ohm, L=1nH, C=1pF）
# TODO: sch.create_resistor / create_inductor / create_capacitor で
#       R1, L1, C1 を location=[0.02,0], [0.04,0], [0.06,0] に配置する
r = ...
l = ...
c = ...

r_left, r_right = left_right(r)
l_left, l_right = left_right(l)
c_left, c_right = left_right(c)

# 3. R→L→C を直列に配線する
# TODO: sch.create_wire([...]) で R右-L左、L右-C左 をつなぐ

# 4. パルス電圧源を配置する
# TODO: sch.create_voltage_pulse(name="V1",
#       value_lists=[0, 1, 0, "1us", "1ns", "1ns", "5us", "10us"],
#       location=[0.0, 0.0]) を作成する
v = ...
v_pins = sorted(v.pins, key=lambda p: p.location[1])  # Y 順（下=負, 上=正）
v_neg, v_pos = v_pins[0].location, v_pins[-1].location

# 5. 接地（GND）を配置する
# TODO: sch.create_gnd(location=[0.0, -0.03]) を作成する
gnd = ...
g = gnd.pins[0].location

# 6. 閉ループに配線する（電源+ → R左、C右 → GND、電源- → GND）
# TODO: sch.create_wire(...) を3本作成する
#       - [v_pos, r_left]
#       - [c_right, [c_right[0], -0.03], [g[0], -0.03], g]
#       - [v_neg, [v_neg[0], -0.03], g]

# 7. 過渡解析（Transient）セットアップを作成する
# TODO: cir.create_setup(name="Transient", setup_type="NexximTransient") を作成し、
#       setup.props["TransientData"] = ["0.01us", "10us"] を設定して update() する
setup = ...

# 8. 解析を実行する
# TODO: setup.analyze() を呼ぶ

# 9. 保存して終了する
cir.save_project()
cir.release_desktop(close_projects=True, close_desktop=True)
