"""演習1: ブリッジ整流回路+コンデンサフィルタの過渡解析（モデル作成〜解析実行）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
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

# 2. 回路の設計変数を定義する
# TODO: tb["V_AMPL"] = "100V"（交流電源の振幅）
#       tb["AC_FREQ"] = "50Hz"（交流電源の周波数。"FREQ"という名前は予約語と衝突するため使わないこと）
#       tb["C_FILTER"] = "1uF"（平滑コンデンサの容量）
#       tb["R_LOAD"] = "100kohm"（負荷抵抗）

sch = tb.modeler.schematic
G = 0.00254  # グリッド間隔[m]。location=[x, y] はこの倍数で指定する

# 3. 部品を配置する
# TODO: sch.create_voltage_source("V_AC", "ESINE", "V_AMPL", "AC_FREQ", location=[-1*G, 0])
#       で交流電圧源を作る（amplitude/freq に変数名の文字列を渡す）
source = ...

# TODO: sch.create_diode(name=..., location=[...], angle=270) を4つ呼んで
#       ブリッジ整流用のダイオード D1〜D4 を配置する
#       D1: [10*G, 6*G] / D2: [20*G, 6*G] / D3: [10*G, -4*G] / D4: [20*G, -4*G]
diode1 = ...
diode2 = ...
diode3 = ...
diode4 = ...

# TODO: sch.create_capacitor(name="C_FILT", value="C_FILTER", location=[29*G, -10*G])
#       sch.create_resistor(name="RL", value="R_LOAD", location=[39*G, -10*G])
#       value に変数名の文字列を渡すこと
capacitor = ...
resistor = ...

# TODO: sch.create_gnd(location=[5*G, -16*G]) で接地を作る
gnd = ...

# 4. 部品を配線する
# TODO: 以下の配線を create_wire(points=[...]) で行う（ピン座標は component.pins[i].location）
#   - ダイオードブリッジを組む（D1-D3、D2-D4、D1-D2、D3-D4 を接続）
#   - 電源の両端をブリッジの上下ノードに接続する
#   - 負荷抵抗・フィルタコンデンサ・GND を接続する
#   詳細な配線パターンに迷ったら solution.py を参考にしてよい。

tb.modeler.zoom_to_fit()

# 5. 過渡解析の終了時間を設定し、解析を実行する
# TODO: tb.set_end_time("100ms")
# TODO: tb.analyze_setup("TR")

# 6. 保存して終了する
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
