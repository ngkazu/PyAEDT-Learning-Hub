"""演習3: コイル・コア電磁石（モデル作成〜解析実行）。"""

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Maxwell3d を Magnetostatic ソリューションで起動し、modeler.model_units = "mm" を設定する
m3d = None

# TODO: 2. コア用の磁性材料(name="core_steel")を追加し、conductivity = 2000000、
#          permeability.value = 1000（比透磁率1000の線形材料として簡略化）を設定する
core_steel = None

# TODO: 3. 寸法をデザイン変数として定義する（ジオメトリ作成前に先に定義する）
#          m3d["core_r"] = "10mm", m3d["core_h"] = "40mm", m3d["coil_ri"] = "15mm",
#          m3d["coil_ro"] = "25mm", m3d["coil_h"] = "20mm", m3d["amp_turns"] = "1000A"
#          （coil_ri > core_r にすることで、コイルとコアが非干渉になる）

# TODO: 4. create_cylinder(orientation="Z", origin=["0mm","0mm","-core_h/2"], radius="core_r",
#          height="core_h", name="Core", material=core_steel.name) でコアを作成する

# TODO: 5. コイルを作成する
#          - create_cylinder(..., radius="coil_ro", height="coil_h", name="Coil", material="copper")
#          - create_cylinder(..., radius="coil_ri", height="coil_h", name="Coil_hole", material="copper")
#          - modeler.subtract(blank_list=["Coil"], tool_list=["Coil_hole"], keep_originals=False) で
#            円環コイルにする

# TODO: 6. modeler.create_region(pad_value=[100,100,100,100,100,100],
#          pad_type="Percentage Offset", name="Region") で解析領域を作成する

# TODO: 7. modeler.section(assignment="Coil", plane="ZX") でコイルを断面切断し、
#          separate_bodies(["Coil_Section1"]) → delete("Coil_Section1_Separate1") で
#          片側だけを残して電流を流す断面を作る

# TODO: 8. assign_coil(assignment=["Coil_Section1"], conductors_number=1, polarity="Positive",
#          name="CoilTerminal") で断面にコイルターミナルを割り当てる

# TODO: 9. assign_winding(assignment=None, winding_type="Current", is_solid=True,
#          current="amp_turns", name="Winding1") でWindingを作成し、
#          add_winding_coils(assignment="Winding1", coils=["CoilTerminal"]) で紐付ける

# TODO: 10. セットアップ "MySetup" を作成し、MaximumPasses=6, MinimumPasses=2,
#           MinimumConvergedPasses=1, PercentError=1, PercentRefinement=30 を設定する

# TODO: 11. 解析を実行する

# TODO: 12. 保存して終了する（normalはここまで。フィールドプロット等のポスト処理はhard以降で追加する）


