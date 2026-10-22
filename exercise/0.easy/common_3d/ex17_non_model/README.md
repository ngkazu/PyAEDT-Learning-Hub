# 演習17: 非モデル（non_model）形状を作る

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/` で使う
`non_model=True`の基本操作だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- 通常のモデル形状（解析対象になるソリッド・シート）と、`non_model=True`で作成する
  「参照・評価専用」の形状の違いを理解する
- ポスト処理のレポート評価コンテキストなど、解析結果には影響させたくない補助形状の作り方を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動する。
2. `modeler.create_box(origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="ModelBox",
   material="aluminum")` で、通常のモデル形状（解析対象になるソリッド）を作成する。
3. `modeler.create_polyline(points=[[0, 0, 15], [10, 10, 15]], name="ReferenceLine",
   non_model=True)` で、評価・参照専用の補助ライン（解析対象には含まれない）を作成する。
4. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `non_model=True`で作成したオブジェクトは、AEDTのモデルツリー上では非表示またはグレーアウト表示
  になり、解析（メッシュ生成・ソルブ）の対象から除外される。
- 典型的な用途は、フィールドレポートの評価用ライン・ポイントなど、「物理的なモデルの一部ではないが、
  参照座標として形状を使いたい」場面。
- ほとんどの形状作成メソッド（`create_box()`、`create_cylinder()`、`create_polyline()`など）が
  `non_model`引数を持つ。

## 評価基準

- [ ] アプリケーションが起動し、通常のモデル形状（`ModelBox`）が作成されている
- [ ] `non_model=True`の補助ライン（`ReferenceLine`）が作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- AEDTのGUIでモデルツリーを開き、`ModelBox`と`ReferenceLine`の表示のされ方の違いを確認してください。
- 実際にレポート評価用のラインとして使われている様子を見たい場合は、
  [2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](../../../2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/)
  に進んでみてください。
