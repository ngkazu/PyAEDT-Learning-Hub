# 演習1: コモンモードチョーク（モデル作成〜解析実行）

**目安時間: 60分**

題材: `AEDT-AI-Assistant/examples/maxwell3d/choke.py`（`modeler.create_choke()` を使ったコモンモードチョーク作成例）を
着想元に、巻線構成を簡略化（3層3巻線→単層2巻線）して独自に作成。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex01_basic_operations/](../../../0.easy/common_3d/ex01_basic_operations/) を確認するとよい。
> `modeler.create_choke()` の基本操作だけを切り出した演習が
> [0.easy/common_3d/ex10_choke_geometry/](../../../0.easy/common_3d/ex10_choke_geometry/) にもある。
> 面の取得（`get_object_faces()`）だけを練習したい場合は
> [0.easy/common_3d/ex11_get_faces/](../../../0.easy/common_3d/ex11_get_faces/) を先に確認するとよい。
> この演習とは別の形式のJSON入出力（デザイン設定のエクスポート/インポート）を練習したい場合は
> [0.easy/common_3d/ex12_export_import_config/](../../../0.easy/common_3d/ex12_export_import_config/) も参考になる。

> この演習は「チョークシリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> [2.hard/maxwell_3d/ex01_choke_lossreport/](../../../2.hard/maxwell_3d/ex01_choke_lossreport/)、さらにPyVista/CSV入出力を追加したものが
> [3.expert/maxwell_3d/ex01_choke_postprocessing/](../../../3.expert/maxwell_3d/ex01_choke_postprocessing/) にある。

## 学習目標

- `modeler.create_choke()` 用のジオメトリパラメータ辞書（コア・巻線の形状定義）をJSON経由で渡す使い方を理解する
- `modeler.check_choke_values()` で辞書の整合性を事前チェックする
- 作成したチョークの巻線に対して、`assign_current()` で位相差のある電流励振（差動モード）を割り当てる
- Maxwell 3D の `EddyCurrent`（渦電流）ソルバーでSetup作成・解析実行までの流れを学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Maxwell3d(solution_type="EddyCurrent", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で
   起動し、`m3d.modeler.model_units = "mm"` を設定する。
2. チョークのジオメトリパラメータを表す `choke_descriptor` 辞書を定義する。値は下表の通りでよい
   （`modeler.check_choke_values()` のdocstringに載っているデフォルト例を元に、巻線数だけ1→2に変更したもの）。

   | キー | 値 |
   |---|---|
   | `"Number of Windings"` | `{"1": False, "2": True, "3": False, "4": False}`（巻線2本） |
   | `"Layer"` | `{"Simple": True, "Double": False, "Triple": False}`（単層） |
   | `"Layer Type"` | `{"Separate": True, "Linked": False}`（**単層の場合は必ず`Separate`**。下記の注意を参照） |
   | `"Similar Layer"` | `{"Similar": True, "Different": False}` |
   | `"Mode"` | `{"Differential": True, "Common": False}`（差動モード） |
   | `"Wire Section"` | `{"None": False, "Hexagon": False, "Octagon": True, "Circle": False}` |
   | `"Core"` | `{"Name": "Core", "Material": "ferrite", "Inner Radius": 11, "Outer Radius": 17, "Height": 7, "Chamfer": 0.8}` |
   | `"Outer Winding"` | `{"Name": "Winding", "Material": "copper", "Inner Radius": 12, "Outer Radius": 16, "Height": 8, "Wire Diameter": 1, "Turns": 10, "Coil Pit(deg)": 9, "Occupation(%)": 0}` |
   | `"Mid Winding"` | `{"Turns": 8, "Coil Pit(deg)": 0.1, "Occupation(%)": 0}`（単層では未使用だが、キー自体は必須） |
   | `"Inner Winding"` | `{"Turns": 12, "Coil Pit(deg)": 0.1, "Occupation(%)": 0}`（単層では未使用だが、キー自体は必須） |

   > **注意（はまりやすい点）**: `"Layer"` が `"Simple"`（単層）のとき、`"Layer Type"` を
   > `"Linked": True` にすると、内部で巻線オブジェクトではなく座標リストだけが返り、後続の
   > `set_crosssection_properties()` 呼び出しが失敗する。単層では必ず `"Separate": True` にすること。

3. 辞書を一時JSONファイルに書き出し、`modeler.check_choke_values(input_dir=choke_fn,
   create_another_file=False)` で整合性を確認したうえで、`modeler.create_choke(input_file=choke_fn)` で
   チョークを作成する。戻り値のリストから `core = list_object[1]`、`winding1 = list_object[2]`、
   `winding2 = list_object[3]` を取り出す（`winding1`/`winding2` は `[Object3d, 座標リスト]` の形）。
4. `modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=0)` で
   解析領域（Region）を作成する（**Regionがないと解析が失敗する**。-Z面は0%、それ以外の5面は100%のパディング）。
5. `modeler.get_object_faces(assignment=winding1[0].name)` で各巻線の両端面を取得し、
   `assign_current()` で巻線1本につき入口・出口の2面に電流励振（振幅1000A、`swap_direction`で
   向きを調整）を割り当てる。差動モードなので、巻線1は位相`"0deg"`、巻線2は位相`"180deg"`にする。
6. セットアップ `"MySetup"` を作成し、`setup.props["Frequency"] = "150kHz"` を設定する
   （EMIチョークの評価で一般的な周波数帯）。
7. `setup.analyze()` で解析を実行する。
8. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
   行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `create_choke()` はJSONファイルのパスを引数に取る仕様のため、辞書を直接渡すことはできない。
  `json.dump()` で一時ファイルに書き出してから渡す。
- チョーク周りには最初からエアボックスが存在しないため、`create_air_region()` で解析領域を
  明示的に作らないと解析エラーになる。`x_pos`/`y_pos`/`z_pos`/`x_neg`/`y_neg`/`z_neg` はそれぞれ+X/+Y/+Z/-X/-Y/-Z
  方向のパディング割合（%）を表す。
- 辞書のプライマリキー・セカンダリキーは固定（追加・削除不可）。変更してよいのは値だけ。
  `"Layer Type"` の `"Linked"` は `"Layer"` が `Double`/`Triple`（複数層）のときに意味を持つ設定で、
  `Simple`（単層）の場合は `"Separate": True` にする。
- `create_choke()` の戻り値の構造は巻線数・層構成によって変わる。本演習の設定（Simple層・2巻線・
  Differential）では `[success, core, [winding1_obj, points1], [winding2_obj, points2]]` という
  固定の形になる。
- `get_object_faces()` が返す面のリストのうち、`[1]`番目を電流の入口、`[0]`番目を出口として使う
  （`swap_direction` で電流の向きを調整している）。

## 評価基準

- [ ] AEDTがEddyCurrentソリューションで起動し、チョーク（コア+2巻線）が作成されている
- [ ] 解析領域（Region、-Z面0%・それ以外100%）が作成されている
- [ ] 2つの巻線それぞれに、位相が180度ずれた電流励振が割り当てられている
- [ ] セットアップ（周波数150kHz）が作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `"Number of Windings"` を `"3"` や `"4"` に変更し、巻線数を増やすとモデル・励振がどう変わるか確認してください。
- 巻線に生じる損失やコア内の磁束密度分布を確認したい場合は、このシリーズのhard
  （[2.hard/maxwell_3d/ex01_choke_lossreport/](../../../2.hard/maxwell_3d/ex01_choke_lossreport/)）に進んでみてください。
