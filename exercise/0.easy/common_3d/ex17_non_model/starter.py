"""演習17: 非モデル（non_model）形状を作る。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動する
app = None

# TODO: 3. 通常のモデル形状（origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="ModelBox",
#          material="aluminum"）を作成する

# TODO: 4. create_polyline(points=[[0, 0, 15], [10, 10, 15]], name="ReferenceLine", non_model=True) で、
#          評価・参照専用の補助ラインを作成する（non_model=Trueなので解析対象には含まれない）

# TODO: 5. 保存する

# TODO: 6. 終了する
