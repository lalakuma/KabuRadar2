# 無料クラウド実行（GitHub Actions）— 本番運用

**KabuRadar2 の本番はクラウド専用**です。株価収集・DB 更新・解析・Web 公開まで、すべて GitHub Actions 上で完結します。

**条件: 無料** — 公開リポジトリなら Actions / Pages / LFS の無料枠内で運用可能です。

## 仕組み

```
平日 12:30 / 16:00 JST（LO・場中1回 / 引け後1回）
  → GitHub Actions (Ubuntu)
  → git lfs pull で data/kaburadar.db を取得
  → yfinance で過去5日分を取得 → SQLite に書込
  → 全銘柄バックテスト → 集計
  → docs/data.json 生成
  → DB + JSON を commit & push
  → GitHub Pages 更新
```

**PC は不要**（設定ファイルを編集するときだけ git clone があれば足ります）。

## 日常の運用

| やること | 頻度 |
|----------|------|
| **Web で結果を見る** | 毎日 · https://lalakuma.github.io/KabuRadar2/ （**今日**タブに買い/返売り） |
| **手動実行** | Actions → Run workflow（`job`: full / analyze / publish） |
| **運用設定** | [runtime.json を編集](https://github.com/lalakuma/KabuRadar2/edit/master/config/runtime.json) |
| **LINE でサマリー** | Secrets 設定後 · 解析成功のたび自動 |
| Actions 成功確認 | 初回のみ / 障害時 |
| 手動再実行 | 必要時 → Actions → Run workflow |
| ローカル screening | **しない** |

### Web で見られる内容

- 全体 PF・勝率・損益合計・銘柄一覧（検索・並び替え）
- 更新日時・モード（HI / LO）
- クラウド実行時は **「今回の実行ログ」** リンク（GitHub Actions の run へ）

## 初回セットアップ（Web + LINE）

### 1. GitHub Pages

1. リポジトリ **Settings** → **Pages**
2. **Build and deployment** → Source: **Deploy from a branch**
3. Branch: **`gh-pages`** / **`/ (root)`** → Save  
   （Actions が `daily-screening` 完了時に `gh-pages` へデプロイします）

### 2. 動作確認

1. **Actions** → **Daily screening (cloud)** → **Run workflow**
2. 成功（緑）まで待つ（10〜30 分程度）
3. https://lalakuma.github.io/KabuRadar2/ を開き、更新日時が変わっているか確認

DB はすでに Git LFS でリポジトリに含まれています。

## スケジュール

| 項目 | 値 |
|------|-----|
| 本体ワークフロー | `.github/workflows/daily-screening.yml`（`schedule` + 手動） |
| 監視ワークフロー | `.github/workflows/schedule-guard.yml`（スロット直後 + 5 分間隔） |
| 既定 | 平日 **12:30・16:00 JST**（いずれも `config_lo.ini`） |
| 12:30 | 場中（午後場・`SCR_JDG_RSI4REV = 0`） |
| 16:00 | 引け後（`SCR_JDG_RSI4REV = 0`） |
| 手動 Run workflow | `config_profile` で lo / hi を選択 |
| 手動 | Actions → Run workflow |

時刻変更は `schedule-guard.yml` の監視ロジック（スロット時刻）を編集して push してください。

## 設定変更

1. `config/config_lo.ini` を編集
2. commit & push
3. 次回 Actions 実行から反映

## LINE 通知（任意）

### Secrets の登録

**既存 KabuRadar (v1) を使っている場合** — `software/src/line.py` と同じトークン・ユーザー ID を移植できます:

```bash
python scripts/sync_line_from_kaburadar.py --env --gh-secrets
```

（`--env` はローカル `.env`、`--gh-secrets` は GitHub Actions 用。v1 を clone 済みか `--line-py` でパス指定）

手動で入れる場合: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | 内容 |
|--------|------|
| `LINE_CHANNEL_ACCESS_TOKEN` | [LINE Developers](https://developers.line.biz/) → Messaging API チャネル → チャネルアクセストークン（長期） |
| `LINE_USER_IDS` | 自分のユーザー ID（`U` で始まる）。複数は **カンマ区切り** |

ユーザー ID の調べ方: チャネルに友だち追加 → Webhook または公式手順で確認。

### 送信される内容（例）

```
KabuRadar LO（RSI4反転なし）
2026-06-01 20:08 JST
PF 2.993 · 勝率 78.1% (57勝16敗) · 損益 +319,100
— 損益上位 —
9024 西武ホールディングス ¥44,000 (W1L0)
…
Web: https://lalakuma.github.io/KabuRadar2/
Log: https://github.com/lalakuma/KabuRadar2/actions/runs/…
```

- 平日のみ送信（土日はスキップ）
- Secrets 未設定のときは Actions ログに `LINE secrets not set, skipping.` のみ（解析は続行）

## 無料枠の目安

| サービス | 公開 repo |
|----------|-----------|
| GitHub Actions | 平日 3 回/日 → 通常問題なし |
| Git LFS | ストレージ 10 GiB / **帯域 10 GiB・月** |
| GitHub Pages | 無料 |

**LFS 帯域:** DB（約 128MB）を平日 3 回/日 pull すると月 ~8.4 GiB 相当。**無料 10 GiB/月** 内に収まる想定です。手動実行や clone が多い場合は [Billing → Git LFS](https://github.com/settings/billing) で使用量を確認してください。

## ローカル clone する人へ

結果をローカルで見る必要はありません。コード編集時のみ:

```bash
git lfs install
git clone <url>
cd KabuRadar2
git lfs pull
```

**`bat\screening.bat` は実行しないでください**（DB が競合します）。

## トラブルシュート

| 症状 | 対処 |
|------|------|
| Actions 失敗 | ログ確認。yfinance エラー・解析 exit 1/2 |
| DB なし | LFS が pull されているか |
| サイト古い | Actions 成功後も Pages 未デプロイだった → **修正済**（screening 末尾で gh-pages へデプロイ） |
| Pages が `errored` | Settings → Pages で branch **`gh-pages`** を指定。Actions を再実行 |
| LINE が来ない | Secrets 名の綴り・友だち追加・平日か確認。Actions の LINE ステップログを見る |
| ローカルと結果が違う | ローカル screening を止める |

## GitHub Pages が更新されない理由

Actions bot が `master` へ push しても、**別 workflow は自動起動しない** GitHub の仕様があります。  
`daily-screening` の末尾で **gh-pages へ直接デプロイ**するよう修正済みです。

## 関連

- [operations.md](operations.md) — 運用概要
- [configuration.md](configuration.md) — ini 項目
- [setup.md](setup.md) — 初回セットアップ
