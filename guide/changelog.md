# 変更履歴メモ

リファクタリング・整理の要点です（詳細は git log を参照）。

## 2026-06 schedule 遅延対策（guard 追加）

- `daily-screening.yml` から直接 `schedule` を外し、`workflow_dispatch` 専用に変更
- 新規 `schedule-guard.yml` を追加（平日 5 分間隔で監視）
- 12:30 / 15:00 / 16:00 JST の未実行スロットを検知したら `daily-screening` を自動起動
- `README.md` / `docs/guide/operations.md` / `docs/guide/cloud.md` の運用手順を更新

## 2026-06 当日シグナル・特別買い・Web タブ（フェーズ A）

- `config/runtime.json` … 広がり閾値・ETF・LINE トグル
- `signals/` … 今日の新買/返売り、特別買いステート（`data/special_state.json`）
- `data.json` に `today` / `special` / `runtime` / `controls`
- Web: タブ（今日・特別買い・損益・設定・実行リンク）
- LINE: 買い/返売り/特別買い通知
- Actions: `workflow_dispatch` で full / analyze / publish、lo / hi

## 2026-06 LINE 設定の v1 からの移植

- `scripts/sync_line_from_kaburadar.py` … v1 `line.py` → `.env` / GitHub Secrets
- `.env` を `.gitignore` に追加
- `notifications/line.py` がプロジェクトルートの `.env` を読むよう修正

## 2026-06 Web 実行表示・LINE 強化

- `data.json` にクラウド実行メタ（`run.pages_url` / `run.workflow_url`）を追加
- Web: 更新元（自動/手動）表示、実行ログへのリンク
- LINE: PF・勝率・Web URL・Actions ログ URL を含むサマリー
- `cloud.md` に Pages / LINE の初回セットアップ手順を追記

## 2026-05 12:30 は config_hi（RSI4反転）

- `config/config_hi.ini` 復活（`SCR_JDG_RSI4REV = 1`）
- 平日 **12:30 JST** → `config_hi.ini`、**15:00 / 16:00** → `config_lo.ini`
- 環境変数 `KABURADAR_CONFIG` で切替（`analyze.py --config` も可）
- Web 表示にモード（HI / LO）を表示

## 2026-05 スケジュール 1日3回

- Daily screening: 平日 **12:30・15:00・16:00 JST**（03:30 / 06:00 / 07:00 UTC）

## 2026-05 スケジュール 1日2回

- Daily screening: 平日 **15:00・16:00 JST**（06:00 / 07:00 UTC）

## 2026-05 クラウド専用運用

- 本番を GitHub Actions のみとする方針にドキュメントを統一
- Actions workflow に LINE 通知（Secrets 設定時）を追加
- ローカル bat / タスクスケジューラは本番では使わない旨を明記

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
