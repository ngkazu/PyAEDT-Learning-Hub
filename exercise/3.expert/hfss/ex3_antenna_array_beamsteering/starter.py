"""演習3: ダイポールアレイアンテナ ビームステアリングの Python 後処理（CSV入出力・PyVista可視化）。"""

import numpy as np
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"
NUM_ELEMENTS = 4  # 配列素子数（Pythonのループ回数として使うだけなので、HFSSの設計変数にはしない）
ELEMENT_SPACING_M = 0.15  # HFSS変数 element_spacing="15cm" と同じ値（Python側の理論計算用）
CENTER_FREQ_HZ = 1.5e9  # HFSS変数 center_freq="1.5GHz" と同じ値（Python側の理論計算用）

settings.release_on_exception = False

# TODO: 1. phase_weights.csv を読み込み、element_index順にソートしたphase_deg のリストを作る

# TODO: 2. 1.normal/hfss/ex3_antenna_array と同じ手順でダイポールアレイアンテナを作成し、解析する
hfss = None

# TODO: 3. sorted(hfss.excitation_names) と phases_deg を対応させ、
#          hfss.edit_sources({name: ("1W", f"{phase}deg") for ...}) で励振位相を変更する
#          （振幅は全素子1Wで固定。解の再計算はしない）

# TODO: 4. NumPyで理論上のアレイファクタを計算する
#          array_factor = sum_n exp(1j * (k * ELEMENT_SPACING_M * n * sin(theta) + phase_n)) の絶対値をdB化する

# TODO: 5-6. 理論アレイファクタをmatplotlibでプロットして画像保存し、
#            theta_deg/array_factor_db をCSVファイル（results_array_factor.csv）に出力する

# TODO: 7. hfss.get_antenna_data() で実際の遠方界データを取得し、
#          ffdata.farfield_data.plot_3d(quantity="RealizedGain", output_file=..., show=False) で
#          PyVistaの3D放射パターンを画像出力する

# TODO: 8. ffdata.farfield_data.plot_3d(quantity="RealizedGain", show=True) で、
#          同じ3D放射パターンをインタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する

# TODO: 9. 保存して終了する
