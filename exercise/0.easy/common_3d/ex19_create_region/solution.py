"""演習19: 解析領域（Region）を作る（create_region）。

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

# 3. 対象の形状を作成する
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=[20, 20, 10],
    name="MyBox",
    material="copper",
)

# 4. Icepakでは既定で"Region"が自動生成されるため、作り直す前にいったん削除する
if "Region" in app.modeler.object_names:
    app.modeler["Region"].delete()

# 5. 形状全体を囲む解析領域（Region）を、全方向100%のパーセントオフセットで作成する
app.modeler.create_region(pad_value=100, pad_type="Percentage Offset")

# 6. Regionのバウンディングボックスを取得する（確認用）
region_bbox = app.modeler["Region"].bounding_box

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
