# /kickstart スキル — プロジェクト立ち上げを自動化する

[< ガイド目次に戻る](README.md)

---

## これは何？

[Phase A：プロジェクトの立ち上げ](workflow-setup.md)の手順（A0〜A8）を、Claude Codeが対話しながら順番に進めてくれるスキルです。

ガイドを読みながら手動で進めることもできますが、`/kickstart` を使えば **Claude Code自身がガイドの手順を把握した状態で、あなたと一緒にプロジェクトの土台を作ってくれます**。

### スキルが自動でやること

[Phase Aの手順](workflow-setup.md)（A0〜A8）を、Claude Codeが対話形式で順番に進めてくれます。具体的には：

- プロジェクトの初期化（`.gitignore`、docs/ の構成とドキュメントの方針、git init）
- 要件（守る方針・作らないもの）の言語化と壁打ち
- 基本仕様と実装の方針（迷ったときの倒し方）の決定と記録
- CLAUDE.md（目次と約束）、サブエージェント4人、スキルの構築
- 秘密の値のコミットを止めるコミットガードの設定
- 初期コミット

各ステップの詳細は[workflow-setup.md](workflow-setup.md)を参照してください。

## セットアップ

### 方法1：個人スキルとしてインストール（全プロジェクトで使える）

```bash
# スキルディレクトリを作成してダウンロード
mkdir -p ~/.claude/skills/kickstart
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/skills/kickstart/SKILL.md \
  -o ~/.claude/skills/kickstart/SKILL.md
```

これで**どのプロジェクトでも** `/kickstart` が使えるようになります。

### 方法2：プロジェクトスキルとしてインストール（特定プロジェクトのみ）

```bash
# プロジェクトルートで実行
mkdir -p .claude/skills/kickstart
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/skills/kickstart/SKILL.md \
  -o .claude/skills/kickstart/SKILL.md
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
        ✓ docs/README.md（ドキュメントの方針）
        ✓ docs/decisions/
        ✓ docs/_wip/
        ✓ git init

        では A1：要件ドキュメントを作りましょう。
        何を作りたいですか？一言で教えてください。

あなた: 飲食店の予約とクチコミを管理するプラットフォーム

Claude: いいですね。いくつか掘り下げさせてください。
        - ターゲットは？（店舗側？ユーザー側？両方？）
        - このサービスだから「守る方針」は何ですか？
        - 似たサービスと比べて、あえて「作らないもの」は？
        ...
```

Claudeが各ステップで質問し、回答をもとにドキュメントとファイルを作成していきます。

### 4. ステップごとに確認

各ステップの完了時にClaudeが確認を取ります。**納得してから次に進んでください**。

```
Claude: docs/requirements.md を作成しました。
        内容を確認してください。修正があれば言ってください。
        OKなら次のステップ（A2：/consult スキル作成）に進みます。

あなた: MVPに検索機能も入れたい

Claude: 了解です。検索機能を追加して更新しました。
        （docs/requirements.md を更新）
        これでOKですか？

あなた: OK、次に進もう
```

### 5. モデル切り替えの案内

A4（基本仕様）とA4.5（実装の方針）ではOpusへの切り替えが案内されます。

```
Claude: 次はA4：基本仕様の決定です。
        深い設計判断が必要なので、Opusへの切り替えをおすすめします。
        /model opus で切り替えてから続けてください。
```

A5以降ではSonnetに戻す案内が出ます。コスト節約のため、案内に従ってモデルを切り替えてください。

### 6. 完了

全ステップ（A0〜A8）が終わると、以下のファイルが揃います：

```
my-new-project/
├── CLAUDE.md                              ← 目次と約束だけの指示書
├── .gitignore                             ← セキュリティ基本設定
├── .githooks/pre-commit                   ← 人間のコミットも検査する
├── scripts/check-staged.sh                ← 秘密の値・DBファイルの検査
├── docs/
│   ├── README.md                          ← ドキュメントの方針（どこに何を書くか）
│   ├── requirements.md                    ← 要件と守る方針
│   ├── spec.md                            ← 基本仕様（変わりにくい骨格だけ）
│   ├── implementation-policy.md           ← 実装の方針（迷ったときの倒し方）
│   ├── decisions/                         ← なぜそう決めたか（1判断1ファイル）
│   └── _wip/                              ← 実装中の詳細設計（終わったら移すか削除）
└── .claude/
    ├── settings.json                      ← フックの登録
    ├── hooks/guard-bash.mjs               ← エージェントのコミットを検査する
    ├── skills/
    │   ├── consult/SKILL.md               ← 要件相談スキル
    │   ├── ask-advisor/SKILL.md           ← advisor への相談
    │   └── commit/SKILL.md                ← コミットスキル
    └── agents/
        ├── advisor.md                     ← 相談役・区切りの全体レビュー（読み取り専用）
        ├── developer.md                   ← 実装担当
        ├── qa-engineer.md                 ← テスト担当
        └── code-reviewer.md               ← コミットごとの軽いレビュー
```

> **Note**: エージェントはまず4人から始め、プロジェクトの成長に合わせて追加します。advisor のモデルは既定で Opus です。Fable に切り替える方法は[サブエージェント](sub-agents.md#advisor-に-fable-を使う)を参照。
> フックはA4で決めた言語で作られます（Node.js なら `guard-bash.mjs`、Python なら `guard_bash.py`）。A8の手順書スキルを作った場合は `.claude/skills/` に追加されます。

Claudeが**Phase Bへの移行ガイド**（日常の開発サイクル、モデルの使い分け、コンテキスト管理のコツ）を表示して完了です。

**ここから Phase B（日常の開発サイクル）に入れます。**

## 各ステップの概要

各ステップの詳しい内容と考え方は [Phase A：プロジェクトの立ち上げ](workflow-setup.md) で解説しています。

| ステップ | 内容 | モデル推奨 |
|----------|------|-----------|
| **A0** | 自動初期化（.gitignore, ディレクトリ, git init） | — |
| **A1** | 要件 — 何を作るか、守る方針、作らないもの | Sonnet |
| **A2** | /consult スキル — 相談相手を作る | Sonnet |
| **A3** | 要件の壁打ち — MVP・優先順位を固める | Sonnet |
| **A4** | 基本仕様 — 技術構成・ブランチ運用・コマンド | **Opus** |
| **A4.5** | 実装の方針 — 迷ったときの倒し方 | **Opus** |
| **A5** | CLAUDE.md — 目次と約束 | Sonnet |
| **A6** | サブエージェント — advisor / developer / qa-engineer / code-reviewer | Sonnet |
| **A7** | スキル・コミットガード・初期コミット | Sonnet |
| **A8** | 手順書スキル（任意） — 取り返しのつかない操作 | Sonnet |

## よくある質問

### 途中で中断しても大丈夫？

大丈夫です。`claude --continue` で前回のセッションを再開すれば、途中から続けられます。ただし、セッションが古くなっている場合は `/clear` してから「A5から再開したい。docs/ の requirements.md、spec.md、implementation-policy.md を読んで」と伝えれば、途中のステップから再開できます。

### A1〜A3はスキップして、A4から始めたい

既に要件が決まっている場合は：

```
> /kickstart
> 要件は docs/requirements.md に書いてある。
  A4の基本仕様の決定から始めたい。
```

Claudeが既存ドキュメントを読み込んでA4から進めてくれます。

### 全ステップを1セッションでやる必要がある？

ありません。むしろ**A1〜A3は1日目、A4〜A8は2日目**くらいのペースがおすすめです。要件を一晩寝かせると、翌日に「あ、これも必要だった」と気づくことが多いです。

### 作られたエージェントやスキルが微妙だったら？

そのまま手動で `.claude/agents/` や `.claude/skills/` のファイルを編集してください。もしくはClaude Codeに「developerの相談の範囲に○○を追加して」と指示すれば修正してくれます。プロジェクト設定は使いながら育てるものです。

### .gitignore の内容を変更したい

A0で作成される `.gitignore` は汎用的な内容です。プロジェクトの技術スタックが決まった後（A4以降）で、必要に応じて追記してください。例えばPython系なら `__pycache__/` や `.venv/` を追加するなど。
