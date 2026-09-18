"""演習1: ダイポールアンテナ S11・遠方界データの Python 後処理（VSWR・帯域幅算出・CSV入出力）。"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画像保存のみのため、GUIバックエンド（Tk等）を使わない
import matplotlib.pyplot as plt
import numpy as np
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 条件CSV（conditions.csv）を読み込む
# l_dipole, center_freq の1行を想定（先頭行はヘッダー）。
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
l_dipole = condition["l_dipole"]
center_freq = condition["center_freq"]

# 2. ダイポールアンテナを作成・解析する（normal/ex1_dipole_antenna と同じ手順。長さと中心周波数はCSVから取得）
hfss = Hfss(
    solution_type="Modal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

hfss["l_dipole"] = l_dipole

component_name = "Dipole_Antenna_DM"
component_path = hfss.components3d[component_name]
component_parameters = hfss.get_component_variables(component_name)
component_parameters["dipole_length"] = "l_dipole"
hfss.modeler.insert_3d_component(
    input_file=component_path,
    geometry_parameters=component_parameters,
    name="Dipole1",
)

hfss.create_open_region(frequency=center_freq)

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

# 3. S11の SolutionData を取得する
# nominal_sweep（"SetupName : SweepName"）を使うと、sweep名を手打ちする必要がない。
# report_category を明示しないと、Modal解析のSパラメータが見つからず例外になることがあるため指定する。
solution_data = hfss.post.get_solution_data(
    expressions=f"S({hfss.excitation_names[0]},{hfss.excitation_names[0]})",
    setup_sweep_name=hfss.nominal_sweep,
    report_category="Modal Solution Data",
)

# 4. 周波数とS11[dB]の配列を取得する
freq, s11_db = solution_data.get_expression_data(
    expression=f"S({hfss.excitation_names[0]},{hfss.excitation_names[0]})",
    formula="db20",
)
freq = np.array(freq, dtype=float)
s11_db = np.array(s11_db, dtype=float)

# 5. VSWR を計算する
gamma_abs = 10 ** (s11_db / 20)
gamma_abs = np.clip(gamma_abs, 0, 0.999)  # |Γ|>=1 となる異常値を除外（ゼロ割回避）
vswr = (1 + gamma_abs) / (1 - gamma_abs)

# 6. -10dB帯域幅を求める
in_band = s11_db <= -10
if np.any(in_band):
    band_low = freq[in_band].min()
    band_high = freq[in_band].max()
else:
    band_low = band_high = None

# 7. S11とVSWRを重ねてプロットする
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(freq, s11_db, "b-", label="S11 [dB]")
ax1.axhline(-10, color="gray", linestyle="--", linewidth=0.8)
ax1.set_xlabel("Frequency [GHz]")
ax1.set_ylabel("S11 [dB]", color="b")

ax2 = ax1.twinx()
ax2.plot(freq, vswr, "r-", label="VSWR")
ax2.set_ylabel("VSWR", color="r")

if band_low is not None:
    ax1.axvspan(band_low, band_high, color="yellow", alpha=0.2, label="-10dB bandwidth")

fig.suptitle("Dipole antenna: S11 and VSWR vs frequency")
fig.tight_layout()

# 8. 画像として保存する
fig.savefig(script_dir / "dipole_s11_vswr.png", dpi=150)

# 9. S11・VSWRの結果をCSVファイルに出力する
with open(script_dir / "results_s11_vswr.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["frequency_ghz", "s11_db", "vswr"])
    for row in zip(freq, s11_db, vswr):
        writer.writerow(row)

# 10. 遠方界（Far Field）データを取得し、PyVistaで3D放射パターンを画像出力する
# setupを省略するとnominal_adaptive（"MySetup : LastAdaptive"）が使われ、
# 無限球面（Infinite Sphere）が未定義の場合は自動的に作成される。
ffdata = hfss.get_antenna_data()
ffdata.farfield_data.plot_3d(
    quantity="RealizedGain",
    output_file=str(script_dir / "dipole_farfield_3d.png"),
    show=False,
)

# 11. 同じ3D放射パターンをインタラクティブなPyVistaウィンドウで表示する
# output_fileを渡さずshow=Trueにすると、マウスで自由に回転・拡大できるウィンドウが開く
# （ウィンドウを閉じるとスクリプトの実行が再開する）。
ffdata.farfield_data.plot_3d(quantity="RealizedGain", show=True)

# 12. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
