"""演習2: 導波管インダクティブアイリスフィルタ（モデル作成〜解析実行）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Hfss を Modal ソリューションで起動する
hfss = None

# TODO: 2. 変数 wg_length="60mm", iris_thickness="2mm", iris_aperture="5mm" を定義する

WG_WIDTH = 22.86  # WG16 (WR-90) 内寸 [mm]
WG_HEIGHT = 10.16  # WG16 (WR-90) 内寸 [mm]

# TODO: 3. modeler.create_waveguide() で標準導波管（WR-90 / WG16）を作成する
#          （wg_direction_axis=2, wg_length="wg_length", create_sheets_on_openings=True）
#          戻り値は (waveguide, port1_sheet, port2_sheet) の3つ


def create_iris(z_position_expr: str, name: str):
    """導波管内寸全体を覆う銅板を作り、中央の開口部をくり抜いてインダクティブアイリスを作る。"""
    # TODO: 導波管内寸全体を覆う銅板（sizes=[WG_WIDTH, WG_HEIGHT, "iris_thickness"]）を作成する
    # TODO: 幅WG_WIDTH・高さ"iris_aperture"（中央配置）の穴を subtract でくり抜く
    return None


# TODO: 4. インダクティブアイリスを2枚作成する（導波管長の1/3, 2/3の位置）

# TODO: 4b. 導波管内寸と同じサイズの空気ボリューム（material="vacuum"）を作成し、
#           アイリス2枚を subtract（keep_originals=True）でくり抜く
#           （create_waveguide()が内部に作った空気領域はsubtract時に消費されてしまうため、
#           このステップを省略すると "At least one material assignment should have solve inside set!"
#           で解析が失敗する）

# TODO: 5. wave_port() で2つの開口部シートに Port1, Port2 を割り当てる

# TODO: 6. セットアップ "MySetup" を作成する（Frequency="10GHz", MaximumPasses=8）
#          周波数掃引 "Sweep1"（Interpolating, 8GHz-12GHz, SaveFields=True）を追加する

# TODO: 7. 解析を実行する

# TODO: 8. 保存して終了する（normalはここまで。ポスト処理はhard以降で追加する）
