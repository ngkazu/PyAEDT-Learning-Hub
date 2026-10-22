"""演習7: Planeを作る。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 box_size="10mm" を定義する

# TODO: 4. 一辺box_sizeの箱 "MyBox" を原点に作成する（材料は任意）

# TODO: 5. modeler.create_plane(name="MyPlane", plane_base_x="0mm", plane_base_y="box_size/2",
#          plane_base_z="0mm", plane_normal_x="0mm", plane_normal_y="1mm", plane_normal_z="0mm") で
#          箱の中心を通るXZ平面にPlaneを作成する

# TODO: 6. 保存する

# TODO: 7. 終了する
