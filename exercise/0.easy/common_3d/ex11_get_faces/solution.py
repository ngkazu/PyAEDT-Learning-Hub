"""演習11: 面（Face）を取得する（get_object_faces→get_face_center/get_face_area）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 箱を作成する
box = app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["10mm", "10mm", "10mm"],
    name="MyBox",
    material="aluminum",
)

# 4. オブジェクト名から面IDのリストを取得する
face_ids = app.modeler.get_object_faces(assignment=box.name)

# 5. 最初の面について、中心座標と面積を取得する
first_face_center = app.modeler.get_face_center(assignment=face_ids[0])
first_face_area = app.modeler.get_face_area(assignment=face_ids[0])

# 6. 保存する
app.save_project()

# 7. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
