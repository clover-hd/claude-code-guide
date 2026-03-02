# /kickstart スキル — プロジェクト立ち上げを自動化する

[< ガイド目次に戻る](README.md)

---

## これは何？

[Phase A：プロジェクトの立ち上げ](05-workflow-setup.md)の手順（A0〜A7）を、Claude Codeが対話しながら順番に進めてくれるスキルです。

ガイドを読みながら手動で進めることもできますが、`/kickstart` を使えば **Claude Code自身がガイドの手順を把握した状態で、あなたと一緒にプロジェクトの土台を作ってくれます**。

### スキルが自動でやること

- `.gitignore` の作成（セキュリティ基本設定）
- ドキュメント用ディレクトリの作成（`docs/specs/`, `docs/architecture-decisions/`）
- git初期化（未初期化の場合）
- 各ステップに適したモデル（Opus/Sonnet）の切り替え案内
- 対話結果のドキュメント化と永続化
- `/consult`, `/commit` スキルの作成
- サブエージェントチームの構築
- 初期コミット

## セットアップ

### 方法1：個人スキルとしてインストール（全プロジェクトで使える）

```bash
# スキルディレクトリを作成
mkdir -p ~/.claude/skills/kickstart

# SKILL.mdをコピー
cp /path/to/claude-code-guide/skills/kickstart/SKILL.md ~/.claude/skills/kickstart/SKILL.md
```

これで**どのプロジェクトでも** `/kickstart` が使えるようになります。

### 方法2：プロジェクトスキルとしてインストール（特定プロジェクトのみ）

```bash
# プロジェクトルートで実行
mkdir -p .claude/skills/kickstart

# SKILL.mdをコピー
cp /path/to/claude-code-guide/skills/kickstart/SKILL.md .claude/skills/kickstart/SKILL.md
```

> **おすすめは方法1**です。kickstartは新しいプロジェクトを始めるたびに使うものなので、個人スキルとして常に使える状態にしておくと便利です。

## 使い方

### 1. 新しいプロジェクトを作成して起動

```bash
mkdir my-new-project && cd my-new-project
claude
```

> `git init` は不要です。スキルが自動で初期化します。

### 2. /kickstart を実行

```
> /kickstart
```

Claudeがまず**A0（自動初期化）**として `.gitignore` やディレクトリ構成を作成し、その後A1から対話を始めます。

### 3. 対話しながら進める

```
Claude: プロジェクトの初期ファイルを作成しました。
        ✓ .gitignore
        ✓ docs/specs/
        ✓ docs/architecture-decisions/
        ✓ git init

        では A1：サービス概要を作りましょう。
        何を作りたいですか？一言で教えてください。

あなた: 飲食店の予約とクチコミを管理するプラットフォーム

Claude: いいですね。いくつか掘り下げさせてください。
        - ターゲットは？（店舗側？ユーザー側？両方？）
        - 「大切にしたいこと」は何ですか？
        ...
```

Claudeが各ステップで質問し、回答をもとにドキュメントとファイルを作成していきます。

### 4. ステップごとに確認

各ステップの完了時にClaudeが確認を取ります。**納得してから次に進んでください**。

```
Claude: docs/service-overview.md を作成しました。
        内容を確認してください。修正があれば言ってください。
        OKなら次のステップ（A2：/consult スキル作成）に進みます。

あなた: MVPに検索機能も入れたい

Claude: 了解です。検索機能を追加して更新しました。
        （docs/service-overview.md を更新）
        これでOKですか？

あなた: OK、次に進もう
```

### 5. モデル切り替えの案内

A4（アーキテクチャ決定）ではOpus 4.6への切り替えが案内されます。

```
Claude: 次はA4：アーキテクチャ決定です。
        深い設計判断が必要なので、Opus 4.6への切り替えをおすすめします。
        /model opus で切り替えてから続けてください。
```

A5以降ではSonnet 4.6に戻す案内が出ます。コスト節約のため、案内に従ってモデルを切り替えてください。

### 6. 完了

全ステップ（A0〜A7）が終わると、以下のファイルが揃います：

```
my-new-project/
├── CLAUDE.md                              ← Claudeへの指示書（200行以内）
├── .gitignore                             ← セキュリティ基本設定
├── docs/
│   ├── service-overview.md                ← サービス概要
│   ├── architecture.md                    ← アーキテクチャ・技術スタック
│   ├── specs/                             ← 機能仕様書の保存先（Phase Bで使用）
│   └── architecture-decisions/            ← 技術判断の記録（ADR）
└── .claude/
    ├── skills/
    │   ├── consult/SKILL.md               ← 要件相談スキル
    │   └── commit/SKILL.md                ← コミットスキル
    └── agents/
        ├── system_architect.md            ← 設計責任者
        ├── tech_researcher.md             ← 技術調査
        ├── backend_developer.md           ← バックエンド（例）
        ├── frontend_developer.md          ← フロントエンド（例）
        ├── qa_engineer.md                 ← 品質管理
        └── technical_writer.md            ← ドキュメント管理
```

Claudeが**Phase Bへの移行ガイド**（日常の開発サイクル、モデルの使い分け、コンテキスト管理のコツ）を表示して完了です。

**ここから Phase B（日常の開発サイクル）に入れます。**

## 各ステップの概要

| ステップ | 内容 | モデル推奨 |
|----------|------|-----------|
| **A0** | 自動初期化（.gitignore, ディレクトリ, git init） | — |
| **A1** | サービス概要ドキュメント作成 | Sonnet |
| **A2** | /consult スキル作成 | Sonnet |
| **A3** | /consult で要件を壁打ち | Sonnet |
| **A4** | アーキテクチャ決定（技術スタック選定） | **Opus** |
| **A5** | CLAUDE.md 作成 | Sonnet |
| **A6** | サブエージェント作成 | Sonnet |
| **A7** | /commit スキル・Hooks・テスト戦略・初期コミット | Sonnet |

## よくある質問

### 途中で中断しても大丈夫？

大丈夫です。`claude --continue` で前回のセッションを再開すれば、途中から続けられます。ただし、セッションが古くなっている場合は `/clear` してから「A4から再開したい。docs/service-overview.md と docs/architecture.md を読んで」と伝えれば、途中のステップから再開できます。

### A1〜A3はスキップして、A4から始めたい

既にサービス概要や要件が決まっている場合は：

```
> /kickstart
> サービス概要は docs/service-overview.md に書いてある。
  A4のアーキテクチャ決定から始めたい。
```

Claudeが既存ドキュメントを読み込んでA4から進めてくれます。

### 全ステップを1セッションでやる必要がある？

ありません。むしろ**A1〜A3は1日目、A4〜A7は2日目**くらいのペースがおすすめです。要件を一晩寝かせると、翌日に「あ、これも必要だった」と気づくことが多いです。

### 作られたエージェントやスキルが微妙だったら？

そのまま手動で `.claude/agents/` や `.claude/skills/` のファイルを編集してください。もしくはClaude Codeに「backend_developerのConstraintsに○○を追加して」と指示すれば修正してくれます。プロジェクト設定は使いながら育てるものです。

### .gitignore の内容を変更したい

A0で作成される `.gitignore` は汎用的な内容です。プロジェクトの技術スタックが決まった後（A4以降）で、必要に応じて追記してください。例えばPython系なら `__pycache__/` や `.venv/` を追加するなど。
