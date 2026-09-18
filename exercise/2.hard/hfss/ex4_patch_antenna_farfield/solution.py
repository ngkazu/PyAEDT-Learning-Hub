"""演習4: プローブ給電パッチアンテナ（S11・遠方界のポスト処理）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modeler.advanced_cad.stackup_3d import Stackup3D

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Hfss を Terminal ソリューションで起動する
hfss = Hfss(
    solution_type="Terminal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
hfss.modeler.model_units = "mm"

# 2. Stackup3D で積層構造を作る
stackup = Stackup3D(hfss)
ground = stackup.add_ground_layer("ground", material="copper", thickness=0.035, fill_material="air")
dielectric = stackup.add_dielectric_layer("dielectric", thickness="0.5mm", material="Duroid (tm)")
signal = stackup.add_signal_layer("signal", material="copper", thickness=0.035, fill_material="air")

# 3. パッチを作成する
patch = signal.add_patch(patch_length=9.57, patch_width=9.25, patch_name="Patch", frequency=1e10)

# 4. パッチサイズに合わせて誘電体・地板をリサイズする
stackup.resize_around_element(patch)

# 5. 解析領域と輻射境界を設定する
region = hfss.modeler.create_region(pad_value=[3, 3, 3, 3, 3, 3], pad_type="Absolute Offset", name="Region")
hfss.assign_radiation_boundary_to_objects(region)

# 6. プローブ給電ポートを割り当てる
patch.create_probe_port(ground, rel_x_offset=0.485)

# 7. セットアップと周波数掃引を作成する
# 遠方界レポートにはフィールドを保存するDiscrete掃引、S11には高速なInterpolating掃引を使う。
setup = hfss.create_setup(name="MySetup", setup_type="HFSSDriven", Frequency="10GHz")
disc_sweep = setup.create_frequency_sweep(
    unit="GHz",
    name="DiscreteSweep",
    start_frequency=8,
    stop_frequency=12,
    num_of_freq_points=9,
    sweep_type="Discrete",
    save_fields=True,
)
interp_sweep = setup.create_frequency_sweep(
    unit="GHz",
    name="InterpolatingSweep",
    start_frequency=8,
    stop_frequency=12,
    sweep_type="Interpolating",
    save_fields=False,
)

# 8. 解析を実行する
setup.analyze()

# 9. S11（リターンロス）のレポートを作成する
hfss.create_scattering(plot="Return Loss", sweep=interp_sweep.name)

# 10. 無限球面（遠方界の基準となる球面）を作成する
# dipole/arrayで使ったcreate_open_region()は輻射境界と同時に既定の無限球面も作成するが、
# パッチアンテナで使ったcreate_region()+assign_radiation_boundary_to_objects()は境界のみで
# 無限球面を作らないため、遠方界レポート作成前に明示的に追加する必要がある。
sphere = hfss.insert_infinite_sphere(
    theta_start=-180, theta_stop=180, theta_step=5, phi_start=0, phi_stop=180, phi_step=5
)

# 11. 中心周波数(10GHz)におけるElevation面のゲインパターン（遠方界）レポートを作成する
# create_report()のcontext引数は、遠方界レポートでは「無限球面の名前」を指定する仕様のため、
# 手順10で作成した無限球面オブジェクトの名前（sphere.name）を明示的に渡す。
variations = hfss.available_variations.nominal_values
variations["Freq"] = ["10GHz"]
variations["Theta"] = ["All"]
variations["Phi"] = ["All"]
elevation_plot = hfss.post.create_report(
    expressions="db(GainTheta)",
    setup_sweep_name=disc_sweep.name,
    variations=variations,
    primary_sweep_variable="Theta",
    context=sphere.name,
    report_category="Far Fields",
    plot_type="Radiation Pattern",
    plot_name="Elevation Gain (dB)",
)
elevation_plot.children["Legend"].properties["Show Trace Name"] = False
elevation_plot.children["Legend"].properties["Show Solution Name"] = False

# 12. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
