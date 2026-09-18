"""演習4: プローブ給電パッチアンテナ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modeler.advanced_cad.stackup_3d import Stackup3D

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Hfss を Terminal ソリューションで起動する
# プローブ給電（同軸プローブ）はLumped/Wave Portではなく、Terminalソリューションで扱う。
hfss = Hfss(
    solution_type="Terminal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
hfss.modeler.model_units = "mm"

# 2. Stackup3D で 地板(ground) → 誘電体基板(dielectric) → 信号層(signal) の積層構造を作る
stackup = Stackup3D(hfss)
ground = stackup.add_ground_layer("ground", material="copper", thickness=0.035, fill_material="air")
dielectric = stackup.add_dielectric_layer("dielectric", thickness="0.5mm", material="Duroid (tm)")
signal = stackup.add_signal_layer("signal", material="copper", thickness=0.035, fill_material="air")

# 3. 信号層にパッチ（矩形パッチアンテナ）を作成する
patch = signal.add_patch(patch_length=9.57, patch_width=9.25, patch_name="Patch", frequency=1e10)

# 4. パッチのサイズに合わせて、誘電体基板・地板を自動リサイズする
stackup.resize_around_element(patch)

# 5. 解析領域（Airbox）を作成し、輻射境界を割り当てる
region = hfss.modeler.create_region(pad_value=[3, 3, 3, 3, 3, 3], pad_type="Absolute Offset", name="Region")
hfss.assign_radiation_boundary_to_objects(region)

# 6. パッチに同軸プローブ給電ポートを割り当てる
# rel_x_offset はパッチ中心からの相対位置（0=中心、1=端）。インピーダンス整合のための給電点探索は本演習の対象外。
patch.create_probe_port(ground, rel_x_offset=0.485)

# 7. セットアップと周波数掃引を作成する
setup = hfss.create_setup(name="MySetup", setup_type="HFSSDriven", Frequency="10GHz")
setup.create_frequency_sweep(
    unit="GHz",
    name="Sweep1",
    start_frequency=8,
    stop_frequency=12,
    sweep_type="Interpolating",
)

# 8. 解析を実行する
setup.analyze()

# 9. 保存して終了する
# normalはSetup作成→解析実行までで終了する（ポスト処理はhard以降で追加するため、ここでは行わない）。
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
