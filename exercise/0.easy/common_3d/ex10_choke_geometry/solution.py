"""演習10: チョークのジオメトリを作る（check_choke_values→create_choke）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)
app.modeler.model_units = "mm"

# 3. チョークのジオメトリパラメータ辞書(choke_descriptor)を定義する
# modeler.check_choke_values() のdocstringに載っているデフォルト例そのまま（巻線1本・単層）を使う。
choke_descriptor = {
    "Number of Windings": {"1": True, "2": False, "3": False, "4": False},
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

# 4. 辞書を一時JSONファイルに書き出す
import json
import tempfile

temp_folder = tempfile.TemporaryDirectory(suffix=".ansys")
choke_fn = f"{temp_folder.name}/choke_descriptor.json"
with open(choke_fn, "w") as outfile:
    json.dump(choke_descriptor, outfile)

# 5. 辞書の整合性を確認してからチョークのジオメトリを作成する（励振・Setupはここでは行わない）
app.modeler.check_choke_values(input_dir=choke_fn, create_another_file=False)
list_object = app.modeler.create_choke(input_file=choke_fn)
core = list_object[1]
winding = list_object[2]

# 6. 保存する
app.save_project()

# 7. 終了する
app.release_desktop(close_projects=True, close_desktop=True)

temp_folder.cleanup()
