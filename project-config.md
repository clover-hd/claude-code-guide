# CLAUDE.md・Hooks によるプロジェクト設定

[< ガイド目次に戻る](README.md)

---

## CLAUDE.mdとは

プロジェクトのルートに `CLAUDE.md` を置くと、Claude Codeが**毎回自動的に読み込む**プロジェクト固有の指示書になります。

## 何を書くべきか

CLAUDE.md は**目次と約束だけ**にするのがおすすめです。要件や仕様の中身は `docs/` に、各エージェントの進め方は `.claude/agents/` の定義ファイルに書き、CLAUDE.md からはリンクで指します。

```markdown
# 飲食店予約プラットフォーム

個人経営の飲食店の予約とクチコミを管理する。

- 要件と守る方針: docs/requirements.md（作業の前に必ず読む）
- 基本仕様: docs/spec.md
- 実装の方針（迷ったときの倒し方）: docs/implementation-policy.md
- なぜそう決めたか: docs/decisions/
- ドキュメントの方針: docs/README.md

## よく使うコマンド
- 型検査: `npm run typecheck`
- テスト: `npm test`
- 開発サーバー: `npm run dev`

## 約束
- 詳細設計はソースを正とする。ドキュメントとソースが食い違ったら、ソースを信じる
- バックエンドのコマンドは必ずDocker内で実行する
- 秘密の値はコミットしない（コミット前のフックで止まる。フックを飛ばさない）
- 作業は develop で行う。main は常に動く状態にする
- 各エージェントの役割と進め方は .claude/agents/ の各定義ファイルに書いてある
```

> **なぜ短くするのか？**
> CLAUDE.md はすべての会話とサブエージェントに読み込まれます。長くなるほど、書いた約束が無視されやすくなります。「コミット前にテストとレビューを通す」のような手順は、それを実行するエージェントの定義ファイルに書けば十分です。コードを読めば分かること（命名規則など、フォーマッターやリンターで強制できること）も書かなくて構いません。

## 階層構造

CLAUDE.mdはディレクトリ階層で配置可能。サブディレクトリにもCLAUDE.mdを置けます。

```
my-project/
├── CLAUDE.md                 ← プロジェクト全体のルール
├── frontend/
│   └── CLAUDE.md             ← フロントエンド固有のルール
└── backend/
    └── CLAUDE.md             ← バックエンド固有のルール
```

---

## Hooks（自動化）

### Hooksとは

ツール実行の前後に**自動的にシェルコマンドを実行**する仕組みです。設定は `.claude/settings.json` に書きます。

フックのコマンドには、ツールの入力が**標準入力のJSON**で渡されます（例：編集したファイルのパスは `tool_input.file_path`、Bash のコマンドは `tool_input.command`）。

### 実例1：編集したファイルを自動フォーマット（PostToolUse）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

この設定により、**Claudeがファイルを編集・作成するたびに自動的にPrettierでフォーマット**されます。手動でフォーマットする手間がゼロになります（`jq` が必要です）。

### 実例2：危険なコマンドを止める・確認を求める（PreToolUse）

`PreToolUse` のフックは、ツールが実行される**前**に呼ばれ、実行を止めたり人間の確認を挟んだりできます。

| したいこと | フックの返し方 |
|---|---|
| 止める（deny） | 終了コード **2** で終わり、理由を標準エラーに書く。理由はClaudeに伝わる |
| 人間に確認を求める（ask） | 標準出力に次のJSONを書いて、終了コード 0 で終わる |
| そのまま通す | 何も書かずに終了コード 0 で終わる |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "本番のDBにマイグレーションを適用するコマンドです。"
  }
}
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.mjs\""
          }
        ]
      }
    ]
  }
}
```

例えば「`git commit --no-verify` は止める」「本番へのマイグレーションは確認を求める」といった使い方ができます。コミット前に秘密の値を検査する例は[セキュリティの基本](security.md#コミットガード--秘密の値を機械的に止める)を参照してください。

> **CLAUDE.md に書くこととの違い**: CLAUDE.md の「〜しない」は、Claudeが守ろうとするお願いです。フックは**機械的に必ず**実行されます。絶対に起きてほしくないことはフックで止めましょう。
