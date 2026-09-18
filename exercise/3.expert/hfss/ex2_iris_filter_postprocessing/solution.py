"""演習2: 導波管インダクティブアイリスフィルタ S/フィールドデータの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

import numpy as np
from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

WG_WIDTH = 22.86  # WG16 (WR-90) 内寸 [mm]
WG_HEIGHT = 10.16  # WG16 (WR-90) 内寸 [mm]

# 1. 条件CSV（conditions.csv）を読み込む
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
wg_length = condition["wg_length"]
iris_thickness = condition["iris_thickness"]
iris_aperture = condition["iris_aperture"]

# 2. モデルを作成・解析する（2.hard/hfss/ex2_iris_filter と同じ手順。寸法はCSVから取得）
hfss = Hfss(
    solution_type="Modal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

hfss["wg_length"] = wg_length
hfss["iris_thickness"] = iris_thickness
hfss["iris_aperture"] = iris_aperture

waveguide, port1_sheet, port2_sheet = hfss.modeler.create_waveguide(
    origin=[0, 0, 0],
    wg_direction_axis=2,
    wgmodel="WG16",
    wg_length="wg_length",
    create_sheets_on_openings=True,
    name="Waveguide",
)


def create_iris(z_position_expr: str, name: str):
    """導波管内寸全体を覆う銅板を作り、中央の開口部をくり抜いてインダクティブアイリスを作る。"""
    full_plate = hfss.modeler.create_box(
        origin=[0, 0, z_position_expr],
        sizes=[WG_WIDTH, WG_HEIGHT, "iris_thickness"],
        name=name,
        material="copper",
    )
    aperture = hfss.modeler.create_box(
        origin=[0, f"({WG_HEIGHT}mm-iris_aperture)/2", z_position_expr],
        sizes=[WG_WIDTH, "iris_aperture", "iris_thickness"],
        name=f"{name}_aperture",
    )
    hfss.modeler.subtract(full_plate, aperture, keep_originals=False)
    return full_plate


iris1 = create_iris("wg_length/3", "Iris1")
iris2 = create_iris("2*wg_length/3", "Iris2")

air_region = hfss.modeler.create_box(
    origin=[0, 0, 0],
    sizes=[WG_WIDTH, WG_HEIGHT, "wg_length"],
    name="AirRegion",
    material="vacuum",
)
hfss.modeler.subtract(air_region, [iris1, iris2], keep_originals=True)

hfss.wave_port(assignment=port1_sheet.name, name="Port1")
hfss.wave_port(assignment=port2_sheet.name, name="Port2")

setup = hfss.create_setup(name="MySetup", Frequency="10GHz", MaximumPasses=8)
setup.add_sweep(
    name="Sweep1",
    sweep_type="Interpolating",
    RangeStart="8GHz",
    RangeEnd="12GHz",
    SaveFields=True,
)

setup.analyze()

# 3. S11・S21の SolutionData を取得する
excitations = hfss.excitation_names
expressions = [f"S({excitations[0]},{excitations[0]})", f"S({excitations[1]},{excitations[0]})"]
solution_data = hfss.post.get_solution_data(
    expressions=expressions,
    setup_sweep_name=hfss.nominal_sweep,
    report_category="Modal Solution Data",
)

# 4. 周波数・S11[dB]・S21[dB]の配列を取得する
freq, s11_db = solution_data.get_expression_data(expression=expressions[0], formula="db20")
_, s21_db = solution_data.get_expression_data(expression=expressions[1], formula="db20")
freq = np.array(freq, dtype=float)
s11_db = np.array(s11_db, dtype=float)
s21_db = np.array(s21_db, dtype=float)

# 5. S11・S21の結果をCSVファイルに出力する
with open(script_dir / "results_s_parameters.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["frequency_ghz", "s11_db", "s21_db"])
    for row in zip(freq, s11_db, s21_db):
        writer.writerow(row)

# 6. 電界分布のフィールドプロットを作成する（導波管中心を通るXZ平面）
cut_plane = hfss.modeler.create_plane(
    name="CutPlane_XZ",
    plane_base_x="0mm",
    plane_base_y=f"{WG_HEIGHT / 2}mm",
    plane_base_z="0mm",
    plane_normal_x="0mm",
    plane_normal_y="1mm",
    plane_normal_z="0mm",
)
hfss.post.create_fieldplot_cutplane(
    assignment=[cut_plane.name],
    quantity="Mag_E",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": "10GHz"},
    plot_name="E_Field_XZ",
)

# 7. フィールドプロットを PyVista で画像出力する
hfss.post.plot_field_from_fieldplot(
    plot_name="E_Field_XZ",
    project_path=str(script_dir),
    image_format="png",
    view="xz",
    show=False,
)

# 8. 同じフィールドプロットをインタラクティブなPyVistaウィンドウで表示する
# project_pathを渡さずshow=Trueにすると、マウスで自由に回転・拡大できるウィンドウが開く
# （ウィンドウを閉じるとスクリプトの実行が再開する）。
hfss.post.plot_field_from_fieldplot(
    plot_name="E_Field_XZ",
    view="xz",
    show=True,
)

# 9. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
