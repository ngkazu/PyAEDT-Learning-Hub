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

# TODO: 1. Hfss を Terminal ソリューションで起動する
hfss = None

# TODO: 2. 1.normal/hfss/ex3_microstrip_line/solution.py と同じ手順で、
#          基板・GND・信号線・エアボックス・Wave Port・輻射境界・検証・Setup作成・解析までを行う

# TODO: 3. hfss.create_scattering(plot="S Parameters") でS11・S21のレポートを作成する

# TODO: 4. hfss.post.create_fieldplot_surface(assignment=[gnd.name, line.name], quantity="Mag_E",
#          setup="Setup1 : LastAdaptive", plot_name=...) でGND・信号線表面のMag_Eフィールドプロットを作成する

# TODO: 5. field_plot.folder_settings.scale_settings.log = True にしてから
#          folder_settings.update() を呼び、対数スケールの凡例に切り替える
#          （folder_settingsはプロジェクトを保存した後でないと正しく読み込まれない点に注意）

# TODO: 6. hfss.modeler.fit_all() を呼んでから、field_plot.export_image() で画像をエクスポートする

# TODO: 7. 保存して終了する
