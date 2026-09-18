"""講義デモ2（変換前）: AEDT内蔵のスクリプト記録機能が出力するコードのイメージ（簡略化）。

このファイルは参考コードであり、単体では実行できない。
`oDesktop` / `oProject` / `oDesign` / `oEditor` は、AEDT自身のスクリプト実行環境
（Tools メニューのスクリプト機能や -RunScript 起動）でのみ、あらかじめ用意されているオブジェクトである。
このコードを PyAEDT（CPython）から動かす方法は demo2_after_pyaedt_conversion.py を参照。
"""

# 以下はAEDT内蔵スクリプト記録の出力イメージ（簡略化した例）。単体実行不可。

oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project1")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.CreateBox(
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
