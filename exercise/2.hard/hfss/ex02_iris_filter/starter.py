"""演習2: 導波管インダクティブアイリスフィルタ（高度なポスト処理）。"""

from ansys.aedt.core import Hfss
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. Hfss を Modal ソリューションで起動する
hfss = None

# TODO: 2. 変数 wg_length, iris_thickness, iris_aperture を定義する

# TODO: 3. create_waveguide() で WG16 (WR-90) の導波管を作成する
#          （wg_direction_axis=2, create_sheets_on_openings=True）

# TODO: 4. 導波管内部にインダクティブアイリスを2枚作成する
#          （全面を覆う銅板を作成 -> 中央の開口部を subtract でくり抜く、を2箇所で繰り返す）
# TODO: 4b. 導波管内部と同じサイズの空気ボリューム（material="vacuum"）を作成し、
#          アイリスをツールに subtract（keep_originals=True）でくり抜く
#          （create_waveguideが作った空気領域はすでに消えているため、このステップが必須）
# TODO: 5. 開口部シートに Port1, Port2 の Wave Port を割り当てる

# TODO: 6. セットアップと SaveFields=True の周波数スイープを作成する
#          （Frequency, MaximumPasses は create_setup の引数として直接渡す）

# TODO: 7. 解析を実行する

# TODO: 8. create_scattering() で S11/S21 レポートを作成する
#          （hfss.excitation_names で実際の励振名一覧を取得して渡すと安全）

# TODO: 9. カットプレーン用の Plane を modeler.create_plane() で作成し、
#          post.create_fieldplot_cutplane() で電界のフィールドプロットを作成する
#          （CutPlaneは座標系上の平面を指す概念であり、シートオブジェクトでは代用できない）
#          setupは f"{setup.name} : LastAdaptive" を指定する（Interpolatingスイープは各周波数でフィールドを保存しないため）

# TODO: 10. 保存して終了する
