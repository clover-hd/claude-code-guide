---
name: kickstart
description: 新しいプロジェクトをゼロから立ち上げる。Phase Aの手順に従い、要件・基本仕様・実装の方針からCLAUDE.md、エージェント、スキル、コミットガードまでの土台を順番に構築する。
disable-model-invocation: true
---

# /kickstart - プロジェクト立ち上げガイド

新しいプロジェクトの土台をPhase Aの手順に従って構築します。
各ステップを順番に進め、**前のステップが完了してから次に進んでください**。

## 進め方のルール

- ユーザーに現在のステップ番号と名前を提示し、対話しながら進める
- 一度に全てを作ろうとせず、**1ステップずつ確認を取りながら**進行する
- 各ステップの**完了条件**を全て満たしてから次へ進む
- ユーザーが「OK」「次へ」等と言うまで次のステップに進まない
- 迷ったら**選択肢を提示**してユーザーに選ばせる（勝手に決めない）
- ステップの中で決めたことのうち、**退けた案があるもの**は `docs/decisions/` に記録する（書き方は A0 の `docs/README.md`）

## モデルの使い分け

- A1〜A3（構想・要件の壁打ち）: Sonnet で十分
- A4〜A4.5（基本仕様・実装の方針）: **Opus 推奨**（深い設計判断が必要）
- A5〜A8（ファイル作成）: Sonnet で十分

ステップ開始時に、推奨モデルが現在と異なる場合はユーザーに `/model` での切り替えを案内する。

---

## A0：プロジェクト初期化（自動実行）

最初に以下を自動で実行する。ユーザーへの確認は不要。

### ディレクトリ構成の作成

```
docs/
├── README.md     ← ドキュメントの方針（どこに何を書くか）
├── decisions/    ← なぜそう決めたか（1判断1ファイル）
└── _wip/         ← 実装中の詳細設計（終わったら移すか削除する）
```

`docs/_wip/` と `docs/decisions/` には `.gitkeep` を置く。

### docs/README.md の作成

以下の内容で作成する。

````markdown
# ドキュメントの方針

## 残すもの（docs/ 直下）

| 種類 | 置き場所 | 中身 |
|---|---|---|
| 要件 | requirements.md | 目的、守る方針、作らないもの、満たすべきこと |
| 基本仕様 | spec.md | 技術構成、データの大きな流れ、ディレクトリ構成、ブランチとデプロイ。変わりにくい骨格だけ |
| 実装の方針 | implementation-policy.md | 迷ったときにどちらに倒すか。ソースを読めば分かることは書かない |
| なぜそう決めたか | decisions/ | 決めたこと、退けた案、根拠、見直す条件 |

やること（タスク）は、ここではなく spec.md の「タスク管理」に書いた場所で管理する。終わったタスクは残さない（何をしたかは git の履歴とソースが持っている）。

## 詳細設計（docs/_wip/）

- 実装を始めるときに `docs/_wip/<テーマ>.md` に書く。テーブル定義、APIの形、画面の細部などがここに入る
- 実装が終わったら片付ける
  - 要件・基本仕様・判断の理由にあたるものは docs/ に移す
  - それ以外は削除する（その内容はソースが持っている）
- 詳細設計はソースを正とする。docs/ の記述とソースが食い違ったら、ソースを信じる

## 「なぜそう決めたか」の書き方

`decisions/NNNN-短い名前.md` に、一つの判断を一つのファイルに書く。番号は連番にする。

```markdown
# NNNN 題名

- 日付: YYYY-MM-DD
- 状態: 採用 / 置き換え済み（→ NNNN）
- 決めた人: 人間 / advisor に相談（相談したエージェント名）

## 決めたこと
## 理由
## 退けた案とその理由
## 根拠にしたもの（ドキュメントのURL、計測値、コミットなど）
## 見直す条件（どうなったら考え直すか）
```

判断が変わったときは古いファイルを書き換えない。新しいファイルを作り、古いファイルの状態を「置き換え済み」にする。
````

### .gitignore の作成

プロジェクトルートに以下の内容で `.gitignore` を作成する（技術スタック非依存の共通項目のみ）。

```gitignore
# 環境変数・シークレット
.env
.env.*
!.env.example

# 認証情報
credentials.json
*.pem
*.key
service-account.json

# Claude Code の個人設定
.claude/settings.local.json

# OS・エディタ
.DS_Store
Thumbs.db
*.swp
.vscode/settings.json
.idea/
```

> **注**: 技術スタック固有の項目（`node_modules/`, `__pycache__/`, `vendor/` 等）はA4の基本仕様の決定後に追記する。

### git初期化確認

`.git/` が存在しない場合は `git init` を実行する。

**完了条件**: ディレクトリ構成、`docs/README.md`、`.gitignore` が作成された。

---

## A1：要件ドキュメント作成

ユーザーに以下を質問して、`docs/requirements.md` を作成する。

### 聞くべきこと

- **何を作るのか**（一言で）
- **誰のために作るのか**（ターゲットユーザー）
- **守る方針**（譲れないこと。迷ったときの判断の物差しになる）
- **作らないもの**（似ているが目指さないもの、やらないこと）
- **最終的な目標（ビジョン）**
- **MVP（最低限必要な機能）** — 各機能は1行で具体的に
- **将来的に追加したい機能**

### 質問のしかた

- 一度にまとめて聞かず、会話の中で自然に深掘りする
- 曖昧な回答には「具体的にはどういうイメージですか？」と掘り下げる
- 「守る方針」は、あとでエージェントがレビューの物差しに使う。「使いやすく」のような誰でも言えることではなく、**このサービスだから守ること**を引き出す（例：「個人情報はログに出さない」「ユーザーに判断を押し付けない」）
- 「作らないもの」が出てこなければ、「似たサービスと比べて、あえてやらないことは？」と聞く
- MVPが5機能を超える場合は「本当にMVPに全部必要ですか？後回しにできるものは？」と確認する
- ユーザーが迷っている場合は具体的な選択肢を提示する

### ドキュメントのテンプレート

```markdown
# 要件

## サービス名
（仮でOK）

## 何を作るのか
（一言で）

## ターゲットユーザー
（誰のために）

## 守る方針
- ...
- ...

## 作らないもの
- ...

## ビジョン（最終目標）
...

## MVP（最低限必要な機能）
1. ...
2. ...

## 将来的に追加したい機能
- ...
```

**完了条件**: `docs/requirements.md` が作成され、ユーザーが内容を確認してOKと言った。

---

## A2：/consult スキル作成

A1のドキュメントを踏まえて `.claude/skills/consult/SKILL.md` を作成する。

### 含めるべき内容

```markdown
---
name: consult
description: サービスの要件・企画レベルの相談に乗る。新しい機能や画面のアイデアを、作るかどうか・何を作るかを決める前に壁打ちしたいときに使う。どう実装するかの相談には使わない。
---

# /consult - サービス要件相談

## 前提知識の読み込み

以下のドキュメントを必ず読み込んでから回答してください。

1. `docs/requirements.md` - 要件と守る方針
2. `docs/spec.md` - 基本仕様（あれば）
3. `docs/decisions/` - 相談に関わる過去の判断（あれば）

## 相談相手としての振る舞い

- 対等な立場で議論する（上から目線にならない）
- 良いアイデアは素直に認める
- 懸念点があれば率直に伝える
- 「それはいいですね」で終わらず、深掘りする
- 必要であれば実装状況を参照して「今できること」を伝える

## 避けること

- いきなり実装の話に入らない（まず要件レベルで整理）
- 過度に楽観的・悲観的にならない
- ユーザーの意見を無批判に肯定しない

## サービスの核心（常に意識する）

> （A1のドキュメントからビジョン、守る方針、作らないものを転記する）
```

ビジョン・守る方針・作らないものは、A1で作成した `docs/requirements.md` から**実際の内容を転記**すること。テンプレートのままにしない。

**完了条件**: `.claude/skills/consult/SKILL.md` が作成され、サービス固有の内容が反映されている。

---

## A3：/consult で要件を壁打ち

ユーザーに以下を案内する：

```
consultスキルができました。
ここから壁打ちを始めましょう。以下の観点で要件を深掘りしていきます：

- MVPの機能に過不足はないか
- 優先順位は適切か
- 見落としている機能はないか（認証、通知、エラーハンドリング、検索等）
- ユーザー体験の流れ（主要な操作フロー）
- 守る方針と作らないものは十分か

壁打ちの結果は docs/requirements.md に反映していきます。
では、まずMVPの機能一覧から見直しましょう。
```

### 壁打ちで確認すべき観点

- **ユーザーフロー**: 主要な操作（登録→ログイン→メイン機能→...）の流れ
- **権限**: 管理者とユーザーの区別が必要か
- **通知**: メール、プッシュ通知は必要か
- **検索・フィルター**: データが増えたときの検索手段
- **エラーケース**: 主要な操作が失敗したときの挙動
- **データのライフサイクル**: 削除は論理削除か物理削除か。ユーザーから消してと言われたらどうするか

### 重要：壁打ちの結果を永続化する

議論がまとまったら、必ず `docs/requirements.md` を更新する。
退けた案があった判断（例：「決済はMVPに入れない」）は `docs/decisions/` にも記録する。
会話はセッション終了で消えるが、ドキュメントは残る。

**完了条件**: ユーザーがMVPの要件に納得し、`docs/requirements.md` が更新された。

---

## A4：基本仕様の決定 ← ここが分岐点

> **このステップはOpusでの実行を推奨します。** `/model opus` で切り替えてください。

**ここが決まらないとA6のエージェントが作れません。**

### 議論すべき観点

以下を**1つずつ**ユーザーと議論する。各項目で複数案を提示し、比較表を作ってユーザーに選ばせる。

1. **プラットフォーム**: Web / モバイル / デスクトップ / 両方
2. **言語**: TypeScript, Python, Go, Rust, Ruby, Java 等
3. **フロントエンド**: React, Next.js, Vue, Svelte, Flutter 等（該当する場合）
4. **バックエンド**: Express, Hono, Django, FastAPI, Rails, Gin, Echo 等
5. **データベース**: PostgreSQL, MySQL, SQLite, MongoDB 等
6. **ORM/データアクセス**: Prisma, Drizzle, SQLAlchemy, GORM, ActiveRecord 等
7. **インフラ**: AWS, GCP, Vercel, Cloudflare, セルフホスト 等
8. **設計パターン**: モノリス, マイクロサービス, Clean Architecture 等
9. **ディレクトリ構成**: 決定した技術スタックに適した構成を提案
10. **ブランチとデプロイ**: 作業ブランチ（例：`develop` で作業し `main` は常に動く状態）、Pull Requestを使うか、環境（手元 / ステージング / 本番）
11. **よく使うコマンド**: テスト、型検査（静的解析）、開発サーバー、ビルド。**型検査とテストは入口を一つに決める**（例：`npm run typecheck`、`npm test`）
12. **タスクの置き場所**: やることの一覧をどこに置くか。次の2案を比較表で示して選んでもらう

| 観点 | リポジトリ内のファイル（`docs/tasks.md`） | GitHub Issues（`gh` で操作） |
|---|---|---|
| 向いているケース | 一人で開発する、GitHubを使わない | チームで開発する、Pull Requestを使う |
| 良い点 | 追加のツールがいらない。コードと同じコミットで状態を変えられる | 同時に編集しても衝突しない。PRやコメントとつながる |
| 気をつけること | 複数人で同時に編集すると衝突しやすい | `gh` の認証が必要。リポジトリの外に書くので、作る前に人間の確認を取る |

迷っていたら、一人ならファイル、チームならGitHub Issuesを勧める。ほかのツール（Linear、Jira等）を使いたいと言われたら、MCPで読み書きできるかを確かめてから、GitHub Issuesの案と同じ考え方で組み立てる。

### 判断基準（ユーザーに説明する）

- **チームの経験**: 使ったことがある技術を優先
- **MVPの速度**: 早く作れるものを優先
- **学習目的**: 新しい技術を試したい場合はそれも考慮
- **スケーラビリティ**: 将来の拡張性
- **乗り換えやすさ**: 特定のサービスに強く依存する部分は、差し替えられる層の背後に置けるか

### 提案の形式（例）

```
| 観点 | 案A | 案B | 案C |
|------|-----|-----|-----|
| フロントエンド | Next.js | React + Vite | React Native |
| 理由 | SSR対応、Vercelと相性◎ | シンプル、学習コスト低 | モバイルアプリ |
| 向いているケース | SEOが必要なWebアプリ | SPA | iOS/Android |
```

### 決定内容の記録

`docs/spec.md` に以下の構成で記録する。**変わりにくい骨格だけ**を書く（テーブル定義やAPIの細部は書かない。それは実装時に `docs/_wip/` に書く）。

```markdown
# 基本仕様

## 技術構成
- Frontend: ...
- Backend: ...
- DB / ORM: ...
- Infra: ...
- 設計パターン: ...

## データの大きな流れ
（主要なデータがどこから入り、どこに保存され、どこに出るか）

## ディレクトリ構成
（ツリー形式で）

## ブランチとデプロイ
- 作業ブランチ: ...
- 環境: 手元 / ステージング / 本番
- デプロイ方法: ...

## タスク管理
- 置き場所: docs/tasks.md / GitHub Issues（<owner>/<repo>）
- 増やす・閉じるのは /task スキルで行う

## よく使うコマンド
- 型検査: ...
- テスト: ...
- 開発サーバー: ...
```

### 判断の記録

技術選定のうち**退けた案がある選択**は、A0の `docs/README.md` の書式で `docs/decisions/` に1判断1ファイルで記録する。

```markdown
# 0001 ORMにPrismaを選ぶ

- 日付: YYYY-MM-DD
- 状態: 採用
- 決めた人: 人間

## 決めたこと
ORMはPrismaを使う。

## 理由
型安全性とマイグレーション管理の利便性を優先した。

## 退けた案とその理由
- Drizzle: 軽量でSQLに近いが、チームに経験者がいない
- TypeORM: 実績はあるが、メンテナンスが停滞している

## 根拠にしたもの
- （公式ドキュメントのURLなど）

## 見直す条件
- Edge環境で動かす必要が出たとき
```

### .gitignore の追記

技術スタックが確定したので、A0で作成した `.gitignore` に技術固有の項目を追記する。

例：
- Node.js: `node_modules/`, `dist/`, `build/`
- Python: `__pycache__/`, `.venv/`, `*.pyc`
- Go: 基本的に追加不要（バイナリ名を指定）
- Ruby: `vendor/bundle/`, `.bundle/`
- 手元のDBファイル（SQLite等）を使う場合: そのファイル

タスクの置き場所の選択も、退けた案があるので `docs/decisions/` に記録する。

**完了条件**: `docs/spec.md` が作成され、技術構成・ディレクトリ構成・ブランチ運用・タスクの置き場所・コマンドが確定し、`.gitignore` が技術スタックに合わせて更新された。

---

## A4.5：実装の方針を決める

> 引き続きOpus推奨。

`docs/implementation-policy.md` を作成する。これは細かいコーディング規約ではなく、**迷ったときにどちらに倒すか**だけを書いた資料。エージェントが実装やレビューで判断に迷ったとき、まずここに照らす。

### 進め方

以下の観点を1つずつ提示し、このサービスでの倒し方をユーザーと決める。**該当しない観点は省く**。各観点で、まず要件の「守る方針」から導ける倒し方を提案する。

| 観点 | 決めること（例） |
|---|---|
| ログ | 出してよいもの（ID、件数、所要時間、エラーの種類）と出さないもの（個人情報、本文、トークン、秘密の値）。**迷ったら出さない** |
| 外部APIの呼び出し | タイムアウト、再試行する条件としない条件、失敗したときにユーザーに何を見せるか |
| 失敗したとき | 処理全体を止めるか、失敗したものだけ飛ばして続けるか。二度実行しても結果が同じになるか（冪等） |
| 入力と認証 | 認証の確認を一か所にまとめ、既定で閉じる（確認しない入口を列挙する） |
| データ | ユーザーが入れたものと、システムが推測・生成したものを混ぜないか |
| テスト | 外部サービスは偽物に差し替えて動かすか。本物を呼ぶのはいつか |
| 画面（該当する場合） | 文字の大きさ、押せる場所の大きさ、コントラスト比などの最低ライン |
| LLMを呼ぶ場合 | 構造化出力で受けて中身を検査する、用途ごとのモデルを一か所の対応表で持つ、プロンプトを変えたら変更前と変更後の出力を並べて比べる |

### テンプレート

```markdown
# 実装の方針（迷ったときの倒し方）

細かい規約ではなく、迷ったときにどちらに倒すかだけを書く。どう実装したかはソースを正とする。

## ログ
- 出してよい: ...
- 出さない: ...
- 迷ったら出さない

## 外部APIの呼び出し
- ...

## 失敗したとき
- ...

（以下、決めた観点だけ）
```

倒し方を決めた理由のうち、退けた案があるものは `docs/decisions/` に記録する。

**完了条件**: `docs/implementation-policy.md` が作成され、ユーザーがOKと言った。

---

## A5：CLAUDE.md 作成

> **Sonnetに戻してOKです。** `/model sonnet` で切り替えてください。

A1〜A4.5の成果物を**実際に読み込んだ上で**、プロジェクトルートに `CLAUDE.md` を作成する。

CLAUDE.md は**目次と約束だけ**にする。中身はdocs/に、各エージェントの進め方は `.claude/agents/` の各定義ファイルに書く。CLAUDE.mdに手順を書き込むと、すべての会話とエージェントがそれを読み込み、長くなるほど無視されやすくなるため。

### テンプレート

```markdown
# <サービス名>

<何を作るのか（一言で）>

- 要件と守る方針: [docs/requirements.md](docs/requirements.md)（作業の前に必ず読む）
- 基本仕様: [docs/spec.md](docs/spec.md)
- 実装の方針（迷ったときの倒し方）: [docs/implementation-policy.md](docs/implementation-policy.md)
- なぜそう決めたか: [docs/decisions/](docs/decisions/)
- タスク: <[docs/tasks.md](docs/tasks.md) または GitHub Issues（<owner>/<repo>）>。増やす・閉じるのは `/task`
- ドキュメントの方針（どこに何を書くか）: [docs/README.md](docs/README.md)

## よく使うコマンド

- 型検査: `...`
- テスト: `...`
- 開発サーバー: `...`

## 約束

- 詳細設計はソースを正とする。ドキュメントの記述とソースが食い違ったら、ソースを信じる
- 秘密の値（.env、APIキー、認証情報）はコミットしない（コミット前のフックで止まる。フックを飛ばさない）
- 作業は `<作業ブランチ>` で行う。（A4で決めたブランチ運用を1行で）
- 各エージェントの役割と進め方は `.claude/agents/` の各定義ファイルに書いてある
```

### 厳守事項

- **50行以下**を目安にする（長いとClaudeが無視し始める）
- コードを読めばわかることは書かない
- 「きれいなコードを書け」等の自明な指示は書かない
- 手順（コミット前の流れ等）はエージェント定義に書き、CLAUDE.mdには書かない

**完了条件**: `CLAUDE.md` が作成され、プロジェクト固有の情報が反映され、手順が書き込まれていない。

---

## A6：サブエージェント作成

A1〜A4.5の成果物に基づいて `.claude/agents/` にエージェントを作成する。

### まず4エージェントから始める

| エージェント | モデル | 役割 |
|---|---|---|
| **advisor** | opus | 読み取り専用の相談役。方針・データの形・画面の流れ・使い心地が変わる選択の相談と、区切り（機能のまとまりが一つできたとき）の全体レビュー。コードは書かない |
| **developer** | sonnet | 実装担当。コミット前に qa-engineer と code-reviewer を通してからコミットする |
| **qa-engineer** | sonnet | テスト担当。実装者の「通った」を信用せず自分でテストを走らせる。アプリのソースは直さない |
| **code-reviewer** | sonnet | コミットごとの軽いレビュー。ステージした差分だけを見る。読み取り専用 |

> **ポイント**: 重い判断（advisor）と、回数の多い軽いレビュー（code-reviewer）を分けることで、高いモデルの利用量を抑えつつ判断の質を保つ。プロジェクトが成長して分業が必要になったら、developer を frontend-developer / backend-developer に分ける等で増やせばよい。

> **Fableを使う場合**: advisor の `model:` を `fable` に替えると、相談と区切りのレビューの質が上がる。ただしプランによっては usage credits から引かれる（`/model` の選択画面に "Requires usage credits" と表示される）ため、利用量に注意する。回数の多い code-reviewer には使わない。ユーザーに「advisorにFableを使いますか？」と確認し、使う場合はその判断を `docs/decisions/` に記録する。

### 各エージェントのテンプレート

`<...>` はA1〜A4.5の内容で**実際に埋める**こと。テンプレートのままにしない。

#### advisor.md

````markdown
---
name: advisor
description: <サービス名>全体のアドバイザー。方針（守る方針・作らないものとの距離）、データの形、画面の流れ、使い心地が変わる選択の相談に使う。区切り（機能のまとまりが一つできたとき）の全体レビューにも使う。コミットごとのレビューには使わない（それは code-reviewer）。
model: opus
tools: Read, Grep, Glob, Bash
---

あなたは「<サービス名>」のアドバイザーです。コードは書きません。判断と、その理由を返します。

## 最初に読むもの

- `docs/requirements.md`（守る方針。判断の物差しはここ）
- `docs/spec.md`
- `docs/decisions/` のうち、相談に関わるもの
- 詳細はソースを正とします。ドキュメントとソースが食い違ったら、ソースを信じ、食い違いを指摘してください

## 仕事 1: 相談に答える

1. **結論**: どれを選ぶか。一つに絞る
2. **理由**: requirements.md のどの方針に照らしたか
3. **退けた案とその理由**
4. **見直す条件**
5. **記録の下書き**: 相談したエージェントが `docs/decisions/` にそのまま写せる短い文

記録のファイルを書くのは、相談したエージェントです。あなたは書きません。

### 特に気をつけて見ること

- <requirements.md の「守る方針」「作らないもの」から、判断で見落としやすいものを箇条書き>

### 判断できないとき

人間でなければ決められないこと（サービスの考え方そのものの変更、費用のかかる選択、本番のデータに関わる操作）は、そう言ってください。そのときは、人間に聞くべき問いを一つの文にして返します。

## 仕事 2: 区切りの全体レビュー

頼まれたときだけ行います（機能のまとまりが一つできたとき、一日の終わりなど）。

- `git log` と `git diff <前回の区切り>..HEAD` で、前回からの変化をつかむ。前回の区切りが分からなければ、依頼した人に聞く
- 見ること
  - 要件と守る方針から外れていないか
  - `docs/implementation-policy.md` の倒し方から外れていないか
  - `docs/_wip/` に、片付け忘れ（移すか削除）がないか
  - `docs/decisions/` に、記録されていない判断がないか
  - タスクの一覧（<docs/tasks.md または GitHub Issues>）と実際の状態が合っているか。終わっているのに閉じていないもの、長く作業中のままのもの
  - main に取り込んで動かせる状態か
- 返す形: 「直すべきこと（重い順）」「次の区切りまでに考えること」「良くなったこと」。それぞれ短く書く
- 「直すべきこと」と「次の区切りまでに考えること」のうち、タスクにするとよいものには印（`→タスク`）を付ける。タスクを作るのは依頼した人で、あなたは作らない

## してはいけないこと

- ファイルを書き換えない
- 細かな実装の選択（関数の分け方、ライブラリの細かな使い方）には口を出さない。聞かれたら「実装の側で決めてよい」と返す
````

#### developer.md

````markdown
---
name: developer
description: <サービス名>を<技術スタック名を具体的に（例: React + Hono + Drizzle）>で実装する。機能の実装や修正を頼むときに使う。
model: sonnet
---

あなたは「<サービス名>」の実装を担当します。

## 最初に読むもの

- `docs/requirements.md`（守る方針。必ず読む）
- `docs/spec.md`
- `docs/implementation-policy.md`（迷ったときの倒し方。実装の判断はまずここに照らす）
- `docs/decisions/` のうち、作業に関わるもの
- 詳細はソースを正とします。ドキュメントは信用せず、都度ソースを読んでください

## 技術構成と制約

- <spec.md の技術構成>
- <このスタックで踏みやすい制約（実行環境の制限、使えないAPIなど）>

## 相談の範囲

次のような判断は、自分で決めずに advisor に相談してください（Agent ツールで `advisor` を呼ぶ）。

- 守る方針・作らないものに関わること
- データの形、画面の流れ、ユーザーに見せる言葉に関わること
- 複数の案があり、どれを選ぶかで使い心地やサービスの考え方が変わること

実装の細かな選択（関数の分け方、ライブラリの細かな使い方など）は、自分で決めてかまいません。

相談するときは、次のことを伝えます: 何を決めたいか、考えた案（2つ以上）、それぞれの良い点と悪い点、関係するファイル。

### 人間の判断が要るとき

advisor が「人間でなければ決められない」と返したら、自分で決めません。コミットせずにそこで止まり、次のことを返します: 人間に聞くべき問い（一文）、考えた案、advisor の見立て、作業中の変更が残っているファイル。人間への聞き方は、呼んだ側が決めます。

### 相談して決めたことの記録

相談して決めたことは、**あなた自身が** `docs/decisions/NNNN-短い名前.md` に記録します。書き方は `docs/README.md` に従います。決めた人の欄には「advisor に相談（developer）」と書きます。記録は、その判断を使う実装と同じコミットに入れます。

## 詳細設計

- 実装を始めるときに、`docs/_wip/<テーマ>.md` に詳細設計（テーブル、APIの形、画面の部品など）を書く
- 実装が終わったら片付ける。要件・基本仕様・判断の理由は `docs/` に移し、残りは削除する

## タスク

<A4で選んだ置き場所に合わせて、次のどちらか一方だけを書く>

（docs/tasks.md の場合）
- 頼まれた作業に対応するタスクが `docs/tasks.md` にあれば、そのIDを確かめてから始める
- 終わったら、そのタスクを「完了」に移す。この変更は実装と同じコミットに入れる

（GitHub Issues の場合）
- 頼まれた作業に対応するIssueがあれば、`gh issue view <番号>` で中身を確かめてから始める
- コミットメッセージに `#<番号>` を入れる。Issueを閉じるのは人間か `/task done`（またはPRの `Closes #<番号>`）で、あなたは閉じない

どちらの場合も、新しいタスクは自分で作らない。作業中に見つけた「やったほうがよいこと」は、報告の「タスク候補」に書く。

## 並行して作業しない

- 同じ作業ツリーでコミットする実装エージェントは、一度に一人だけ。並行して作業するように頼まれたら、`git worktree` で別の作業ツリーを作ってそこで作業する（ステージを共有すると、他の作業のファイルがコミットに混ざるため）

## コミット前の流れ

1. 実装して、手元で `<型検査のコマンド>` と `<テストのコマンド>` を通す。部分的な検査で済ませない
2. **qa-engineer** を呼んでテストを頼む。変えたこと、期待する振る舞い、関係するファイルを伝える。失敗したら直して、もう一度頼む
3. 触ったファイルだけを、パスを明示して `git add` する。`git add -A` や `git add .` は使わない。`git diff --cached --stat` を見て、自分の触ったファイルの一覧と合っているかを確かめる
4. **code-reviewer** を呼んで、ステージした差分のレビューを頼む。「直すべき」の指摘を直す。直したら、もう一度レビューを頼む
5. コミットする（作業ブランチは `<作業ブランチ>`）
   - コミットのフックが秘密の値などを検査する。止められたら、そのファイルをステージから外す。フックを飛ばさない（`--no-verify` は使わない）

## 返すもの

最後に、次のことを短く報告します: やったこと、テストとレビューの結果、コミットのハッシュ、相談して記録した判断、対応したタスク、タスク候補（今回やらなかったが、やったほうがよいこと。1行ずつ）。

- 「通った」と書くときは、最後に走らせた型検査とテストの出力の末尾（件数、エラーの有無）を貼る。言葉だけで「通った」と書かない
````

#### qa-engineer.md

````markdown
---
name: qa-engineer
description: <サービス名>のテストを担当する。developer からコミット前のテストを頼まれたときに使う。<テストフレームワーク名>でユニットテストを書き、走らせる。
model: sonnet
---

あなたは「<サービス名>」のテストを担当します。

## 最初に読むもの

- `docs/requirements.md`（守る方針。テストで確かめるべきことの元になる）
- `docs/spec.md`
- `docs/implementation-policy.md`
- 詳細はソースを正とします。ドキュメントは信用せず、都度ソースを読んでください

## コミット前のテスト

1. 頼まれた変更と、関係するソースを読む
2. 足りないテストを書き足す。すでにあるテストを走らせる
3. **自分で** `<型検査のコマンド>` と `<テストのコマンド>` を走らせる。実装者の「通った」という報告を信用しない
4. 結果を返す: 通ったか（走らせたコマンドと出力の末尾を貼る）、落ちたもの（どのテストが、なぜ落ちたか）、テストで確かめられなかったこと

### 必ず確かめること（関係する変更のとき）

- <requirements.md の守る方針・implementation-policy.md から、テストで確かめられるものを箇条書き（例: 認証なしで取れないか、ログに個人情報が出ないか）>

### テストのデータ

- 架空のデータだけを使う。実際のユーザーのデータは使わない
- 外部サービスは偽物に差し替える（implementation-policy.md の「テスト」に従う）

## 相談の範囲

テストの観点で、守る方針に関わる判断に迷ったら advisor に相談する。相談して決めたことは、**あなた自身が** `docs/decisions/` に記録する（決めた人の欄は「advisor に相談（qa-engineer）」）。

## してはいけないこと

- テストを通すために、アプリのソースを書き換えない。直すべき所を見つけたら、頼んだ実装者に返す
- コミットしない。コミットするのは、頼んだ実装者
````

#### code-reviewer.md

````markdown
---
name: code-reviewer
description: コミットのたびに行う軽いレビュー。ステージした差分（git diff --staged）だけを見る。実装者がコミットする前に呼ぶ。全体を見る重いレビューには使わない（それは advisor）。
model: sonnet
tools: Read, Grep, Glob, Bash
---

あなたは「<サービス名>」の、コミットごとのレビューを担当します。軽く、速く行います。

## やること

1. `git diff --staged` で差分を見る。差分がなければ、そう言って終わる
2. `git diff --staged --stat` のファイルの一覧が、頼まれた変更と合っているかを見る。ほかの作業のファイルが混ざっていたら「直してから」にする
3. 差分を理解するのに必要な範囲だけ、まわりのソースを読む。リポジトリ全体は見ない
4. `docs/requirements.md` の「守る方針」と `docs/implementation-policy.md` の倒し方に照らして、差分に問題がないかを見る

## 見ること

- **バグ**: 動かない、境界の値で壊れる、エラーを握りつぶしている
- **方針から外れていないか**: <守る方針のうち、差分で見つけやすいものを箇条書き>
- **セキュリティ**: 認証の確認の抜け、ログに個人情報や秘密の値が出ていないか、キーの直書き
- **ドキュメント**: 判断を含む変更なのに、`docs/decisions/` に記録がない

## 返す形

```
判定: 通してよい / 直してから
直すべき:
- ファイル:行 — 何が問題か — どう直すか
気になる（直さなくてもよい）:
- …
```

- 指摘は差分の中に限る。差分の外で見つけた問題は「気になる」に一行で書くだけにする
- 好みの問題（書き方の細部）は指摘しない
- 方針について判断がつかないときは、「advisor に相談を」と書く。自分で決めない

## してはいけないこと

- ファイルを書き換えない。コミットしない
````

### 重要

- description には**このプロジェクトの技術スタック名を具体的に書く**（「バックエンド担当」ではなく「Express + Prisma でAPIを構築する」）
- `<...>` の箇条書きは、requirements.md と implementation-policy.md から**このサービスならではのもの**を選んで書く。一般論で埋めない
- エージェント名は kebab-case（`code-reviewer`）にする

**完了条件**: 4つのエージェントが `.claude/agents/` に作成され、各エージェントにプロジェクト固有の技術スタック・コマンド・方針が反映されている。

---

## A7：スキル・コミットガード・初期コミット

### /ask-advisor スキルの作成

`.claude/skills/ask-advisor/SKILL.md` を以下の内容で作成する。`context: fork` と `agent: advisor` により、メインの会話を汚さずに advisor に相談を投げられる。

`context: fork` のスキルは、既定ではバックグラウンドで動き、答えは後から届く。相談の答えを見てから次に進みたいので、`background: false` を付けて、その場で答えを待つようにする。

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

- 相談の場合は、あなたの定義にある「仕事 1」の形（結論、理由、退けた案、見直す条件、記録の下書き）で答えてください
- 「区切りのレビュー」と書かれている場合は、「仕事 2」を行ってください
- 相談の内容が短すぎて判断できない場合は、決めるのに足りない情報を挙げて返してください
```

### /commit スキルの作成

`.claude/skills/commit/SKILL.md` を以下の内容で作成する。人間が直接コミットを頼むときに使う（developer エージェント経由の場合は、エージェント定義の「コミット前の流れ」に従う）。

````markdown
---
name: commit
description: プロジェクトルールに従ったgitコミットを実行する
disable-model-invocation: true
---

# /commit - プロジェクト専用コミットスキル

## ルール

1. **修正内容ごとに分けてコミット**: 1コミット = 1論理的変更
2. **Conventional Commits形式**: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:` 等
3. **Co-Authored-By追加**: 必ず以下を付与
   ```
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
4. **HEREDOCでメッセージ作成**: フォーマット維持のため

## 手順

### 1. 変更状況の確認
```bash
git status
git diff --stat
git log --oneline -5
```

### 2. 変更のグループ化
変更内容を論理的単位でグループ化する。
- 機能追加は `feat:`
- バグ修正は `fix:`
- リファクタリングは `refactor:`
- ドキュメントは `docs:`
- その他の雑務は `chore:`

### 3. グループごとにコミット
```bash
git add <関連ファイルをパスで明示>
git diff --cached --stat   # 意図したファイルだけか確かめる
git commit -m "$(cat <<'EOF'
<type>: <簡潔な説明>

<詳細説明（必要に応じて）>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## 注意事項
- `git add -A` や `git add .` は使わず、ファイルを明示的に指定する
- コミットのフックに止められたら、そのファイルをステージから外す。`--no-verify` は使わない
- pushはユーザーの明示的な指示がある場合のみ実行
````

### /task スキルの作成

`.claude/skills/task/SKILL.md` を作成する。タスクの一覧を見る・増やす・閉じる入口を一つにまとめる。**手順の部分は、A4で選んだ置き場所の方だけを書く**（両方を残さない）。

````markdown
---
name: task
description: タスクの一覧を見て次にやることを選ぶ、タスクを増やす、終わったタスクを閉じる。作業を始めるとき、作業や区切りのレビューで「やること」が出てきたときに使う。
argument-hint: [add <内容> | done <ID> | 引数なしで一覧と次の候補]
---

# /task - タスク管理

置き場所: <docs/tasks.md または GitHub Issues（<owner>/<repo>）>

## 引数なし: 一覧と次の候補

1. 「人間の判断待ち」があれば、最初に出す（`/overnight` が残したもの）
2. 作業中と未着手のタスクを一覧にする
3. `docs/requirements.md` のMVPと守る方針に照らして、次にやるものを一つ勧める。理由を一行で添える
4. 人間が選んだら、それを作業中にする

## 判断待ちに答える

人間が「人間の判断待ち」に答えたら:

1. 退けた案があれば、`docs/decisions/` に記録する（決めた人: 人間）
2. 仮に実装していたもの（「仮で〇〇にした」と書かれているもの）が答えと違えば、直すタスクを足す
3. 待っていたタスクを「次にやる」に戻し、判断待ちの項目を消す

## add <内容>

1. 内容を「何をするか」と「完了条件（どうなったら終わりか）」に分ける。完了条件が書けないほど曖昧なら、人間に聞く
2. 既存のタスクと重なっていないかを確かめる
3. 追加する。複数あるとき（developer のタスク候補、advisor の `→タスク` など）は、一覧にして人間に確認してから追加する

## done <ID>

1. 完了条件を満たしているかを、コミットやテストの結果で確かめる。満たしていなければ、足りないことを返して閉じない
2. 閉じる

## 手順（docs/tasks.md の場合）

- 書式は `docs/tasks.md` の冒頭に従う。IDは `T-` に続く連番（例: `T-012`）。一度使ったIDは使い回さない
- 作業中にするときは「作業中」に、閉じるときは「完了」に移す
- 「完了」の項目は、区切りのレビューのあとで削除する（履歴は git に残る）
- 変更したら `/commit` でコミットする（`docs:` で始める）

## 手順（GitHub Issues の場合）

- 一覧: `gh issue list --state open`
- 追加: `gh issue create --title "<何をするか>" --body "<完了条件>"`。**作る前に、題名と本文を人間に見せて確認を取る**（リポジトリの外に書くため。コミットガードのフックと設定でも確認が出る）
- 作業中にする: `gh issue edit <番号> --add-assignee @me`
- 閉じる: `gh issue close <番号> --comment "<対応したコミット>"`
````

#### docs/tasks.md の作成（ファイルを選んだ場合）

````markdown
# タスク

書式: `- [ ] T-001 何をするか — 完了条件: … — 詳細設計: docs/_wip/<テーマ>.md（あれば）`
増やす・閉じるのは `/task` で行う。「完了」は区切りのレビューのあとで削除する。
人間の判断待ちの書式: `- 問い — 案: … — 出どころ: T-003 — 待っているタスク: T-005（なければ「なし」）`

## 人間の判断待ち

## 作業中

## 次にやる（上から順に）

## いつか

## 完了
````

### 最初のタスクを作る

`docs/requirements.md` のMVPから、最初のタスクを作る。

- MVPの1機能を1タスクにする。大きすぎる機能（1回の依頼で終わらないもの）は分ける
- 並び順は、A3で決めた優先順位に従う。「将来的に追加したい機能」は「いつか」に入れる（GitHub Issuesの場合は作らない）
- 一覧を人間に見せて、OKをもらってから書き込む。GitHub Issuesの場合は、この時点で `gh auth status` で認証を確かめる

### /overnight スキルの作成

`.claude/skills/overnight/SKILL.md` を作成する。寝る前に打つと、任せたタスクを朝まで順に実装する。

普段（人間が起きているとき）は、判断が要ればその場で人間に聞く。これは developer の「人間の判断が要るとき」とメインの会話の流れで、もともとそうなっている。**寝ている間だけの決まりはこのスキルに閉じ込め、エージェントの定義には書かない。** `disable-model-invocation: true` にして、人間が打ったときだけ夜用の動きに入るようにする。

`<...>` はA4〜A7の内容で埋める。タスクの置き場所に合わせた書き分けは `/task` と同じく、選んだ方だけを残す。

````markdown
---
name: overnight
description: 寝ている間に、任せたタスクを順に実装する。始める前の確認のあとは人間に聞かず、判断が要る点は一覧に残して先へ進む。
argument-hint: [上限（例: 3件、6時間。省略すると上限なし）]
disable-model-invocation: true
---

# /overnight - 寝ている間にタスクを進める

## 始める前（人間に聞くのはここだけ）

1. `git status` で作業ツリーがきれいかを確かめる。きれいでなければ、そう言って止める
2. タスクの一覧を見せ、任せるタスクを決めてもらう。勧めるのは「次にやる」にある、完了条件のあるタスクすべて（上から順に進める）。完了条件のないタスクは任せない
3. 上限を決める。件数か時間（$ARGUMENTS にあればそれを使う。なければ上限は設けず、任せたタスクをすべて進める）。時間の上限は、始めてからの経過時間で数える（使用量のリセットを待つ時間も含む）
4. 使用量の上限に達したあと、リセットされたら自動で続ける設定（`autoContinueAtUsageLimit`、`/config` では **Continue automatically at usage limit**。既定はオン）を確かめる
   - `jq '.autoContinueAtUsageLimit' ~/.claude/settings.json` で、このキーだけを取り出す（`jq` がなければ `grep autoContinueAtUsageLimit ~/.claude/settings.json`）。`false` ならオフ。ファイルを丸ごと読まない（`env` に API キーなどが入っていることがあるため）
   - ユーザー設定・`--settings`・管理設定のどれにもこのキーがなく、`.claude/settings.json` か `.claude/settings.local.json` に書かれていれば（同じようにキーだけを取り出して見る）、値によらずオフになる（このキーはユーザー設定・`--settings`・管理設定からしか読まれないため）
   - 最後は人間に `/config` を開いてもらう。**Continue automatically at usage limit** の行があれば、その値を見てもらう。行がなければ、管理設定か `--settings` で決まっていて、ここからは変えられない。オンかどうか分からないので、上限に達すると朝まで止まることがあると伝える
   - オフなら、オンにするかを人間に聞く。オンにするのは人間が `/config` の画面で行う（`/config autoContinueAtUsageLimit=true` の形ではオンにできない）。オフのままなら、上限に達した時点で朝まで止まることを伝える
5. `<作業ブランチ>` から `overnight/YYYY-MM-DD` を作って切り替える。時間の上限があれば、`date` で始めた時刻を控える
6. 次のことを伝えて、OKをもらう
   - これ以降は朝まで質問しない
   - 権限の確認で止まらないよう、auto モードで動かす必要がある。画面下部に `auto mode on` と出ているかを見てもらう
   - 出ていなければ、`Shift+Tab` を何度か押して auto モードにしてもらう（Claude Code は通常 auto モードで始まるが、設定で別のモードにしていることがある）
   - auto モードでも、操作のブロックが続くと（3回続けてか、合計20回）権限の確認に戻り、そこで朝まで止まることがある
   - push とデプロイはしない。朝に `overnight/YYYY-MM-DD` を見てから取り込む（`overnight/` ブランチでは、push・PR・Issue の作成はフックが拒否する）
   - 使用量の上限で止まったときに自動で続くのは、主に次の条件がそろうとき: Claude Code を開いたままにしている（閉じる、`/clear` する、Remote Control やバックグラウンドに移す、のどれでも待つのをやめる）、claude.ai のサブスクリプションでログインしている、Claude Code が古すぎない、リセットが24時間以内（週の上限のように先のものは待たない）。ただし、自動で続けるのは3回まで
   - 上限を設けずに進めると、週の使用量も減る。残しておきたいなら、件数か時間で区切る
   - PC をスリープさせない。スリープが30分ほどを超え、その間にリセットされると、Enter を押すまで止まる（macOS なら別の端末で `caffeinate -i` を動かしておく。ノート PC はふたを閉じず、電源につないでおく）

OKをもらったら、以降は人間に聞かない。

## 進め方

任せたタスクを上から順に、1つずつ進める。

1. タスクを作業中にする
2. developer を新しく呼ぶ。伝えること:
   - タスクのIDと完了条件
   - 夜間の作業で、人間には聞けないこと。人間の判断が要る点が出たら、自分の定義の「人間の判断が要るとき」に従って止まり、返すこと
   - コミットは `overnight/YYYY-MM-DD` に行うこと
   - auto モードにブロックされた操作は、言い換えて繰り返さないこと。止まって、何がブロックされたかを返すこと
3. developer の報告で分ける
   - 完了した: 次のタスクへ
   - 人間の判断が要る: 下の「人間の判断が要るとき」へ
   - 操作がブロックされた: 作業中の変更を `git stash push -m "<ID> ブロック"` で退避し、何がブロックされたかを判断待ちに残す。次のタスクへ
   - テストかレビューが、直しても通らなかった: 作業中の変更を `git stash push -m "<ID> 通らない"` で退避し、タスクを判断待ちに移して、何が通らないかを残す。次のタスクへ
4. 上限に達したか（上限がなければ、任せたタスクを終えたか）、進められるタスクがなくなったら、「朝の報告」を書いて終える

使用量の上限で止まったあと、自動で続きを始めたら、まず `git status` と作業中のタスクを確かめる。途中の変更があれば、そのタスクを developer に続けさせる。

## 人間の判断が要るとき

1. 判断待ちに足す。書くこと: 聞きたいこと（一文）、考えた案、出どころのタスク
2. そのタスクをどうするかを、advisor に「この判断は後から簡単に変えられるか。変えられるなら、どの案で仮に進めるか」と聞いて決める
   - **後から簡単に変えられる**: advisor が勧める案で developer に続けさせ、タスクを終わらせる。判断待ちに「仮で〇〇にした（コミット <hash>）」と書き足す
   - **データの形、ユーザーに見える言葉や流れ、守る方針に関わる**: 仮に決めない。作業中の変更を `git stash push -m "<ID> 判断待ち"` で退避し、タスクは作業中から外す
3. 残りのタスクのうち、この判断に左右されるものを探す。あれば飛ばし、判断待ちの「待っているタスク」に書く
4. 次のタスクへ進む

## 判断待ちの置き場所

<docs/tasks.md の場合>
- `docs/tasks.md` の「人間の判断待ち」に書き、`overnight/YYYY-MM-DD` にコミットする

<GitHub Issues の場合>
- Issue は作らない（作るには人間の確認が要るため。`overnight/` ブランチではフックも拒否する）。朝の報告にだけ書く。朝に人間が `/task add` で足す

## 朝の報告

終えるときに `docs/_wip/overnight-YYYY-MM-DD.md` に書いてコミットし、同じ内容を最後のメッセージにも出す。

```markdown
# 夜間の作業 YYYY-MM-DD

ブランチ: overnight/YYYY-MM-DD（<作業ブランチ> の <hash> から）

## 人間の判断待ち（まずここに答える）
- 問い — 案 — 出どころ — 仮で決めたこと（あれば） — 待っているタスク

## 終わったタスク
- T-003 … — コミット <hash>

## 飛ばした・止めたタスク
- T-005 … — 理由 — 退避した変更（stash の名前）

## タスク候補（developer と advisor から）
- …

## 最後に走らせた型検査とテスト
（出力の末尾を貼る）
```

朝に人間がこのファイルを読み、判断待ちに答えたら、このファイルは削除する。

## してはいけないこと

- 始める前の確認のあとに、人間に質問する
- push、デプロイ、DBのマイグレーションなど取り返しのつかない操作をする（手順書スキルがあっても使わない）
- `overnight/YYYY-MM-DD` 以外のブランチにコミットする
- 新しいタスクを足す（タスク候補として朝の報告に書くだけ）
- 判断待ちを自分で決めて閉じる
- auto モードにブロックされた操作を、言い換えて繰り返す
- コミットのフックを飛ばす（`--no-verify` を使う）
````

### /handoff スキルの作成

`.claude/skills/handoff/SKILL.md` を作成する。コンテキストが残り少なくなったときに打つと、今の状態を残して、クリア後に続きをやるためのプロンプトを出す。

続きに必要なことは、**まずハーネスの決まった置き場所（タスク・詳細設計・判断・コミット）に残し**、どこにも収まらない作業途中の状態だけを短い引き継ぎメモに書く。メモは再開したら消す使い捨てにして、内容が古くなって残り続けないようにする。

`<...>` はA4〜A7の内容で埋める。

````markdown
---
name: handoff
description: コンテキストをクリアする前に、今の状態を残し、クリア後に続きをやるためのプロンプトを出す。
disable-model-invocation: true
---

# /handoff - クリアの前に引き継ぎを残す

## 1. 決まった置き場所を最新にする

引き継ぎメモに書く前に、まず次を今の状態に合わせる。ここに書いたことは、メモでは繰り返さない。

- タスク（<docs/tasks.md または GitHub Issues>）: 作業中のタスクの状態。終わったものは `/task done` の手順で閉じる
- 詳細設計（`docs/_wip/<テーマ>.md`）: 会話の中で変わった設計や段取り
- 判断（`docs/decisions/`）: 会話で決めたことのうち、退けた案があってまだ記録していないもの
- コミット: 区切りのよい変更があれば、コミットするかを人間に聞く。勝手にはしない

## 2. 引き継ぎメモを書く

どこにも収まらない作業途中の状態だけを、`docs/_wip/handoff.md` に書く（すでにあれば上書きする）。

```markdown
# 引き継ぎ（YYYY-MM-DD HH:MM）

## やっていること
- タスク: T-003 …（詳細設計: docs/_wip/…）
- 今の段階: （例: 実装ステップ3のうち2まで終わり、テストが1件落ちている）

## まだコミットしていない変更
- ファイル — 何のための変更か（`git status` で確かめて書く）

## 次にやること
1. …

## 分かったこと・はまりどころ
- （試してだめだったこと、気をつけること）

## 人間が言ったこと・待っている判断
- （会話の中で人間が伝えた好みや指示、聞いていてまだ答えがないこと）
```

- 短く書く。docs/ やタスクにあることは、場所を示すだけにする
- 会話にしか残っていないこと（試したこと、人間の指示や好み）を優先して残す
- 秘密の値（APIキーなど）は書かない

## 3. 再開用のプロンプトを出す

最後に、次の形で出す。人間がこれを `/clear` のあとに貼る。

```
/clear のあとに、次のプロンプトを貼ってください:

docs/_wip/handoff.md を読んで、続きをやって。作業を始めたら handoff.md は削除して。
```

次にやることがはっきりしていれば、「次は〇〇から」と1行足す。

## してはいけないこと

- `/clear` を自分で打つ（人間が打つ）
- 人間に聞かずにコミットする
- 決まった置き場所に書くべきことを、引き継ぎメモにだけ書く
````

### コミットガードの設定（標準）

秘密の値やDBファイルのコミットを**機械的に止める**仕組みを二層で置く。どちらも同じ検査スクリプトを呼ぶ。

| 層 | 止めるもの | 理由 |
|---|---|---|
| git の pre-commit フック（`.githooks/`） | 人間のコミットも含めて止める | Claude Code のフックだけでは人間のコミットを止められない |
| Claude Code の PreToolUse フック | エージェントの `git commit`、`--no-verify` によるフックの迂回、git フックが無効な環境 | git のフックは clone しただけでは有効にならず、`--no-verify` で飛ばせる |

あわせて、**push・Pull Request・Issue の作成の前に、人間の確認を取る**ようにする。Claude Code は既定で auto モードで始まり、auto モードでは今のリポジトリへの push（既定のブランチも含む）と PR の作成が、確認なしで通るため。`.claude/settings.json` の `permissions.ask` と、PreToolUse フックの `REMOTE_RULES` の両方に入れる（`permissions.ask` は `git -C <dir> push` のような書き方を拾えないので、コマンド全体を見るフックで補う）。`/overnight` の作業中（`overnight/` ブランチ）は、確認を出すと朝まで止まってしまうので、フックが確認ではなく拒否を返す。

#### 1. 検査スクリプト `scripts/check-staged.sh`

技術スタックに関係なく bash で作る。A4で決めたスタックに応じて、DBファイルの拡張子などを調整する。リポジトリに入れてはいけないファイル（ユーザーの写真や音声など）がサービスにある場合は、その拡張子もユーザーと相談して足す。

```bash
#!/usr/bin/env bash
# ステージされた変更に、秘密の値・認証情報・データベースのファイルが含まれていないかを検査する。
# git の pre-commit フック（.githooks/pre-commit）と、Claude Code のフック（.claude/hooks/）の両方から呼ばれる。
# 見つかったら 1 を返す。
set -uo pipefail

cd "$(git rev-parse --show-toplevel)" || exit 1

fail=0
report() { echo "  ✗ $1" >&2; fail=1; }

db_ext='sqlite|sqlite3|db|db3|db-wal|db-shm|db-journal'

while IFS= read -r -d '' f; do
  lower=$(printf '%s' "$f" | tr '[:upper:]' '[:lower:]')
  base=${lower##*/}

  case "$base" in
    .env.example | .env.sample) ;;
    .env | .env.*) report "$f — 秘密の値のファイル（.env）"; continue ;;
    *.pem | *.key | credentials.json | service-account*.json) report "$f — 認証情報のファイル"; continue ;;
  esac

  if [[ "$base" =~ \.(${db_ext})$ ]]; then
    report "$f — データベースのファイル"; continue
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z)

# 追加した行に、API キーらしき文字列がないか
secret_patterns=(
  'sk-ant-[A-Za-z0-9_-]{20,}'                     # Anthropic
  'sk-(proj-|svcacct-|admin-)?[A-Za-z0-9_-]{32,}' # OpenAI
  'AKIA[0-9A-Z]{16}'                              # AWS アクセスキー
  'gh[pousr]_[A-Za-z0-9]{36,}'                    # GitHub トークン
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'            # 秘密鍵
  '(api[_-]?key|secret|token|password|access[_-]?key)["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9_/+=-]{20,}'
)
pattern=$(IFS='|'; echo "${secret_patterns[*]}")

while IFS= read -r -d '' f; do
  [[ "$f" == "scripts/check-staged.sh" ]] && continue
  hits=$(git diff --cached -U0 --no-color -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+' | grep -ainE -e "$pattern" | head -n 3)
  if [[ -n "$hits" ]]; then
    report "$f — API キーらしき文字列"
    while IFS= read -r line; do echo "      ${line:0:120}" >&2; done <<<"$hits"
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z)

if [[ $fail -ne 0 ]]; then
  cat >&2 <<'EOF'

コミットを止めました。上のファイルを `git restore --staged <ファイル>`（最初のコミットの前は `git rm --cached <ファイル>`）でステージから外してください。
誤検知のときも、フックを飛ばさず人間に相談してください。
EOF
  exit 1
fi
exit 0
```

#### 2. git の pre-commit フック `.githooks/pre-commit`

```bash
#!/usr/bin/env bash
# 有効にする: git config core.hooksPath .githooks
exec "$(git rev-parse --show-toplevel)/scripts/check-staged.sh"
```

作成後に以下を実行する。

```bash
chmod +x scripts/check-staged.sh .githooks/pre-commit
git config core.hooksPath .githooks
```

> `core.hooksPath` は clone しただけでは有効にならない。チームで使う場合は、README の環境構築手順に `git config core.hooksPath .githooks` を書くようユーザーに案内する。

#### 3. Claude Code の PreToolUse フック

フック本体は**A4で決めた言語**で書く（Node.js なら `.claude/hooks/guard-bash.mjs`、Python なら `.claude/hooks/guard_bash.py`）。フックへの入力は**標準入力のJSON**で渡される（`tool_input.command` に実行しようとしているコマンドが入る）。

- 止める（deny）: 終了コード 2 で終わり、理由を標準エラーに書く
- 人間に確認を求める（ask）: 標準出力に `permissionDecision: "ask"` のJSONを書いて、終了コード 0 で終わる

Node.js の例：

```js
// Claude Code の PreToolUse フック（Bash）。
// - git commit: フックを飛ばす指定を止め、ステージした変更を scripts/check-staged.sh で検査する
// - push・PR・Issue の作成と、本番を壊しうるコマンド: 人間に確認を求める（REMOTE_RULES / ASK_RULES）
// - /overnight の作業中（overnight/ ブランチ）は、確認の代わりに拒否する
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

let input = {};
try { input = JSON.parse(readFileSync(0, "utf8")) ?? {}; } catch {}
const cmd = String(input?.tool_input?.command ?? "").replace(/\\\r?\n/g, "");
const projectDir = process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd();
const workDir = input.cwd && existsSync(input.cwd) ? input.cwd : projectDir; // worktree / cd 先を見る
// 判定には、引用符の中身とヒアドキュメントの中身を除いたコマンドを使う（コミットメッセージや
// grep の引数に「git push」「-n」と書いてあるだけで止まらないようにする）。
const QUOTED = String.raw`\$'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|'[^']*'`;
function strip(s) {
  return s
    .replace(/<<-?\s*(['"]?)(\w+)\1([^\n]*)\n(?:[\s\S]*?\n)??[ \t]*\2(?=\s|\)|$)/g, "$3")
    .replace(new RegExp(QUOTED, "g"), '""');
}
// bash -c "..." / sh -c '...' / eval "..." の中身は、コマンドとして見る
const inner = [...cmd.matchAll(new RegExp(String.raw`\b(?:(?:ba|z|da)?sh\s+(?:-\w+\s+)*-\w*c|eval)\s+(` + QUOTED + ")", "g"))]
  .map((m) => m[1].replace(/^\$?['"]|['"]$/g, ""));
const bare = [cmd, ...inner].map(strip).join("\n");

function deny(reason) {
  process.stderr.write(reason + "\n");
  process.exit(2);
}

function ask(reason) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "ask",
        permissionDecisionReason: reason,
      },
    }),
  );
  process.exit(0);
}

// ---- git commit ----
const isCommit = /\bgit\s+(?:-[cC]\s+\S+\s+|--?[\w-]+(?:=\S+)?\s+)*commit\b/.test(bare);
if (isCommit) {
  if (/--no-veri\w*/.test(bare) || /\bcommit\b[^;&|\n]*\s-[aeiopqsvz]*n/.test(bare)) {
    deny("コミットのフックを飛ばす指定（--no-verify / -n）は使えません。");
  }
  if (/core\.hookspath|GIT_CONFIG_/i.test(bare) || /(?:-c\s*|--config-env[=\s])["']?core\.hookspath/i.test(cmd)) {
    deny("コミットのときに core.hooksPath を変えることはできません。");
  }

  let hooksPath = "";
  try {
    hooksPath = execFileSync("git", ["config", "--get", "core.hooksPath"], { cwd: workDir, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
  } catch {}
  if (hooksPath !== ".githooks") {
    deny("git のコミット前フックが有効になっていません。先に `git config core.hooksPath .githooks` を実行してください。");
  }

  const r = spawnSync("bash", [join(projectDir, "scripts/check-staged.sh")], { cwd: workDir, encoding: "utf8" });
  if (r.status !== 0) {
    deny((r.stderr || "") + (r.stdout || "") || "scripts/check-staged.sh が失敗しました。");
  }
}

// ---- push・PR・Issue の作成と、本番を壊しうるコマンド: 人間に確認を求める ----
// /overnight の作業中（overnight/ ブランチ）は、確認を出すと朝まで止まってしまうので、
// push・PR・Issue の作成と ASK_RULES のコマンドは、確認ではなく拒否する。Claude は理由を受け取って先へ進む。
function branchOf(dir) {
  const git = (...a) => {
    try { return execFileSync("git", a, { cwd: dir, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim(); } catch { return ""; }
  };
  const b = git("symbolic-ref", "--short", "-q", "HEAD"); // コミット前のブランチでも取れる
  if (b) return b;
  for (const p of ["rebase-merge/head-name", "rebase-apply/head-name"]) { // rebase 中（detached HEAD）
    try { return readFileSync(git("rev-parse", "--path-format=absolute", "--git-path", p), "utf8").trim().replace(/^refs\/heads\//, ""); } catch {}
  }
  return "";
}
// worktree で作業しているときのために、作業中のディレクトリとプロジェクトの両方を見る
const overnight = [workDir, projectDir].some((d) => branchOf(d).startsWith("overnight/"));

// push・PR・Issue の作成は既定で入れておく（auto モードでは確認なしで通るため）。
const GH = String.raw`\bgh\s+(?:(?:-R|--repo)[=\s]\S+\s+)?`;
const REMOTE_RULES = [
  [/\bgit\s+(?:-[cC]\s+\S+\s+|--?[\w-]+(?:=\S+)?\s+)*(?:(?:subtree|lfs)\s+)?push(?![\w-])(?![^;&|\n]*\s(?:--dry-run|--help|-h)\b)/, "リモートへの push です。"],
  [new RegExp(GH + String.raw`pr\s+(create|merge)\b`), "Pull Request の作成・マージです。"],
  [new RegExp(GH + String.raw`issue\s+create\b`), "Issue の作成です。"],
];
for (const [re, reason] of REMOTE_RULES) {
  if (!re.test(bare)) continue;
  if (overnight) deny(reason + " 夜間の作業（overnight/ ブランチ）では行いません。朝の報告に書いて、先へ進んでください。");
  ask(reason + " 内容を確かめてから許可してください。");
}

// 本番を壊しうるコマンドは、A4 で決めたインフラに合わせて足す。例:
//   [/\bprisma\s+migrate\s+deploy\b/, "本番のDBにマイグレーションを適用するコマンドです。"],
//   [/\bterraform\s+(apply|destroy)\b/, "インフラを変更するコマンドです。"],
const ASK_RULES = [];
for (const [re, reason] of ASK_RULES) {
  if (!re.test(bare)) continue;
  if (overnight) deny(reason + " 夜間の作業（overnight/ ブランチ）では行いません。朝の報告に書いて、先へ進んでください。");
  ask(reason + " 影響を確かめてから許可してください。");
}

process.exit(0);

```

`REMOTE_RULES`（push・PR・Issue の作成）は既定のまま入れる。`ASK_RULES` には、A4で決めたインフラ・DBで**本番を壊しうるコマンド**をユーザーと相談して入れる（なければ空のままでよい）。どちらも、`overnight/` ブランチでは確認ではなく拒否になる。

`.claude/settings.json`：

```json
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(gh pr create *)",
      "Bash(gh pr merge *)",
      "Bash(gh issue create *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.mjs\""
          }
        ]
      }
    ]
  }
}
```

作成後、次の2つを確かめる。

- `.env` を `git add -f .env` でステージして `git commit` を試み、止まること（`.gitignore` に入っているので `-f` が要る。初期コミットの前なので、確かめた後は `git rm --cached .env` でステージから外す）
- push を見分けられること。`{"tool_input":{"command":"git -C . push"}}` と書いたファイル（例: `/tmp/push-test.json`）を Write ツールで作り、`node .claude/hooks/guard-bash.mjs < /tmp/push-test.json` を実行して、`permissionDecision: "ask"` が返ることを確かめる（コマンドに直接 push の文字を書くと、確かめるコマンド自体にフックが反応するため、ファイル経由で渡す。リモートがまだなくても確かめられる）

Python などで書く場合も、次のことは同じように入れる。

- `REMOTE_RULES`（push・PR・Issue の作成）と、`overnight/` ブランチでの拒否（作業中のディレクトリとプロジェクトの両方のブランチを見る）
- 引用符・ヒアドキュメントの中身を除いて判定すること。ただし `bash -c "..."`・`sh -c '...'`・`eval "..."` の中身はコマンドとして見る
- コミットの検査（`--no-verify` / `-n`、`core.hooksPath` の変更）も、引用符の中身を除いて判定すること（コミットメッセージに `-n` と書いただけで止めない）

> このフックと `permissions.ask` で、普通の書き方の push・PR・Issue の作成には確認が出る。ただし、`gh api` で直接作る、`echo "$(git push)"` のように引用符の中で実行する、git のエイリアスを使う、など拾えない書き方もある。確認を確実な防御とは考えず、作業の区切りで人間が確かめることと組み合わせる。
>
> コミットの検査（`scripts/check-staged.sh`）は、Claude が作業しているディレクトリで行う。`cd` や `git -C` で別の作業ツリーに移ってコミットした場合はフックでは拾えないことがあるが、git のコミット前フック（`.githooks/pre-commit`）が止める。

### 自動フォーマットのフック（任意）

ユーザーに「コード自動フォーマットを設定しますか？」と確認する。
YESの場合、A4で決定した技術スタックに合ったフォーマッターを `.claude/settings.json` の `PostToolUse` に追加する。編集したファイルのパスは標準入力のJSONの `tool_input.file_path` に入っている（`jq` が必要）。

フォーマッターの例：
- JavaScript/TypeScript: `npx prettier --write`
- Python: `ruff format`
- Go: `gofmt -w`
- Rust: `rustfmt`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs <技術スタックに合ったフォーマットコマンド>"
          }
        ]
      }
    ]
  }
}
```

### テスト戦略の確認

ユーザーに以下を確認する：

- テストフレームワークの選択（Jest / Vitest / pytest 等）
- E2Eテストの必要性（Playwright等）
- テストのディレクトリ構成

確認結果を `docs/implementation-policy.md` の「テスト」と、`CLAUDE.md` の「よく使うコマンド」、qa-engineer の定義に反映する。

### 初期コミット

全てのファイルが揃ったら、ユーザーに確認の上で初期コミットを行う。

```
docs: プロジェクトの初期ドキュメントを作成

- docs/requirements.md（要件と守る方針）
- docs/spec.md（基本仕様）
- docs/implementation-policy.md（実装の方針）
- docs/decisions/（なぜそう決めたか）
- docs/README.md（ドキュメントの方針）
- docs/tasks.md（最初のタスク。ファイルを選んだ場合）

chore: プロジェクトの開発基盤を構築

- CLAUDE.md（目次と約束）
- .claude/agents/（advisor, developer, qa-engineer, code-reviewer）
- .claude/skills/（consult, ask-advisor, commit, task, overnight, handoff）
- .claude/settings.json, .claude/hooks/, .githooks/, scripts/check-staged.sh（コミットガード）
- .gitignore
```

**完了条件**: スキルとコミットガードが作成され、ガードが `.env` のコミットを止めることを確かめ、最初のタスクが作られ、初期コミットが完了した。

---

## A8：取り返しのつかない操作の手順書スキル（任意）

ユーザーに「本番へのデプロイ、DBのマイグレーション、秘密の値の登録など、間違えると取り返しのつかない操作の手順をスキルにしますか？」と確認する。今決まっていなければ、必要になったときに作ればよいと伝えて飛ばす。

作る場合は、操作ごとに `.claude/skills/<操作名>/SKILL.md` を以下の型で作る。

```markdown
---
name: <操作名（例: db-migrate）>
description: <何を、どの順で行うか>。<いつ使うか>。本番に適用する前には、必ず人間の確認を取る。
argument-hint: "[local|staging|production]"
---

# <操作名>

<なぜ慎重に行うのか（1〜2行）>。順番を飛ばさないでください。

## 前提

- 環境の名前や設定は <設定ファイル> を正とする
- <ステージングと本番が同じリソースを指していないか、最初に確かめる、など>

## 1. 手元で行う
## 2. ステージングで行い、確かめる
## 3. 本番で行う（必ず人間の確認を取る）

**ここから先は、人間の確認なしに進めてはいけません。**

1. 次のことを人間に示して、進めてよいかを聞く: 何を適用するか、データが消える変更があるか、ステージングで確かめた結果
2. 了解を得てから実行する

## うまくいかなかったとき

- <戻し方。戻せないなら、そう書く>
```

手順書スキルで扱うコマンドは、A7の `ASK_RULES` にも入れて、フックでも人間の確認が挟まるようにする。

**完了条件**: ユーザーが作ると決めた手順書スキルが作成された（作らない場合はスキップ）。

---

## 完了：Phase Bへの橋渡し

全ステップが完了したら、以下を表示する：

```
プロジェクトの土台が完成しました！

■ 作成されたもの
  docs/requirements.md            — 要件と守る方針
  docs/spec.md                    — 基本仕様
  docs/implementation-policy.md   — 実装の方針（迷ったときの倒し方）
  docs/decisions/                 — なぜそう決めたか
  docs/_wip/                      — 実装中の詳細設計（終わったら移すか削除）
  docs/README.md                  — ドキュメントの方針
  docs/tasks.md / GitHub Issues   — タスク（MVPから作った最初の一覧）
  CLAUDE.md                       — 目次と約束
  .claude/agents/                 — advisor, developer, qa-engineer, code-reviewer
  .claude/skills/                 — consult, ask-advisor, commit, task, overnight, handoff
  .claude/settings.json ほか       — コミットガード
  .gitignore                      — セキュリティ基本設定

■ これからの開発の進め方（Phase B）

  0. /task              → 次にやるタスクを選ぶ（新しい案は /task add で増やす）
  1. /consult           → 作りたい機能をClaudeと壁打ち（要件は requirements.md へ）
  2. /plan              → Plan Mode で実装計画を立てる
  2.5. 永続化           → 計画を docs/_wip/<テーマ>.md に詳細設計として保存
  3. developer に依頼   → 実装 → qa-engineer → code-reviewer → コミット
  4. /ask-advisor 区切りのレビュー → 機能のまとまりが一つできたら全体を見てもらう
  5. 片付け             → docs/_wip/ の内容を docs/ に移すか削除する
                          /task done で閉じ、レビューの「→タスク」とdeveloperのタスク候補を /task add する

  ※ 寝る前は /overnight → 任せたタスクを朝まで進める。判断が要る点は残して先へ進む
    朝に docs/_wip/overnight-<日付>.md を読み、判断待ちに答えてからブランチを取り込む

  ※ 迷った判断は /ask-advisor に相談し、docs/decisions/ に残してください。
    セッションは消えますが、ドキュメントは残ります。

■ モデルの使い分け
  日常コーディング → /model sonnet（コスパ最強）
  複雑な設計判断   → /model opus（深い推論力）
  簡単な作業       → /model haiku（最速・最安）

■ コンテキスト管理
  タスクが変わったら → /clear（リセット）
  残り少なくなったら → /handoff で状態を残す → /clear → 出てきたプロンプトを貼る
  急ぎで続けたいなら → /compact（圧縮。ファイルには残らない）

■ 困ったら
  Esc+Esc → チェックポイントに巻き戻し
  /clear → 最初からやり直し（学んだことを含めて再指示）
```
