"""演習3: マイクロストリップ線路（S/フィールドのポスト処理）。"""

import os

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.constants import Plane
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

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

# 2. 基板を作成する
substrate = hfss.modeler.create_box(
    origin=[0, -SUB_W / 2, 0],
    sizes=[LINE_L, SUB_W, SUB_H],
    name="Substrate",
    material="alumina_96pct",
)

# 3. GND と信号線を作成する
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
airbox = hfss.modeler.create_box(
    origin=[0, -SUB_W / 2, SUB_H],
    sizes=[LINE_L, SUB_W, AIR_H],
    name="AirBox",
    material="vacuum",
)

# 5. Wave Portを作成する
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

# 6. 輻射境界を面ごとに割り当てる
rad_faces = []
for f in airbox.faces:
    x, y, z = f.center
    is_bottom = abs(z - SUB_H) < 1e-6
    is_port_end = abs(x - 0) < 1e-6 or abs(x - LINE_L) < 1e-6
    if not is_bottom and not is_port_end:
        rad_faces.append(f.id)
hfss.assign_radiation_boundary_to_faces(assignment=rad_faces, name="Rad_top_sides")

# 7. モデルを検証する
_, passed = hfss.validate_full_design()
if not passed:
    hfss.logger.warning("Design validation reported issues. Check the AEDT message manager.")

# 8. セットアップと周波数スイープを作成する
setup = hfss.create_setup(name="Setup1", Frequency="10GHz", MaxDeltaS=0.02, MaximumPasses=6)
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

# 10. S11・S21のレポートを作成する
hfss.create_scattering(plot="S Parameters")

# 11. GNDと信号線の表面にMag_Eのフィールドプロットを作成する
# InterpolatingスイープはSaveFields=Trueが既定でも各周波数のフィールドを保存しないため、
# setup にはアダプティブメッシュ結果（LastAdaptive）を指定する。
field_plot = hfss.post.create_fieldplot_surface(
    assignment=[gnd.name, line.name],
    quantity="Mag_E",
    setup="Setup1 : LastAdaptive",
    plot_name="MagE_Surface",
)

# 12. 対数スケールの凡例に切り替え、画像としてエクスポートする
# 導体端付近と平坦部で電界強度が桁違いになるため、線形スケールでは分布が見えにくい。
hfss.save_project()  # folder_settingsはAEDT側の保存済み設定を読み込むため、先に保存しておく。
folder_settings = field_plot.folder_settings
folder_settings.scale_settings.log = True
folder_settings.update()

hfss.save_project()
hfss.modeler.fit_all()  # 実行しないと、エクスポート画像が視野外で真っ黒になることがある。
field_plot.export_image(
    full_path=os.path.join(hfss.working_directory, "MagE_Surface_log.jpg"),
    width=1920,
    height=1080,
    orientation="isometric",
)

# 13. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
