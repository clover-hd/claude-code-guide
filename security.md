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

> ただし CLAUDE.md のルールは「お願い」です。確実に止めたい場合は、後述の[コミットガード](#コミットガード--秘密の値を機械的に止める)を置きましょう。

## Claudeに渡してはいけない情報

Claude Codeはクラウド上のAIと通信しています。以下は入力しないでください：

- 本番環境のデータベース接続情報
- お客様の個人情報（名前、メールアドレス等）
- 本番環境のAPIキーやシークレット

> 開発用のダミーデータやテスト環境の情報であれば問題ありません。

## .gitignore のテンプレート

新しいプロジェクトを始めるとき、最低限これを入れておきましょう（`/kickstart` の A0 で作られるものと同じです）：

```gitignore
# 環境変数・シークレット
.env
.env.*
!.env.example

# 認証情報
credentials.json
*.pem
*.key
service-account.json

# Claude Code の個人設定
.claude/settings.local.json

# OS・エディタ
.DS_Store
Thumbs.db
*.swp
.vscode/settings.json
.idea/
```

技術スタックが決まったら、それに合わせた項目を足します（Node.js なら `node_modules/`、`dist/`、`build/`、Python なら `__pycache__/`、`.venv/` など）。

> `.claude/settings.local.json` には、承認の確認で「今後は聞かない」を選んだルールなど、個人の設定が保存されます。チームで共有する設定は `.claude/settings.json` に書きます。

## コミットガード — 秘密の値を機械的に止める

`.gitignore` と CLAUDE.md のルールだけでは、`git add -f` や、エージェントの見落としで秘密の値がコミットされることがあります。一度コミットしたものは**履歴から完全に消すのが難しい**ため、コミットの前に**機械的に**検査して止める仕組みを置きましょう。

### 二層で止める

同じ検査スクリプト `scripts/check-staged.sh` を、二つの入口から呼びます。

| 層 | 止めるもの | これだけでは足りない理由 |
|---|---|---|
| git の pre-commit フック（`.githooks/pre-commit`） | 人間のコミットも含めて止める | clone しただけでは有効にならない。`--no-verify` で飛ばせる |
| Claude Code の PreToolUse フック（`.claude/settings.json`） | エージェントの `git commit`。`--no-verify` によるフックの迂回も止める | 人間のコミットは止められない |

どちらか片方では穴が残るので、二層にします。

### 検査スクリプトが見るもの

- `.env`、`*.pem`、`*.key`、`credentials.json` などの秘密の値・認証情報のファイル
- `*.sqlite`、`*.db` などのデータベースのファイル
- 追加した行の中の、APIキーらしき文字列（`sk-ant-...`、`AKIA...`、`-----BEGIN ... PRIVATE KEY-----` など）

```bash
# 抜粋：ステージされたファイルを1つずつ見る
while IFS= read -r -d '' f; do
  base=$(basename "$f" | tr '[:upper:]' '[:lower:]')
  case "$base" in
    .env.example) ;;
    .env | .env.*) report "$f — 秘密の値のファイル（.env）" ;;
  esac
done < <(git diff --cached --name-only --diff-filter=ACMR -z)
```

### PreToolUse フックが行うこと

- `git commit --no-verify` / `-n`（git のフックを飛ばす指定）を**止める**
- git のフック（`core.hooksPath`）が有効になっていなければ**止めて**、有効にするよう伝える
- 検査スクリプトを走らせ、引っかかったら**止める**（理由はClaudeに伝わり、Claudeがそのファイルをステージから外す）
- push・Pull Request・Issue の作成と、本番を壊しうるコマンド（本番DBへのマイグレーションなど）は、**人間に確認を求める**

### push と Pull Request の前に確認を入れる

Claude Code は既定で **auto モード**で始まります。auto モードでは、今のリポジトリへの push（既定のブランチも含む）と Pull Request の作成が、**確認なしで通ります**。CLAUDE.md に書いた指示は分類器も読みますが、必ず確認が出る保証にはなりません。会話の中で「push しないで」と伝えただけの指示は、会話が圧縮されると消えることがあります。

push の前に人間の確認を取りたいなら、`.claude/settings.json` の `permissions.ask` に入れます。このルールに当たる操作には、auto モードでも必ず確認が出ます。

```json
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(gh pr create *)",
      "Bash(gh pr merge *)",
      "Bash(gh issue create *)"
    ]
  }
}
```

このルールは `git push` と書かれたコマンド（`&&` でつないだ一部も含む）に当たります。`git -C <dir> push` のような別の書き方は拾えないので、上の PreToolUse フックでもコマンド全体を見て確認を求めます。`/kickstart` では、この両方が設定されます。

それでも、`gh api` で直接作るなど、書き方によっては拾えないものがあります。確認の設定は確実な防御ではなく「普通の書き方なら止まる」ものと考え、作業の区切りで人間が確かめることと組み合わせましょう。

フックの書き方は[CLAUDE.md・Hooks](project-config.md#hooks自動化)、スクリプトとフックの全文は [kickstart スキル](skills/kickstart/SKILL.md) の A7 にあります。`/kickstart` を使えば、プロジェクトの立ち上げ時に自動で設定されます。

> **誤検知で止められたとき**も、フックを飛ばさないでください。例外を足す前に、そのファイルの置き場所を変えられないかを先に考えましょう。

> **チームで使う場合**: `core.hooksPath` は clone しただけでは有効にならないので、README の環境構築手順に `git config core.hooksPath .githooks` を書いておきましょう。
