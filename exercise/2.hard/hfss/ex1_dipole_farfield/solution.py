"""演習1: 半波長ダイポールアンテナ（S11・遠方界のポスト処理）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Hfss を Modal ソリューションで起動する
hfss = Hfss(
    solution_type="Modal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# 2. 設計変数を定義する
hfss["l_dipole"] = "10.2cm"
center_freq = "1.5GHz"

# 3. 組み込み3Dコンポーネントを挿入する
component_name = "Dipole_Antenna_DM"
component_path = hfss.components3d[component_name]
component_parameters = hfss.get_component_variables(component_name)
component_parameters["dipole_length"] = "l_dipole"
hfss.modeler.insert_3d_component(
    input_file=component_path,
    geometry_parameters=component_parameters,
    name="Dipole1",
)

# 4. 解析領域を作成する
hfss.create_open_region(frequency=center_freq)

# 5. セットアップを作成する
setup = hfss.create_setup(
    name="MySetup",
    MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"],
    MaximumPasses=2,
)

# 6. 周波数掃引を追加する
# 遠方界（フィールド）データを使うレポートには、フィールドを保存するDiscrete掃引が必要。
# S11のような広帯域応答の確認には、高速なInterpolating掃引を別途追加する。
disc_sweep = setup.add_sweep(
    name="DiscreteSweep",
    sweep_type="Discrete",
    RangeStart="1GHz",
    RangeEnd="2GHz",
    RangeStep="0.5GHz",
    SaveFields=True,
)
interp_sweep = setup.add_sweep(
    name="InterpolatingSweep",
    sweep_type="Interpolating",
    RangeStart="1GHz",
    RangeEnd="2GHz",
    SaveFields=False,
)

# 7. 解析を実行する
setup.analyze()

# 8. S11（リターンロス）のレポートを作成する
hfss.create_scattering(plot="Return Loss", sweep=interp_sweep.name)

# 9. Elevation面のゲインパターン（遠方界）レポートを作成する
# variationsでFreq/Theta/Phiを明示することで、中心周波数における角度掃引のレポートになる。
variations = hfss.available_variations.nominal_values
variations["Freq"] = [center_freq]
variations["Theta"] = ["All"]
variations["Phi"] = ["All"]
elevation_plot = hfss.post.create_report(
    expressions="db(GainTheta)",
    setup_sweep_name=disc_sweep.name,
    variations=variations,
    primary_sweep_variable="Theta",
    context="Elevation",
    report_category="Far Fields",
    plot_type="Radiation Pattern",
    plot_name="Elevation Gain (dB)",
)
elevation_plot.children["Legend"].properties["Show Trace Name"] = False
elevation_plot.children["Legend"].properties["Show Solution Name"] = False

# 10. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
