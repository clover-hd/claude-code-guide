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
| [モデルの違い・Sonnet 4.6](models.md) | Opus/Sonnet/Haikuの使い分け、Sonnet 4.6の飛躍的進化 |

### 開発ワークフロー

| セクション | 内容 |
|-----------|------|
| [Phase A：プロジェクトの立ち上げ](workflow-setup.md) | ゼロからの土台作り（A1〜A7の依存関係付き手順） |
| [Phase B：日常の開発サイクル](workflow-daily.md) | consult→Plan→永続化→実装→テスト→commitの流れ |

### Claude Codeの拡張機能

| セクション | 内容 |
|-----------|------|
| [サブエージェント](sub-agents.md) | 専門AIチームの構築 |
| [スキル（Skills）](skills.md) | `/commit`, `/consult` 等のテンプレート化（新SKILL.md形式） |
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
| [/kickstart スキル](kickstart-skill.md) | 新プロジェクトの立ち上げをClaudeが対話で案内。Phase A（A1〜A7）を自動化 |

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
| `/model sonnet` | Sonnet 4.6に切り替え（日常使いはこれ） |
| `/model opus` | Opus 4.6に切り替え（複雑な設計時） |
| `Shift + Tab` | Plan Mode ON/OFF |
| `/clear` | コンテキストをリセット |
| `/compact` | 会話を圧縮してコンテキスト延命 |
| `/init` | CLAUDE.mdを自動生成 |
| `Esc` | 実行中のタスクを中断 |
| `Esc + Esc` | チェックポイント選択（巻き戻し） |

### 日常の開発サイクル（Phase B 要約）

```
1. /consult     → 何を作るか壁打ち
2. Shift+Tab    → Plan Modeで設計
2.5. 永続化     → 仕様書をdocs/specs/に保存
3. Shift+Tab    → 通常モードで実装
3.5. テスト     → ユニットテスト & E2Eテスト
4. /commit      → ルールに従ってコミット
```

### モデル使い分けの目安

```
日常コーディング・バグ修正     → Sonnet 4.6（Opusの1/5コスト）
大規模設計・複雑なリファクタ   → Opus 4.6
簡単な質問・定型作業           → Haiku 4.5
```

---

## まとめ

| 機能 | 何ができるか | 設定場所 |
|------|-------------|----------|
| **モデル切替** | タスクに応じて性能/コストを最適化 | `/model` コマンド |
| **サブエージェント** | 専門AIチームの構築 | `.claude/agents/*.md` |
| **スキル** | よく使う操作のテンプレート化 | `.claude/skills/<name>/SKILL.md` |
| **MCPサーバー** | 外部ツール・サービスとの連携 | `.mcp.json` / 設定ファイル |
| **CLAUDE.md** | プロジェクト固有のルール・知識 | ルートディレクトリ |
| **Hooks** | ツール実行前後の自動処理 | `.claude/settings.json` |
| **ステータスライン** | 使用率・コンテキスト残量のリアルタイム表示 | `~/.claude/settings.json` + [`statusline.py`](statusline.md) |

**まずはSonnet 4.6で日常のコーディングを始めてみてください。** AIと一緒にコードを書く体験は、きっと「ニヤリとする瞬間」をもたらしてくれるはずです。
