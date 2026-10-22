"""演習1: コモンモードチョーク（巻線損失・コア損失レポート、Bフィールドプロット）。"""

import json
import tempfile

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Maxwell3d を EddyCurrent ソリューションで起動する
m3d = Maxwell3d(
    solution_type="EddyCurrent",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 2. チョークのジオメトリパラメータを辞書で定義する（normalと同じモデル）
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
        "Turns": 10,
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

# 3. 辞書の整合性を確認してからチョークを作成する
m3d.modeler.check_choke_values(input_dir=choke_fn, create_another_file=False)
list_object = m3d.modeler.create_choke(input_file=choke_fn)
core = list_object[1]
winding1 = list_object[2]
winding2 = list_object[3]

# 4. 解析領域（Region）を作成する（-Z面は0%、それ以外は100%のパディング）
m3d.modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=0)

# 5. 各巻線の両端面に電流励振を割り当てる（差動モードなので位相を180度ずらす）
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

# 6. セットアップを作成する（normalと同じ150kHz）
setup = m3d.create_setup(name="MySetup")
setup.props["Frequency"] = "150kHz"

# 7. 解析を実行する
setup.analyze()

# 8. 巻線のオーミック損失（SolidLoss）とコア損失（CoreLoss）をデータテーブルレポートとして作成する
m3d.post.create_report(
    expressions=["SolidLoss"],
    report_category="Fields",
    plot_type="Data Table",
    plot_name="WindingLoss",
)
m3d.post.create_report(
    expressions=["CoreLoss"],
    report_category="Fields",
    plot_type="Data Table",
    plot_name="CoreLoss",
)

# 9. コア表面のB磁束密度（Mag_B）のフィールドプロットを作成する
m3d.post.create_fieldplot_surface(
    assignment=core.name,
    quantity="Mag_B",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": "150kHz", "Phase": "0deg"},
    plot_name="CoreMagB",
)

# 10. 保存して終了する
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)

temp_folder.cleanup()
