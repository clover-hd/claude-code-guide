# スキル（Skills）

[< ガイド目次に戻る](README.md)

---

## スキルとは

**スキル（Skills）** は、Claudeに専門知識や手順をテンプレートとして持たせ、`/スキル名` で呼び出せる機能です。

> **注意**: 旧バージョンでは `.claude/commands/` にMarkdownファイルを置く方式でしたが、最新版では **`.claude/skills/` ディレクトリに `SKILL.md` を配置する方式が推奨**されています。旧方式も後方互換で動作しますが、新規作成はskills形式で行いましょう。

## 設定方法

`.claude/skills/<スキル名>/SKILL.md` の構造で配置します。

```
.claude/
└── skills/
    ├── commit/
    │   └── SKILL.md         ← /commit で呼び出し
    └── consult/
        ├── SKILL.md         ← /consult で呼び出し
        └── examples.md      ← 補助ファイル（任意）
```

旧形式との比較：

| | 旧形式（commands） | 新形式（skills）推奨 |
|--|-------------------|---------------------|
| **配置場所** | `.claude/commands/commit.md` | `.claude/skills/commit/SKILL.md` |
| **補助ファイル** | 不可 | 可（テンプレート、スクリプト等を同梱） |
| **呼び出し制御** | 限定的 | frontmatterで柔軟に制御可能 |
| **自動呼び出し** | Claudeが判断 | `disable-model-invocation` で制御可 |

## スキル定義の書き方（SKILL.md）

```markdown
---
name: commit
description: プロジェクトルールに従ったgitコミットを実行する
disable-model-invocation: true   # ユーザーのみ呼び出し可（副作用ありのため）
---

# /commit - プロジェクト専用コミットスキル

## ルール
1. 1コミット = 1論理的変更
2. Conventional Commits形式: feat:, fix:, chore:, refactor:, docs:
...
```

frontmatterの主要フィールド：

| フィールド | 説明 |
|-----------|------|
| `name` | スキル名（`/name` で呼び出し） |
| `description` | Claudeがいつ使うか判断するための説明 |
| `disable-model-invocation: true` | ユーザーのみ呼び出し可（デプロイ等の副作用ある操作に） |
| `user-invocable: false` | Claudeのみ使用（バックグラウンド知識の提供に） |

## スキルの配置スコープ

| スコープ | 配置場所 | 効果範囲 |
|---------|---------|---------|
| **個人** | `~/.claude/skills/<name>/SKILL.md` | 自分の全プロジェクト |
| **プロジェクト** | `.claude/skills/<name>/SKILL.md` | このプロジェクトのみ |

個人スキルは自分専用のショートカット、プロジェクトスキルはチーム共有のルールとして使い分けます。

## 実例1：/commit（プロジェクト専用コミット）

コミットルールをスキルとして定義する例です。

```markdown
---
name: commit
description: プロジェクトルールに従ったgitコミットを実行する
disable-model-invocation: true
---

# /commit - プロジェクト専用コミットスキル

## ルール
1. 1コミット = 1論理的変更
2. Conventional Commits形式: feat:, fix:, chore:, refactor:, docs:
3. Co-Authored-By追加
4. git add -A は避け、ファイルを明示的に指定

## 手順
### 1. 変更状況の確認
git status / git diff --stat / git log --oneline -5

### 2. 変更のグループ化
変更内容を論理的単位でグループ化

### 3. グループごとにコミット
関連ファイルをステージング → HEREDOCでコミット
```

**使い方**: ターミナルで `/commit` と打つだけ。Claudeが自動的にルールに従ってコミットを実行します。

## 実例2：/consult（サービス要件相談）

```markdown
---
name: consult
description: サービスの要件・企画レベルの相談を行う
---

# /consult - サービス要件相談

## 前提知識の読み込み
1. サービス要件書を読み込む
2. 機能実装状況を把握する

## 相談相手としての振る舞い
- 対等な立場で議論する
- 良いアイデアは素直に認める
- 懸念点があれば率直に伝える
```

**使い方**: `/consult` と打つと、Claudeがサービス仕様を読み込んだ上で企画パートナーとして相談に乗ってくれます。

## skillsの強み：補助ファイル

commands形式との最大の違いは、**補助ファイルを同梱**できること。

```
.claude/skills/review/
├── SKILL.md           ← メインの指示
├── checklist.md       ← レビューチェックリスト
├── examples.md        ← 良い/悪いレビューの例
└── scripts/
    └── lint-check.sh  ← 自動実行スクリプト
```

`SKILL.md` を簡潔に保ちつつ、詳細はファイルに分離できます。

## スキルの活用アイデア

| スキル名 | 用途 | `disable-model-invocation` |
|----------|------|---------------------------|
| `/commit` | プロジェクトルールに従ったコミット | `true`（副作用あり） |
| `/review` | コードレビュー | `false` |
| `/test` | テスト生成＆実行 | `false` |
| `/deploy` | デプロイ手順の実行 | `true`（副作用あり） |
| `/consult` | サービス企画の壁打ち | `false` |
