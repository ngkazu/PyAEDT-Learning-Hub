"""講義デモ1: 起動 -> 変数定義 -> 箱を作る -> 保存 -> 終了 の最小デモ。

講義中に画面を見せながら実行する。AEDT_VERSION は手元の環境に合わせて変更する。
"""

from ansys.aedt.core import Hfss

AEDT_VERSION = "2026.1"

# 1. 起動（新規プロジェクトでHFSSを開く）
hfss = Hfss(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# 2. 変数を定義する（GUIの設計変数として登録される）
hfss["box_size"] = "10mm"

# 3. 箱を作る（形状作成）
hfss.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="Box1",
    material="vacuum",
)

# 4. 保存する
hfss.save_project()

# 5. 終了する（AEDTプロセスとプロジェクトを閉じる）
hfss.release_desktop(close_projects=True, close_desktop=True)
