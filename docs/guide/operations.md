# 日常運用（封印）

> **本番は [KabuRadar3](https://github.com/lalakuma/KabuRadar3)（ローカル）です。**  
> KabuRadar2 では毎日の screening / LINE を回しません。

## 封印後にやること

| やること | 場所 |
|----------|------|
| 毎日の解析・通知 | **KabuRadar3** |
| このリポ | 参照のみ（アーカイブ想定） |

## 旧クラウド手順（保管）

以前は GitHub Actions の `daily-screening` で平日実行していましたが、schedule は無効化済みです。

## ローカルでやらないこと（本リポ）

| やらないこと | 理由 |
|--------------|------|
| `screening.bat` | 本番は KabuRadar3 |
| `run_scheduler.bat` / タスクスケジューラ | 同上 |
| 本リポの DB を本番更新 | 同上 |

## 参考: 開発・緊急時のみ

`bat/` / `sh/` は開発用に残しています。封印後の本番利用は想定しません。
