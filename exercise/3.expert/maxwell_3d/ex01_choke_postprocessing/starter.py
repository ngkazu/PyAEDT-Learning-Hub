"""演習1: コモンモードチョーク 損失・Bフィールドデータの Python 後処理（CSV入出力・PyVista可視化）。"""

import csv
import json
import tempfile
from pathlib import Path

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# TODO: 1. conditions.csv を読み込み、turns / frequency_khz を取得する

# TODO: 2. 1.normal/maxwell_3d/ex01_choke/solution.py と同じ手順でチョークを作成し、
#          Region作成・電流励振・Setup作成・解析を行う
#          （"Outer Winding"の"Turns"はCSVのturns、setup.props["Frequency"]はCSVのfrequency_khzを使う）
m3d = None

# TODO: 3. m3d.post.get_solution_data(expressions=["SolidLoss", "CoreLoss"],
#          setup_sweep_name=m3d.nominal_sweep, report_category="Fields") で
#          巻線のオーミック損失・コア損失のSolutionDataを取得する

# TODO: 4. get_expression_data(expression="SolidLoss", formula="real") / (expression="CoreLoss", ...) で
#          損失の値を取得する

# TODO: 5. turns・frequency_khz・損失の値をCSVファイル（results_losses.csv）に出力する

# TODO: 6. m3d.post.create_fieldplot_surface(assignment=core.name, quantity="Mag_B",
#          setup=f"{setup.name} : LastAdaptive", intrinsics={"Freq": f"{frequency_khz}kHz", "Phase": "0deg"},
#          plot_name=...) でコア表面のフィールドプロットを作成する

# TODO: 7. m3d.post.plot_field_from_fieldplot(plot_name=..., project_path=..., image_format="png",
#          view="isometric", log_scale=True, show=False) で、PyVistaによる画像を出力する

# TODO: 8. project_pathを渡さずshow=Trueで同じplot_field_from_fieldplot()を呼び、
#          インタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する

# TODO: 9. 保存して終了する
