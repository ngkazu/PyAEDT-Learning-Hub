"""演習10: チョークのジオメトリを作る（check_choke_values→create_choke）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る
（`modeler.create_choke()`は3Dモデラー系アプリ共通のメソッドのため）。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動し、modeler.model_units = "mm" を設定する
app = None

# TODO: 3. チョークのジオメトリパラメータ辞書(choke_descriptor)を定義する（README.mdの参考値表を参照）
#          "Number of Windings": {"1": True, "2": False, "3": False, "4": False}
#          "Layer": {"Simple": True, "Double": False, "Triple": False}
#          "Layer Type": {"Separate": True, "Linked": False}  ← 単層では必ずSeparate
#          "Similar Layer": {"Similar": True, "Different": False}
#          "Mode": {"Differential": True, "Common": False}
#          "Wire Section": {"None": False, "Hexagon": False, "Octagon": True, "Circle": False}
#          "Core": {"Name": "Core", "Material": "ferrite", "Inner Radius": 11, "Outer Radius": 17,
#                   "Height": 7, "Chamfer": 0.8}
#          "Outer Winding": {"Name": "Winding", "Material": "copper", "Inner Radius": 12, "Outer Radius": 16,
#                            "Height": 8, "Wire Diameter": 1, "Turns": 10, "Coil Pit(deg)": 9, "Occupation(%)": 0}
#          "Mid Winding": {"Turns": 8, "Coil Pit(deg)": 0.1, "Occupation(%)": 0}（単層では未使用だがキーは必須）
#          "Inner Winding": {"Turns": 12, "Coil Pit(deg)": 0.1, "Occupation(%)": 0}（単層では未使用だがキーは必須）
choke_descriptor = {}

# TODO: 4. choke_descriptor を一時JSONファイルに書き出す（json.dump()を使う）

# TODO: 5. modeler.check_choke_values(input_dir=choke_fn, create_another_file=False) で整合性を確認し、
#          modeler.create_choke(input_file=choke_fn) でチョークのジオメトリを作成する
#          （励振の割り当てやSetup作成はこの演習では行わない）
#          戻り値は [success, core, [winding_obj, 座標リスト]] のリスト

# TODO: 6. 保存する

# TODO: 7. 終了する
