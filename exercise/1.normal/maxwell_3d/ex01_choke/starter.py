"""演習1: コモンモードチョーク（モデル作成〜解析実行）。"""

import json
import tempfile

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Maxwell3d を EddyCurrent ソリューションで起動し、modeler.model_units = "mm" を設定する
m3d = None

# TODO: 2. チョークのジオメトリパラメータ辞書(choke_descriptor)を定義する（README.mdの参考値表を参照）
#          "Number of Windings": {"1": False, "2": True, "3": False, "4": False}
#          "Layer": {"Simple": True, "Double": False, "Triple": False}
#          "Layer Type": {"Separate": True, "Linked": False}  ← 単層では必ずSeparate（README.mdの注意参照）
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

# TODO: 3. choke_descriptor を一時JSONファイルに書き出し、
#          modeler.check_choke_values(input_dir=..., create_another_file=False) で整合性を確認したうえで、
#          modeler.create_choke(input_file=...) でチョークを作成する
#          戻り値は [success, core, [winding1_obj, points], [winding2_obj, points]] のリスト

# TODO: 4. modeler.create_air_region() で解析領域（Region）を作成する（Regionがないと解析が失敗する）
#          -Z面は0%、それ以外（x_pos, y_pos, z_pos, x_neg, y_neg）は100%のパディングにする

# TODO: 5. modeler.get_object_faces() で各巻線の両端面を取得し、
#          assign_current() で電流励振を割り当てる（差動モードなので2つの巻線の位相を180度ずらす）

# TODO: 6. セットアップ "MySetup" を作成し、setup.props["Frequency"] = "150kHz" を設定する

# TODO: 7. 解析を実行する

# TODO: 8. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
