"""演習1: ブスバー解析（モデル作成〜解析実行）。"""

from ansys.aedt.core import Q3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. Q3d を起動する
q3d = Q3d(
    design="Busbar",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
q3d.modeler.model_units = "mm"

# 2. 3本のブスバーを作成する（矩形断面の線状導体）
q3d.modeler.create_polyline(
    points=[[0, 0, 0], [-100, 0, 0]],
    name="Bar1",
    material="copper",
    xsection_type="Rectangle",
    xsection_width="5mm",
    xsection_height="1mm",
)
q3d.modeler.create_polyline(
    points=[[0, -15, 0], [-150, -15, 0]],
    name="Bar2",
    material="aluminum",
    xsection_type="Rectangle",
    xsection_width="5mm",
    xsection_height="1mm",
)
q3d.modeler.create_polyline(
    points=[[0, -30, 0], [-175, -30, 0], [-175, -10, 0]],
    name="Bar3",
    material="copper",
    xsection_type="Rectangle",
    xsection_width="5mm",
    xsection_height="1mm",
)

# 3. 基板を作成する
q3d.modeler.create_box(
    origin=[50, 30, -0.5],
    sizes=[-250, -100, -3],
    name="substrate",
    material="FR4_epoxy",
)

# 4. ネットを自動識別する
q3d.auto_identify_nets()

# 5. 各バーにソース・シンクを割り当てる
q3d.source(assignment="Bar1", direction=q3d.axis_directions.XPos, name="Source1")
q3d.sink(assignment="Bar1", direction=q3d.axis_directions.XNeg, name="Sink1")

q3d.source(assignment="Bar2", direction=q3d.axis_directions.XPos, name="Source2")
q3d.sink(assignment="Bar2", direction=q3d.axis_directions.XNeg, name="Sink2")

q3d.source(assignment="Bar3", direction=q3d.axis_directions.XPos, name="Source3")
q3d.sink(assignment="Bar3", direction=q3d.axis_directions.YPos, name="Sink3")

# 6. セットアップを作成する
setup = q3d.create_setup(name="MySetup", props={"AdaptiveFreq": "1000MHz"})

# 7. 周波数スイープを追加する
# Interpolatingスイープは各点を実解析せず補間するため SaveFields が常に False になり、
# hard以降でのマトリクスデータ取得・ポスト処理ができなくなる。Discrete + save_fields=True にしておく。
setup.create_linear_step_sweep(
    name="my_sweep",
    unit="GHz",
    start_frequency=0,
    stop_frequency=10,
    step_size=1,
    sweep_type="Discrete",
    save_fields=True,
)

# 8. 解析を実行する
q3d.analyze()

# 9. 保存して終了する
# normalはSetup作成→解析実行までで終了する（縮退行列・レポート作成はhard以降で追加するため、ここでは行わない）。
q3d.save_project()
q3d.release_desktop(close_projects=True, close_desktop=True)
