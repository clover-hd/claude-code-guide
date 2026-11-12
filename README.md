[🇺🇸 English](README.en.md)

# Claude Code 使い方ガイド

---

## はじめに

このガイドは、Claude Codeを使った開発の全体像をまとめたものです。各セクションの詳細はリンク先の個別ファイルを参照してください。

> **おすすめの進め方**: [インストール](setup.md) → [チュートリアル](tutorial.md) → [ウォークスルー](walkthrough.md) → 残りは必要に応じて参照

---

## 目次

### はじめの一歩

| セクション | 内容 |
|-----------|------|
| [インストール・初期設定](setup.md) | macOS/Linux/Windows(WSL)でのセットアップ手順 |
| [最初の30分チュートリアル](tutorial.md) | インストール後すぐに手を動かして「ニヤリとする瞬間」を体験する |
| [ウォークスルー：おでかけプランナーを作る](walkthrough.md) | /kickstart → Phase A → Phase B の流れを実際のプロジェクトで体験する |

### Claude Codeの基本

| セクション | 内容 |
|-----------|------|
| [Claude Codeとは・基本操作](overview.md) | 何ができるか、**権限モードと承認の注意事項**、よく使うコマンド |
| [モデルの違いと選び方](models.md) | Fable/Opus/Sonnet/Haikuの使い分け、ワークフロー別の選び方 |

### 開発ワークフロー

| セクション | 内容 |
|-----------|------|
| [Phase A：プロジェクトの立ち上げ](workflow-setup.md) | ゼロからの土台作り（A0〜A8の依存関係付き手順。タスクの置き場所もここで決める） |
| [Phase B：日常の開発サイクル](workflow-daily.md) | タスク選択→consult→Plan→永続化→実装→テスト→commit→区切りの流れ。寝ている間に進める `/overnight` |

### Claude Codeの拡張機能

| セクション | 内容 |
|-----------|------|
| [サブエージェント](sub-agents.md) | 専門AIチームの構築 |
| [スキル（Skills）](skills.md) | `/commit`, `/consult`, `/task`, `/overnight` 等のテンプレート化（新SKILL.md形式） |
| [MCPサーバー](mcp.md) | 外部ツール連携（Sequential Thinking, Serena, Context7） |
| [CLAUDE.md・Hooks](project-config.md) | プロジェクト設定ファイルと自動化 |

### 実践ガイド

| セクション | 内容 |
|-----------|------|
| [実践的なノウハウ](best-practices.md) | 検証手段、コンテキスト管理、セッション管理、アンチパターン等12項目 |
| [セキュリティの基本](security.md) | コミット禁止ファイル、Claudeに渡してはいけない情報、.gitignore |
| [デバッグの進め方](debugging.md) | エラー調査パターン、ログ分析、再現テスト駆動 |
| [コスト・トークン管理](cost.md) | プラン料金、使用制限、トークン節約テクニック |

### カスタマイズ

| セクション | 内容 |
|-----------|------|
| [ステータスライン](statusline.md) | リアルタイムで使用率・コンテキスト残量・ブランチを表示するカスタムステータスバー |
| [/kickstart スキル](kickstart-skill.md) | 新プロジェクトの立ち上げをClaudeが対話で案内。Phase A（A0〜A8）を自動化 |

> `/kickstart` のスキル定義ファイルは [skills/kickstart/SKILL.md](skills/kickstart/SKILL.md) にあります。

### その他

| セクション | 内容 |
|-----------|------|
| [エージェントチーム クイックデモ](examples/team-demo-quick.md) | Phase A完了後にAIチームの並列開発を10分で見せるデモ手順 |
| [トラブルシューティング / FAQ](troubleshooting.md) | レート制限、ハルシネーション、同じ間違いの繰り返し等への対処法 |
| [用語集](glossary.md) | コンテキストウィンドウ、トークン、ハルシネーション等の用語解説 |

---

## クイックリファレンス

### よく使うコマンド

| コマンド | 説明 |
|----------|------|
| `/model sonnet` | Sonnetに切り替え（日常使いはこれ） |
| `/model opus` | Opusに切り替え（複雑な設計時） |
| `Shift + Tab` | 操作モードを切り替え（auto → 手動 → Auto-Accept → Plan Mode） |
| `/plan` | Plan Mode に入る |
| `/clear` | コンテキストをリセット |
| `/compact` | 会話を圧縮してコンテキスト延命 |
| `/init` | CLAUDE.mdを自動生成 |
| `Esc` | 実行中のタスクを中断 |
| `Esc + Esc` | チェックポイント選択（巻き戻し） |

### 日常の開発サイクル（Phase B 要約）

```
0. /task       → 次にやるタスクを選ぶ（新しい案は /task add）
1. /consult     → 何を作るか壁打ち
2. /plan        → Plan Modeで設計
2.5. 永続化     → 計画を docs/_wip/ に詳細設計として保存して止まる
3. developer   → /clear して @agent-developer に実装を頼む
3.5. テスト     → ユニットテスト & E2Eテスト
4. /commit      → レビューを通してコミット
5. 区切り       → /ask-advisor で全体レビュー、docs/_wip/ を片付け、/task done

寝る前       → /overnight で任せたタスクを朝まで進める
               判断が要る点は「人間の判断待ち」に残して先へ進む
```

### モデル使い分けの目安

```
日常コーディング・バグ修正     → Sonnet（まずはこれ）
大規模設計・複雑なリファクタ   → Opus
方針を左右する難しい判断       → Fable（プランによっては usage credits から引かれる）
簡単な質問・定型作業           → Haiku
```

> バージョン番号や価格は新しいモデルが出るたびに変わるので、このガイドには書いていません。`/model sonnet` のように系統名で指定すると、その系統の最新モデルが使われます。

---

## まとめ

| 機能 | 何ができるか | 設定場所 |
|------|-------------|----------|
| **モデル切替** | タスクに応じて性能/コストを最適化 | `/model` コマンド |
| **サブエージェント** | 専門AIチームの構築 | `.claude/agents/*.md` |
| **スキル** | よく使う操作のテンプレート化 | `.claude/skills/<name>/SKILL.md` |
| **MCPサーバー** | 外部ツール・サービスとの連携 | `.mcp.json` / 設定ファイル |
| **CLAUDE.md** | プロジェクト固有のルール・知識 | ルートディレクトリ |
| **タスク管理** | やることの一覧を残し、`/task` で選ぶ・増やす・閉じる。`/overnight` で寝ている間に進める | `docs/tasks.md` または GitHub Issues |
| **Hooks** | ツール実行前後の自動処理 | `.claude/settings.json` |
| **ステータスライン** | 使用率・コンテキスト残量のリアルタイム表示 | `~/.claude/settings.json` + [`statusline.py`](statusline.md) |

**まずはSonnetで日常のコーディングを始めてみてください。** AIと一緒にコードを書く体験は、きっと「ニヤリとする瞬間」をもたらしてくれるはずです。
