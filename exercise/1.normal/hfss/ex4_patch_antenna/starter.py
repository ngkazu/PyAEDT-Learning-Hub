"""演習4: プローブ給電パッチアンテナ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modeler.advanced_cad.stackup_3d import Stackup3D

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Hfss を Terminal ソリューションで起動する（プローブ給電はTerminalソリューションで扱う）
hfss = None

# TODO: 2. Stackup3D(hfss) で積層構造を作る準備をし、
#          add_ground_layer("ground", material="copper", thickness=0.035, fill_material="air") →
#          add_dielectric_layer("dielectric", thickness="0.5mm", material="Duroid (tm)") →
#          add_signal_layer("signal", material="copper", thickness=0.035, fill_material="air")
#          の順にレイヤーを積み上げる

# TODO: 3. signal.add_patch(patch_length=9.57, patch_width=9.25, patch_name="Patch", frequency=1e10) で
#          信号層にパッチを作成する

# TODO: 4. stackup.resize_around_element(patch) で誘電体・地板をパッチに合わせてリサイズする

# TODO: 5. modeler.create_region(pad_value=[3,3,3,3,3,3], pad_type="Absolute Offset", name="Region") で
#          解析領域を作成し、assign_radiation_boundary_to_objects() で輻射境界を割り当てる

# TODO: 6. patch.create_probe_port(ground, rel_x_offset=0.485) でプローブ給電ポートを割り当てる

# TODO: 7. セットアップ "MySetup"（setup_type="HFSSDriven", Frequency="10GHz"）を作成し、
#          setup.create_frequency_sweep(unit="GHz", name="Sweep1", start_frequency=8, stop_frequency=12,
#          sweep_type="Interpolating") で周波数掃引を追加する

# TODO: 8. 解析を実行する

# TODO: 9. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
