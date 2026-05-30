# 開発・テスト

## 環境

```bat
set PYTHONPATH=src
```

IDE ではワークスペースルートを開き、`src` をソースルートに指定すると import が楽です。

## テスト

```bat
pytest
```

GitHub Actions の **CI** ワークフロー（`.github/workflows/ci.yml`）でも同じテストが走ります。

| ファイル | 内容 |
|----------|------|
| `tests/test_config.py` | ini / DB パス |
| `tests/test_publish_payload.py` | CSV → JSON |
| `tests/test_publish_unchanged.py` | データ未変更時は JSON を書かない |
| `tests/test_analyze_exit_code.py` | 解析パイプラインの終了コード |
| `tests/test_strategy_rsi.py` | RSI インジケータ |
| `tests/test_encoding.py` | CSV UTF-8 BOM / 旧 cp932 読込 |
| `tests/test_package_imports.py` | 機能ブロック import |
| `tests/test_legacy_imports.py` | 後方互換 import |

## ドキュメントを直すタイミング

**コード・設定・bat・パスを変えたら、同じ PR / 変更で `docs/guide/` も更新する。**

| 変更 | 更新先の目安 |
|------|----------------|
| bat / CLI | `operations.md`, `README.md` |
| ini / パス | `configuration.md`, `setup.md` |
| パッケージ構成 | `architecture.md`, `changelog.md` |

詳細はリポジトリルートの `.cursor/rules/sync-docs-on-change.mdc`（Cursor 向けルール）を参照。

## コーディング方針

- 新規コードは機能ブロックごとの `kaburadar.*` import（例: `kaburadar.strategy.engine`, `kaburadar.data.repository`）
- 旧パス `kaburadar.analysis.*` は互換用 re-export のみ（新規では使わない）
- 設定値は `config_lo.ini` に集約し、`kaburadar.settings.loader.read_config`（または `kaburadar.config`）で読む

## 解析の一部だけ試す

```bat
python src\kaburadar\cli\analyze.py
```

全銘柄は数分かかります。ログは `output/logs/debug.log`。

## Pages 用 JSON の確認

```bat
python src\kaburadar\cli\publish.py
```

## 今後の拡張候補

- LINE: `analyze.py --notify` / `screening_notify.bat`（`.env` 設定時）
- `analyze` の終了コード（失敗銘柄時に非ゼロ返却）
- CI での pytest 自動実行
- `sqlight.py` → `database.py` へのリネーム
