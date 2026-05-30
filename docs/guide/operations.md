# 日常運用

## OS 別ランチャー

| OS | フォルダ | 例 |
|----|----------|-----|
| Windows 10/11 | `bat\` | `bat\screening.bat` |
| Linux / macOS | `sh/` | `bash sh/screening.sh` または `make screening` |

Python の処理本体は同じです。`scheduling/launcher.py` は OS を見て `bat` / `sh` を自動選択します。

## 推奨 bat 一覧（Windows）

| bat | 処理内容 |
|-----|----------|
| `screening.bat` | 株価更新 → 全銘柄解析 |
| `analyze.bat` | 解析のみ |
| `update_prices.bat` | 株価更新のみ |
| `publish.bat` | `docs/data.json` 生成 |
| `publish.bat --push` | 上記 + `master` へ push |
| `analyze_and_publish.bat` | 解析 + JSON 生成 + push |
| `screening_notify.bat` | 株価更新 → 解析 → LINE サマリー（.env 設定時） |
| `healthcheck.bat` | 設定・DB・CLI の存在確認 |
| `run_scheduler.bat` | 時間帯に応じて上記を自動起動 |

いずれも `bat\_env.bat` で `PYTHONPATH=src` を設定します。

## 推奨 sh 一覧（Linux / macOS）

| sh | 処理内容（bat と同等） |
|----|------------------------|
| `sh/screening.sh` | 株価更新 → 全銘柄解析 |
| `sh/analyze.sh` | 解析のみ |
| `sh/update_prices.sh` | 株価更新のみ |
| `sh/publish.sh` | `docs/data.json` 生成 |
| `sh/analyze_and_publish.sh` | 解析 + JSON + push |
| `sh/screening_notify.sh` | 更新 + 解析 + LINE |
| `sh/healthcheck.sh` | 環境チェック |
| `sh/run_scheduler.sh` | 時間帯スケジューラ |

詳細: [linux.md](linux.md)

## 典型的な流れ

### 平日の解析 → スマホで確認

```bat
bat\screening.bat
bat\publish.bat --push
```

### 解析結果を LINE にも送る（個人運用）

`.env` に `LINE_CHANNEL_ACCESS_TOKEN` と `LINE_USER_IDS` を設定したうえで:

```bat
bat\screening_notify.bat
```

または:

```bat
bat\screening.bat
python src\kaburadar\cli\analyze.py --notify
```

### 環境チェック（トラブル時）

```bat
bat\healthcheck.bat
```

1〜2 分後: https://lalakuma.github.io/KabuRadar2/

### 解析済みで Web だけ更新

```bat
bat\publish.bat --push
```

### 一括（解析 + 公開）

```bat
bat\analyze_and_publish.bat
```

**前提:** `git push` がパスワード入力なしでできること（SSH 鍵または Git Credential Manager）。

## CLI から直接実行

```bat
set PYTHONPATH=src
python src\kaburadar\cli\update_prices.py --menu 1
python src\kaburadar\cli\analyze.py
python src\kaburadar\cli\publish.py --push
```

## 旧 bat 名（互換）

| 旧名 | 実体 |
|------|------|
| `2-2.KabuStation_kessai_GetYahooF.bat` | `screening.bat` |
| `2-3.GetKabuka_GetYahooF.bat` | `update_prices.bat` |
| `1.kabu_main.bat` | `run_scheduler.bat` |
| `publish_results.bat` | `publish.bat` |

## 出力の場所

| パス | 内容 |
|------|------|
| `output/results/` | 銘柄別 CSV、集計 CSV（`Y*_PF*.csv`）、Excel |
| `output/logs/debug.log` | 解析・スケジューラのログ |
| `output/workspace/` | 作業用（設定スナップショット等） |
| `docs/data.json` | GitHub Pages 用 JSON |

## スケジューラ

`run_scheduler.bat` → `scheduling/launcher.py`（`scheduler/launcher.py` は互換シム）が時刻で bat を起動します。

| 時刻帯 | 実行 |
|--------|------|
| 11:30〜12:00 | `screening.bat` |
| 9:00〜14:30 | `screening.bat` |
| 15:00〜15:30 | `update_prices.bat` |

必要に応じて `src/kaburadar/scheduling/launcher.py` を編集してください。

## トラブルシュート

| 症状 | 確認事項 |
|------|----------|
| DB エラー | `data/kaburadar.db` の存在、`PATH_DB` |
| push 失敗 | `git remote`, 認証, リモートが先行していないか |
| 集計 CSV がない | `analyze` が完走したか、`output/results/` を確認 |
| 高値株だけスキップ | `price over` は仕様（価格上限フィルタ） |
