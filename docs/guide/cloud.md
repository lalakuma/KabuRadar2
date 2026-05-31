# 無料クラウド実行（GitHub Actions）

**条件: 無料** — 公開リポジトリなら Actions / Pages / LFS の無料枠内で運用可能です。

## 仕組み

```
平日 16:00 JST (cron)
  → GitHub Actions (Ubuntu)
  → git lfs pull で data/kaburadar.db を取得
  → 株価更新 → 全銘柄解析 → docs/data.json 生成
  → DB + JSON を commit & push
  → Pages デプロイ（docs/ 変更時）
```

PC がオフでも **解析〜Web 公開まで自動**できます。

## 前提

| 項目 | 内容 |
|------|------|
| リポジトリ | **公開**推奨（Actions 無料枠が広い） |
| DB | `data/kaburadar.db` を **Git LFS** で管理（約 100MB 超のため） |
| ブランチ | push 先は `KABURADAR_GIT_BRANCH` または git 自動検出 |

## 初回セットアップ（ローカル）

### 1. Git LFS を有効化

```bash
git lfs install
```

Windows では [Git LFS](https://git-lfs.com/) をインストールしてください。

### 2. DB を LFS で追加（初回のみ）

```bash
git lfs track data/kaburadar.db
git add .gitattributes data/kaburadar.db data/README.md
git commit -m "DB を Git LFS で追加"
git push origin master
```

### 3. Actions を確認

リポジトリ **Actions** タブ → **Daily screening (cloud)**  
手動実行: **Run workflow**

## スケジュール

| 項目 | 値 |
|------|-----|
| ワークフロー | `.github/workflows/daily-screening.yml` |
| 既定 | 平日 **16:00 JST**（`0 7 * * 1-5` UTC） |
| 手動 | Actions → Run workflow |

時刻変更は workflow 内の `cron` を編集してください。

## 無料枠の目安

| サービス | 公開 repo |
|----------|-----------|
| GitHub Actions | 実質十分（全銘柄解析 〜20 分 × 平日） |
| Git LFS | ストレージ 1GB / 帯域 1GB・月（DB 更新 push で消費） |
| GitHub Pages | 無料 |

**注意:** DB を毎日 push すると LFS **帯域**を消費します。月 1GB を超える場合は、ローカル解析 + JSON のみ push（従来方式）に戻すか、更新頻度を下げてください。

## LINE 通知（任意）

Actions から LINE を送る場合はリポジトリ **Secrets** に設定:

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_USER_IDS`

workflow に `--notify` ステップを足す拡張が可能（現状は未配線）。

## ローカル運用との併用

| 方式 | 用途 |
|------|------|
| **クラウド only** | PC 不要。Actions に任せる |
| **ローカル only** | `bat\screening.bat`（従来） |
| **併用** | どちらか一方を主に（同日両方は DB 競合に注意） |

同日にローカルと Actions の両方で解析すると、**後から push した方が DB を上書き**します。

## トラブルシュート

| 症状 | 対処 |
|------|------|
| push で 100MB エラー | LFS 未設定 → `git lfs track data/kaburadar.db` |
| clone 後 DB が小さい/壊れる | `git lfs pull` |
| Actions が DB なし | LFS ファイルがリモートに push されているか確認 |
| 解析タイムアウト | workflow の `timeout-minutes` を増やす |

## 関連

- [linux.md](linux.md) — 自前 VPS / cron
- [setup.md](setup.md) — 初回環境
- [operations.md](operations.md) — bat / sh 一覧
