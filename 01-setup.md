# インストール・初期設定

[< ガイド目次に戻る](README.md)

---

## 前提条件

| 項目 | 要件 |
|------|------|
| **OS** | macOS 13.0+ / Windows 10 1809+ / Ubuntu 20.04+ |
| **メモリ** | 4GB以上 |
| **ネットワーク** | インターネット接続が必要 |
| **アカウント** | Claude Pro, Max, Teams, Enterprise のいずれか（無料プランでは利用不可） |

> 今回のプロジェクトでは**Proライセンスを会社が全額負担**します。

## インストール手順

### macOS / Linux

```bash
# 1. Claude Codeをインストール（推奨方法）
curl -fsSL https://claude.ai/install.sh | bash

# 2. インストール確認
claude --version

# 3. 初回起動（ブラウザでログイン認証が開きます）
claude
```

### Windows（WSL推奨）

Claude Codeは内部的にBashでコマンドを実行するため、**WSL（Windows Subsystem for Linux）上で使うことを強く推奨**します。PowerShellでも動作しますが、以下の理由からWSLの方が圧倒的に快適です。

| | PowerShell | WSL（推奨） |
|--|-----------|------------|
| **コマンド互換性** | Linux系コマンドが動かないことがある | macOS/Linuxと同じコマンドがそのまま動く |
| **Docker連携** | Docker Desktop経由で間接的に動作 | WSL 2 + Docker でネイティブに動作 |
| **チーム環境** | macOSメンバーと手順が異なる | 全員が同じBash環境で統一できる |
| **Claude Codeの安定性** | Git Bashを内部で使うため追加設定が必要 | そのまま動く |
| **サンドボックス** | 非対応 | WSL 2で対応（セキュリティ向上） |

```bash
# 1. WSLをインストール（PowerShellを管理者として実行）
wsl --install -d Ubuntu-24.04

# 2. PCを再起動後、Ubuntuが自動的にセットアップされる
#    ユーザー名とパスワードを設定

# 3. WSL内でClaude Codeをインストール（macOSと同じコマンド）
curl -fsSL https://claude.ai/install.sh | bash

# 4. インストール確認
claude --version

# 5. 初回起動
claude
```

> **npmでのインストールは非推奨になりました。** 上記のネイティブインストーラーが推奨です。自動アップデートにも対応しています。

> **Tip**: WSLからWindowsのファイルには `/mnt/c/Users/...` でアクセスできますが、パフォーマンスのためWSL内のファイルシステム（`~/projects/` 等）で作業するのがベストです。

## 初回起動後にやること

```bash
# 1. プロジェクトディレクトリに移動して起動
cd my-project && claude

# 2. CLAUDE.mdを自動生成（既存プロジェクトの場合）
> /init

# 3. ステータスラインを設定（推奨）
#    使用率やコンテキスト残量をリアルタイム表示 → 詳細は 18-statusline.md
cp tools/statusline.py ~/.claude/statusline.py

# 4. インストール状態の診断（問題がある場合）
claude doctor
```

## アップデート

ネイティブインストールの場合、バックグラウンドで**自動アップデート**されます。手動で更新したい場合は：

```bash
claude update
```
