"""演習1: 半波整流回路（単一ダイオード）の配置（起動 → 配置 → 配線 → 保存 → 終了）。

Twin Builder 固有の操作として、矩形パルス波形の電圧源と、非線形素子であるダイオードを
配置する。整流回路シリーズ（`1.normal/twin_builder/ex01_rectifier/`）の全波整流（ブリッジ）
の前段として、ダイオード1個だけの最もシンプルな半波整流回路を組む。
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
#    amplitude=10V, freq=1000Hz
v_in = sch.create_voltage_source("V_IN", "EPULSE", 10.0, 1000.0, location=[0, 0])

# 3. ダイオードを1個配置する（半波整流: 負の電圧をカットする）
diode = sch.create_diode(name="D1", location=[10 * G, 0], angle=0)

# 4. 負荷抵抗を配置する
resistor = sch.create_resistor(name="RL", value=1000, location=[20 * G, 0])

# 5. 接地（GND）を配置する
gnd = sch.create_gnd(location=[10 * G, -10 * G])


def left_right(component):
    """部品のピンを X 座標でソートし、(左ピン座標, 右ピン座標) を返す。"""
    pins = sorted(component.pins, key=lambda p: p.location[0])
    return pins[0].location, pins[-1].location


# 6. 配線する（電源 → ダイオード → 負荷抵抗 → GND → 電源、の直列ループ）
s_left, s_right = left_right(v_in)
d_left, d_right = left_right(diode)
r_left, r_right = left_right(resistor)

sch.create_wire(points=[s_right, d_left])
sch.create_wire(points=[d_right, r_left])
sch.create_wire(points=[r_right, [r_right[0], -10 * G], gnd.pins[0].location])
sch.create_wire(points=[s_left, [s_left[0], -10 * G], gnd.pins[0].location])

tb.modeler.zoom_to_fit()

# 7. 保存して終了する（easy なので Setup 作成・解析は行わない）
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
