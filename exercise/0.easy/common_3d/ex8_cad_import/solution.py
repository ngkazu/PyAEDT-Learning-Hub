"""演習8: CADのインポート（エクスポート→インポートの往復）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 設計変数を定義する
app["box_size"] = "10mm"

# 4. 箱を作成する（この演習では、外部CADファイルの代わりに自分で作った形状を使う）
box = app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="MyBox",
    material="aluminum",
)

# 5. 箱をSTEPファイルとしてエクスポートする（working_directoryに保存される）
app.modeler.export_3d_model(
    file_name="my_box",
    file_path=app.working_directory,
    file_format=".step",
    assignment_to_export=[box.name],
)

# 6. 元の箱をモデルから削除する（インポートし直すことが分かるように）
app.modeler.delete([box.name])

# 7. エクスポートしたSTEPファイルをCADインポートで読み込み直す
step_file_path = f"{app.working_directory}/my_box.step"
app.modeler.import_3d_cad(input_file=step_file_path)

# 8. 保存する
app.save_project()

# 9. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
