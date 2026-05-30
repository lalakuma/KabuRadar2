# セットアップ

## 前提

- Python 3.10 以上推奨
- **Windows:** `bat/`（cmd / PowerShell）
- **Linux / macOS:** `sh/` または Makefile（[linux.md](linux.md)）
- Git（GitHub Pages 自動 push を使う場合）

## 1. リポジトリの取得

```bat
git clone <repository-url>
cd KabuRadar2
```

## 2. Python 環境

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. データベース

`data/kaburadar.db` は Git に含まれません。元プロジェクトからコピーします。

```bat
mkdir data
copy C:\share\MorinoFolder\Python\KabuRadar\DB\KabuRadar.db data\kaburadar.db
```

パスは `config/config_lo.ini` の `PATH_DB = data\kaburadar.db` と一致している必要があります。

## 4. 環境変数（任意）

```bat
copy .env.example .env
```

`.env` を編集します。解析だけなら不要です。LINE 通知を使う場合は `LINE_CHANNEL_ACCESS_TOKEN` と `LINE_USER_IDS` を設定し、`bat\screening_notify.bat` または `analyze.py --notify` を使います。

## 5. 動作確認

```bat
set PYTHONPATH=src
pytest
python src\kaburadar\cli\publish.py
```

`output\results\` に過去の集計 CSV がある場合、`publish` が `docs\data.json` を生成します。

## 6. GitHub Pages（初回のみ）

リポジトリの **Settings → Pages** で:

- Branch: `gh-pages`
- Folder: `/ (root)`

`bat\publish.bat --push` または `bat\analyze_and_publish.bat` 実行後、Actions が `gh-pages` ブランチを更新します。
