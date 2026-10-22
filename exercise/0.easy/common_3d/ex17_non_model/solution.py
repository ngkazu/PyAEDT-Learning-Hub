"""演習17: 非モデル（non_model）形状を作る。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 通常のモデル形状（解析対象になるソリッド）を作成する
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["10mm", "10mm", "10mm"],
    name="ModelBox",
    material="aluminum",
)

# 4. 評価・参照専用の補助ライン（non_model=True）を作成する
# non_model=True にすると、解析対象のモデル形状には含まれない「参照用」オブジェクトになる。
app.modeler.create_polyline(
    points=[[0, 0, 15], [10, 10, 15]],
    name="ReferenceLine",
    non_model=True,
)

# 5. 保存する
app.save_project()

# 6. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
