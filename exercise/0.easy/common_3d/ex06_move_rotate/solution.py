"""演習6: 形状の移動（Move）と回転（Rotate）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 設計変数を定義する
app["box_size"] = "10mm"

# 4. 箱を原点に作成する
box = app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="MyBox",
    material="aluminum",
)

# 5. 箱をX軸方向に移動する
app.modeler.move(assignment=box.name, vector=["box_size*2", 0, 0])

# 6. 箱をZ軸周りに45度回転する
app.modeler.rotate(assignment=box.name, axis="Z", angle=45, units="deg")

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
