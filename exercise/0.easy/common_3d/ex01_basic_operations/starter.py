"""演習1: AEDTの基本操作（起動 -> 変数 -> 形状 -> 保存 -> 終了）。

docs/app-selection.md の common_3d 分類から使いたいアプリケーションを選び、
下記の import とアプリ生成部分を書き換えてから進めること。
"""

from ansys.aedt.core import Icepak  # TODO: 使いたいアプリケーションのクラスに書き換える
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. 選んだアプリケーションを起動する（new_desktop=True, non_graphical=False）
app = None

# TODO: 3. 設計変数 box_size = "10mm" を定義する

# TODO: 4. 原点[0, 0, 0]、一辺box_sizeの立方体を "MyBox" という名前で作成する

# TODO: 5. MyBox の材料を "aluminum" に変更する

# TODO: 6. box_size の値を "20mm" に変更する

# TODO: 7. プロジェクトを保存する

# TODO: 8. release_desktop() でAEDTを終了する
