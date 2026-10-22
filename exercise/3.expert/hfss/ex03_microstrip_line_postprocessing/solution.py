"""演習3: マイクロストリップ線路 S/フィールドデータの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

SUB_W = 6.0  # 基板の幅 [mm]（Y方向）
SUB_H = 1.0  # 基板の厚さ [mm]（Z方向）
AIR_H = 3.0  # 基板上部のエアボックス高さ [mm]

# 1. 条件CSV（conditions.csv）を読み込む
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
line_w = float(condition["line_w_mm"])
line_l = float(condition["line_l_mm"])

# 2. マイクロストリップ線路を作成する（normal/ex03_microstrip_line と同じ手順。導体幅・長さはCSVから取得）
hfss = Hfss(
    solution_type="Terminal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
hfss.modeler.model_units = "mm"

substrate = hfss.modeler.create_box(
    origin=[0, -SUB_W / 2, 0],
    sizes=[line_l, SUB_W, SUB_H],
    name="Substrate",
    material="alumina_96pct",
)

gnd = hfss.modeler.create_rectangle(
    orientation=Plane.XY,
    origin=[0, -SUB_W / 2, 0],
    sizes=[line_l, SUB_W],
    name="GND",
)
hfss.assign_finite_conductivity(assignment=gnd.name, material="copper", name="GND_FC")

line = hfss.modeler.create_rectangle(
    orientation=Plane.XY,
    origin=[0, -line_w / 2, SUB_H],
    sizes=[line_l, line_w],
    name="Line",
)
hfss.assign_finite_conductivity(assignment=line.name, material="copper", name="Line_FC")

airbox = hfss.modeler.create_box(
    origin=[0, -SUB_W / 2, SUB_H],
    sizes=[line_l, SUB_W, AIR_H],
    name="AirBox",
    material="vacuum",
)

p1 = hfss.modeler.create_rectangle(
    orientation=Plane.YZ,
    origin=[0, -SUB_W / 2, 0],
    sizes=[SUB_W, SUB_H + AIR_H],
    name="Port1_sheet",
)
hfss.wave_port(assignment=p1.name, name="P1", modes=1, renormalize=True, impedance=50)

p2 = hfss.modeler.create_rectangle(
    orientation=Plane.YZ,
    origin=[line_l, -SUB_W / 2, 0],
    sizes=[SUB_W, SUB_H + AIR_H],
    name="Port2_sheet",
)
hfss.wave_port(assignment=p2.name, name="P2", modes=1, renormalize=True, impedance=50)

rad_faces = []
for f in airbox.faces:
    x, y, z = f.center
    is_bottom = abs(z - SUB_H) < 1e-6
    is_port_end = abs(x - 0) < 1e-6 or abs(x - line_l) < 1e-6
    if not is_bottom and not is_port_end:
        rad_faces.append(f.id)
hfss.assign_radiation_boundary_to_faces(assignment=rad_faces, name="Rad_top_sides")

_, passed = hfss.validate_full_design()
if not passed:
    hfss.logger.warning("Design validation reported issues. Check the AEDT message manager.")

setup = hfss.create_setup(name="Setup1", Frequency="10GHz", MaxDeltaS=0.02, MaximumPasses=6)
hfss.create_linear_count_sweep(
    setup="Setup1",
    unit="GHz",
    start_frequency=0.1,
    stop_frequency=10,
    num_of_freq_points=201,
    name="Sweep",
    sweep_type="Interpolating",
)

setup.analyze()

# 3. S11・S21のSolutionDataを取得する
excitations = sorted(hfss.excitation_names)
expressions = [f"S({excitations[0]},{excitations[0]})", f"S({excitations[1]},{excitations[0]})"]
solution_data = hfss.post.get_solution_data(
    expressions=expressions,
    setup_sweep_name=hfss.nominal_sweep,
    report_category="Terminal Solution Data",
)

# 4. 周波数・S11[dB]・S21[dB]の配列を取得する
freq, s11_db = solution_data.get_expression_data(expression=expressions[0], formula="db20")
_, s21_db = solution_data.get_expression_data(expression=expressions[1], formula="db20")

# 5. S11・S21の結果をCSVファイルに出力する
with open(script_dir / "results_s_parameters.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["frequency_ghz", "s11_db", "s21_db"])
    for row in zip(freq, s11_db, s21_db):
        writer.writerow(row)

# 6. GND・信号線表面のMag_Eフィールドプロットを作成する
field_plot = hfss.post.create_fieldplot_surface(
    assignment=[gnd.name, line.name],
    quantity="Mag_E",
    setup="Setup1 : LastAdaptive",
    plot_name="MagE_Surface",
)

# 7. フィールドプロットを PyVista で画像出力する
hfss.post.plot_field_from_fieldplot(
    plot_name="MagE_Surface",
    project_path=str(script_dir),
    image_format="png",
    view="isometric",
    log_scale=True,
    show=False,
)

# 8. 同じフィールドプロットをインタラクティブなPyVistaウィンドウで表示する
hfss.post.plot_field_from_fieldplot(
    plot_name="MagE_Surface",
    view="isometric",
    log_scale=True,
    show=True,
)

# 9. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
