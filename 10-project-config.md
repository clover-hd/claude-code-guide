# CLAUDE.md・Hooks によるプロジェクト設定

[< ガイド目次に戻る](README.md)

---

## CLAUDE.mdとは

プロジェクトのルートに `CLAUDE.md` を置くと、Claude Codeが**毎回自動的に読み込む**プロジェクト固有の指示書になります。

## 何を書くべきか

```markdown
# CLAUDE.md

## プロジェクト概要
- このプロジェクトは○○です
- 技術スタック: React, Express, MySQL

## 重要なルール
- バックエンドコマンドは必ずDocker内で実行
- テストは必ずパスさせてからコミット

## ディレクトリ構成
- src/domain/ - ドメインロジック
- src/interface/ - APIエンドポイント

## コーディング規約
- 変数名はcamelCase
- 関数名は動詞で始める
```

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

ツール実行の前後に**自動的にシェルコマンドを実行**する仕組みです。

### 実例：Hooks設定

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

この設定により、**Claudeがファイルを編集するたびに自動的にPrettierでフォーマット**されます。手動でフォーマットする手間がゼロになります。
