# ステータスライン

[< ガイド目次に戻る](README.md)

---

Claude Codeのターミナル下部に、**使用率・コンテキスト残量・ブランチ情報をリアルタイム表示**できます。レート制限やコンテキスト枯渇に気づかず作業してしまう事故を防げます。

## 表示内容

```
ai:main ↑2 | Claude Opus 4.6 | 5h:32% | 7d all:18% / opus:25% / sonnet:12% | ctx:85%
```

| セクション | 内容 |
|-----------|------|
| **repo:branch** | リポジトリ名、ブランチ名、↑↓でpush/pull状態 |
| **モデル名** | 現在使用中のモデル |
| **5h** | 5時間ローリングウィンドウの使用率（OAuth Usage API） |
| **7d** | 7日間の使用率（all/opus/sonnet別） |
| **ctx** | コンテキストウィンドウの残量 |

### 色分け

- 使用率（5h/7d）: 🟢 50%未満 → 🟡 50〜80% → 🔴 80%以上
- コンテキスト残量: 🟢 50%以上 → 🟡 20〜50% → 🔴 20%未満
- リセットまでの残り時間も表示（例: `3h24m`）

## 他のステータスラインツール

ステータスライン機能はClaude Codeの標準機能で、表示内容はスクリプトで自由にカスタマイズできます。本ガイドでは `statusline.py` を使いますが、OSSでも様々な実装が公開されています。

| ツール | 特徴 |
|--------|------|
| 本ガイドの `statusline.py` | 使用率・コンテキスト・git情報をシンプルに表示 |
| [claude-code-power-pack](https://github.com/nicobailon/claude-code-power-pack) | ステータスライン含む総合ツールキット |
| コミュニティ実装各種 | GitHubで `claude code statusline` で検索 |

どのツールを使っても構いません。大事なのは**使用量を常に見える状態にしておくこと**です。

## セットアップ（statusline.py）

### 1. スクリプトを配置

本リポジトリの [`tools/statusline.py`](tools/statusline.py) を `~/.claude/` にダウンロードします。

```bash
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/tools/statusline.py \
  -o ~/.claude/statusline.py
```

### 2. settings.json に追加

`~/.claude/settings.json` に `statusLine` を追加します。

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py",
    "padding": 0
  }
}
```

> 既に `settings.json` に他の設定がある場合は、`statusLine` キーだけ追記してください。

### 3. Claude Codeを再起動

設定を反映するにはClaude Codeを再起動します。ターミナル下部にステータスラインが表示されれば成功です。

## 仕組み

### データソース

| データ | 取得元 |
|--------|--------|
| repo/branch/ahead-behind | `git` コマンド |
| モデル名 | Claude Codeからstdinで渡されるJSON |
| コンテキスト残量 | Claude Codeからstdinで渡されるJSON |
| 使用率（5h/7d） | [OAuth Usage API](https://docs.anthropic.com/) + OAuthトークン |

### OAuthトークンの取得

- **macOS**: macOS Keychainから自動取得（Claude Codeログイン済みなら設定不要）
- **Linux/WSL**: `~/.claude/.credentials.json` から読み取り

### APIキャッシュ

Usage APIの呼びすぎを防ぐため、レスポンスを `~/.claude/statusline-usage-cache.json` に**10分間キャッシュ**します。API障害時はキャッシュから古いデータを表示します。

## トラブルシューティング

| 症状 | 原因・対策 |
|------|-----------|
| ステータスラインが表示されない | `python3` にパスが通っているか確認。`python3 ~/.claude/statusline.py` を手動実行してエラーを確認 |
| 使用率が `--` のまま | OAuthトークンが取得できていない。Claude Codeに再ログインしてみる |
| 使用率が更新されない | キャッシュTTLは10分。`~/.claude/statusline-usage-cache.json` を削除すれば即座に再取得 |
| ブランチが表示されない | gitリポジトリ外で起動している |
