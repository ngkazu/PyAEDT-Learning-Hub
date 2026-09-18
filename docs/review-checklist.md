# レビュー・品質チェックリスト

課題（README/starter.py/solution.py の3点セット）を作成・レビューする際の共通チェック項目。
各課題の README.md の「評価基準」はこのリストをベースに、その課題固有の項目を追加する。

## 実行・環境

- [ ] `solution.py` がエラーなく最後まで実行でき、AEDTプロジェクト（`.aedt`）が保存される
- [ ] `AEDT_VERSION` 変数など、環境依存の値が冒頭にまとめられている
- [ ] スクリプト終了時に `release_desktop()`（または `Edb` の場合は適切な `close()`）が呼ばれ、
      AEDTプロセス・ライセンスが正しく解放される
- [ ] `starter.py` は `get_errors` 等で Python構文エラーがないことを確認済み（`# TODO` 部分は未実装でよい）

## 内容

- [ ] 要求された境界条件・励振・回路要素が意図した通りに割り当てられている（GUIで確認）
- [ ] 要求されたレポート・後処理結果が作成され、妥当な値になっている
- [ ] 難易度基準（`docs/difficulty-criteria.md`）に沿った内容になっている
  （例: normalで連成解析を使っていないか、hard/expertで扱う内容が混在していないか）
- [ ] 公式サンプル（examples.aedt.docs.pyansys.com）のコードを丸写ししていない
      （着想元として参照した場合でも、独自の実装になっている）

## フォーマット・書式

- [ ] `docs/exercise-template.md` の必須セクション（タイトル/目安時間/題材/学習目標/課題/ヒント/評価基準/発展課題）
      がすべて含まれている
- [ ] `README.md` / `starter.py` / `solution.py` の日本語ドキュメント・コメントが日本語で書かれている
      （コード・API名・引数名・識別子・ファイルパスは英語のまま）
- [ ] `common_3d` / `common_2d` / `common_circuit` の課題は、`docs/app-selection.md` を参照する形になっており、
      対応表を課題内に重複記載していない
- [ ] 製品名の表記が `docs/app-selection.md` の表示名と統一されている（例: 「Q3D」ではなく「Q3D Extractor」）

## 進捗管理

- [ ] `docs/roadmap/coverage.md` の該当セルのステータスを更新した（未着手 → 下書き → レビュー中 → 完了）
