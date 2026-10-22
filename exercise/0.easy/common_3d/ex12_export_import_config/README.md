# 演習12: デザイン設定のJSON入出力（configurations.export_config→import_config）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。PyAEDTの設定ファイル（Configuration）機能
（`app.configurations.export_config()` / `import_config()`）を使ったJSON入出力を練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `app.configurations.export_config()` で、デザインの変数・材料などの設定をJSONファイルに書き出す
- `app.insert_design()` で同じプロジェクト内に新しいデザインを追加する
- `app.configurations.import_config()` で、JSONファイルから別デザインへ設定を読み込んで再現する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動する。
2. デザイン変数 `box_size = "10mm"` を定義し、それを使って
   `modeler.create_box(origin=[0, 0, 0], sizes=["box_size", "box_size", "box_size"], name="MyBox",
   material="aluminum")` で箱を作成する。
3. `app.configurations.export_config(config_file, overwrite=True)` で、現在のデザイン設定
   （変数・材料など）をJSONファイルにエクスポートする（`config_file` は
   `f"{app.working_directory}/my_config.json"` などとする）。
4. `app.insert_design(name="ImportedDesign")` で、同じプロジェクト内に新しいデザインを追加する
   （この時点では変数・形状は存在しない）。
5. `app.configurations.import_config(config_file)` で、エクスポートしたJSONファイルを
   新しいデザインにインポートする。
6. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `export_config()`/`import_config()` はEDB専用の機能ではなく、HFSS/Maxwell 3D/Icepak/Q3D Extractor/
  IcepakFEAなど3Dモデラー系アプリ共通で使える（`app.configurations`プロパティ経由）。
- エクスポートされるJSONの内容（変数・材料・境界条件・Setupなど、どの項目を含めるか）は
  `app.configurations.options` で調整できるが、本演習ではデフォルト設定のまま使う。
- `insert_design()` を呼ぶと、以降 `app` オブジェクトは新しいデザインを指すようになる
  （新しいアプリインスタンスを作り直す必要はない）。

## 評価基準

- [ ] アプリケーションが起動し、変数・箱が作成されている
- [ ] 設定がJSONファイルにエクスポートされている
- [ ] 新しいデザインが追加されている
- [ ] JSONファイルから新しいデザインに設定がインポートされている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- エクスポートされたJSONファイルの中身を開いて、変数や材料がどのように記述されているか確認してください。
- `app.configurations.options` の設定項目（`export_materials`、`export_variables`など）を調べ、
  エクスポートする内容を絞り込んでみてください。
