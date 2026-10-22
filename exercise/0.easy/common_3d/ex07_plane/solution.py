"""演習7: Planeを作る。

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

# 4. 箱を作成する（Planeが何を切るのか分かりやすくするための土台）
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="MyBox",
    material="aluminum",
)

# 5. 箱の中心を通るXZ平面（y = box_size/2）にPlaneを作成する
# PlaneはシートやCADオブジェクトではなく、座標系上の「基準点＋法線ベクトル」で定義される特殊な平面。
# フィールドプロットのカットプレーンなど、座標平面そのものを指定する必要がある場面で使う。
app.modeler.create_plane(
    name="MyPlane",
    plane_base_x="0mm",
    plane_base_y="box_size/2",
    plane_base_z="0mm",
    plane_normal_x="0mm",
    plane_normal_y="1mm",
    plane_normal_z="0mm",
)

# 6. 保存する
app.save_project()

# 7. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
