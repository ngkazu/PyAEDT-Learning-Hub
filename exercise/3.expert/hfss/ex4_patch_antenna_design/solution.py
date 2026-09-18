"""演習4: プローブ給電パッチアンテナの設計計算とPython後処理（CSV入出力・PyVista可視化）。"""

import csv
import math
from pathlib import Path

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modeler.advanced_cad.stackup_3d import Stackup3D

AEDT_VERSION = "2026.1"
SPEED_OF_LIGHT_M_S = 3e8

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 設計条件CSV（design_conditions.csv）を読み込む
# design_freq_ghz, eps_r, substrate_thickness_mm の1行を想定（先頭行はヘッダー）。
with open(script_dir / "design_conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
design_freq_ghz = float(condition["design_freq_ghz"])
eps_r = float(condition["eps_r"])
h_mm = float(condition["substrate_thickness_mm"])

# 2. マイクロストリップパッチアンテナの伝送線路モデル（transmission-line model）で、
# パッチの幅(W)・長さ(L)を理論計算する（Balanis の標準的な設計式）。
f0_hz = design_freq_ghz * 1e9
h_m = h_mm / 1000

width_m = (SPEED_OF_LIGHT_M_S / (2 * f0_hz)) * math.sqrt(2 / (eps_r + 1))
eps_reff = (eps_r + 1) / 2 + (eps_r - 1) / 2 * (1 + 12 * h_m / width_m) ** -0.5
delta_l_m = (
    0.412
    * h_m
    * (eps_reff + 0.3)
    * (width_m / h_m + 0.264)
    / ((eps_reff - 0.258) * (width_m / h_m + 0.8))
)
length_m = SPEED_OF_LIGHT_M_S / (2 * f0_hz * math.sqrt(eps_reff)) - 2 * delta_l_m

width_mm = width_m * 1000
length_mm = length_m * 1000

# 3. 計算結果をCSVファイルに出力する
with open(script_dir / "results_patch_dimensions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["parameter", "value"])
    writer.writerow(["design_freq_ghz", design_freq_ghz])
    writer.writerow(["eps_r", eps_r])
    writer.writerow(["substrate_thickness_mm", h_mm])
    writer.writerow(["eps_reff", eps_reff])
    writer.writerow(["patch_width_mm", width_mm])
    writer.writerow(["patch_length_mm", length_mm])

# 4. Hfss を Terminal ソリューションで起動し、計算したW/Lでパッチアンテナを作成する
hfss = Hfss(
    solution_type="Terminal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
hfss.modeler.model_units = "mm"

stackup = Stackup3D(hfss)
ground = stackup.add_ground_layer("ground", material="copper", thickness=0.035, fill_material="air")
dielectric = stackup.add_dielectric_layer("dielectric", thickness=f"{h_mm}mm", material="Duroid (tm)")
signal = stackup.add_signal_layer("signal", material="copper", thickness=0.035, fill_material="air")
patch = signal.add_patch(
    patch_length=length_mm,
    patch_width=width_mm,
    patch_name="Patch",
    frequency=f0_hz,
)
stackup.resize_around_element(patch)

region = hfss.modeler.create_region(pad_value=[3, 3, 3, 3, 3, 3], pad_type="Absolute Offset", name="Region")
hfss.assign_radiation_boundary_to_objects(region)

patch.create_probe_port(ground, rel_x_offset=0.485)

# 5. セットアップと周波数掃引を作成する
setup = hfss.create_setup(name="MySetup", setup_type="HFSSDriven", Frequency=f"{design_freq_ghz}GHz")
setup.create_frequency_sweep(
    unit="GHz",
    name="Sweep1",
    start_frequency=design_freq_ghz * 0.8,
    stop_frequency=design_freq_ghz * 1.2,
    sweep_type="Interpolating",
)

# 6. 解析を実行する
setup.analyze()

# 7. 遠方界データを取得し、PyVistaで3D放射パターンを画像出力する
ffdata = hfss.get_antenna_data()
ffdata.farfield_data.plot_3d(
    quantity="RealizedGain",
    output_file=str(script_dir / "patch_farfield_3d.png"),
    show=False,
)

# 8. 同じ3D放射パターンをインタラクティブなPyVistaウィンドウで表示する
ffdata.farfield_data.plot_3d(quantity="RealizedGain", show=True)

# 9. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
