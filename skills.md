# スキル（Skills）

[< ガイド目次に戻る](README.md)

---

## スキルとは

**スキル（Skills）** は、Claudeに専門知識や手順をテンプレートとして持たせ、`/スキル名` で呼び出せる機能です。

> **注意**: 以前は `.claude/commands/` にMarkdownファイルを置く方式（カスタムコマンド）でしたが、今はスキルに統合されています。`.claude/commands/deploy.md` と `.claude/skills/deploy/SKILL.md` は、どちらも `/deploy` になり、同じように動きます。既存の commands もそのまま使えますが、補助ファイルを置けるなどの利点があるので、新しく作るならskills形式がおすすめです。

## 設定方法

`.claude/skills/<スキル名>/SKILL.md` の構造で配置します。

```
.claude/
└── skills/
    ├── commit/
    │   └── SKILL.md         ← /commit で呼び出し
    ├── consult/
    │   ├── SKILL.md         ← /consult で呼び出し
    │   └── examples.md      ← 補助ファイル（任意）
    ├── ask-advisor/
    │   └── SKILL.md         ← /ask-advisor で呼び出し
    ├── task/
    │   └── SKILL.md         ← /task で呼び出し
    ├── overnight/
    │   └── SKILL.md         ← /overnight で呼び出し
    └── handoff/
        └── SKILL.md         ← /handoff で呼び出し
```

> `/kickstart` で作るプロジェクトには、この6つのスキルが入ります。中身は [kickstart スキル](skills/kickstart/SKILL.md) の A2 と A7 を参照してください。

旧形式との比較：

| | 旧形式（commands） | 新形式（skills）推奨 |
|--|-------------------|---------------------|
| **配置場所** | `.claude/commands/commit.md` | `.claude/skills/commit/SKILL.md` |
| **補助ファイル** | 不可 | 可（テンプレート、スクリプト等を同梱） |
| **frontmatter** | `name` と `paths` 以外は同じものが使える | すべて使える |
| **同じ名前があるとき** | — | skills の方が優先される |

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
| `argument-hint` | `/name` の後に入れる引数のヒント。本文では `$ARGUMENTS` で受け取る |
| `context: fork` | メインの会話とは別のコンテキストで実行する |
| `agent` | `context: fork` のときに使うサブエージェント |
| `background` | `context: fork` のときだけ使う。既定は `true` で、バックグラウンドで動き、結果は後から届く。`false` にすると、その場で結果を待つ |

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
description: サービスの要件・企画レベルの相談に乗る。新しい機能や画面のアイデアを、作るかどうか・何を作るかを決める前に壁打ちしたいときに使う。どう実装するかの相談には使わない。
---

# /consult - サービス要件相談

## 前提知識の読み込み
1. docs/requirements.md（要件と守る方針）
2. docs/spec.md（基本仕様。あれば）
3. docs/decisions/ のうち、相談に関わる過去の判断（あれば）

## 相談相手としての振る舞い
- 対等な立場で議論する
- 良いアイデアは素直に認める
- 懸念点があれば率直に伝える
```

**使い方**: `/consult` と打つと、Claudeがサービス仕様を読み込んだ上で企画パートナーとして相談に乗ってくれます。

## 実例3：/ask-advisor（サブエージェントに相談を投げる）

`context: fork` と `agent:` を組み合わせると、スキルの中身を**指定したサブエージェントに、別のコンテキストで**実行させられます。相談の過程でメインの会話が埋まりません。

`context: fork` のスキルは、既定ではバックグラウンドで動き、結果は後から届きます。相談の答えを見てから次に進みたいので、`background: false` を付けてその場で待つようにしています。

```markdown
---
name: ask-advisor
description: advisor に相談する。方針、データの形、画面の流れ、使い心地が変わる選択で迷ったとき。区切りの全体レビューを頼むときにも使う。
argument-hint: [相談したいこと、または「区切りのレビュー」]
context: fork
agent: advisor
background: false
---

# /ask-advisor - advisor に相談する

次の相談に答えてください。

$ARGUMENTS

- 相談の場合は、結論、理由、退けた案、見直す条件、記録の下書きの形で答えてください
- 「区切りのレビュー」と書かれている場合は、前回の区切りからの変化を全体レビューしてください
```

**使い方**: `/ask-advisor 予約のキャンセル期限をユーザーごとに変えられるようにすべき？` のように打ちます。advisor エージェントについては[サブエージェント](sub-agents.md)を参照してください。

## 実例4：手順書スキル（取り返しのつかない操作）

本番へのデプロイ、DBのマイグレーション、秘密の値の登録など、**間違えると戻せない操作**は、手順をスキルにしておきます。順番を飛ばさないことと、本番の前に人間の確認を取ることを手順に書き込むのがポイントです。

```markdown
---
name: db-migrate
description: DBのマイグレーションを、手元 → ステージング → 本番の順に適用する。スキーマを変えたときに使う。本番に適用する前には、必ず人間の確認を取る。
argument-hint: "[local|staging|production]"
---

# DBのマイグレーション

データベースの変更は取り返しがつきません。順番を飛ばさないでください。

## 前提
- 環境の名前や接続先は <設定ファイル> を正とする
- ステージングと本番が同じDBを指していないか、最初に確かめる

## 1. マイグレーションを作り、SQLを読む（データが消える変更なら止めて人間に知らせる）
## 2. 手元に適用して、テストを通す
## 3. ステージングに適用して、確かめる
## 4. 本番に適用する（必ず人間の確認を取る）
適用するファイル、データが消える変更の有無、ステージングでの結果を人間に示し、了解を得てから実行する

## うまくいかなかったとき
- <戻し方。戻せないなら、そう書く>
```

手順書に書くだけでなく、同じコマンドを `PreToolUse` フックの「確認を求める（ask）」対象にもしておくと、手順書を通らずに実行されたときにも人間の確認が挟まります（[Hooks](project-config.md#hooks自動化)参照）。

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
| `/ask-advisor` | advisor エージェントへの相談・区切りのレビュー | `false` |
| `/task` | タスクを見る・増やす・閉じる | `false` |
| `/overnight` | 寝ている間に、任せたタスクを順に実装する | `true`（人間が打ったときだけ夜用の動きに入る） |
| `/handoff` | クリアの前に今の状態を残し、再開用のプロンプトを出す | `true`（人間が打ったときだけ） |
