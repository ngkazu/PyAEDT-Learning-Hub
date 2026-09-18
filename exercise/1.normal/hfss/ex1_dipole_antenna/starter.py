"""演習1: 半波長ダイポールアンテナ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Hfss を Modal ソリューションで起動する
hfss = None

# TODO: 2. 設計変数 l_dipole = "10.2cm" を定義する

# TODO: 3. Dipole_Antenna_DM を挿入する（get_component_variables でパラメータ辞書を取得し、
#          dipole_length を "l_dipole" に書き換えてから insert_3d_component に渡す）

# TODO: 4. create_open_region(frequency="1.5GHz") で解析領域を作成する

# TODO: 5. セットアップ "MySetup" を作成する
#          （MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"], MaximumPasses=2 を create_setup の引数として渡す）

# TODO: 6. 周波数スイープ "Sweep1"（Interpolating, 1GHz-2GHz）を追加する

# TODO: 7. 解析を実行する

# TODO: 8. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
