# 無料クラウド実行（GitHub Actions）— 本番運用

**KabuRadar2 の本番はクラウド専用**です。株価収集・DB 更新・解析・Web 公開まで、すべて GitHub Actions 上で完結します。

**条件: 無料** — 公開リポジトリなら Actions / Pages / LFS の無料枠内で運用可能です。

## 仕組み

```
平日 15:00 / 16:00 JST（各2回）
  → GitHub Actions (Ubuntu)
  → git lfs pull で data/kaburadar.db を取得
  → yfinance で株価更新 → SQLite に書込
  → 全銘柄バックテスト → 集計
  → docs/data.json 生成
  → DB + JSON を commit & push
  → GitHub Pages 更新
```

**PC は不要**（設定ファイルを編集するときだけ git clone があれば足ります）。

## 日常の運用

| やること | 頻度 |
|----------|------|
| 結果を見る | https://lalakuma.github.io/KabuRadar2/ |
| Actions 成功確認 | 初回のみ / 障害時 |
| 手動再実行 | 必要時 → Actions → Run workflow |
| ローカル screening | **しない** |

## 初回確認

1. リポジトリ **Actions** → **Daily screening (cloud)**
2. **Run workflow** → 成功（緑）になるまで待つ（10〜30 分程度）
3. Pages を開いて結果を確認

DB はすでに Git LFS でリポジトリに含まれています。

## スケジュール

| 項目 | 値 |
|------|-----|
| ワークフロー | `.github/workflows/daily-screening.yml` |
| 既定 | 平日 **15:00・16:00 JST**（`0 6` / `0 7` UTC、月〜金） |
| 手動 | Actions → Run workflow |

時刻変更は workflow 内の `cron` を編集して push してください。

## 設定変更

1. `config/config_lo.ini` を編集
2. commit & push
3. 次回 Actions 実行から反映

## LINE 通知（任意）

**Settings → Secrets and variables → Actions** に追加:

| Secret | 内容 |
|--------|------|
| `LINE_CHANNEL_ACCESS_TOKEN` | Messaging API トークン |
| `LINE_USER_IDS` | ユーザー ID（カンマ区切り） |

解析成功後、損益上位銘柄を自動送信します。未設定ならスキップ。

## 無料枠の目安

| サービス | 公開 repo |
|----------|-----------|
| GitHub Actions | 平日 1 回/日 → 通常問題なし |
| Git LFS | ストレージ 1GB / **帯域 1GB・月** |
| GitHub Pages | 無料 |

**LFS 帯域:** DB（約 128MB）を毎日 push すると月 ~2.8GB 相当になり、**無料 1GB を超える可能性**があります。超えた場合は GitHub の LFS 帯域追加（有料）か、DB push 頻度の見直しが必要です。

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
| ローカルと結果が違う | ローカル screening を止める |

## GitHub Pages が更新されない理由

Actions bot が `master` へ push しても、**別 workflow は自動起動しない** GitHub の仕様があります。  
`daily-screening` の末尾で **gh-pages へ直接デプロイ**するよう修正済みです。

## 関連

- [operations.md](operations.md) — 運用概要
- [configuration.md](configuration.md) — ini 項目
- [setup.md](setup.md) — 初回セットアップ
