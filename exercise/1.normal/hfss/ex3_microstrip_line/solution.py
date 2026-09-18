"""演習3: マイクロストリップ線路（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 設計寸法（このプロジェクトの他演習とは異なり、Python側の定数として扱う。理由は課題文を参照）。
SUB_W = 6.0  # 基板の幅 [mm]（Y方向）
SUB_H = 1.0  # 基板の厚さ [mm]（Z方向）
LINE_W = 1.5  # マイクロストリップ導体幅 [mm]（Y方向）
LINE_L = 10.0  # マイクロストリップ導体長さ [mm]（X方向、伝送方向）
AIR_H = 3.0  # 基板上部のエアボックス高さ [mm]

# 1. Hfss を Terminal ソリューションで起動する
hfss = Hfss(
    solution_type="Terminal",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
hfss.modeler.model_units = "mm"

# 2. 基板（3Dソリッド）を作成する
substrate = hfss.modeler.create_box(
    origin=[0, -SUB_W / 2, 0],
    sizes=[LINE_L, SUB_W, SUB_H],
    name="Substrate",
    material="alumina_96pct",
)

# 3. GND と信号線を2Dシートとして作成する
# シート（2Dオブジェクト）には Material プロパティが存在しない。assign_material() は何も起こさず
# 失敗にも見えないため、導体らしく振る舞わせるには assign_finite_conductivity() を明示的に割り当てる。
gnd = hfss.modeler.create_rectangle(
    orientation=Plane.XY,
    origin=[0, -SUB_W / 2, 0],
    sizes=[LINE_L, SUB_W],
    name="GND",
)
hfss.assign_finite_conductivity(assignment=gnd.name, material="copper", name="GND_FC")

line = hfss.modeler.create_rectangle(
    orientation=Plane.XY,
    origin=[0, -LINE_W / 2, SUB_H],
    sizes=[LINE_L, LINE_W],
    name="Line",
)
hfss.assign_finite_conductivity(assignment=line.name, material="copper", name="Line_FC")

# 4. エアボックスを作成する
# 基板上面（z=SUB_H）から積み上げる。z=0から作ると基板と体積的に重なってしまう。
airbox = hfss.modeler.create_box(
    origin=[0, -SUB_W / 2, SUB_H],
    sizes=[LINE_L, SUB_W, AIR_H],
    name="AirBox",
    material="vacuum",
)

# 5. エアボックスの両端面にWave Portを作成する
p1 = hfss.modeler.create_rectangle(
    orientation=Plane.YZ,
    origin=[0, -SUB_W / 2, 0],
    sizes=[SUB_W, SUB_H + AIR_H],
    name="Port1_sheet",
)
hfss.wave_port(assignment=p1.name, name="P1", modes=1, renormalize=True, impedance=50)

p2 = hfss.modeler.create_rectangle(
    orientation=Plane.YZ,
    origin=[LINE_L, -SUB_W / 2, 0],
    sizes=[SUB_W, SUB_H + AIR_H],
    name="Port2_sheet",
)
hfss.wave_port(assignment=p2.name, name="P2", modes=1, renormalize=True, impedance=50)

# 6. エアボックスの輻射境界を面ごとに割り当てる
# assign_radiation_boundary_to_objects("AirBox") は6面すべてに割り当ててしまい、
# 下面（GND_FCと重複）や両端面（Wave Portと重複）と衝突する。上面と側面2面だけに絞る。
rad_faces = []
for f in airbox.faces:
    x, y, z = f.center
    is_bottom = abs(z - SUB_H) < 1e-6
    is_port_end = abs(x - 0) < 1e-6 or abs(x - LINE_L) < 1e-6
    if not is_bottom and not is_port_end:
        rad_faces.append(f.id)
hfss.assign_radiation_boundary_to_faces(assignment=rad_faces, name="Rad_top_sides")

# 7. モデルを検証する
# 境界を手動で割り当てた場合、重複などの問題は作成時ではなくここで検出される。
_, passed = hfss.validate_full_design()
if not passed:
    hfss.logger.warning("Design validation reported issues. Check the AEDT message manager.")

# 8. セットアップと周波数掃引を作成する
setup = hfss.create_setup(name="Setup1", Frequency="10GHz", MaxDeltaS=0.02, MaximumPasses=6)
# create_linear_count_sweep は setup オブジェクトではなく hfss（アプリ）側のメソッド。
hfss.create_linear_count_sweep(
    setup="Setup1",
    unit="GHz",
    start_frequency=0.1,
    stop_frequency=10,
    num_of_freq_points=201,
    name="Sweep",
    sweep_type="Interpolating",
)

# 9. 解析を実行する
setup.analyze()

# 10. 保存して終了する
# normalはSetup作成→解析実行までで終了する（ポスト処理はhard以降で追加するため、ここでは行わない）。
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
