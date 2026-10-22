"""演習3: コイル・コア電磁石 インダクタンスデータのPython後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.generic.settings import settings
from ansys.aedt.core.modules.boundary.maxwell_boundary import MatrixMagnetostatic, SourceMagnetostatic

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# TODO: 1. conditions.csv を読み込み、amp_turns / core_r_mm を取得する

# TODO: 2. 2.hard/maxwell_3d/ex03_coil_core_fieldplot/solution.py と同じ手順でモデルを作成し、
#          Matrix割り当て・Setup作成・解析を行う
#          （"amp_turns"と"core_r"はCSVから読み込んだ値を使う）
m3d = None

# TODO: 6. post.get_solution_data(expressions=["Matrix1.L(Winding1,Winding1)"]) で
#          自己インダクタンスのSolutionDataを取得し、get_expression_data(formula="real") で
#          値を取得する

# TODO: 7. amp_turns・core_r_mm・インダクタンスの値をCSVファイル（results_inductance.csv）に出力する

# TODO: 8. post.create_fieldplot_surface(assignment="Core", quantity="Mag_B",
#          setup=f"{setup.name} : LastAdaptive", plot_name=...) でコア表面のフィールドプロットを作成する

# TODO: 9. post.plot_field_from_fieldplot(plot_name=..., project_path=..., image_format="png",
#          view="isometric", log_scale=True, show=False) で、PyVistaによる画像を出力する

# TODO: 10. project_pathを渡さずshow=Trueで同じplot_field_from_fieldplot()を呼び、
#           インタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する

# TODO: 11. 保存して終了する
