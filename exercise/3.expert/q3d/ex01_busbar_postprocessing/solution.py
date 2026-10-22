"""演習1: ブスバー解析 容量・インダクタンスデータのPython後処理（CSV入出力・PyVista可視化）。"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ansys.aedt.core import Q3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

script_dir = Path(__file__).parent

# 1. conditions.csv を読み込む
with open(script_dir / "conditions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    row = next(reader)
    bar1_length_mm = float(row["bar1_length_mm"])

# 2. hardと同じ手順でモデルを作成する（Bar1の経路終点のみCSVの値を使う）
q3d = Q3d(
    design="Busbar",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
q3d.modeler.model_units = "mm"

q3d.modeler.create_polyline(
    points=[[0, 0, 0], [-bar1_length_mm, 0, 0]],
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

q3d.modeler.create_box(
    origin=[50, 30, -0.5],
    sizes=[-250, -100, -3],
    name="substrate",
    material="FR4_epoxy",
)

q3d.auto_identify_nets()

q3d.source(assignment="Bar1", direction=q3d.axis_directions.XPos, name="Source1")
q3d.sink(assignment="Bar1", direction=q3d.axis_directions.XNeg, name="Sink1")

q3d.source(assignment="Bar2", direction=q3d.axis_directions.XPos, name="Source2")
q3d.sink(assignment="Bar2", direction=q3d.axis_directions.XNeg, name="Sink2")

q3d.source(assignment="Bar3", direction=q3d.axis_directions.XPos, name="Source3")
q3d.sink(assignment="Bar3", direction=q3d.axis_directions.YPos, name="Sink3")

setup = q3d.create_setup(name="MySetup", props={"AdaptiveFreq": "1000MHz"})
setup.create_linear_step_sweep(
    name="my_sweep",
    unit="GHz",
    start_frequency=0,
    stop_frequency=10,
    step_size=1,
    sweep_type="Discrete",
    save_fields=True,
)

mr_series = q3d.insert_reduced_matrix(
    operation_name="JoinSeries",
    assignment=["Sink1", "Source2"],
    reduced_matrix="MR_Series",
    new_net_name="Series1",
)
mr_series.add_operation(
    operation_type="JoinParallel",
    source_names=["Source1", "Source3"],
    new_net_name="SeriesPar",
    new_source_name="src_par",
    new_sink_name="snk_par",
)

# 3. 解析を実行する
q3d.analyze()

# 4. ブスバー表面の電流密度（AC Surface Current Density）をフィールドプロットとして作成する
q3d.post.create_fieldplot_surface(
    assignment=["Bar1", "Bar2", "Bar3"],
    quantity="Mag_SurfaceJac",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": "1GHz"},
    plot_name="BusbarCurrentDensity",
)

# 5. 自己容量・自己インダクタンスの式リストを用意する
original_self = q3d.matrices[0].get_sources_for_plot(get_self_terms=True, get_mutual_terms=False)
reduced_self = mr_series.get_sources_for_plot(get_self_terms=True, get_mutual_terms=False, category="ACL")

# 6. SolutionDataを取得する
original_data = q3d.post.get_solution_data(expressions=original_self, context="Original")
reduced_data = q3d.post.get_solution_data(expressions=reduced_self, context="MR_Series")

# 7. 周波数・各値をNumPy配列として取り出す
freq = None
capacitance_columns = {}
for expr in original_self:
    x, y = original_data.get_expression_data(expression=expr, formula="mag")
    if freq is None:
        freq = x
    capacitance_columns[expr] = y

inductance_columns = {}
for expr in reduced_self:
    x, y = reduced_data.get_expression_data(expression=expr, formula="mag")
    inductance_columns[expr] = y

# 8. CSVファイルに出力する
with open(script_dir / "results_q3d_busbar.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    header = ["freq_ghz"] + list(capacitance_columns.keys()) + list(inductance_columns.keys())
    writer.writerow(header)
    columns = list(capacitance_columns.values()) + list(inductance_columns.values())
    for row_values in zip(freq, *columns):
        writer.writerow(row_values)

# 9. 周波数特性をグラフ化する
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
for expr, values in capacitance_columns.items():
    ax1.plot(freq, values, label=expr)
ax1.set_xlabel("Frequency [GHz]")
ax1.set_ylabel("Capacitance [F]")
ax1.set_title("Self Capacitance (Original Matrix)")
ax1.legend()

for expr, values in inductance_columns.items():
    ax2.plot(freq, values, label=expr)
ax2.set_xlabel("Frequency [GHz]")
ax2.set_ylabel("ACL [H]")
ax2.set_title("Self Inductance (Reduced Matrix)")
ax2.legend()

fig.tight_layout()
fig.savefig(script_dir / "results_q3d_busbar.png")
plt.close(fig)

# 10. 電流密度コンター図をPyVista画像として出力する
q3d.post.plot_field_from_fieldplot(
    plot_name="BusbarCurrentDensity",
    project_path=str(script_dir),
    image_format="png",
    view="isometric",
    show=False,
)

# 11. 同じフィールドプロットをインタラクティブなPyVistaウィンドウで表示する
q3d.post.plot_field_from_fieldplot(plot_name="BusbarCurrentDensity", view="isometric", show=True)

# 12. 保存して終了する
q3d.save_project()
q3d.release_desktop(close_projects=True, close_desktop=True)
