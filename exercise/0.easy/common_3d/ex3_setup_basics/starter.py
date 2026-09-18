"""演習3: セットアップ（解析条件）を作ってみる。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 box_size="10mm" を定義し、"MyBox" という箱を作成する（材料は任意）

# TODO: 4. app.create_setup(name="MySetup") でセットアップを作成する
setup = None

# TODO: 5. setup.props に "MaximumPasses" があれば 5 に変更し、setup.update() を呼ぶ
#          （存在しない場合は何もしない。プロパティ名はアプリによって異なる）

# TODO: 6. 保存する

# TODO: 7. 終了する
