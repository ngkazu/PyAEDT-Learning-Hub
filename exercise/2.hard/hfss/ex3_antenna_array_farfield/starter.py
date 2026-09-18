"""演習3: ダイポールアレイアンテナ（S/遠方界のポスト処理）。"""

import itertools

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"
NUM_ELEMENTS = 4  # 配列素子数（Pythonのループ回数として使うだけなので、HFSSの設計変数にはしない）

settings.release_on_exception = False

# TODO: 1. Hfss を Modal ソリューションで起動する
hfss = None

# TODO: 2. 設計変数 l_dipole = "10.2cm", element_spacing = "15cm" と center_freq = "1.5GHz" を定義する

# TODO: 3. 1.normal/hfss/ex3_antenna_array/solution.py と同じ手順で、NUM_ELEMENTS個の
#          Dipole_Antenna_DM をローカル座標系ごとに配置する
component_name = "Dipole_Antenna_DM"

# TODO: 4. create_open_region(frequency=center_freq) で解析領域を作成する

# TODO: 5. セットアップ "MySetup" を作成する
#          （MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"], MaximumPasses=2 を create_setup の引数として渡す）

# TODO: 6. 周波数掃引を2つ追加する
#          - "DiscreteSweep"（Discrete, 1GHz-2GHz, RangeStep="0.5GHz", SaveFields=True）
#          - "InterpolatingSweep"（Interpolating, 1GHz-2GHz, SaveFields=False）

# TODO: 7. 解析を実行する

# TODO: 8. hfss.excitation_names の全組み合わせ（itertools.product）を ports/ports_excited に渡し、
#          create_scattering() で自己反射・相互結合を含むSパラメータレポートを作成する

# TODO: 9. hfss.available_variations.nominal_values を取得し、Freq/Theta/Phiを書き換えてから
#          hfss.post.create_report(expressions="db(GainTheta)", setup_sweep_name=disc_sweep.name,
#          variations=variations, primary_sweep_variable="Theta", context="Elevation",
#          report_category="Far Fields", plot_type="Radiation Pattern", plot_name=...) で
#          アレイ全体のElevation面ゲインパターンをレポート作成する

# TODO: 10. 保存して終了する
