"""演習14: 断面を切ってターミナル面を作る（section→separate_bodies→delete）。

例としてIcepakを使用している。他のcommon_3dアプリ（Hfss, Maxwell3d, Q3d, Mechanical）でも
import とアプリ生成部分を書き換えるだけで同じ手順が通る。
"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1-2. アプリケーションを起動する
app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 3. 円環（外円柱から内円柱をsubtractしたリング）を作成する
app.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "0mm"],
    radius="20mm",
    height="10mm",
    name="Ring",
    material="copper",
)
app.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "0mm"],
    radius="12mm",
    height="10mm",
    name="Ring_hole",
    material="copper",
)
app.modeler.subtract(blank_list=["Ring"], tool_list=["Ring_hole"], keep_originals=False)

# 4. 円環をZX平面で断面切断する（円環は左右2枚の離れた面になる）
app.modeler.section(assignment="Ring", plane="ZX")

# 5. 離れた2枚の面を別オブジェクトに分離する
app.modeler.separate_bodies(["Ring_Section1"])

# 6. 分離で生成された片方を削除し、もう片方（Ring_Section1）だけを残す
app.modeler.delete("Ring_Section1_Separate1")

# 7. 保存する
app.save_project()

# 8. 終了する
app.release_desktop(close_projects=True, close_desktop=True)
