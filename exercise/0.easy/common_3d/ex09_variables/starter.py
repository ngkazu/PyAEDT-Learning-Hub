"""演習9: プロジェクト変数とデザイン変数を作る・変更する。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. デザイン変数 design_box_size="10mm" を定義する（app["design_box_size"] = "10mm"）

# TODO: 4. プロジェクト変数 $project_scale="2" を定義する（変数名の先頭に "$" を付ける）

# TODO: 5. 両方の変数を使って一辺 "design_box_size*$project_scale" の箱 "MyBox" を作成する

# TODO: 6. デザイン変数の値を "20mm" に変更する

# TODO: 7. プロジェクト変数の値を "3" に変更する

# TODO: 8. 保存する

# TODO: 9. 終了する
