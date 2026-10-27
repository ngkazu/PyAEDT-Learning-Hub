"""演習1: 半波整流回路（単一ダイオード）の配置（起動 → 配置 → 配線 → 保存 → 終了）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
"""

from ansys.aedt.core import TwinBuilder
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Twin Builder を起動する
tb = TwinBuilder(
    design="HalfWave",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
sch = tb.modeler.schematic

G = 0.00254  # グリッド間隔[m]

# 2. パルス波形の電圧源を配置する（source_type="EPULSE"）
# TODO: sch.create_voltage_source("V_IN", "EPULSE", 10.0, 1000.0, location=[0, 0])
v_in = ...

# 3. ダイオードを1個配置する
# TODO: sch.create_diode(name="D1", location=[10*G, 0], angle=0)
diode = ...

# 4. 負荷抵抗を配置する
# TODO: sch.create_resistor(name="RL", value=1000, location=[20*G, 0])
resistor = ...

# 5. 接地（GND）を配置する
# TODO: sch.create_gnd(location=[10*G, -10*G])
gnd = ...


def left_right(component):
    """部品のピンを X 座標でソートし、(左ピン座標, 右ピン座標) を返す。"""
    pins = sorted(component.pins, key=lambda p: p.location[0])
    return pins[0].location, pins[-1].location


# 6. 配線する（電源 → ダイオード → 負荷抵抗 → GND → 電源、の直列ループ）
# TODO: left_right() でピン座標を取得し、create_wire() で配線する
#       （電源右 → D左、D右 → R左、R右 → GND、電源左 → GND）

tb.modeler.zoom_to_fit()

# 7. 保存して終了する
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
