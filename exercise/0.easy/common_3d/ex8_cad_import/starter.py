"""演習8: CADのインポート（エクスポート→インポートの往復）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. docs/app-selection.md からアプリケーションを選び、起動する
app = None

# TODO: 3. 設計変数 box_size="10mm" を定義する

# TODO: 4. 一辺box_sizeの箱 "MyBox" を原点に作成する（材料は任意）

# TODO: 5. modeler.export_3d_model(file_name="my_box", file_path=app.working_directory,
#          file_format=".step", assignment_to_export=[box.name]) で箱をSTEPファイルとして書き出す

# TODO: 6. modeler.delete([box.name]) で元の箱を削除する

# TODO: 7. modeler.import_3d_cad(input_file=f"{app.working_directory}/my_box.step") で
#          エクスポートしたSTEPファイルを読み込み直す

# TODO: 8. 保存する

# TODO: 9. 終了する
