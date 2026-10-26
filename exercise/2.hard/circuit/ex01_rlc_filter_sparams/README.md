# 演習1: RLCローパスフィルタのSパラメータ解析（AEDT内ポスト処理）

**目安時間: 90分**

題材: `1.normal/circuit/ex01_rlc_transient/`（RLC直列回路）と同じ R/L/C を、2ポートの
ローパスフィルタとして構成し、周波数ドメインで S パラメータを解析する。

> この演習は「RLC回路シリーズ」の hard レベル。normal（過渡解析）で作った R/L/C を
> 2ポート化し、**周波数特性（S パラメータ）** を見る形に発展させる。さらに Python 後処理
> （CSV入出力・matplotlib）を追加したものが `3.expert/circuit/ex01_rlc_filter_postprocessing/`。

## 学習目標

- 回路に入出力インターフェースポート（`create_interface_port`）を配置する
- 周波数ドメイン解析（LNA, `NexximLNA`）のセットアップと周波数スイープを作成する
- S パラメータ（S21 挿入損失・S11 反射）の AEDT レポートを作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Circuit(design="RLC_LowpassFilter", ...)` で起動する。
2. R1（50ohm, `[0.02,0]`）、L1（10nH, `[0.04,0]`）、C1（1nF, `[0.06,0]`）を配置する
   （この L/C だとカットオフ約 2.4GHz のローパスになる）。
3. R→L を直列に配線する（L の右端が出力ノードになる）。
4. 入力 `Port1`（`[0.0,0.0]`）と出力 `Port2`（`[0.08,0.0]`）を `create_interface_port` で配置する。
5. 接地 `create_gnd(location=[0.06,-0.03])` を配置する。
6. 次の4本を配線する:
   - `Port1` → R左
   - L右 → C左
   - L右 → `Port2`
   - C右 → GND
   （R-L が直列、C が出力ノードと GND の間に入る → L型ローパス構成）
7. `cir.create_setup(name="LNA", setup_type="NexximLNA")` で周波数ドメイン解析を作成し、
   `setup.add_sweep_count(sweep_variable="Freq", start=0.01, stop=5, count=401, units="GHz", count_type="Linear")`
   で 0.01〜5GHz を401点スイープする。
8. `setup.analyze()` で解析を実行する。
9. **AEDT内ポスト処理**として、S21（`dB(S(Port2,Port1))`）と S11（`dB(S(Port1,Port1))`）の
   レポートを `cir.post.create_report(..., domain="Sweep")` で作成する。
10. プロジェクトを保存し、`cir.release_desktop()` で終了する。

## ヒント

- インターフェースポートは `sch.create_interface_port(name=..., location=[x, y])`。
  配置した端子のネットがそのままポート名（`Port1`/`Port2`）になる。
- 周波数ドメイン解析のセットアップ種別は `setup_type="NexximLNA"`。周波数スイープは
  `add_sweep_count`（点数指定）または `add_sweep_step`（ステップ指定）で追加する。
- S パラメータのトレース式はポート名を使って `S(出力ポート, 入力ポート)` と書く
  （例: `dB(S(Port2,Port1))` = S21 を dB 表示）。`create_report` の `domain` は周波数掃引なので
  `"Sweep"` を指定する。
- レポートが正しく作れたかは `rep = cir.post.create_report(...)` の戻り値（真偽）と、
  GUI のレポート欄で確認できる。

## 評価基準

- [ ] 2ポート（Port1/Port2）の RLC ローパスフィルタが配線されている
- [ ] NexximLNA セットアップと 0.1〜20GHz・201点の周波数スイープが作成されている
- [ ] 解析がエラーなく完走している
- [ ] S21・S11 のレポートが作成されている（`.aedt` に保存されている）

## 発展課題（任意）

- C や L の値を変えて、カットオフ周波数（S21 が −3dB になる周波数）がどう動くか観察してください。
- S パラメータデータを Python で取り出してカットオフ周波数を自動算出したい場合は、このシリーズの
  expert（`3.expert/circuit/ex01_rlc_filter_postprocessing/`）に進んでください。
