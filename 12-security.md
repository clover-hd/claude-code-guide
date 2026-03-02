# セキュリティの基本

[< ガイド目次に戻る](README.md)

---

会社のプロジェクトでは、セキュリティ意識は最低限持っておく必要があります。

## コミットしてはいけないもの

| ファイル | 内容 | 対策 |
|---------|------|------|
| `.env` | APIキー、DB接続情報、シークレット | `.gitignore` に追加 |
| `credentials.json` | サービスアカウントキー | `.gitignore` に追加 |
| `*.pem`, `*.key` | SSL証明書、秘密鍵 | `.gitignore` に追加 |
| `node_modules/` | 依存パッケージ | `.gitignore` に追加 |

**CLAUDE.mdにルールを書いておく**と、Claudeが自動的に避けてくれます：

```markdown
# CLAUDE.md（抜粋）

## セキュリティルール
- .env ファイルは絶対にコミットしない
- APIキーやパスワードをコードにハードコードしない
- 認証情報は環境変数経由で取得する
```

## Claudeに渡してはいけない情報

Claude Codeはクラウド上のAIと通信しています。以下は入力しないでください：

- 本番環境のデータベース接続情報
- お客様の個人情報（名前、メールアドレス等）
- 本番環境のAPIキーやシークレット

> 開発用のダミーデータやテスト環境の情報であれば問題ありません。

## .gitignore のテンプレート

新しいプロジェクトを始めるとき、最低限これを入れておきましょう：

```gitignore
# 環境変数・シークレット
.env
.env.local
.env.production

# 認証情報
credentials.json
*.pem
*.key
service-account.json

# 依存パッケージ
node_modules/

# ビルド成果物
dist/
build/

# OS・エディタ
.DS_Store
.vscode/settings.json
```
