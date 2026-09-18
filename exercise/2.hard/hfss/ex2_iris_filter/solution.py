"""演習2: 導波管インダクティブアイリスフィルタ（高度なポスト処理）。

未検証事項: このスクリプトはローカルのpyaedtソースでAPIシグネチャを確認して作成したが、
実際のAEDT環境での実行検証はまだ行っていない（docs/review-checklist.md に沿って要検証）。
"""

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

# 2. 変数を定義する
hfss["wg_length"] = "60mm"
hfss["iris_thickness"] = "2mm"
hfss["iris_aperture"] = "5mm"

WG_WIDTH = 22.86  # WG16 (WR-90) 内寸 [mm]
WG_HEIGHT = 10.16  # WG16 (WR-90) 内寸 [mm]

# 3. 標準導波管（WR-90）を作成する
waveguide, port1_sheet, port2_sheet = hfss.modeler.create_waveguide(
    origin=[0, 0, 0],
    wg_direction_axis=2,
    wgmodel="WG16",
    wg_length="wg_length",
    create_sheets_on_openings=True,
    name="Waveguide",
)


def create_iris(z_position_expr: str, name: str):
    """導波管内寸全体を覆う銅板を作り、中央の開口部をくり抜いてインダクティブアイリスを作る。"""
    full_plate = hfss.modeler.create_box(
        origin=[0, 0, z_position_expr],
        sizes=[WG_WIDTH, WG_HEIGHT, "iris_thickness"],
        name=name,
        material="copper",
    )
    aperture = hfss.modeler.create_box(
        origin=[0, f"({WG_HEIGHT}mm-iris_aperture)/2", z_position_expr],
        sizes=[WG_WIDTH, "iris_aperture", "iris_thickness"],
        name=f"{name}_aperture",
    )
    hfss.modeler.subtract(full_plate, aperture, keep_originals=False)
    return full_plate


# 4. インダクティブアイリスを2枚作成する（導波管長の1/3, 2/3の位置）
iris1 = create_iris("wg_length/3", "Iris1")
iris2 = create_iris("2*wg_length/3", "Iris2")

# 4b. 導波管内部の空気領域を明示的に作成する
# create_waveguide() が内部で作った空気領域は subtract 時に消費されてしまい、
# モデル内に Solve Inside=True の実体が残っていない（アイリスの金属はSolve Inside=False）。
# そのままだと "At least one material assignment should have solve inside set!" で解析が失敗するため、
# 導波管内寸と同じサイズの空気ボリュームを作り直し、アイリスと重ならないよう subtract でくり抜く。
air_region = hfss.modeler.create_box(
    origin=[0, 0, 0],
    sizes=[WG_WIDTH, WG_HEIGHT, "wg_length"],
    name="AirRegion",
    material="vacuum",
)
hfss.modeler.subtract(air_region, [iris1, iris2], keep_originals=True)

# 5. Wave Port を割り当てる
hfss.wave_port(assignment=port1_sheet.name, name="Port1")
hfss.wave_port(assignment=port2_sheet.name, name="Port2")

# 6. セットアップと周波数掃引を作成する
# props経由での事後変更ではなく、create_setup の引数として直接渡す（native APIのプロパティ名）。
setup = hfss.create_setup(name="MySetup", Frequency="10GHz", MaximumPasses=8)

setup.add_sweep(
    name="Sweep1",
    sweep_type="Interpolating",
    RangeStart="8GHz",
    RangeEnd="12GHz",
    SaveFields=True,
)

# 7. 解析を実行する
setup.analyze()

# 8. S11/S21 レポートを作成する
# ポート名は自分で付けた名前（"Port1"/"Port2"）ではなく、実際の励振名（モード接尾辞付きの場合がある）を
# hfss.excitation_names から取得する。sweep省略時は nominal_sweep が自動的に使われる。
excitations = hfss.excitation_names
hfss.create_scattering(
    plot="S Parameters",
    ports=excitations,
    ports_excited=[excitations[0]] * len(excitations),
)

# 9. 電界分布のフィールドプロットを作成する（導波管中心を通るXZ平面）
# AEDTの「CutPlane」は座標系上の平面（基準点+法線ベクトル）を指す概念なので、
# シートオブジェクトではなく modeler.create_plane() で作成した Plane オブジェクトを渡す。
cut_plane = hfss.modeler.create_plane(
    name="CutPlane_XZ",
    plane_base_x="0mm",
    plane_base_y=f"{WG_HEIGHT / 2}mm",
    plane_base_z="0mm",
    plane_normal_x="0mm",
    plane_normal_y="1mm",
    plane_normal_z="0mm",
)
hfss.post.create_fieldplot_cutplane(
    assignment=[cut_plane.name],
    quantity="Mag_E",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": "10GHz"},
    plot_name="E_Field_XZ",
)

# 10. 保存して終了する
hfss.save_project()
hfss.release_desktop(close_projects=True, close_desktop=True)
