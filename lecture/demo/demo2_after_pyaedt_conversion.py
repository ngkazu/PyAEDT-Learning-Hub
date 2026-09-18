"""講義デモ2（変換後）: demo2_before_native_script.py と同じ操作を PyAEDT から実行する。

(a) 橋渡し方式: app.oeditor など、ネイティブAPIオブジェクトへ直接アクセスして
    記録スクリプトの呼び出しをほぼそのまま貼り付ける。
(b) 高レベルAPI方式（推奨）: hfss.modeler.create_box(...) のようなPyAEDTのAPIに書き直す。

AEDT_VERSION は手元の環境に合わせて変更する。
"""

from ansys.aedt.core import Hfss

AEDT_VERSION = "2026.1"

hfss = Hfss(version=AEDT_VERSION, new_desktop=True, non_graphical=False)

# (a) 橋渡し方式: 記録スクリプトの oEditor.CreateBox(...) を app.oeditor.CreateBox(...) に置き換えるだけ
hfss.oeditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "0mm",
        "YPosition:=", "0mm",
        "ZPosition:=", "0mm",
        "XSize:=", "10mm",
        "YSize:=", "10mm",
        "ZSize:=", "10mm",
    ],
    [
        "NAME:Attributes",
        "Name:=", "Box1",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0,
        "PartCoordinateSystem:=", "Global",
        "UDMId:=", "",
        "MaterialValue:=", "\"vacuum\"",
        "SurfaceMaterialValue:=", "\"\"",
        "SolveInside:=", True,
    ],
)

# (b) 高レベルAPI方式（推奨）: 同じ箱を PyAEDT の modeler API で作成
hfss.modeler.create_box(
    origin=[20, 0, 0],
    sizes=[10, 10, 10],
    name="Box2",
    material="vacuum",
)

hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
