"""演習1: ブスバー解析（縮退行列・キャパシタンス/インダクタンスレポート）。"""

from ansys.aedt.core import Q3d
from ansys.aedt.core.generic.settings import settings

AEDT_VERSION = "2026.1"

settings.release_on_exception = False

# TODO: 1. normalと同じ手順でモデルを作成する（Q3d起動、3本のブスバー＋基板、auto_identify_nets()、
#          各バーへのソース・シンク割り当て、セットアップ＋周波数スイープまで）
q3d = None

# TODO: 2. insert_reduced_matrix(operation_name="JoinSeries", assignment=["Sink1", "Source2"],
#          reduced_matrix="MR_Series", new_net_name="Series1") で縮退行列を作る

# TODO: 3. mr_series.add_operation(operation_type="JoinParallel", source_names=["Source1", "Source3"],
#          new_net_name="SeriesPar", new_source_name="src_par", new_sink_name="snk_par") を追加する

# TODO: 4. 解析を実行する

# TODO: 5. 元の行列の自己容量・相互容量をレポート化する
#          original_self = q3d.matrices[0].get_sources_for_plot(get_self_terms=True, get_mutual_terms=False)
#          original_mutual = q3d.matrices[0].get_sources_for_plot(get_self_terms=False, get_mutual_terms=True)
#          post.create_report(expressions=original_self, plot_name="Original, Self Capacitances")
#          post.create_report(expressions=original_mutual, context="Original",
#                              plot_name="Original, Mutual Capacitances")

# TODO: 6. 縮退行列の自己インダクタンス（ACL）をレポート化する
#          reduced_self = mr_series.get_sources_for_plot(get_self_terms=True, get_mutual_terms=False,
#                                                          category="ACL")
#          post.create_report(expressions=reduced_self, context="MR_Series",
#                              plot_name="MR_Series, Self Inductances")

# TODO: 7. post.create_fieldplot_surface(assignment=["Bar1", "Bar2", "Bar3"], quantity="Mag_SurfaceJac",
#          setup=f"{setup.name} : LastAdaptive", intrinsics={"Freq": "1GHz"},
#          plot_name="BusbarCurrentDensity") で、ブスバー表面の電流密度をフィールドプロットとして作成する

# TODO: 8. 保存して終了する
