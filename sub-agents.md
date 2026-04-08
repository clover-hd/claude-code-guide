# サブエージェント

[< ガイド目次に戻る](README.md)

---

## サブエージェントとは

Claude Codeの最も強力な機能の一つ。**専門的なAIアシスタントを複数定義**して、それぞれに異なる役割・権限・制約を持たせることができます。

各サブエージェントは**独自のコンテキストウィンドウ**で動作するため、メインの会話を汚染せずに独立して作業できます。

## 設定方法

`.claude/agents/` ディレクトリにMarkdownファイルを配置します。

```
.claude/
└── agents/
    ├── system_architect.md     ← 設計責任者
    ├── developer.md            ← フルスタック実装担当
    ├── qa_engineer.md          ← 品質管理
    └── ...                     ← 必要に応じて追加
```

## まず3人から始める — スターター構成

サブエージェントは多ければいいわけではありません。**まずは3エージェントから始めて**、必要に応じて増やすのがおすすめです。

| エージェント | 役割 | できること | できないこと |
|-------------|------|-----------|-------------|
| **system_architect** | 設計責任者 | 設計、API仕様、DB設計 | コードの実装 |
| **developer** | 実装担当 | コーディング、テスト | 設計判断（architectに差し戻す） |
| **qa_engineer** | 品質管理 | テスト作成、バグ報告 | プロダクトコードの編集 |

この3人で「設計→実装→検証」のサイクルが回ります。ソロ開発や小規模チームならこれで十分です。

> **ポイント**: `developer` のdescriptionにはプロジェクトの技術スタックを具体的に書いてください。例えば「React + Express + SQLiteでフルスタック開発を行う」のように。分業が必要になったら下記の「スケールアップ」を参照。

## スケールアップ — プロジェクトが大きくなったら

フロントエンドとバックエンドが分離している、モバイルアプリがある、といった規模になったら分業を広げます。

| エージェント | 追加するタイミング |
|-------------|-------------------|
| **tech_researcher** | ライブラリ選定や技術調査が増えてきたら。Read-Onlyなので安全 |
| **frontend_developer** | フロント/バックが別技術スタックになったら |
| **mobile_developer** | モバイルアプリ開発が始まったら |
| **ui_ux_designer** | デザインシステムの管理が必要になったら |
| **technical_writer** | ドキュメント整備を本格的に進めるとき |

必要になった時点で追加すれば十分です。最初から9エージェント揃える必要はありません。

## エージェント定義ファイルの書き方

```markdown
---
name: tech-researcher
description: 技術調査、ライブラリ選定、バグの原因特定を行う。
             コードの変更は行わず、解決策のみを提案する。
---

# Role (役割)
あなたは**シニア・テクニカル・リサーチャー**です。
あなたの仕事は「実装すること」ではなく、
「実装する方法を見つけること」です。

# Goals (目標)
1. ライブラリ選定: 最適なライブラリを調査・比較する
2. バグ特定: 根本原因(Root Cause)を特定する
3. 技術検証: 技術的な問いに回答する

# Available Tools (利用可能ツール)
- WebSearch, WebFetch, Grep, Glob, Read

# Constraints (制約)
- **Read-Only**: コードを書き換えてはいけない
- **Summarize**: 結論と参照リンクだけを簡潔にまとめる
```

## なぜサブエージェントが強力なのか

1. **専門性**: 各エージェントが自分の領域に集中できる
2. **安全性**: 権限を制限することで、意図しないファイル変更を防止
3. **並列実行**: 複数のエージェントが同時に独立して作業可能
4. **コンテキスト保護**: メインの会話が長大な調査結果で埋まらない

---

## 汎用エージェント vs プロジェクト専用エージェント

GitHubなどにはOSSの汎用エージェント定義が多数公開されています。これらは参考になりますが、**そのままコピーして使うのはおすすめしません**。

### なぜプロジェクト専用に作るべきか

汎用の「developer」エージェントは「一般的な開発」の知識しか持っていません。あなたのプロジェクトの固有ルール — 技術スタック、設計パターン、ディレクトリ構成 — を何も知らない状態で動きます。

```
汎用エージェント:
  「バックエンドを実装できます」
  → でも、あなたのプロジェクトがClean Architectureなのか、
    Prismaを使っているのか、Docker内でコマンドを実行すべきかは知らない
  → 毎回プロジェクトの構成を推測するところから始まる

プロジェクト専用エージェント:
  「Prisma ORM + Clean Architectureでdomain/配下のAPIを実装します」
  → 最初からプロジェクトの文脈の中で動く
  → 参照すべき仕様書のパス、触ってはいけないディレクトリも把握している
```

この差は使えば使うほど効いてきます。

### 参考：OSSのエージェント定義コレクション

GitHubにはサブエージェントの定義集が多数公開されています。「どんな役割分担があるか」「Constraintsをどう書くか」のお手本として活用してください。

#### 企業公式のエージェント・スキル定義

有名企業が自社フレームワーク向けの公式エージェント/スキル定義を公開しています。「プロが実際にどう書いているか」の最良のお手本です。

| リポジトリ | 内容 |
|-----------|------|
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | **Vercel公式**のエージェントスキル集 |
| [vercel/next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md) | Next.js公式のAIエージェント向け指示書（CLAUDE.mdの実例） |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | Anthropic, Vercel, Stripe, Cloudflare, Sentry, Expo等の**公式スキル + コミュニティスキル** 380以上を集約 |

> **Tip**: Next.jsプロジェクトでは `npx @next/codemod agents-md` を実行すると、プロジェクトのNext.jsバージョンに合ったドキュメントインデックスをCLAUDE.mdに自動生成してくれます。

#### コミュニティのエージェント定義集

| リポジトリ | 内容 |
|-----------|------|
| [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 100以上の専門エージェントをカテゴリ別に整理。インストールスクリプト付き |
| [claude-code-subagents](https://github.com/0xfurai/claude-code-subagents) | 100以上のプロダクションレディなエージェント集 |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | エージェントだけでなくスキル、Hooks、MCPプラグインも含むキュレーションリスト |
| [awesome-claude-agents](https://github.com/rahulvrane/awesome-claude-agents) | コミュニティ投稿型のエージェント・フレームワーク集 |
| [agents (wshobson)](https://github.com/wshobson/agents) | 112エージェント + 16ワークフローオーケストレーターの本格的なマルチエージェントシステム |

> **重要**: これらはあくまで**構造と書き方の参考**です。そのままコピーしても「あなたのプロジェクト」のことは何も知らないエージェントにしかなりません。以下の手順でプロジェクト専用にカスタマイズしましょう。

### 推奨：OSSを参考にしつつ、Claude Codeに作らせる

ゼロから手書きする必要はありません。**OSSのエージェント定義を「お手本」としてClaudeに渡し、プロジェクト専用版を生成させる**のが最も効率的で正確です。

Claudeはプロジェクトのコードベースを実際に読んだ上でエージェントを作るため、手書きでは見落としがちなディレクトリ構成や依存関係も正確に反映してくれます。

### 実践の流れ

```
Step 1: OSSのエージェント定義を探して読む
        → 「こういう役割分担やConstraintsの書き方があるのか」を知る

Step 2: プロジェクトのアーキテクチャを決める（Phase A4）
        → 技術スタック、設計パターン、ディレクトリ構成が確定

Step 3: Claude Codeに指示してエージェントを生成する（↓下記参照）
        → コードベースを読んだ上でプロジェクト専用のエージェントが完成
```

### Claude Codeへの指示例

```
あなた: サブエージェントを作りたい。
        以下のOSSのエージェント定義を参考にして、
        このプロジェクト専用のdeveloperエージェントを作って。

        【参考にしたいOSSの定義】
        （ここにOSSのエージェント定義を貼る）

        このプロジェクトのアーキテクチャは docs/architecture.md を見て。
        CLAUDE.md のルールも反映して。
        .claude/agents/developer.md に保存して。

Claude: コードベースを確認しました。
        - 技術スタック: React + Express + SQLite + TypeScript
        - 設計パターン: Clean Architecture
        - ディレクトリ: src/domain/, src/infrastructure/, src/interface/
        - テスト: Jest, tests/unit/ 配下

        これらを反映したエージェント定義を作成します...
        （.claude/agents/developer.md を生成）
```

Claudeはプロジェクトの実際のコードを読んだ上で、OSSの構造をベースにしつつ以下を自動的に反映します：

- プロジェクト固有の技術スタック名
- 実際のディレクトリ構成に基づく分業の境界
- 参照すべき仕様書・設計書のパス
- CLAUDE.mdに書かれたルールとの整合性

### 生成結果の例（汎用 → プロジェクト専用）

```markdown
# 汎用（OSSから取得した元の定義）
---
name: backend-developer
description: バックエンドAPIを構築する
---
# Role
バックエンド開発の専門家。
# Constraints
- フロントエンドのコードは触らない

# ↓ Claude Codeがプロジェクト固有に生成 ↓

---
name: backend-developer
description: Express + Prisma でAPIを構築する。Clean Architectureに従う。
---
# Role
Node.js (Express), MySQL, Prisma ORM のスペシャリスト。

# Goals
1. docs/specs/ の仕様に従ってAPIを実装する
2. src/domain/ のClean Architectureパターンを維持する
3. テストは tests/unit/ に Jest で作成する

# Constraints
- src/mobile/ 配下のコードは一切触らない
- DBスキーマの変更が必要な場合は system_architect に差し戻す
- 環境変数は .env.example を参照し、ハードコードしない

# References
- docs/architecture.md — アーキテクチャ全体像
- docs/specs/api/ — APIエンドポイント仕様
```

汎用版の3行が、プロジェクトのコードベースを実際に読んだClaude Codeの手によって、「このプロジェクトの中で何をすべきか」を正確に理解するエージェントに変換されます。

> **ポイント**: 生成後に中身を確認して、不足があれば「Constraintsに○○を追加して」と追加指示するだけ。最初から完璧を目指す必要はなく、使いながら育てていけばOKです。
