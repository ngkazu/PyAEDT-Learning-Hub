"""演習3: ダイポールアレイアンテナ（S/遠方界のポスト処理）。"""

import itertools

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"
NUM_ELEMENTS = 4  # 配列素子数（Pythonのループ回数として使うだけなので、HFSSの設計変数にはしない）

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
hfss["element_spacing"] = "15cm"
center_freq = "1.5GHz"

# 3. 組み込み3Dコンポーネントを、素子数だけ座標系を変えて挿入する
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

# 4. 解析領域を作成する
hfss.create_open_region(frequency=center_freq)

# 5. セットアップを作成する
setup = hfss.create_setup(
    name="MySetup",
    MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"],
    MaximumPasses=2,
)

# 6. 周波数掃引を追加する
# 遠方界レポートにはフィールドを保存するDiscrete掃引、Sパラメータには高速なInterpolating掃引を使う。
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

# 8. S11・素子間結合（S21等）のレポートを作成する
# create_scattering() にports/ports_excitedを渡さないと対角成分（自己反射）しか作られないため、
# 全素子の組み合わせ（自己反射＋相互結合）を itertools.product で明示的に作る。
excitations = hfss.excitation_names
port_pairs = list(itertools.product(excitations, repeat=2))
hfss.create_scattering(
    plot="Return Loss and Coupling",
    sweep=interp_sweep.name,
    ports=[p for p, _ in port_pairs],
    ports_excited=[q for _, q in port_pairs],
)

# 9. アレイ全体のElevation面ゲインパターン（遠方界）レポートを作成する
# 各素子は既定で等振幅・同位相（0deg）で励振されるため、アレイ全体の合成パターンが得られる。
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
    plot_name="Array Elevation Gain (dB)",
)
elevation_plot.children["Legend"].properties["Show Trace Name"] = False
elevation_plot.children["Legend"].properties["Show Solution Name"] = False

# 10. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
