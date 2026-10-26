"""演習1: 回路要素の配置と配線（起動 → 配置 → 配線 → 保存 → 終了）。"""

from ansys.aedt.core import Circuit
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False


def left_right(component):
    """部品のピンを X 座標でソートし、(左ピン座標, 右ピン座標) を返す。

    回路部品はピン名が種類ごとに異なる（抵抗=terminals_0/1、インダクタ=n1/n2、
    コンデンサ=positive/negative）。ピン名に依存せず位置で左右を判定することで、
    配線を部品種類に関わらず共通化する。
    """
    pins = sorted(component.pins, key=lambda p: p.location[0])
    return pins[0].location, pins[-1].location


# 1. Circuit を起動する（Twin Builder を選んだ場合も以降のコードは同じ）
app = Circuit(
    design="Circuit_Basics",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
sch = app.modeler.schematic

# 2. 抵抗・インダクタ・コンデンサを横一列に配置する
r = sch.create_resistor(name="R1", value=100, location=[0.02, 0.0])
l = sch.create_inductor(name="L1", value=1e-6, location=[0.04, 0.0])
c = sch.create_capacitor(name="C1", value=1e-9, location=[0.06, 0.0])

# 3. 各部品の左右ピン座標を取得する
r_left, r_right = left_right(r)
l_left, l_right = left_right(l)
c_left, c_right = left_right(c)

# 4. R→L→C を直列に配線する
sch.create_wire([r_right, l_left])
sch.create_wire([l_right, c_left])

# 5. 接地（GND）を配置する
sch.create_gnd(location=[0.06, -0.03])

# 6. 保存して終了する（easy なので Setup 作成・解析は行わない）
app.save_project()
app.release_desktop(close_projects=True, close_desktop=True)
