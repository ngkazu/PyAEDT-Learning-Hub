"""演習3: コイル・コア電磁石（モデル作成〜解析実行）。"""

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Maxwell3d を Magnetostatic ソリューションで起動する
m3d = Maxwell3d(
    design="coil_core_electromagnet",
    solution_type="Magnetostatic",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
m3d.modeler.model_units = "mm"

# 2. コア用の磁性材料を作る（BH曲線は使わず、比透磁率1000の線形材料として簡略化）
core_steel = m3d.materials.add_material(name="core_steel")
core_steel.conductivity = 2000000
core_steel.permeability.value = 1000

# 3. 寸法をデザイン変数として定義する（ジオメトリ作成前に先に定義する）
m3d["core_r"] = "10mm"  # コア半径
m3d["core_h"] = "40mm"  # コア高さ
m3d["coil_ri"] = "15mm"  # コイル内半径（core_rより大→コアと非干渉）
m3d["coil_ro"] = "25mm"  # コイル外半径
m3d["coil_h"] = "20mm"  # コイル高さ
m3d["amp_turns"] = "1000A"  # 起磁力（アンペアターン）

# 4. コア（Z軸中心の円柱）を作成する
m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-core_h/2"],
    radius="core_r",
    height="core_h",
    name="Core",
    material=core_steel.name,
)

# 5. コイル（外円柱から内円柱をsubtractして円環にする）を作成する
m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-coil_h/2"],
    radius="coil_ro",
    height="coil_h",
    name="Coil",
    material="copper",
)
m3d.modeler.create_cylinder(
    orientation="Z",
    origin=["0mm", "0mm", "-coil_h/2"],
    radius="coil_ri",
    height="coil_h",
    name="Coil_hole",
    material="copper",
)
m3d.modeler.subtract(blank_list=["Coil"], tool_list=["Coil_hole"], keep_originals=False)

# 6. 解析領域（Region）を作成する（全方向+100%パディング）
m3d.modeler.create_region(pad_value=[100, 100, 100, 100, 100, 100], pad_type="Percentage Offset", name="Region")

# 7. コイルをZX平面で断面切断し、片側だけを残して電流を流す断面を作る
m3d.modeler.section(assignment="Coil", plane="ZX")
m3d.modeler.separate_bodies(["Coil_Section1"])
m3d.modeler.delete("Coil_Section1_Separate1")

# 8. 断面にコイルターミナル（Coil Terminal）を割り当てる
m3d.assign_coil(assignment=["Coil_Section1"], conductors_number=1, polarity="Positive", name="CoilTerminal")

# 9. Winding（電流源・ソリッド・amp_turns）を作成し、コイルターミナルを紐付ける
m3d.assign_winding(assignment=None, winding_type="Current", is_solid=True, current="amp_turns", name="Winding1")
m3d.add_winding_coils(assignment="Winding1", coils=["CoilTerminal"])

# 10. セットアップを作成する
setup = m3d.create_setup(name="MySetup")
setup.props["MaximumPasses"] = 6
setup.props["MinimumPasses"] = 2
setup.props["MinimumConvergedPasses"] = 1
setup.props["PercentError"] = 1
setup.props["PercentRefinement"] = 30

# 11. 解析を実行する
setup.analyze()

# 12. 保存して終了する
# normalはSetup作成→解析実行までで終了する（フィールドプロット等のポスト処理はhard以降で追加する）。
m3d.save_project()
m3d.release_desktop(close_projects=True, close_desktop=True)

