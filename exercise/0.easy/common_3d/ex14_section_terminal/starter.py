"""演習14: 断面を切ってターミナル面を作る（section→separate_bodies→delete）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
アプリケーションクラスのimport部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1-2. アプリケーションを起動する
app = None

# TODO: 3. 外円柱(radius="20mm", name="Ring")と内円柱(radius="12mm", name="Ring_hole")を作成し、
#          modeler.subtract(blank_list=["Ring"], tool_list=["Ring_hole"], keep_originals=False) で
#          円環にする

# TODO: 4. modeler.section(assignment="Ring", plane="ZX") で円環をZX平面で断面切断する
#          （円環は左右2枚の離れた面になる）

# TODO: 5. modeler.separate_bodies(["Ring_Section1"]) で離れた2枚の面を別オブジェクトに分離する

# TODO: 6. modeler.delete("Ring_Section1_Separate1") で分離された片方を削除し、
#          もう片方（Ring_Section1）だけを残す

# TODO: 7. 保存する

# TODO: 8. 終了する
