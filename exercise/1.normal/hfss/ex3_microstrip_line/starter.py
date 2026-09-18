"""演習3: マイクロストリップ線路（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 設計寸法（このプロジェクトの他演習とは異なり、Python側の定数として扱う。理由は課題文を参照）。
SUB_W = 6.0  # 基板の幅 [mm]（Y方向）
SUB_H = 1.0  # 基板の厚さ [mm]（Z方向）
LINE_W = 1.5  # マイクロストリップ導体幅 [mm]（Y方向）
LINE_L = 10.0  # マイクロストリップ導体長さ [mm]（X方向、伝送方向）
AIR_H = 3.0  # 基板上部のエアボックス高さ [mm]

# TODO: 1. Hfss を Terminal ソリューションで起動する
hfss = None

# TODO: 2. 基板（3Dソリッド、origin=[0,-SUB_W/2,0], sizes=[LINE_L,SUB_W,SUB_H], material="alumina_96pct"）
#          を作成する

# TODO: 3. GND と信号線を2Dシート（create_rectangle）として作成し、
#          それぞれ assign_finite_conductivity(assignment=..., material="copper", name=...) を割り当てる
#          （シートには Material プロパティが無いため、assign_material() では導体にならない点に注意）

# TODO: 4. エアボックス（origin=[0,-SUB_W/2,SUB_H], sizes=[LINE_L,SUB_W,AIR_H], material="vacuum"）を
#          基板の上面から作成する

# TODO: 5. エアボックスの両端面（YZ平面のシート）にWave Port（modes=1, renormalize=True, impedance=50）
#          を作成する

# TODO: 6. エアボックスの面のうち、下面・両端面（Wave Port面）を除いた面だけに
#          assign_radiation_boundary_to_faces() で輻射境界を割り当てる
#          （assign_radiation_boundary_to_objects() は6面すべてに割り当ててしまい、
#          GND/Line や Wave Port と重複するため使わない）

# TODO: 7. hfss.validate_full_design() でモデルを検証する

# TODO: 8. セットアップ "Setup1"（Frequency="10GHz", MaxDeltaS=0.02, MaximumPasses=6）を作成し、
#          hfss.create_linear_count_sweep(setup="Setup1", ...) で周波数スイープを追加する
#          （create_linear_count_sweep は setup オブジェクトではなく hfss 側のメソッドである点に注意）

# TODO: 9. 解析を実行する

# TODO: 10. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
