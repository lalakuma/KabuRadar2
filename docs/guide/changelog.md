# 変更履歴メモ

リファクタリング・整理の要点です（詳細は git log を参照）。

## 2026-05 無料クラウド（GitHub Actions）

- `data/kaburadar.db` を Git LFS でリポジトリ管理可能に
- `.github/workflows/daily-screening.yml` … 平日 16:00 JST に解析 + push
- `docs/guide/cloud.md` を追加

## 2026-05 すぐ効く改善

- `publish --push` のブランチを `.env` / git 自動検出に変更
- 解析完了時に `enabled/written/skipped` をコンソール表示
- 取説に Windows 11 タスクスケジューラ手順、LINE 設定手順を追記
- `development.md` の拡張候補を現状に合わせて更新

## 2026-05 Linux 対応

- `sh/` ランチャー、`Makefile`、`docs/guide/linux.md`
- `config_lo.ini` のパスを `/` 表記に統一（Windows でも可）
- `scheduling/launcher` が OS に応じて bat / sh を選択
- CSV を **UTF-8 BOM**（`utf-8-sig`）に統一。読込は旧 cp932 もフォールバック

## 2026-05 個人運用向け

- LINE: `--notify` / `screening_notify.bat` / 集計 CSV から上位銘柄を送信
- `healthcheck.bat` … 設定・DB・CLI の確認
- 統合テスト: 最小 SQLite で `backtst_proc` を検証

## 2026-05 品質向上

- GitHub Actions **CI**（`pytest`）を追加
- `pipeline/analyze.run()` が失敗時に非ゼロ終了コードを返す（1=出力なし, 2=集計なし）
- `publish` が集計データ未変更時は `docs/data.json` を更新しない（無意味 commit 抑制）
- テスト追加（終了コード・RSI・publish 差分・パッケージ import）

## 2026-05 取扱説明書

- `docs/guide/manual.md` を追加（利用者向けの全体ガイド）

## 2026-05 機能ブロック構成

- `settings` / `domain` / `data` / `strategy` / `pipeline` / `market_data` / `publishing` / `scheduling` / `notifications` に分割
- `analysis/` は後方互換 import のみ（実装は上記パッケージへ移動）
- `legacy/`・`tasks/` ディレクトリ削除

## 2026-05 構成整理（前半）

- `legacy/` → 一時的に `analysis/`、`tasks/` → `cli/`
- `DB/` → `data/kaburadar.db`
- `output/honban/` → `output/results/`
- `config_hi.ini` 削除（LO / 短期 RSI 一本化）
- 未使用 `technical_*.py` 7 ファイル削除、RSI4 専用の `backtest_proc.py` に縮小
- bat を分かりやすい名前に整理（旧名は互換ラッパー）
- `docs/guide/` にプロジェクトドキュメントを追加

## 以前の改善（REFAC_SUMMARY より）

- 機密情報の `.env` 化
- 絶対パス依存の削減
- `requirements.txt` 整備
- GitHub Pages パイプライン（`publish` + Actions）
