"""演習12: デザイン設定のJSON入出力（configurations.export_config→import_config）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. デザイン変数を定義し、それを使った箱を作成する
app["box_size"] = "10mm"
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="MyBox",
    material="aluminum",
)

# 4. 現在のデザイン設定（変数・材料など）をJSONファイルにエクスポートする
config_file = f"{app.working_directory}/my_config.json"
app.configurations.export_config(config_file, overwrite=True)

# 5. 新しいデザインを同じプロジェクト内に追加する（この時点では変数・形状は存在しない）
app.insert_design(name="ImportedDesign")

# 6. エクスポートしたJSONファイルを新しいデザインにインポートする
app.configurations.import_config(config_file)

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
