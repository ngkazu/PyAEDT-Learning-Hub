"""演習5: ブーリアン演算（Unite）で2つの箱を結合する。

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

# 4. 1つ目の箱を作成する
box1 = app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="Box1",
    material="aluminum",
)

# 5. 2つ目の箱を、1つ目と一部重なる位置に作成する
box2 = app.modeler.create_box(
    origin=["box_size/2", 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="Box2",
    material="aluminum",
)

# 6. 2つの箱を1つに結合する（Box2はモデルツリーから消え、Box1に統合される）
app.modeler.unite([box1.name, box2.name])

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
