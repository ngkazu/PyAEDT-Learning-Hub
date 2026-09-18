"""演習4: プローブ給電パッチアンテナ（S11・遠方界のポスト処理）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modeler.advanced_cad.stackup_3d import Stackup3D

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Hfss を Terminal ソリューションで起動する
hfss = None

# TODO: 2. 1.normal/hfss/ex4_patch_antenna/solution.py と同じ手順で、
#          Stackup3D・パッチ・プローブ給電ポートまでを作成する

# TODO: 3. セットアップ "MySetup"（setup_type="HFSSDriven", Frequency="10GHz"）を作成する

# TODO: 4. 周波数掃引を2つ追加する
#          - "DiscreteSweep"（sweep_type="Discrete", 8-12GHz, num_of_freq_points=9, save_fields=True）
#          - "InterpolatingSweep"（sweep_type="Interpolating", 8-12GHz, save_fields=False）

# TODO: 5. 解析を実行する

# TODO: 6. create_scattering(plot="Return Loss", sweep=interp_sweep.name) でS11レポートを作成する

# TODO: 7. hfss.insert_infinite_sphere(theta_start=-180, theta_stop=180, theta_step=5,
#          phi_start=0, phi_stop=180, phi_step=5) で無限球面を作成する（戻り値を sphere 変数に保持する）
#          （create_open_regionと違い、create_region+assign_radiation_boundary_to_objectsだけでは
#          無限球面が作られないため、遠方界レポートの前に明示的に追加する必要がある）

# TODO: 8. hfss.available_variations.nominal_values を取得し、Freq/Theta/Phiを書き換えてから
#          hfss.post.create_report(expressions="db(GainTheta)", setup_sweep_name=disc_sweep.name,
#          variations=variations, primary_sweep_variable="Theta", context=sphere.name,
#          report_category="Far Fields", plot_type="Radiation Pattern", plot_name=...) で
#          Elevation面のゲインパターンをレポート作成する
#          （contextには手順7で作った無限球面の名前(sphere.name)を渡す。遠方界レポートのcontextは
#          「無限球面の名前」を指定する仕様のため）

# TODO: 9. 保存して終了する
