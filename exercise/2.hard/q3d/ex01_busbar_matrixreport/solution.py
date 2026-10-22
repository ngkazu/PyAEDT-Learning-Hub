"""演習1: ブスバー解析（縮退行列・キャパシタンス/インダクタンスレポート）。"""

from ansys.aedt.core import Q3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# 1. normalと同じ手順でモデルを作成する
q3d = Q3d(
    design="Busbar",
    version=AEDT_VERSION,
    new_desktop=True,
    non_graphical=False,
)
q3d.modeler.model_units = "mm"

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

# 2. Bar1とBar2を直列結合した縮退行列を作る
mr_series = q3d.insert_reduced_matrix(
    operation_name="JoinSeries",
    assignment=["Sink1", "Source2"],
    reduced_matrix="MR_Series",
    new_net_name="Series1",
)

# 3. Bar3を並列結合として追加する
mr_series.add_operation(
    operation_type="JoinParallel",
    source_names=["Source1", "Source3"],
    new_net_name="SeriesPar",
    new_source_name="src_par",
    new_sink_name="snk_par",
)

# 4. 解析を実行する
q3d.analyze()

# 5. 元の行列（Original）の自己容量・相互容量をレポート化する
original_self = q3d.matrices[0].get_sources_for_plot(get_self_terms=True, get_mutual_terms=False)
original_mutual = q3d.matrices[0].get_sources_for_plot(get_self_terms=False, get_mutual_terms=True)
q3d.post.create_report(expressions=original_self, plot_name="Original, Self Capacitances")
q3d.post.create_report(
    expressions=original_mutual,
    context="Original",
    plot_name="Original, Mutual Capacitances",
)

# 6. 縮退行列（MR_Series）の自己インダクタンス（ACL）をレポート化する
reduced_self = mr_series.get_sources_for_plot(get_self_terms=True, get_mutual_terms=False, category="ACL")
q3d.post.create_report(
    expressions=reduced_self,
    context="MR_Series",
    plot_name="MR_Series, Self Inductances",
)

# 7. ブスバー表面の電流密度（AC Surface Current Density）をフィールドプロットとして作成する
q3d.post.create_fieldplot_surface(
    assignment=["Bar1", "Bar2", "Bar3"],
    quantity="Mag_SurfaceJac",
    setup=f"{setup.name} : LastAdaptive",
    intrinsics={"Freq": "1GHz"},
    plot_name="BusbarCurrentDensity",
)

# 8. 保存して終了する
q3d.save_project()
q3d.release_desktop(close_projects=True, close_desktop=True)
