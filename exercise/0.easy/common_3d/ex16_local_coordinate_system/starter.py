"""演習16: ローカル座標系を作る（create_coordinate_system→set_working_coordinate_system）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動する
app = None

# TODO: 3. modeler.create_coordinate_system(origin=[10, 10, 10], reference_cs="Global", name="MyCS") で
#          グローバル座標系の原点から離れた位置にローカル座標系を作成する

# TODO: 4. modeler.set_working_coordinate_system("MyCS") で作業座標系をローカル座標系に切り替える

# TODO: 5. 箱（origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="BoxOnLocalCS",
#          material="aluminum"）を作成する（原点はローカル座標系上の位置になる）

# TODO: 6. modeler.set_working_coordinate_system("Global") で作業座標系をグローバルに戻す

# TODO: 7. 保存する

# TODO: 8. 終了する
