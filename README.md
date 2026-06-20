# KabuRadar2

短期 RSI 戦略のバックテスト・集計・GitHub Pages 公開。**本番は GitHub Actions（クラウド専用）**。

**運用:** [クラウド運用ガイド](docs/guide/cloud.md) · [取扱説明書](docs/guide/manual.md)

## 本番の流れ（PC 不要）

```
平日 12:30 / 15:00 / 16:00 JST
  daily-screening（schedule）+ schedule-guard（未実行補完）
  → 株価更新 → 解析 → Web 公開
```

| 確認 | URL |
|------|-----|
| **解析結果（Web）** | https://lalakuma.github.io/KabuRadar2/ |
| **実行ログ** | [Actions · Daily screening](https://github.com/lalakuma/KabuRadar2/actions/workflows/daily-screening.yml) |
| **LINE** | [cloud.md](docs/guide/cloud.md) の Secrets 設定後、自動通知 |

手動実行: GitHub **Actions** → **Daily screening (cloud)** → **Run workflow**
（自動監視は **Daily screening schedule guard**）

## ディレクトリ構成

```
KabuRadar2/
├── .github/workflows/   # CI + 本番 daily-screening + schedule-guard
├── config/config_lo.ini # LO 戦略（SCR_JDG_RSI4REV=0）
├── config/config_hi.ini # HI 戦略（SCR_JDG_RSI4REV=1・12:30用）
├── data/kaburadar.db    # SQLite（Git LFS）
├── docs/                # GitHub Pages + data.json
└── src/kaburadar/       # Python 本体
```

`bat/` / `sh/` は **開発・デバッグ用**（本番では使わない）。

## 初回セットアップ

1. リポジトリを clone（`git lfs pull`）
2. Actions で **Daily screening (cloud)** を手動実行
3. 成功したら Pages を確認

詳細: [docs/guide/cloud.md](docs/guide/cloud.md)

## 開発（ローカル）

```bat
set PYTHONPATH=src
pip install -r requirements.txt
pytest
```

本番の `screening.bat` は **実行しない**（DB 競合防止）。

## 公開 URL

https://lalakuma.github.io/KabuRadar2/
