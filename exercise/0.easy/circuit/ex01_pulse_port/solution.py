"""演習1: パルス電圧源とインターフェースポートの配置（起動 → 配置 → 配線 → 保存 → 終了）。

Circuit 固有の基本操作として、パルス波形を持つ電圧源と、回路の入出力インターフェース
（インターフェースポート）を扱う。インターフェースポートは、このシリーズの hard課題
（`2.hard/circuit/ex01_rlc_filter_sparams/`）でSパラメータ解析の入出力として使うものと同じ。
"""

from ansys.aedt.core import Circuit
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Circuit を起動する
cir = Circuit(
    design="PulsePort",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
sch = cir.modeler.schematic

# 2. パルス電圧源を配置する
#    value_lists = [初期値, パルス値, 遅延, 立上り, 立下り, パルス幅, 周期]
v = sch.create_voltage_pulse(
    name="V1",
    value_lists=[0, 5, 0, "1ns", "1ns", "10ns", "20ns"],
    location=[0.0, 0.0],
)

# 3. 抵抗を配置する
r = sch.create_resistor(name="R1", value=50, location=[0.02, 0.0])

# 4. インターフェースポート（回路の入出力端子）を2つ配置する
#    【重要】create_interface_port の戻り値は CircuitComponent ではなく Excitations 型。
#    .parameters["InstanceName"] には名前が入らないので、.name 属性でポート名を取得する。
p1 = sch.create_interface_port(name="Port1", location=[-0.02, 0.0])
p2 = sch.create_interface_port(name="Port2", location=[0.04, 0.0])

# 5. 接地（GND）を配置する
gnd = sch.create_gnd(location=[0.02, -0.02])

# 6. 配線する（Port1 → 電源+、電源- → GND、Port1 → R左、R右 → Port2）
v_pins = sorted(v.pins, key=lambda p: p.location[1])  # Y 順（下=負, 上=正）
v_neg, v_pos = v_pins[0].location, v_pins[-1].location
r_pins = sorted(r.pins, key=lambda p: p.location[0])
r_left, r_right = r_pins[0].location, r_pins[-1].location

sch.create_wire(points=[p1.pins[0].location, v_pos])
sch.create_wire(points=[v_neg, [v_neg[0], -0.02], gnd.pins[0].location])
sch.create_wire(points=[p1.pins[0].location, [-0.02, 0.0], r_left])
sch.create_wire(points=[r_right, p2.pins[0].location])

# 7. 保存して終了する（easy なので Setup 作成・解析は行わない）
cir.save_project()
cir.release_desktop(close_projects=True, close_desktop=True)
