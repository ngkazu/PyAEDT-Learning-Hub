"""演習15: ポリラインの回転複製で環状形状を作る（create_polyline→duplicate_around_axis→unite）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動し、modeler.model_units = "mm" を設定する
app = None

# 3. 4分の1形状のポイント定義（変更不要）
P1 = [20, -10, 0]
P2 = [20, 10, 0]
P3 = [14, 14, 0]  # 円弧の経由点
P4 = [10, 20, 0]  # 円弧の終点

# TODO: 4. create_polyline(points=[P1, P2, P3, P4], segment_type=["Line", "Arc"], name="Quarter") で
#          直線1区間＋円弧1区間からなる4分の1形状を描画する
quarter = None

# TODO: 5. set_crosssection_properties(section="Rectangle", width=5, height=10) で
#          断面形状を設定し、1本の棒状ソリッドにする

# TODO: 6. modeler.duplicate_around_axis(assignment="Quarter", axis="Z", angle=90, clones=4,
#          create_new_objects=True, is_3d_comp=False) で、Z軸まわりに90度ずつ回転複製する

# TODO: 7. modeler.unite(["Quarter", "Quarter_1", "Quarter_2", "Quarter_3"]) で
#          複製した4つを結合し、1つの環状形状にする

# TODO: 8. 保存する

# TODO: 9. 終了する
