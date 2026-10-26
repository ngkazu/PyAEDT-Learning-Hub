"""演習18: 直線方向への複製（duplicate_along_line）でフィン列を作る。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する。
#           modeler.model_units = "mm" も設定する
app = None

# TODO: 3. フィン1枚目("Fin")を origin=[0, 0, 0], sizes=[40, 2, 20],
#          material="Al-Extruded" で作成する

# TODO: 4. _ok, clone_names = modeler.duplicate_along_line(assignment="Fin",
#          vector=[0, 5, 0], clones=6) で、Y方向にピッチ5mmで合計6枚に複製する

# TODO: 5. all_fin_names = ["Fin"] + clone_names で、全フィン名のリストを作る
#          （戻り値の clone_names には元のオブジェクト名は含まれない）

# TODO: 6. 保存する

# TODO: 7. 終了する
