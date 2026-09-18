"""演習3: ダイポールアレイアンテナ ビームステアリングの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画像保存のみのため、GUIバックエンド（Tk等）を使わない
import matplotlib.pyplot as plt
import numpy as np
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"
NUM_ELEMENTS = 4  # 配列素子数（Pythonのループ回数として使うだけなので、HFSSの設計変数にはしない）
ELEMENT_SPACING_M = 0.15  # HFSS変数 element_spacing="15cm" と同じ値（Python側の理論計算用）
CENTER_FREQ_HZ = 1.5e9  # HFSS変数 center_freq="1.5GHz" と同じ値（Python側の理論計算用）

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 位相重みCSV（phase_weights.csv）を読み込む
# element_index, phase_deg の列を持つ、素子数分の行を想定（先頭行はヘッダー）。
with open(script_dir / "phase_weights.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    phase_weights = sorted(
        ((int(row["element_index"]), float(row["phase_deg"])) for row in reader),
        key=lambda item: item[0],
    )
phases_deg = [phase for _, phase in phase_weights]

# 2. ダイポールアレイアンテナを作成する（normal/ex3_antenna_array と同じ手順）
hfss = Hfss(
    solution_type="Modal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

hfss["l_dipole"] = "10.2cm"
hfss["element_spacing"] = "15cm"

component_name = "Dipole_Antenna_DM"
component_path = hfss.components3d[component_name]
component_parameters = hfss.get_component_variables(component_name)
component_parameters["dipole_length"] = "l_dipole"

for i in range(NUM_ELEMENTS):
    cs_name = f"CS_Element{i}"
    hfss.modeler.create_coordinate_system(
        origin=[f"{i}*element_spacing", 0, 0],
        name=cs_name,
    )
    hfss.modeler.insert_3d_component(
        input_file=component_path,
        geometry_parameters=component_parameters,
        coordinate_system=cs_name,
        name=f"Dipole_{i}",
    )

hfss.create_open_region(frequency="1.5GHz")

setup = hfss.create_setup(
    name="MySetup",
    MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"],
    MaximumPasses=2,
)
setup.add_sweep(
    name="Sweep1",
    sweep_type="Interpolating",
    RangeStart="1GHz",
    RangeEnd="2GHz",
)

setup.analyze()

# 3. 各素子の励振位相をCSVの値に変更する（振幅は全素子1Wで固定）
# 解の再計算はせず、AEDT側で保存済みのフィールドを重み付け合成し直すだけ（高速）。
excitations = sorted(hfss.excitation_names)
sources = {name: ("1W", f"{phase}deg") for name, phase in zip(excitations, phases_deg)}
hfss.edit_sources(sources)

# 4. 理論上のアレイファクタ（Array Factor）をNumPyで計算する
# 単純化のため、素子はX軸上に等間隔に並び、observation angle thetaはX軸周りの角度とする
# （実際の3Dモデルの角度定義とは厳密には一致しない、比較用の簡易モデル）。
wavelength_m = 3e8 / CENTER_FREQ_HZ
k = 2 * np.pi / wavelength_m
theta_deg = np.linspace(-90, 90, 361)
theta_rad = np.deg2rad(theta_deg)
phases_rad = np.deg2rad(phases_deg)

array_factor = np.zeros_like(theta_rad, dtype=complex)
for n, phase_n in enumerate(phases_rad):
    array_factor += np.exp(1j * (k * ELEMENT_SPACING_M * n * np.sin(theta_rad) + phase_n))

af_db = 20 * np.log10(np.abs(array_factor) / NUM_ELEMENTS + 1e-12)
peak_angle_deg = theta_deg[np.argmax(af_db)]

# 5. 理論アレイファクタをプロットし、画像として保存する
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(theta_deg, af_db, "b-")
ax.axvline(peak_angle_deg, color="red", linestyle="--", label=f"Peak: {peak_angle_deg:.1f} deg")
ax.set_xlabel("Theta [deg]")
ax.set_ylabel("Array Factor [dB]")
ax.set_title("Theoretical array factor (beam steering)")
ax.legend()
fig.tight_layout()
fig.savefig(script_dir / "array_factor_theory.png", dpi=150)

# 6. 理論アレイファクタの結果をCSVファイルに出力する
with open(script_dir / "results_array_factor.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["theta_deg", "array_factor_db"])
    for row in zip(theta_deg, af_db):
        writer.writerow(row)

# 7. 実際のシミュレーション結果（遠方界）を取得し、PyVistaで3D放射パターンを画像出力する
# edit_sources() で設定した位相重みが反映された、実際にビームが傾いたパターンが得られる。
ffdata = hfss.get_antenna_data()
ffdata.farfield_data.plot_3d(
    quantity="RealizedGain",
    output_file=str(script_dir / "array_farfield_3d.png"),
    show=False,
)

# 8. 同じ3D放射パターンをインタラクティブなPyVistaウィンドウで表示する
ffdata.farfield_data.plot_3d(quantity="RealizedGain", show=True)

# 9. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
