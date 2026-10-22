# 演習3: コイル・コア電磁石（モデル作成〜解析実行）

**目安時間: 60分**

題材: サポート対応で作成されたMagnetostaticサンプル（`build_project40_magsta.py`）を着想元に、
Setup・材料設定などを整理して構成。円柱のみで構成されたシンプルな電磁石モデル。

> この演習は「コイル・コア電磁石シリーズ」の normal レベル。同じモデルにフィールドプロット等の
> ポスト処理を追加したものが [2.hard/maxwell_3d/ex03_coil_core_fieldplot/](../../../2.hard/maxwell_3d/ex03_coil_core_fieldplot/)、さらにPython側で
> CSV入出力・PyVista可視化を追加したものが [3.expert/maxwell_3d/ex03_coil_core_postprocessing/](../../../3.expert/maxwell_3d/ex03_coil_core_postprocessing/)
> にある。

> カスタム材料の作成だけを練習したい場合は
> [0.easy/common_3d/ex13_custom_material/](../../../0.easy/common_3d/ex13_custom_material/)、
> 断面切断＆ターミナル作成のパターンだけを練習したい場合は
> [0.easy/common_3d/ex14_section_terminal/](../../../0.easy/common_3d/ex14_section_terminal/) を先に確認するとよい。

## 学習目標

- Maxwell 3Dの`Magnetostatic`（静磁場）ソリューションタイプの使い方を学ぶ
- 比透磁率を指定した線形磁性材料を自作し、コアに割り当てる方法を学ぶ
- 円柱の`subtract()`で円環形状（コイル）を作るモデリング手法を学ぶ
- `assign_coil()`→`assign_winding()`→`add_winding_coils()` という、choke演習の`assign_current()`とは
  異なる「ワインディング」方式の励振割り当てパターンを学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Maxwell3d(solution_type="Magnetostatic", version=AEDT_VERSION, new_desktop=True,
   non_graphical=False)` で起動し、`m3d.modeler.model_units = "mm"` を設定する。
2. 磁性材料 `"core_steel"` を追加し、`conductivity = 2000000`、`permeability.value = 1000`
   （比透磁率1000の線形材料として簡略化）を設定する。
3. 寸法をデザイン変数として定義する。値は下表の通りでよい（`coil_ri`を`core_r`より大きくすることで、
   コイルとコアが非干渉になる）。

   | 変数 | 値 | 意味 |
   |---|---|---|
   | `core_r` | `10mm` | コア半径 |
   | `core_h` | `40mm` | コア高さ |
   | `coil_ri` | `15mm` | コイル内半径 |
   | `coil_ro` | `25mm` | コイル外半径 |
   | `coil_h` | `20mm` | コイル高さ |
   | `amp_turns` | `1000A` | 起磁力（アンペアターン） |
4. `create_cylinder()`でコア（Z軸中心の円柱）を作成する。
5. `create_cylinder()`で外円柱・内円柱を作り、`subtract()`で円環コイルを作成する。
6. `modeler.create_region()`で解析領域（Region）を作成する。
7. `modeler.section()`でコイルをZX平面で断面切断し、`separate_bodies()`/`delete()`で
   片側だけを残して電流を流す断面を作る。
8. `assign_coil()`で断面にコイルターミナル（Coil Terminal）を割り当てる。
9. `assign_winding()`でWinding（電流源）を作成し、`add_winding_coils()`でコイルターミナルを紐付ける。
10. セットアップ `"MySetup"` を作成し、`MaximumPasses=6`、`MinimumPasses=2`、
    `MinimumConvergedPasses=1`、`PercentError=1`、`PercentRefinement=30` を設定する。
11. `setup.analyze()` で解析を実行する。
12. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する（**フィールドプロット等の
    ポスト処理は行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `section()`の`plane`引数に使える正式な値は`"XY"`/`"YZ"`/`"ZX"`の3つ。`"XZ"`のような表記は
  正式な値として認識されない点に注意（内部実装では未知の値は`"ZX"`にフォールバックするため
  動作はするが、意図を明確にするため正式な値を使う）。
- コイルを`section()`で断面切断すると、円環形状は左右2枚の離れた面になる。
  `separate_bodies()`で分離してから、不要な片方を`delete()`する、という定型パターンを使う
  （TEAM7演習の非対称導体でも同じパターンを使った）。
- `assign_winding()`の`assignment`引数は`None`のままでよい。コイルとの紐付けは
  `add_winding_coils()`で後から行う。
- `is_solid=True`は、巻線ではなく単一のソリッド導体（円環コイル全体）に一様な電流が流れることを表す。

## 評価基準

- [ ] AEDTがMagnetostaticソリューションで起動し、コア（円柱）とコイル（円環）が作成されている
- [ ] 解析領域（Region）が作成されている
- [ ] コイルの断面にコイルターミナルとWindingが割り当てられている
- [ ] セットアップが作成され、解析がエラーなく完走している
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `amp_turns`や`core_r`などの寸法を変えて再解析し、結果がどう変わるか確認してください。
- コア内部の磁束密度分布を見たい場合は、このシリーズのhard
  （`2.hard/maxwell_3d/ex03_coil_core_fieldplot/`、準備中）に進んでみてください。

