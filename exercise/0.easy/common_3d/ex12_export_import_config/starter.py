"""演習12: デザイン設定のJSON入出力（configurations.export_config→import_config）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動する
app = None

# TODO: 3. デザイン変数(box_size="10mm")を定義し、それを使った箱(MyBox, material="aluminum")を作成する

# TODO: 4. app.configurations.export_config(config_file, overwrite=True) で
#          現在のデザイン設定（変数・材料など）をJSONファイルにエクスポートする
#          （config_file は f"{app.working_directory}/my_config.json" などとする）

# TODO: 5. app.insert_design(name="ImportedDesign") で新しいデザインを同じプロジェクト内に追加する

# TODO: 6. app.configurations.import_config(config_file) でJSONファイルを新しいデザインにインポートする

# TODO: 7. 保存する

# TODO: 8. 終了する
