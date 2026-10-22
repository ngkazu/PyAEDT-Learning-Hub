"""演習16: ローカル座標系を作る（create_coordinate_system→set_working_coordinate_system）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. グローバル座標系の原点から離れた位置にローカル座標系を作成する
app.modeler.create_coordinate_system(
    origin=[10, 10, 10],
    reference_cs="Global",
    name="MyCS",
)

# 4. 作業座標系をローカル座標系に切り替える
app.modeler.set_working_coordinate_system("MyCS")

# 5. 箱を作成する（原点[0,0,0]はローカル座標系上の位置になる）
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["10mm", "10mm", "10mm"],
    name="BoxOnLocalCS",
    material="aluminum",
)

# 6. 作業座標系をグローバルに戻す
app.modeler.set_working_coordinate_system("Global")

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
