# KabuRadar2（封印・アーカイブ）

> **このリポジトリは運用終了しています。**  
> 後継・本番は **[KabuRadar3](https://github.com/lalakuma/KabuRadar3)**（ローカル本番）を使ってください。

短期 RSI 戦略のバックテスト・集計・GitHub Pages 公開の旧版です。

| 項目 | 状態 |
|------|------|
| 毎日の自動実行 | **停止済み**（KabuRadar3 へ移行） |
| GitHub Actions schedule | **無効** |
| LINE 通知 | **クラウドからは送らない**（KabuRadar3 側） |
| コード・履歴 | 参照用として残置（読み取り専用想定） |

旧 Web（更新停止）: https://lalakuma.github.io/KabuRadar2/

## ドキュメント（参考）

- [docs/guide/](docs/guide/README.md) — 当時の構成・設定の説明（現行運用ではない）

## 開発メモ

ローカルでコードを読むだけの場合:

```bat
set PYTHONPATH=src
pip install -r requirements.txt
pytest
```

**新規の本番運用・毎日の screening は行わないでください。**
