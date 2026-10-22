"""演習1: コモンモードチョーク 損失・Bフィールドデータの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
import json
import tempfile
from pathlib import Path

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. 条件CSV（conditions.csv）を読み込む
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    condition = next(reader)
turns = int(condition["turns"])
frequency_khz = float(condition["frequency_khz"])

# 2. Maxwell3d を EddyCurrent ソリューションで起動する
m3d = Maxwell3d(
    solution_type="EddyCurrent",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 3. チョークのジオメトリパラメータを辞書で定義する（hard/normalと同じモデル。巻数はCSVから取得）
choke_descriptor = {
    "Number of Windings": {"1": False, "2": True, "3": False, "4": False},
    "Layer": {"Simple": True, "Double": False, "Triple": False},
    "Layer Type": {"Separate": True, "Linked": False},
    "Similar Layer": {"Similar": True, "Different": False},
    "Mode": {"Differential": True, "Common": False},
    "Wire Section": {"None": False, "Hexagon": False, "Octagon": True, "Circle": False},
    "Core": {
        "Name": "Core",
        "Material": "ferrite",
        "Inner Radius": 11,
        "Outer Radius": 17,
        "Height": 7,
        "Chamfer": 0.8,
    },
    "Outer Winding": {
        "Name": "Winding",
        "Material": "copper",
        "Inner Radius": 12,
        "Outer Radius": 16,
        "Height": 8,
        "Wire Diameter": 1,
        "Turns": turns,
        "Coil Pit(deg)": 9,
        "Occupation(%)": 0,
    },
    "Mid Winding": {"Turns": 8, "Coil Pit(deg)": 0.1, "Occupation(%)": 0},
    "Inner Winding": {"Turns": 12, "Coil Pit(deg)": 0.1, "Occupation(%)": 0},
}

temp_folder = tempfile.TemporaryDirectory(suffix=".ansys")
choke_fn = f"{temp_folder.name}/choke_descriptor.json"
with open(choke_fn, "w") as outfile:
    json.dump(choke_descriptor, outfile)

# 4. 辞書の整合性を確認してからチョークを作成する
m3d.modeler.check_choke_values(input_dir=choke_fn, create_another_file=False)
list_object = m3d.modeler.create_choke(input_file=choke_fn)
core = list_object[1]
winding1 = list_object[2]
winding2 = list_object[3]

# 5. 解析領域（Region）を作成する（-Z面は0%、それ以外は100%のパディング）
m3d.modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=0)

# 6. 各巻線の両端面に電流励振を割り当てる（差動モードなので位相を180度ずらす）
winding1_faces = m3d.modeler.get_object_faces(assignment=winding1[0].name)
winding2_faces = m3d.modeler.get_object_faces(assignment=winding2[0].name)

m3d.assign_current(
    assignment=[winding1_faces[1]],
    amplitude=1000,
    phase="0deg",
    swap_direction=False,
    name="winding1_in",
)
m3d.assign_current(
    assignment=[winding1_faces[0]],
    amplitude=1000,
    phase="0deg",
    swap_direction=True,
    name="winding1_out",
)
m3d.assign_current(
    assignment=[winding2_faces[1]],
    amplitude=1000,
    phase="180deg",
    swap_direction=False,
    name="winding2_in",
)
m3d.assign_current(
    assignment=[winding2_faces[0]],
    amplitude=1000,
    phase="180deg",
    swap_direction=True,
    name="winding2_out",
)

# 7. セットアップを作成する（解析周波数はCSVから取得）
setup = m3d.create_setup(name="MySetup")
setup.props["Frequency"] = f"{frequency_khz}kHz"

# 8. 解析を実行する
setup.analyze()

# 9. 巻線のオーミック損失（SolidLoss）とコア損失（CoreLoss）のSolutionDataを取得する
solution_data = m3d.post.get_solution_data(
    expressions=["SolidLoss", "CoreLoss"],
    setup_sweep_name=m3d.nominal_sweep,
    report_category="Fields",
)
_, winding_loss_w = solution_data.get_expression_data(expression="SolidLoss", formula="real")
_, core_loss_w = solution_data.get_expression_data(expression="CoreLoss", formula="real")

# 10. 損失データをCSVファイルに出力する
with open(script_dir / "results_losses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["turns", "frequency_khz", "winding_loss_w", "core_loss_w"])
    writer.writerow([turns, frequency_khz, winding_loss_w[0], core_loss_w[0]])

# 11. コア表面のB磁束密度（Mag_B）のフィールドプロットを作成する
m3d.post.create_fieldplot_surface(
    assignment=core.name,
    quantity="Mag_B",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": f"{frequency_khz}kHz", "Phase": "0deg"},
    plot_name="CoreMagB",
)

# 12. フィールドプロットを PyVista で画像出力する
m3d.post.plot_field_from_fieldplot(
    plot_name="CoreMagB",
    project_path=str(script_dir),
    image_format="png",
    view="isometric",
    log_scale=True,
    show=False,
)

# 13. 同じフィールドプロットをインタラクティブなPyVistaウィンドウで表示する
m3d.post.plot_field_from_fieldplot(
    plot_name="CoreMagB",
    view="isometric",
    log_scale=True,
    show=True,
)

# 14. 保存して終了する
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)

temp_folder.cleanup()
