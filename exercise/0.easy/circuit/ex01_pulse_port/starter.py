"""演習1: パルス電圧源とインターフェースポートの配置（起動 → 配置 → 配線 → 保存 → 終了）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
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
# TODO: sch.create_voltage_pulse(name="V1",
#         value_lists=[0, 5, 0, "1ns", "1ns", "10ns", "20ns"], location=[0.0, 0.0])
v = ...

# 3. 抵抗を配置する
# TODO: sch.create_resistor(name="R1", value=50, location=[0.02, 0.0])
r = ...

# 4. インターフェースポート（回路の入出力端子）を2つ配置する
#    【重要】create_interface_port の戻り値は CircuitComponent ではなく Excitations 型。
#    .parameters["InstanceName"] には名前が入らないので、.name 属性でポート名を取得する。
# TODO: sch.create_interface_port(name="Port1", location=[-0.02, 0.0])
#       sch.create_interface_port(name="Port2", location=[0.04, 0.0])
p1 = ...
p2 = ...

# 5. 接地（GND）を配置する
# TODO: sch.create_gnd(location=[0.02, -0.02])
gnd = ...

# 6. 配線する（Port1 → 電源+、電源- → GND、Port1 → R左、R右 → Port2）
# TODO: 部品のピン座標（component.pins[i].location）を使って create_wire() で配線する

# 7. 保存して終了する
cir.save_project()
cir.release_desktop(close_projects=True, close_desktop=True)
