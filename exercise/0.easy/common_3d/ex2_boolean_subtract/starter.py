"""演習2: ブーリアン演算（Subtract）で中空の箱を作る。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 outer_size="20mm", inner_size="10mm", wall_gap="(outer_size-inner_size)/2" を定義する

# TODO: 4. 外側の箱 "OuterBox"（sizes=[outer_size]*3, material="aluminum"）を原点に作成する

# TODO: 5. 内側の箱 "InnerBox"（sizes=[inner_size]*3）を、原点から wall_gap だけずらした位置に作成する
#          （外側の箱の内部中央に収まるように配置する）

# TODO: 6. modeler.subtract(blank_list=outer_box, tool_list=inner_box, keep_originals=False) で
#          外側の箱から内側の箱をくり抜く

# TODO: 7. 保存する

# TODO: 8. 終了する
