"""演習15: ポリラインの回転複製で環状形状を作る（create_polyline→duplicate_around_axis→unite）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)
app.modeler.model_units = "mm"

# 3. 4分の1形状をポリラインで描画する（直線1区間＋円弧1区間）
P1 = [20, -10, 0]
P2 = [20, 10, 0]
P3 = [14, 14, 0]  # 円弧の経由点
P4 = [10, 20, 0]  # 円弧の終点

quarter = app.modeler.create_polyline(
    points=[P1, P2, P3, P4],
    segment_type=["Line", "Arc"],
    name="Quarter",
)

# 4. 断面形状（矩形）を設定し、1本の棒状ソリッドにする
quarter.set_crosssection_properties(section="Rectangle", width=5, height=10)

# 5. Z軸まわりに90度ずつ回転複製し、4分の1形状から全体を作る
app.modeler.duplicate_around_axis(
    assignment="Quarter",
    axis="Z",
    angle=90,
    clones=4,
    create_new_objects=True,
    is_3d_comp=False,
)

# 6. 複製した4つを結合して、1つの環状形状にする
app.modeler.unite(["Quarter", "Quarter_1", "Quarter_2", "Quarter_3"])

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
