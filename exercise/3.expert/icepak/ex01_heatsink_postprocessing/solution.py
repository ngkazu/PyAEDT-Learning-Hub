"""演習1: ヒートシンク熱解析 温度データのPython後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 条件CSV（conditions.csv）を読み込む
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
power_w = float(condition["power_w"])

# 2. Icepak を SteadyState ソリューションで起動する
ipk = Icepak(
    design="IcepakDesign1",
    solution_type="SteadyState",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
ipk.modeler.model_units = "mm"

# 3. 周囲温度・重力方向を設定する（hard/normalと同じモデル）
ipk.edit_design_settings(ambient_temperature="20cel", gravity_dir=2)

# 4. ベースを作成する
ipk.modeler.create_box(origin=[0, -50, -50], sizes=[10, 100, 100], name="base", material="Al-Extruded")

# 5. ベースに温度ポイントモニタを割り当てる
ipk.assign_point_monitor_in_object(name="base", monitor_type="Temperature", monitor_name="Monitor_base")

# 6. フィン1枚目を作成し、Y方向にピッチ9.5mmで11枚に複製する
ipk.modeler.create_box(origin=[10, -50, -50], sizes=[40, 5, 100], name="fin", material="Al-Extruded")
_ok, fin_clone_names = ipk.modeler.duplicate_along_line(assignment="fin", vector=[0, 9.5, 0], clones=11)
fin_names = ["fin"] + fin_clone_names

# 7. 発熱面シートを作成する
ipk.modeler.create_rectangle(orientation="YZ", origin=[0, -50, -50], sizes=[100, 100], name="Rectangle1")

# 8. 解析領域（Region）を作成する
ipk.modeler.create_region(pad_value=[25, 25, 50, 50, 50, 50], pad_type="Absolute Offset")

# 9. 発熱面に、CSVから読み込んだ発熱量を割り当てる
ipk.assign_source(
    assignment="Rectangle1",
    thermal_condition="Total Power",
    assignment_value=f"{power_w}W",
    boundary_name="Source1",
    radiate=False,
)

# 10. Regionの6面（±X, ±Y, ±Z）の中心座標から面IDを特定する
region = ipk.modeler["Region"]
xmin, ymin, zmin, xmax, ymax, zmax = region.bounding_box
xc, yc, zc = (xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2

face_xmax = ipk.modeler.get_faceid_from_position([xmax, yc, zc], assignment="Region")
face_xmin = ipk.modeler.get_faceid_from_position([xmin, yc, zc], assignment="Region")
face_ymax = ipk.modeler.get_faceid_from_position([xc, ymax, zc], assignment="Region")
face_ymin = ipk.modeler.get_faceid_from_position([xc, ymin, zc], assignment="Region")
face_zmax = ipk.modeler.get_faceid_from_position([xc, yc, zmax], assignment="Region")
face_zmin = ipk.modeler.get_faceid_from_position([xc, yc, zmin], assignment="Region")

# 11. Regionの±Z面に圧力開口を割り当てる
ipk.assign_pressure_free_opening(assignment=[face_zmax], boundary_name="Opening1", no_reverse_flow=True)
ipk.assign_pressure_free_opening(assignment=[face_zmin], boundary_name="Opening2", no_reverse_flow=False)

# 12. Regionの±X, ±Y面（4面）に固定温度壁を割り当てる
ipk.assign_stationary_wall(
    geometry=[face_xmax, face_xmin, face_ymax, face_ymin],
    boundary_condition="Temperature",
    name="StationaryWall1",
    temperature="AmbientTemp",
    material="Al-Extruded",
    radiate=True,
)

# 13. セットアップを作成する
setup = ipk.create_setup(name="Setup1")
setup.props["Flow Regime"] = "Laminar"
setup.props["Include Temperature"] = True
setup.props["Include Flow"] = True
setup.props["Include Gravity"] = True
setup.props["Convergence Criteria - Max Iterations"] = 500
setup.update()

# 14. 解析を実行する
setup.analyze()
setup_sweep = f"{setup.name} : {ipk.solution_type}"

# 15. ベースの温度モニタ値（Min/Max/Mean/Stdev）を取得する
monitor_result = ipk.post.evaluate_monitor_quantity(
    monitor="Monitor_base",
    quantity="Temperature",
    setup_name=setup_sweep,
)

# 16. 条件・結果をCSVファイルに出力する
with open(script_dir / "results_thermal.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["power_w", "base_max_temperature", "temperature_unit"])
    writer.writerow([power_w, monitor_result["Max"], monitor_result["Unit"]])

# 17. ヒートシンク表面（base+フィン11枚）の温度フィールドプロットを作成する
ipk.post.create_fieldplot_surface(
    assignment=["base"] + fin_names,
    quantity="Temperature",
    setup=setup_sweep,
    plot_name="HeatsinkTemperature",
)

# 18. フィールドプロットを PyVista で画像出力する
ipk.post.plot_field_from_fieldplot(
    plot_name="HeatsinkTemperature",
    project_path=str(script_dir),
    image_format="png",
    view="isometric",
    log_scale=False,
    show=False,
)

# 19. 同じフィールドプロットをインタラクティブなPyVistaウィンドウで表示する
ipk.post.plot_field_from_fieldplot(
    plot_name="HeatsinkTemperature",
    view="isometric",
    log_scale=False,
    show=True,
)

# 20. 保存して終了する
ipk.save_project()
ipk.release_desktop(close_projects=True, close_desktop=True)
