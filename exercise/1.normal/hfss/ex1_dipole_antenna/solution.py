"""演習1: 半波長ダイポールアンテナ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

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

# 3. 組み込み3Dコンポーネントを挿入する
component_name = "Dipole_Antenna_DM"
component_path = hfss.components3d[component_name]
component_parameters = hfss.get_component_variables(component_name)
component_parameters["dipole_length"] = "l_dipole"
hfss.modeler.insert_3d_component(
    input_file=component_path,
    geometry_parameters=component_parameters,
    name="Dipole1",
)

# 4. 解析領域を作成する
hfss.create_open_region(frequency="1.5GHz")

# 5. セットアップを作成する
# MultipleAdaptiveFreqsSetup で帯域の両端(1GHz/2GHz)にアダプティブメッシュを行うことで、
# 掃引全体（特に共振点1.5GHz付近）でのメッシュ精度を安定させる。
# props経由での事後変更ではなく、create_setup の引数として直接渡す（native APIのプロパティ名）。
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
