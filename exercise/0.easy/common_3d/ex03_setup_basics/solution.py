"""演習3: セットアップ（解析条件）を作ってみる。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る（create_setup自体はアプリ共通のAPI）。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 設計変数を定義し、形状を作成する（セットアップだけ単体では意味がないため、最低限のモデルを用意する）
app["box_size"] = "10mm"
app.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="MyBox",
    material="copper",
)

# 4. セットアップを作成する（名前だけ指定し、他はアプリごとの既定値のまま作成する）
setup = app.create_setup(name="MySetup")

# 5. 作成したセットアップのプロパティ（props）の一部を確認・変更する
# MaximumPasses は多くのソルバー系アプリに共通するプロパティ（存在しない場合はそのままにする）。
if "MaximumPasses" in setup.props:
    setup.props["MaximumPasses"] = 5
    setup.update()

# 6. 保存する
app.save_project()

# 7. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
