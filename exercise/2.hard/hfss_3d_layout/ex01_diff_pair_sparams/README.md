# 演習1: 差動ペア伝送線路（HFSS 3D Layout, 差動Sパラメータ解析・AEDT内ポスト処理）

**目安時間: 90分**

題材: `1.normal/hfss_3d_layout/ex01_diff_pair/`（差動ペア伝送線路）と同じストリップラインモデルに、
入出力の P/N ポートを**差動ペア**として設定し、差動Sパラメータ（Sdd21・Sdd11）のレポートを追加する。

> この演習は「差動ペア伝送線路シリーズ」の hard レベル。normal（モデル作成〜解析実行）で作った
> 構造に、**差動ペア設定** と **AEDT内ポスト処理（Sdd21/Sdd11レポート）** を追加する。
> さらに Python 後処理（CSV入出力・matplotlib・Touchstone出力）を追加したものが
> `3.expert/hfss_3d_layout/ex01_diff_pair_postprocessing/`。

## 使用するパッケージ

normal と同じく、ジオメトリ作成を **PyEDB**（`from pyedb import Edb`）で行い、解析を
**PyAEDT の `Hfss3dLayout`** で行う。

## 学習目標

- 入出力それぞれの P/N ポートを `set_differential_pair()` で差動ペアとして登録する
- 差動モード・コモンモードのインピーダンス（100Ω / 25Ω）を指定する
- 差動Sパラメータ（Sdd21: 挿入損失、Sdd11: 反射）の AEDT 内レポートを作成する
  （`context="Differential Pairs"` が必須）

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください
（モデル作成部分は normal 課題と同じ。迷ったら `1.normal/hfss_3d_layout/ex01_diff_pair/solution.py`
を参考にしてよい）。

1. normal と同じ手順で EDB を作る（スタックアップ・差動ペア2本・GNDプレーン・vertical gap ポート4つ:
   `P_in`, `P_out`, `N_in`, `N_out`）。
2. `Hfss3dLayout` で開き、`create_setup(name="MySetup")` と周波数スイープ（0〜20GHz・201点・
   Interpolating）を作成する。
3. 入力側 `P_in`/`N_in` を差動ペア `Diff_In`（コモンモード名 `Comm_In`）として
   `set_differential_pair(assignment="P_in", reference="N_in", ...)` で登録する。
   出力側 `P_out`/`N_out` も同様に `Diff_Out`/`Comm_Out` として登録する
   （差動インピーダンス100Ω、コモンモードインピーダンス25Ω）。
4. `h3d.analyze_setup(name="MySetup")` で解析を実行する。
5. **AEDT内ポスト処理**として、Sdd21（`dB(S(Diff_Out,Diff_In))`）と
   Sdd11（`dB(S(Diff_In,Diff_In))`）のレポートを `context="Differential Pairs"` 付きで作成する。
6. プロジェクトを保存し、`h3d.release_desktop()` で終了する。

## ヒント

- `set_differential_pair(assignment=正側ポート名, reference=負側ポート名, differential_mode=差動モード名,
  common_mode=コモンモード名, differential_reference=100, common_reference=25)`。戻り値は成功時 `True`。
- 差動ペア名の一覧は `h3d.get_differential_pairs()` で確認できる
  （例: `['Diff_In', 'Diff_Out']`）。
- 差動Sパラメータの式は `S(出力側ペア名, 入力側ペア名)`（例: `S(Diff_Out,Diff_In)` = Sdd21）。
  反射は同じペア名同士（例: `S(Diff_In,Diff_In)` = Sdd11）。
- **`create_report()` に `context="Differential Pairs"` を指定しないと、式の文法が正しくても
  プロットが空になる。** 単一導体のSパラメータ（normalで使うような `S(P1,P1)` 形式）と混同しないこと。
- `setup_sweep_name` は `f"{setup.name} : {sweep.name}"` の形式。`create_linear_count_sweep` の
  **戻り値**から `.name` を取ること（`setup.sweeps[0]` は再取得タイミングによって空のことがある）。

## 評価基準

- [ ] normal と同じ4ポート（P_in/P_out/N_in/N_out）のモデルが作成されている
- [ ] 差動ペア `Diff_In`（P_in/N_in）と `Diff_Out`（P_out/N_out）が設定されている
      （`h3d.get_differential_pairs()` で確認できる）
- [ ] 解析がエラーなく完走している
- [ ] Sdd21・Sdd11 のレポートが `context="Differential Pairs"` 付きで作成されている
      （`.aedt` に保存されている）

## 発展課題（任意）

- コモンモードSパラメータ（Scc21など）や、モード変換（Sdc21, Scd21）もレポートに追加してみてください。
- 差動Sパラメータデータを Python で取り出して挿入損失の傾向を自動評価したい場合は、このシリーズの
  expert（`3.expert/hfss_3d_layout/ex01_diff_pair_postprocessing/`）に進んでください。
