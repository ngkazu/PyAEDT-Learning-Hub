"""演習1: ダイポールアンテナ S11・遠方界データの Python 後処理（VSWR・帯域幅算出・CSV入出力）。"""

import numpy as np
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. conditions.csv を読み込み、l_dipole / center_freq を取得する（csv.DictReaderを使う）
l_dipole = None
center_freq = None

# TODO: 2. normal/ex01_dipole_antenna と同じ手順でダイポールアンテナを作成・解析する
#          （l_dipole, center_freqはCSVから読み込んだ値を使う）
hfss = None

# TODO: 3. post.get_solution_data() でS11の SolutionData を取得する
#          （hfss.excitation_names[0]で実際の励振名を取得し、setup_sweep_nameとreport_category="Modal Solution Data"を指定する）
solution_data = None

# TODO: 4. get_expression_data(formula="db20") で周波数とS11[dB]の配列を取得する
freq = None
s11_db = None

# TODO: 5. VSWR を計算する（gamma_abs = 10 ** (s11_db / 20)）

# TODO: 6. -10dB帯域幅を求める

# TODO: 7-8. matplotlib で S11とVSWRを重ねてプロットし、画像として保存する

# TODO: 9. S11・VSWRの結果をCSVファイル（results_s11_vswr.csv）に出力する

# TODO: 10. hfss.get_antenna_data() で遠方界データを取得し、
#           ffdata.farfield_data.plot_3d(quantity="RealizedGain", output_file=..., show=False) で
#           PyVistaの3D放射パターンを画像出力する

# TODO: 11. ffdata.farfield_data.plot_3d(quantity="RealizedGain", show=True) で、
#           同じ3D放射パターンをインタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する

# TODO: 12. 保存して終了する
