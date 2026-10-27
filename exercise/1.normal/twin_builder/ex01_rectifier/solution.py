"""演習1: ブリッジ整流回路+コンデンサフィルタの過渡解析（モデル作成〜解析実行）。

交流電源 → ダイオードブリッジ整流 → コンデンサ平滑フィルタ → 負荷抵抗、という
AC-DC変換回路を Twin Builder で組み、過渡解析を実行する。
電圧振幅・周波数・フィルタ容量・負荷抵抗は設計変数として定義し、ハードコードしない。
"""

from ansys.aedt.core import TwinBuilder
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Twin Builder を起動する
tb = TwinBuilder(
    design="Rectifier",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# 2. 回路の設計変数を定義する（値をハードコードせず、変数名を部品の value に渡す）
#    【重要】"FREQ" という変数名は Twin Builder の内部予約語と衝突して登録されない。
#    周波数の変数名には "AC_FREQ" のような別名を使うこと。
tb["V_AMPL"] = "100V"  # 交流電源の振幅
tb["AC_FREQ"] = "50Hz"  # 交流電源の周波数
tb["C_FILTER"] = "1uF"  # 平滑コンデンサの容量
tb["R_LOAD"] = "100kohm"  # 負荷抵抗

sch = tb.modeler.schematic

# 3. 部品を配置する（グリッド間隔 G[m]。location=[x, y] はこの間隔の倍数で指定する）
G = 0.00254

# 交流電圧源（ESINE=正弦波）。amplitude/freq に変数名の文字列を渡す
source = sch.create_voltage_source(
    "V_AC", "ESINE", "V_AMPL", "AC_FREQ", location=[-1 * G, 0]
)

# ブリッジ整流用のダイオード4個（angle はラジアンではなく度数で指定する回転角）
diode1 = sch.create_diode(name="D1", location=[10 * G, 6 * G], angle=270)
diode2 = sch.create_diode(name="D2", location=[20 * G, 6 * G], angle=270)
diode3 = sch.create_diode(name="D3", location=[10 * G, -4 * G], angle=270)
diode4 = sch.create_diode(name="D4", location=[20 * G, -4 * G], angle=270)

# 平滑コンデンサ・負荷抵抗（value に変数名の文字列を渡す）
capacitor = sch.create_capacitor(
    name="C_FILT", value="C_FILTER", location=[29 * G, -10 * G]
)
resistor = sch.create_resistor(name="RL", value="R_LOAD", location=[39 * G, -10 * G])

# 接地（GND）
gnd = sch.create_gnd(location=[5 * G, -16 * G])

# 4. 部品を配線する（ダイオードブリッジを組み、電源・フィルタ・負荷・GNDを接続する）
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

# 5. 過渡解析の終了時間を設定し、解析を実行する
tb.set_end_time("100ms")
tb.analyze_setup("TR")

# 6. 保存して終了する
# normalはSetup作成→解析実行までで終了する（ポスト処理はhard以降で追加するため、ここでは行わない）。
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
