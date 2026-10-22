"""演習6: 形状の移動（Move）と回転（Rotate）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 box_size="10mm" を定義する

# TODO: 4. 一辺box_sizeの箱 "MyBox" を原点に作成する（材料は任意）

# TODO: 5. modeler.move(assignment=box.name, vector=["box_size*2", 0, 0]) で箱をX軸方向に移動する

# TODO: 6. modeler.rotate(assignment=box.name, axis="Z", angle=45, units="deg") で
#          箱をZ軸周りに45度回転する

# TODO: 7. 保存する

# TODO: 8. 終了する
