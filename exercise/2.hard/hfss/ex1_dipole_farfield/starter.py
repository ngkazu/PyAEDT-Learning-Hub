"""演習1: 半波長ダイポールアンテナ（S11・遠方界のポスト処理）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Hfss を Modal ソリューションで起動する
hfss = None

# TODO: 2. 設計変数 l_dipole = "10.2cm" と center_freq = "1.5GHz" を定義する

# TODO: 3. Dipole_Antenna_DM を挿入する（get_component_variables でパラメータ辞書を取得し、
#          dipole_length を "l_dipole" に書き換えてから insert_3d_component に渡す）

# TODO: 4. create_open_region(frequency=center_freq) で解析領域を作成する

# TODO: 5. セットアップ "MySetup" を作成する
#          （MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"], MaximumPasses=2 を create_setup の引数として渡す）

# TODO: 6. 周波数掃引を2つ追加する
#          - "DiscreteSweep"（Discrete, 1GHz-2GHz, RangeStep="0.5GHz", SaveFields=True）
#          - "InterpolatingSweep"（Interpolating, 1GHz-2GHz, SaveFields=False）

# TODO: 7. 解析を実行する

# TODO: 8. create_scattering(plot="Return Loss", sweep=interp_sweep.name) でS11レポートを作成する

# TODO: 9. Elevation面のゲインパターン（遠方界）レポートを作成する
#          hfss.available_variations.nominal_values を取得し、Freq/Theta/Phiを書き換えてから
#          hfss.post.create_report(expressions="db(GainTheta)", setup_sweep_name=disc_sweep.name,
#          variations=variations, primary_sweep_variable="Theta", context="Elevation",
#          report_category="Far Fields", plot_type="Radiation Pattern", plot_name=...) に渡す

# TODO: 10. 保存して終了する
