"""演習13: カスタム材料を作る（add_material→conductivity/permeability設定）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動する
app = None

# TODO: 3. materials.add_material(name="my_custom_material") でカスタム材料を追加し、
#          conductivity = 3.526e7、permeability.value = 1000 を設定する
my_material = None

# TODO: 4. material=my_material.name を指定して箱（origin=[0,0,0], sizes=["10mm","10mm","10mm"],
#          name="MyBox"）を作成する

# TODO: 5. 保存する

# TODO: 6. 終了する
