# インストール・初期設定

[< ガイド目次に戻る](README.md)

---

## 前提条件

| 項目 | 要件 |
|------|------|
| **OS** | macOS 13.0+ / Windows 10 1809+ / Ubuntu 20.04+ |
| **メモリ** | 4GB以上 |
| **ネットワーク** | インターネット接続が必要 |
| **アカウント** | Claude Code を含む有料プラン、または Claude Console のアカウント（無料プランでは利用不可。対象のプランは[料金ページ](https://claude.com/pricing)を参照） |

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

### Windows

Windows では、**ネイティブ**（PowerShell / CMD）と **WSL** のどちらでも使えます。

| | ネイティブの Windows | WSL 2 |
|--|-----------|------------|
| **向いているもの** | Windows のプロジェクトやツールを使う | Linux 向けのツールを使う。macOS のメンバーと手順をそろえたい |
| **必要なもの** | なし（Git for Windows は任意） | WSL 2 を有効にする |
| **シェル** | Git for Windows があれば Git Bash、なければ PowerShell でコマンドを実行する | macOS/Linux と同じ Bash |
| **サンドボックス** | 非対応 | 対応 |

このガイドのコマンド例は Bash で書いているので、チームで手順をそろえたいなら WSL 2 が楽です。

**ネイティブの Windows（PowerShell）:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

CMD の場合は `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` を実行します。管理者として実行する必要はありません。

**WSL:**

```bash
# 1. WSLをインストール（PowerShellを管理者として実行）
wsl --install -d Ubuntu-24.04

# 2. PCを再起動後、Ubuntuが自動的にセットアップされる
#    ユーザー名とパスワードを設定

# 3. WSL内でClaude Codeをインストール（macOSと同じコマンド）
curl -fsSL https://claude.ai/install.sh | bash
```

どちらの場合も、インストールが終わったら新しいターミナルを開き、`claude --version` で確認してから `claude` で起動します。

> **インストール方法について**: 上記のネイティブインストーラーがおすすめです。バックグラウンドで自動更新されます。ほかに Homebrew・WinGet・npm でも入れられますが、Homebrew と WinGet は自動更新されないので、自分で更新する必要があります。

> **Tip**: WSLからWindowsのファイルには `/mnt/c/Users/...` でアクセスできますが、パフォーマンスのためWSL内のファイルシステム（`~/projects/` 等）で作業するのがベストです。

## 初回起動後にやること

```bash
# 1. プロジェクトディレクトリに移動して起動
cd my-project && claude

# 2. CLAUDE.mdを自動生成（既存プロジェクトの場合）
> /init

# 3. ステータスラインを設定（推奨）
#    使用率やコンテキスト残量をリアルタイム表示 → 詳細は statusline.md
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/tools/statusline.py -o ~/.claude/statusline.py

# 4. インストール状態の診断（問題がある場合）
claude doctor
```

## アップデート

ネイティブインストールの場合、バックグラウンドで**自動アップデート**されます。手動で更新したい場合は：

```bash
claude update
```
