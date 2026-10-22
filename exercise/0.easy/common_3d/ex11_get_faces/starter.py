"""演習11: 面（Face）を取得する（get_object_faces→get_face_center/get_face_area）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動する
app = None

# TODO: 3. 箱（例: origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="MyBox", material="aluminum"）を作成する
box = None

# TODO: 4. modeler.get_object_faces(assignment=box.name) でオブジェクトの面IDリストを取得する
face_ids = None

# TODO: 5. face_ids[0] について、modeler.get_face_center() で中心座標、
#          modeler.get_face_area() で面積を取得する

# TODO: 6. 保存する

# TODO: 7. 終了する
