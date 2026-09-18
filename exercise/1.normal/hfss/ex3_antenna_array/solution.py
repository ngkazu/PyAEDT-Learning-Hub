"""演習3: ダイポールアレイアンテナ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"
NUM_ELEMENTS = 4  # 配列素子数（Pythonのループ回数として使うだけなので、HFSSの設計変数にはしない）

settings.release_on_exception = False

# 1. Hfss を Modal ソリューションで起動する
hfss = Hfss(
    solution_type="Modal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)

# 2. 設計変数を定義する
hfss["l_dipole"] = "10.2cm"
hfss["element_spacing"] = "15cm"

# 3. 組み込み3Dコンポーネントを、素子数だけ座標系を変えて挿入する
# 各素子ごとにX軸方向へ element_spacing だけずらしたローカル座標系を作り、
# その座標系を基準にコンポーネントを挿入することで、位置合わせを行う。
component_name = "Dipole_Antenna_DM"
component_path = hfss.components3d[component_name]
component_parameters = hfss.get_component_variables(component_name)
component_parameters["dipole_length"] = "l_dipole"

for i in range(NUM_ELEMENTS):
    cs_name = f"CS_Element{i}"
    hfss.modeler.create_coordinate_system(
        origin=[f"{i}*element_spacing", 0, 0],
        name=cs_name,
    )
    hfss.modeler.insert_3d_component(
        input_file=component_path,
        geometry_parameters=component_parameters,
        coordinate_system=cs_name,
        name=f"Dipole_{i}",
    )

# 4. 解析領域を作成する
hfss.create_open_region(frequency="1.5GHz")

# 5. セットアップを作成する
setup = hfss.create_setup(
    name="MySetup",
    MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"],
    MaximumPasses=2,
)

# 6. 周波数掃引を追加する
setup.add_sweep(
    name="Sweep1",
    sweep_type="Interpolating",
    RangeStart="1GHz",
    RangeEnd="2GHz",
)

# 7. 解析を実行する
setup.analyze()

# 8. 保存して終了する
# normalはSetup作成→解析実行までで終了する（ポスト処理はhard以降で追加するため、ここでは行わない）。
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
