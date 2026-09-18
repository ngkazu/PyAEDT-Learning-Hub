"""演習4: シート形状（矩形・円）を作る。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 rect_w="10mm", rect_h="20mm", circle_r="5mm" を定義する

# TODO: 4. modeler.create_rectangle(orientation=Plane.XY, origin=[0,0,0],
#          sizes=["rect_w","rect_h"], name="MyRectangle") で矩形シートを作成する

# TODO: 5. modeler.create_circle(orientation=Plane.XY, origin=["rect_w+circle_r+5mm",0,0],
#          radius="circle_r", name="MyCircle") で矩形と重ならない位置に円形シートを作成する

# TODO: 6. 保存する

# TODO: 7. 終了する
