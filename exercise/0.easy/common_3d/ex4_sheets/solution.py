"""演習4: シート形状（矩形・円）を作る。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 設計変数を定義する
app["rect_w"] = "10mm"
app["rect_h"] = "20mm"
app["circle_r"] = "5mm"

# 4. 矩形シートを作成する（XY平面、原点、幅rect_w×高さrect_h）
app.modeler.create_rectangle(
    orientation=Plane.XY,
    origin=[0, 0, 0],
    sizes=["rect_w", "rect_h"],
    name="MyRectangle",
)

# 5. 円形シートを作成する（XY平面、矩形と重ならない位置に配置）
app.modeler.create_circle(
    orientation=Plane.XY,
    origin=["rect_w+circle_r+5mm", 0, 0],
    radius="circle_r",
    name="MyCircle",
)

# 6. 保存する
app.save_project()

# 7. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
