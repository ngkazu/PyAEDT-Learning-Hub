"""演習2: ブーリアン演算（Subtract）で中空の箱を作る。

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
app["outer_size"] = "20mm"
app["inner_size"] = "10mm"
app["wall_gap"] = "(outer_size-inner_size)/2"

# 4. 外側の箱を作成する
outer_box = app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["outer_size", "outer_size", "outer_size"],
    name="OuterBox",
    material="aluminum",
)

# 5. 内側の箱を作成する（外側の箱の内部中央に収まる位置に配置する）
inner_box = app.modeler.create_box(
    origin=["wall_gap", "wall_gap", "wall_gap"],
    sizes=["inner_size", "inner_size", "inner_size"],
    name="InnerBox",
)

# 6. 外側の箱から内側の箱をくり抜く（内側の箱は削除される）
app.modeler.subtract(blank_list=outer_box, tool_list=inner_box, keep_originals=False)

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
