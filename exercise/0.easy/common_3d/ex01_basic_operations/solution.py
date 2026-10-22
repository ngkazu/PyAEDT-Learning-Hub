"""演習1: AEDTの基本操作（起動 -> 変数 -> 形状 -> 保存 -> 終了）。

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

# 4. 立方体を作成する
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="MyBox",
)

# 5. 材料を変更する
app.assign_material(assignment="MyBox", material="aluminum")

# 6. 変数の値を変更する（形状はこの変数を参照しているので自動的にサイズが変わる）
app["box_size"] = "20mm"

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
