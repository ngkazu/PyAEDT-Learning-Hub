"""演習9: プロジェクト変数とデザイン変数を作る・変更する。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. デザイン変数を定義する（このデザインの中だけで使える変数。プレフィックスなし）
app["design_box_size"] = "10mm"

# 4. プロジェクト変数を定義する（同じプロジェクト内の他のデザインからも参照できる変数。"$"で始める）
app["$project_scale"] = "2"

# 5. 両方の変数を使って箱を作成する（デザイン変数×プロジェクト変数、という式も書ける）
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["design_box_size*$project_scale", "design_box_size*$project_scale", "design_box_size"],
    name="MyBox",
    material="aluminum",
)

# 6. デザイン変数の値を変更する（"design_"で始まる名前だが実際のプレフィックス判定は"$"の有無）
app["design_box_size"] = "20mm"

# 7. プロジェクト変数の値を変更する
app["$project_scale"] = "3"

# 8. 保存する
app.save_project()

# 9. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
