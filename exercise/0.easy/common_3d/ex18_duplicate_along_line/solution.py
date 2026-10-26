"""演習18: 直線方向への複製（duplicate_along_line）でフィン列を作る。

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

# 3. フィン1枚目を作成する
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=[40, 2, 20],
    name="Fin",
    material="Al-Extruded",
)

# 4. Y方向にピッチ5mmで合計6枚に複製する
_ok, clone_names = app.modeler.duplicate_along_line(
    assignment="Fin",
    vector=[0, 5, 0],
    clones=6,
)

# 5. 全フィン名のリストを作っておく（元のオブジェクト名は戻り値に含まれない）
all_fin_names = ["Fin"] + clone_names

# 6. 保存する
app.save_project()

# 7. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
