# KabuRadar2

短期 RSI 戦略のバックテスト・集計・GitHub Pages 公開用ワークスペース。

**ドキュメント:** [取扱説明書](docs/guide/manual.md) · [無料クラウド](docs/guide/cloud.md) · [docs/guide/](docs/guide/)

## ディレクトリ構成

```
KabuRadar2/
├── bat/                 # Windows 10/11 用ランチャー（*.bat）
├── sh/                  # Linux / macOS 用（*.sh・[linux.md](docs/guide/linux.md)）
├── Makefile             # Linux 向け make ターゲット（任意）
├── config/
│   └── config_lo.ini    # 実行設定
├── data/
│   └── kaburadar.db     # SQLite（Git LFS・[cloud.md](docs/guide/cloud.md)）
├── docs/                # GitHub Pages + [プロジェクト文書](docs/guide/)
├── output/              # 生成物（Git 除外）
│   ├── results/         # 解析 CSV・集計 Excel
│   ├── workspace/       # 作業用
│   └── logs/            # ログ
├── src/kaburadar/
│   ├── settings/        # 設定・パス
│   ├── data/            # DB アクセス
│   ├── strategy/        # RSI バックテスト
│   ├── pipeline/        # 解析・集計
│   ├── market_data/     # 株価更新
│   ├── publishing/      # GitHub Pages
│   ├── cli/             # 実行エントリ
│   └── scheduling/    # 時間帯起動
└── tests/
```

旧 bat 名（`2-2.KabuStation_...` 等）は互換用ラッパーとして残しています。

## Quick start

1. 仮想環境を作成し `pip install -r requirements.txt`
2. `.env.example` を `.env` にコピー（任意）
3. `data/kaburadar.db` を配置（[data/README.md](data/README.md) 参照）
4. 実行例:

**Windows**

```bat
bat\screening.bat
bat\publish.bat
```

**Linux / macOS**

```bash
bash sh/screening.sh
bash sh/publish.sh
# または: make screening && make publish
```

## GitHub Pages

**Windows:** `bat\analyze_and_publish.bat`  
**Linux:** `bash sh/analyze_and_publish.sh`

解析済みのときだけ JSON 生成 + push:

```bat
bat\publish.bat --push
```

```bash
bash sh/publish.sh --push
```

公開 URL: https://lalakuma.github.io/KabuRadar2/

## 開発

```bat
set PYTHONPATH=src
pytest
python src\kaburadar\cli\analyze.py
```
