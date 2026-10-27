"""演習1: ブリッジ整流回路+コンデンサフィルタの波形ポスト処理（AEDT内ポスト処理）。

starter 版: `# TODO` を埋めて solution.py と同じ動作を目指す。
モデル作成部分は normal 課題と同じなので、迷ったら
`1.normal/twin_builder/ex01_rectifier/solution.py` を参考にしてよい。
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
# TODO: V_AMPL / AC_FREQ / C_FILTER / R_LOAD を定義する
#       （"FREQ"という名前は使わないこと。予約語と衝突する）

sch = tb.modeler.schematic
G = 0.00254

# 3. 部品を配置する（normalと同じ回路構成: 電源・ダイオード4個・コンデンサ・抵抗・GND）
# TODO: normal課題と同じ部品配置・配線を行う

# 4. 過渡解析を実行する
# TODO: tb.set_end_time("100ms")
# TODO: tb.analyze_setup("TR")

# ---------------------------------------------------------------------------
# 5. AEDT内ポスト処理: 入力交流電圧・出力DC電圧の波形レポートを作成する
# ---------------------------------------------------------------------------
# 【重要】Twin Builder の過渡解析データは report_category="Standard" を明示しないと
# get_solution_data / create_report が正しく動かない。
# TODO: tb.post.create_report(expressions="V_AC.V", setup_sweep_name="TR", domain="Time",
#         report_category="Standard", plot_name="AC_Input_Voltage")
# TODO: tb.post.create_report(expressions="RL.V", setup_sweep_name="TR", domain="Time",
#         report_category="Standard", plot_name="DC_Output_Voltage")

# 6. 保存して終了する
tb.save_project()
tb.release_desktop(close_projects=True, close_desktop=True)
