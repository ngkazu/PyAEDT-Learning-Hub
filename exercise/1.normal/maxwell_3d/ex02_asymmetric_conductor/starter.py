"""演習2: TEAM7非対称導体（モデル作成〜解析実行）。"""

from math import sqrt

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Maxwell3d を EddyCurrent ソリューションで起動し、modeler.model_units = "mm" を設定する
#          design="TEAM_7_Asymmetric_Conductor" を付けると分かりやすい
m3d = None

# TODO: 2. セットアップ "Setup1" を作成し、setup.props["Frequency"] = "200Hz" を設定する
#          （実測値比較用の50Hzスイープはexpertで追加するため、ここでは単一周波数のみ）

# 3. コイルの寸法を定義する（TEAM7図面の値。変更不要）
coil_external = 150 + 25 + 25
coil_internal = 150
coil_r1 = 25
coil_r2 = 50
coil_thk = coil_r2 - coil_r1
coil_height = 100
coil_centre = [294 - 25 - 150 / 2, 25 + 150 / 2, 19 + 30 + 100 / 2]

dim1 = coil_internal / 2 + (coil_external - coil_internal) / 4
dim2 = coil_internal / 2 - coil_r1
dim3 = dim2 + sqrt(((coil_r1 + (coil_r2 - coil_r1) / 2) ** 2) / 2)

P1 = [dim1, -dim2, 0]
P2 = [dim1, dim2, 0]
P3 = [dim3, dim3, 0]
P4 = [dim2, dim1, 0]

# TODO: 4. modeler.create_coordinate_system(origin=coil_centre, mode="view", view="XY", name="Coil_CS") で
#          ローカル座標系を作り、create_polyline(points=[P1, P2, P3, P4], segment_type=["Line", "Arc"],
#          name="Coil") で4分の1コイルを描画し、set_crosssection_properties(section="Rectangle",
#          width=coil_thk, height=coil_height) で断面を設定する。
#          その後 modeler.duplicate_around_axis(assignment="Coil", axis="Global", angle=90, clones=4,
#          create_new_objects=True, is_3d_comp=False) で90度回転複製し、
#          modeler.unite("Coil, Coil_1, Coil_2") → modeler.unite("Coil, Coil_3") で結合して
#          全体のコイル形状を作る

# TODO: 5. assign_material(assignment="Coil", material="Copper") でコイルに銅を割り当て、
#          solve_inside("Coil") で内部の電磁界解を有効にする

# TODO: 6. modeler.section(assignment="Coil", plane="YZ") でコイルを半分に切り、
#          modeler.separate_bodies(assignment="Coil_Section1") で分離し、
#          modeler.delete(assignment="Coil_Section1_Separate1") で不要な半分を削除する

# TODO: 7. デザイン変数 Coil_Excitation="2742A" を定義し、
#          assign_current(assignment="Coil_Section1", amplitude="Coil_Excitation", solid=False) で
#          コイルに電流励振を割り当てる。最後に modeler.set_working_coordinate_system("Global") を呼ぶ

# TODO: 8. materials.add_material("team7_aluminium") でアルミ板用の専用材料を追加し、
#          conductivity = 3.526e7 を設定する

# TODO: 9. modeler.create_box(origin=[0, 0, 0], sizes=[294, 294, 19], name="Plate",
#          material="team7_aluminium") でアルミ板を作成し、
#          modeler.create_box(origin=[18, 18, 0], sizes=[108, 108, 19], name="Hole") で穴用の箱を作り、
#          modeler.subtract(blank_list="Plate", tool_list=["Hole"], keep_originals=False) で穴を開ける

# TODO: 10. modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=100) で
#           解析領域（Region）を作成する

# TODO: 11. eddy_effects_on(assignment=["Coil"], enable_eddy_effects=False) と
#           eddy_effects_on(assignment=["Plate"], enable_displacement_current=False) で
#           渦電流・変位電流の有無を設定する

# TODO: 12. 解析を実行する

# TODO: 13. 保存して終了する（normalはここまで。$B_z$の評価やレポート作成はhard以降で追加する）
