"""演習1: ブスバー解析（モデル作成〜解析実行）。"""

from ansys.aedt.core import Q3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Q3d を起動し、modeler.model_units = "mm" を設定する
q3d = None

# TODO: 2. 3本のブスバーを create_polyline(xsection_type="Rectangle", xsection_width="5mm",
#          xsection_height="1mm") で作成する（README.mdの表を参照）
#          Bar1: copper, [0,0,0] -> [-100,0,0]
#          Bar2: aluminum, [0,-15,0] -> [-150,-15,0]
#          Bar3: copper, [0,-30,0] -> [-175,-30,0] -> [-175,-10,0]

# TODO: 3. 基板を create_box(origin=[50, 30, -0.5], sizes=[-250, -100, -3], material="FR4_epoxy") で作成する

# TODO: 4. auto_identify_nets() でネットを自動識別する

# TODO: 5. 各バーにソース・シンクを割り当てる（README.mdの表を参照、direction は q3d.axis_directions を使う）
#          Bar1: Source1(XPos) / Sink1(XNeg)
#          Bar2: Source2(XPos) / Sink2(XNeg)
#          Bar3: Source3(XPos) / Sink3(YPos)

# TODO: 6. セットアップを create_setup(name="MySetup", props={"AdaptiveFreq": "1000MHz"}) で作成する

# TODO: 7. setup.create_linear_step_sweep(name="my_sweep", unit="GHz", start_frequency=0,
#          stop_frequency=10, step_size=1, sweep_type="Discrete", save_fields=True) で
#          周波数スイープを追加する
#          （sweep_type="Interpolating"だとSaveFieldsが常にFalseになり、hard以降のポスト処理ができなくなる）

# TODO: 8. 解析を実行する

# TODO: 9. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
