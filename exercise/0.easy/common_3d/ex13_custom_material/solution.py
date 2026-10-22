"""演習13: カスタム材料を作る（add_material→conductivity/permeability設定）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. カスタム材料を追加し、導電率・比透磁率を設定する
my_material = app.materials.add_material(name="my_custom_material")
my_material.conductivity = 3.526e7
my_material.permeability.value = 1000

# 4. 作成した材料を割り当てた箱を作成する
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["10mm", "10mm", "10mm"],
    name="MyBox",
    material=my_material.name,
)

# 5. 保存する
app.save_project()

# 6. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
