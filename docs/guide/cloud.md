# 無料クラウド実行（GitHub Actions）— 旧メモ

> **封印:** KabuRadar2 の本番運用は終了しています。現行は [KabuRadar3](https://github.com/lalakuma/KabuRadar3) です。  
> 以下は移行前のクラウド運用メモです。**新規セットアップはしないでください。**

## 仕組み（当時）

```
（自動 schedule は無効）
手動 Run workflow のみ
  → 株価更新 → 解析 → Web 公開
```

## 日常の運用（封印後）

| やること | 場所 |
|----------|------|
| 毎日の解析・LINE | **KabuRadar3** |
| 本リポ | 参照のみ |
| 旧 Web | https://lalakuma.github.io/KabuRadar2/ （更新停止） |

## スケジュール

| 項目 | 値 |
|------|-----|
| `daily-screening.yml` | **手動のみ**（cron 無効） |
| `schedule-guard.yml` | **手動のみ**（cron 無効） |

## LINE

クラウドからは送らない。KabuRadar3 ローカル本番を使う。
