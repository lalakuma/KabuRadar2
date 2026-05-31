# data/

SQLite データベース `kaburadar.db` を置くフォルダです。

## Git 管理

`kaburadar.db` は **Git LFS** でリポジトリに含めます（約 100MB 超のため通常 Git では push 不可）。

初回 clone 後:

```bash
git lfs install
git lfs pull
```

`config/config_lo.ini` の `PATH_DB = data/kaburadar.db` を確認してください。

## ローカルから別 DB を使う場合

上書きしたいときだけ、元の `KabuRadar.db` を `data/kaburadar.db` にコピーし、LFS 経由で commit します。
