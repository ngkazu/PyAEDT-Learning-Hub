"""演習19: 解析領域（Region）を作る（create_region）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する。
#           modeler.model_units = "mm" も設定する
app = None

# TODO: 3. 対象の形状("MyBox")を origin=[0, 0, 0], sizes=[20, 20, 10],
#          material="copper" で作成する

# TODO: 4. Icepakでは既定で"Region"が自動生成されるため、
#          if "Region" in modeler.object_names: modeler["Region"].delete() で
#          作り直す前にいったん削除する

# TODO: 5. create_region(pad_value=100, pad_type="Percentage Offset") で、
#          形状全体を囲む解析領域（Region）を全方向100%のパーセントオフセットで作成する

# TODO: 6. modeler["Region"].bounding_box でRegionのバウンディングボックスを取得する（確認用）

# TODO: 7. 保存する

# TODO: 8. 終了する
