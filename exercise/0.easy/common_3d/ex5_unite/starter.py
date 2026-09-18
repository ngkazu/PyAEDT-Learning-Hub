"""演習5: ブーリアン演算（Unite）で2つの箱を結合する。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 box_size="10mm" を定義する

# TODO: 4. 一辺box_sizeの箱 "Box1" を原点に作成する（材料は任意）

# TODO: 5. 同じサイズの箱 "Box2" を、Box1と一部重なる位置（例: origin=["box_size/2",0,0]）に作成する

# TODO: 6. modeler.unite([box1.name, box2.name]) で2つの箱を1つに結合する

# TODO: 7. 保存する

# TODO: 8. 終了する
