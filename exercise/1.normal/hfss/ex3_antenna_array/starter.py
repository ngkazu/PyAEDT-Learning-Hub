"""演習3: ダイポールアレイアンテナ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"
NUM_ELEMENTS = 4  # 配列素子数（Pythonのループ回数として使うだけなので、HFSSの設計変数にはしない）

settings.release_on_exception = False

# TODO: 1. Hfss を Modal ソリューションで起動する
hfss = None

# TODO: 2. 設計変数 l_dipole = "10.2cm", element_spacing = "15cm" を定義する

# TODO: 3. NUM_ELEMENTS回ループし、各素子ごとに
#          modeler.create_coordinate_system(origin=[f"{i}*element_spacing", 0, 0], name=f"CS_Element{i}") で
#          ローカル座標系を作り、その座標系（coordinate_system=cs_name）を指定して
#          Dipole_Antenna_DM を挿入する（dipole_length を "l_dipole" に紐づける）
component_name = "Dipole_Antenna_DM"

# TODO: 4. create_open_region(frequency="1.5GHz") で解析領域を作成する

# TODO: 5. セットアップ "MySetup" を作成する
#          （MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"], MaximumPasses=2 を create_setup の引数として渡す）

# TODO: 6. 周波数掃引 "Sweep1"（Interpolating, 1GHz-2GHz）を追加する

# TODO: 7. 解析を実行する

# TODO: 8. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
