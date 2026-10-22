# 演習2: TEAM7非対称導体（モデル作成〜解析実行）

**目安時間: 60分**

題材: `AEDT-AI-Assistant/examples/maxwell3d/asymmetric_conductor.py`（COMPUMAG TEAM7問題「非対称導体の渦電流解析」の
実装例）を着想元に、公開実測データとの比較・フィールド評価（ポスト処理）部分を除いて構成。

> この演習は「TEAM7非対称導体シリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> [2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](../../../2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/)、さらにPython側で公開実測データと比較したものが
> [3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/](../../../3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/) にある。

> カスタム材料の作成だけを練習したい場合は
> [0.easy/common_3d/ex13_custom_material/](../../../0.easy/common_3d/ex13_custom_material/)、
> 断面切断＆ターミナル作成のパターンだけを練習したい場合は
> [0.easy/common_3d/ex14_section_terminal/](../../../0.easy/common_3d/ex14_section_terminal/)、
> ポリラインの回転複製だけを練習したい場合は
> [0.easy/common_3d/ex15_polyline_duplicate/](../../../0.easy/common_3d/ex15_polyline_duplicate/)、
> ローカル座標系の作成だけを練習したい場合は
> [0.easy/common_3d/ex16_local_coordinate_system/](../../../0.easy/common_3d/ex16_local_coordinate_system/)
> を先に確認するとよい。

## 学習目標

- **TEAM7問題**（COMPUMAG国際ワークショップが策定した渦電流ソルバー検証用ベンチマーク問題）のモデル構成を理解する
- `modeler.create_polyline()` でポリライン断面をスイープし、`duplicate_around_axis()` で回転複製・`unite()` で
  結合する、円環状コイルのモデリング手法を学ぶ
- `modeler.section()`/`separate_bodies()`/`delete()` を使った「断面を切って半分を削除しターミナルを作る」という、
  ソリッド導体への電流励振の定型パターンを学ぶ
- `eddy_effects_on()` で、オブジェクトごとに渦電流・変位電流の有無を設定する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください
（コイルの寸法定義部分は固定値なので変更不要です）。

1. `Maxwell3d(solution_type="EddyCurrent", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で
   起動し、`m3d.modeler.model_units = "mm"` を設定する。
2. セットアップ `"Setup1"` を作成し、`setup.props["Frequency"] = "200Hz"` を設定する。
3. `modeler.create_coordinate_system()` でコイル用のローカル座標系を作り、`create_polyline()` で
   4分の1コイル形状を描画、`set_crosssection_properties()` で断面（矩形）を設定する。
   `duplicate_around_axis()` で90度ずつ回転複製（4つ）し、`unite()` で結合して全体のコイルを作る。
4. コイルに銅材料を割り当て（`assign_material()`）、`solve_inside()` で内部の電磁界解を有効にする。
5. `modeler.section()`/`separate_bodies()`/`delete()` で、コイルの断面を切って電流励振用のターミナル面を作る。
6. デザイン変数 `Coil_Excitation = "2742A"` を定義し、`assign_current(solid=False)` でターミナル面に
   電流励振を割り当てる。
7. アルミ板用の専用材料（`team7_aluminium`、導電率 `3.526e7`）を追加する。
8. 中央に矩形の穴が開いたアルミ板を、2つの箱の `subtract()` で作成する。
9. `modeler.create_air_region()` で解析領域（Region）を作成する。
10. `eddy_effects_on()` で、コイル側は渦電流を無効、板側は変位電流を無効にする。
11. `setup.analyze()` で解析を実行する。
12. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する（**$B_z$の評価やレポート作成は
    行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- コイルは「4分の1形状を描いて90度ずつ回転複製し結合する」ことで円環状の立体を作る、という
  TEAM7特有のモデリング手法を使う。寸法定義（`coil_external`等）はTEAM7の公式図面に基づく固定値なので
  変更する必要はない。
- `duplicate_around_axis()` の `axis="Global"` は、直前に作成したローカル座標系（`Coil_CS`）の
  Z軸を基準に回転複製する際の指定方法（参考実装通りの値をそのまま使う）。
- `section()` でオブジェクトを平面で切ると `<元の名前>_Section1` のような名前の新しいオブジェクトが
  作られる。`separate_bodies()` で分離された片方を `delete()` で消すことで、電流が流れ込む
  ターミナル面（ソリッドの断面）を作る、という定型パターン。
- TEAM7問題の詳細は
  [公式PDF](https://www.compumag.org/wp/wp-content/uploads/2018/06/problem7.pdf) を参照（任意）。

## 評価基準

- [ ] AEDTがEddyCurrentソリューションで起動し、円環状コイル・穴あきアルミ板が作成されている
- [ ] コイルに電流励振（`Coil_Excitation = 2742A`）が割り当てられている
- [ ] 解析領域（Region）が作成されている
- [ ] 渦電流・変位電流の設定（コイル側無効・板側無効）がされている
- [ ] セットアップ（周波数200Hz）が作成され、解析がエラーなく完走している
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `$B_z$`（磁束密度Z成分）を評価するラインや、実測値との比較を行いたい場合は、このシリーズのhard
  （`2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/`、準備中）に進んでみてください。
