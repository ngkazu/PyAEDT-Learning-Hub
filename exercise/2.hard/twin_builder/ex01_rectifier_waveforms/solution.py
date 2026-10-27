"""演習1: ブリッジ整流回路+コンデンサフィルタの波形ポスト処理（AEDT内ポスト処理）。

normal（モデル作成〜解析実行）と同じ回路に、以下を追加する:
  - 交流入力電圧（V_AC.V）の波形レポートを作成する
  - 負荷（整流後のDC出力）電圧（RL.V）の波形レポートを作成する

どちらも過渡解析（Time domain）の波形レポートで、AEDT内で直接グラフとして確認できる。
"""

from ansys.aedt.core import TwinBuilder
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Twin Builder を起動する
tb = TwinBuilder(
    design="RectifierWaveforms",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# 2. 回路の設計変数を定義する（normalと同じ）
tb["V_AMPL"] = "100V"
tb["AC_FREQ"] = "50Hz"
tb["C_FILTER"] = "1uF"
tb["R_LOAD"] = "100kohm"

sch = tb.modeler.schematic
G = 0.00254

# 3. 部品を配置する（normalと同じ回路構成）
source = sch.create_voltage_source(
    "V_AC", "ESINE", "V_AMPL", "AC_FREQ", location=[-1 * G, 0]
)
diode1 = sch.create_diode(name="D1", location=[10 * G, 6 * G], angle=270)
diode2 = sch.create_diode(name="D2", location=[20 * G, 6 * G], angle=270)
diode3 = sch.create_diode(name="D3", location=[10 * G, -4 * G], angle=270)
diode4 = sch.create_diode(name="D4", location=[20 * G, -4 * G], angle=270)
capacitor = sch.create_capacitor(
    name="C_FILT", value="C_FILTER", location=[29 * G, -10 * G]
)
resistor = sch.create_resistor(name="RL", value="R_LOAD", location=[39 * G, -10 * G])
gnd = sch.create_gnd(location=[5 * G, -16 * G])

# 4. 配線する（normalと同じ）
sch.create_wire(points=[diode1.pins[0].location, diode3.pins[0].location])
sch.create_wire(points=[diode2.pins[1].location, diode4.pins[1].location])
sch.create_wire(points=[diode1.pins[1].location, diode2.pins[0].location])
sch.create_wire(points=[diode3.pins[1].location, diode4.pins[0].location])
sch.create_wire(
    points=[source.pins[1].location, [0, 10 * G], [15 * G, 10 * G], [15 * G, 5 * G]]
)
sch.create_wire(
    points=[source.pins[0].location, [0, -10 * G], [15 * G, -10 * G], [15 * G, -5 * G]]
)
sch.create_wire(points=[resistor.pins[0].location, [40 * G, 0], [22 * G, 0]])
sch.create_wire(points=[capacitor.pins[0].location, [30 * G, 0]])
sch.create_wire(
    points=[resistor.pins[1].location, [40 * G, -15 * G], gnd.pins[0].location]
)
sch.create_wire(points=[capacitor.pins[1].location, [30 * G, -15 * G]])
sch.create_wire(points=[gnd.pins[0].location, [5 * G, 0], [8 * G, 0]])

tb.modeler.zoom_to_fit()

# 5. 過渡解析を実行する
tb.set_end_time("100ms")
tb.analyze_setup("TR")

# ---------------------------------------------------------------------------
# 6. AEDT内ポスト処理: 入力交流電圧・出力DC電圧の波形レポートを作成する
# ---------------------------------------------------------------------------
# 【重要】Twin Builder の過渡解析データは report_category="Standard" を明示しないと
# get_solution_data / create_report が正しく動かない（データなしの False/空プロットになる）。
tb.post.create_report(
    expressions="V_AC.V",
    setup_sweep_name="TR",
    domain="Time",
    report_category="Standard",
    plot_name="AC_Input_Voltage",
)
tb.post.create_report(
    expressions="RL.V",
    setup_sweep_name="TR",
    domain="Time",
    report_category="Standard",
    plot_name="DC_Output_Voltage",
)

# 7. 保存して終了する
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
