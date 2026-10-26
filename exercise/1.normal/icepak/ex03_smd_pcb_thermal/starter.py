"""演習3: PCB表面実装部品の熱解析（モデル作成〜解析実行）。"""

from ansys.aedt.core import Icepak
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modules.mesh_icepak import MeshRegion

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Icepak を SteadyState ソリューションで起動し、modeler.model_units = "mm" を設定する
ipk = None

# TODO: 2. edit_design_settings(ambient_temperature="20cel", gravity_dir=2) で
#          周囲温度20℃・重力方向-Zを設定する

# TODO: 3. PCB基板とその上の層を下から順にBoxで積み重ねて作成する（README.mdの表を参照）
#          "Box1" PCB基板: origin=[0, 0, 0], sizes=[50, 50, 1.6], material="fr4_epoxy"
#          "Box2" ベタ銅箔: origin=[0, 0, 0], sizes=[50, 50, 0.035], material="copper"
#          "Box3" 表面パッドA: origin=[24.5, 0, 1.565], sizes=[1, 24.5, 0.035], material="copper"
#          "Box4" 表面パッドB: origin=[24.5, 25.5, 1.565], sizes=[1, 24.5, 0.035], material="copper"
#          "Box5" はんだA: origin=[24.5, 24, 1.6], sizes=[1, 0.5, 0.05], material="solder"
#          "Box6" はんだB: origin=[24.5, 25.5, 1.6], sizes=[1, 0.5, 0.05], material="solder"
#          "Box7" 部品本体: origin=[24.5, 24, 1.65], sizes=[1, 2, 0.5], material="ceramic_material"
#          "Box8" Siダイ: origin=[24.7, 24.5, 1.9], sizes=[0.6, 1, 0.02], material="si-typical_ref"

# TODO: 4. メッシュリージョンを3つ作成する（Regionより先に作る）。各リージョンごとに
#          MeshRegion(ipk, parts, name) でインスタンスを作成し、
#          mr.assignment.padding_types / padding_values で6面分のパディングを
#          Absolute Offsetで指定、mr.manual_settings=True、mr.settings["MaxElementSizeX/Y/Z"]
#          とmr.settings["MaxLevels"]でメッシュサイズを指定、mr.update()で適用する。
#          "MeshRegion1": parts=["Box1"], padding=["0"]*6, 1mm/Lv1
#          、さらに2Dマルチレベルメッシュを有効化（mr.settings["EnforeMLMType"]="2D"、
#          mr.settings["2DMLMType"]="2DMLM_XY"でXY面を指定）
#          "MeshRegion2": parts=["Box5","Box6","Box7","Box8"],
#            padding=["0.4","0.4","0.4","0.4","0.4","0"], 0.2mm/Lv3
#          "MeshRegion3": parts=["Box1"..."Box8"],
#            padding=["4","4","4","4","4.4","4"], 1mm/Lv1

# TODO: 5. 解析領域("Region")を作り直す。Icepakデザイン作成時に自動生成される既定の
#          "Region"を ipk.modeler["Region"].delete() でいったん削除してから、
#          create_region(pad_type=["Absolute Offset"] * 6,
#          pad_value=["25mm", "25mm", "25mm", "25mm", "50mm", "10mm"]) で
#          絶対値パディングのRegionを作成する（並びは+X,-X,+Y,-Y,+Z,-Z）

# TODO: 6. assign_solid_block(object_name="Box8", power_assignment="0.05W",
#          boundary_name="Block1") でSiダイに総発熱量0.05Wを割り当てる

# TODO: 7. modeler["Region"].bounding_box から6面の中心座標を計算し、
#          get_faceid_from_position() で各面の面IDを特定する

# TODO: 8. Regionの+Z面に assign_pressure_free_opening(assignment=[+Z面],
#          boundary_name="Opening1", no_reverse_flow=True) で圧力開口を割り当てる

# TODO: 9. Regionの±X, ±Y面（4面）に assign_pressure_free_opening(assignment=[4面],
#          boundary_name="Opening2", no_reverse_flow=False) で圧力開口を割り当てる

# TODO: 10. Regionの-Z面に assign_stationary_wall_with_htc(geometry=-Z面,
#          name="StationaryWall1", thickness="30mm", material="Epoxy Resin-JSME",
#          htc="10w_per_m2kel", ref_temperature="AmbientTemp", shell_conduction=True) で
#          HTC壁面境界条件を割り当てる

# TODO: 11. セットアップ "Setup1" を作成し、Flow Regime="Laminar"、
#           Include Gravity=True、Radiation Model="Discrete Ordinates Model"、
#           最大反復500、収束条件（Flow=0.001、Energy=1e-07）、
#           Linear Solver Type - Pressure="V" を設定する

# TODO: 12. 解析を実行する

# TODO: 13. 保存して終了する（normalはここまで。ポスト処理は行わない）
