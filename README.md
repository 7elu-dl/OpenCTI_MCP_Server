# OpenCTI FastMCP サーバー

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.13+-green.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **English documentation is available in [README_EN.md](README_EN.md)**

Claude AIを[OpenCTI](https://www.opencti.io/)脅威インテリジェンスプラットフォームに接続するModel Context Protocol (MCP)サーバーです。[FastMCP](https://github.com/jlowin/fastmcp)で構築され、OpenCTIの機能をAI駆動の脅威インテリジェンス分析のための使いやすいツールとして公開します。

## 🌟 機能

### 検索と発見
- **11の検索ツール**: インジケーター、脅威アクター、侵入セット、キャンペーン、マルウェア、攻撃パターン、インフラストラクチャ、脆弱性、レポート、ツール、インシデントを検索
- **スマートフィルタリング**: キーワードで検索し、結果を制限
- **豊富なメタデータ**: STIX準拠の包括的な脅威インテリジェンスデータを取得

### Observable管理
- **自動検出**: IPアドレス、ドメイン、ファイルハッシュを自動識別
- **重複排除**: 作成前に既存のObservableをチェック
- **VirusTotal統合**: VirusTotalコネクタ経由でObservableのエンリッチメントをリクエスト

### 関係性と分析ツール
- **関係性分析**: エンティティ間の接続を探索
- **エンティティインジケーター**: 特定のエンティティに関連するインジケーターを取得
- **攻撃パターンマッピング**: 脅威アクターやマルウェアが使用するTTPを取得
- **Observable追跡**: エンティティに関連付けられたObservableを検索
- **ノート管理**: アナリストのノートやコメントにアクセス

### 高度な機能
- **GraphQLクエリ**: カスタムデータ取得のための任意のGraphQLクエリを実行
- **エンティティ取得**: 任意のSTIXオブジェクトの詳細情報を取得
- **STIX ID検索**: STIX識別子でエンティティを検索
- **コネクタ管理**: エンリッチメントコネクタの一覧表示と管理
- **マルウェア分析**: 包括的なマルウェアファミリー情報を取得
- **型安全性**: IDE サポート向上のための完全なPython型ヒント

## 📋 要件

- **Python**: 3.10以上
- **OpenCTI**: OpenCTIインスタンスへのアクセス (v5.x または v6.x)
- **APIトークン**: 適切な権限を持つ有効なOpenCTI APIトークン

## 🚀 クイックスタート

### 1. インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/OpenCTI_MCP_Claude.git
cd OpenCTI_MCP_Claude

# パッケージをインストール
pip install -e .
```

### 2. 設定

プロジェクトルートに`.env`ファイルを作成:

```bash
# 必須
OPENCTI_URL=https://your-opencti.example.com
OPENCTI_TOKEN=your_api_token_here

# オプション
OPENCTI_VERIFY_SSL=true                    # SSL検証の有効化/無効化 (デフォルト: true)
OPENCTI_TIMEOUT=30                         # リクエストタイムアウト（秒）(デフォルト: 30)
VIRUSTOTAL_CONNECTOR_ID=your_vt_connector  # VirusTotalエンリッチメント用
```

### 3. サーバーの起動

```bash
# MCPサーバーを起動（STDIO トランスポート）
opencti-mcp

# または、Pythonで直接実行
python -m opencti_mcp.server
```

サーバーが起動し、STDIO経由でMCPプロトコルメッセージをリスニングし、Claude Desktopやその他のMCPクライアントと接続できる状態になります。

## 🔧 Claude Desktop統合

Claude Desktopの設定ファイルに以下の設定を追加してください:

**macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "opencti": {
      "command": "python",
      "args": [
        "D:/code/OpenCTI_MCP_Claude/opencti_mcp/server.py"
      ],
      "env": {
        "OPENCTI_URL": "https://your-opencti.example.com",
        "OPENCTI_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Claude Desktopを再起動してサーバーをロードしてください。

## 🛠️ 利用可能なツール（全23種類）

### 検索ツール（11種類）

すべての検索ツールは以下のオプションパラメータを受け取ります:
- `search` (文字列、オプション): 結果をフィルタリングする検索語句
- `limit` (整数、デフォルト: 25): 返す結果の最大数

#### 1. `search_indicators`
OpenCTI内のIndicators of Compromise (IoC)を検索します。

**戻り値**: パターンタイプ、有効期限、スコア、STIXメタデータを含むインジケーター

**例**:
```
Claude: 「ransomware」に関連するインジケーターを検索して
```

#### 2. `search_threat_actors`
脅威アクターのプロファイルとAPTグループを検索します。

**戻り値**: エイリアス、動機、高度化レベル、目標を含む脅威アクター

**例**:
```
Claude: スパイ活動キャンペーンに関連する脅威アクターを見つけて
```

#### 3. `search_intrusion_sets`
組織化された脅威グループと侵入セットを検索します。

**戻り値**: エイリアス、目標、リソースレベル、動機を含む侵入セット

#### 4. `search_campaigns`
攻撃キャンペーンを検索します。

**戻り値**: 目的、時系列情報、エイリアスを含むキャンペーン

#### 5. `search_malware`
マルウェアファミリーとサンプルを検索します。

**戻り値**: タイプ、機能、実装言語、実行環境を含むマルウェア

#### 6. `search_attack_patterns`
MITRE ATT&CKパターンを含むTTPs（戦術、技術、手順）を検索します。

**戻り値**: MITRE ID、プラットフォーム、必要な権限、検出方法を含む攻撃パターン

#### 7. `search_infrastructures`
攻撃者のインフラストラクチャを検索します。

**戻り値**: タイプ、時間範囲、エイリアスを含むインフラストラクチャ

#### 8. `search_vulnerabilities`
CVEと脆弱性情報を検索します。

**戻り値**: CVSSスコア、深刻度、攻撃ベクトル、影響評価を含む脆弱性

#### 9. `search_reports`
脅威インテリジェンスレポートを検索します。

**戻り値**: タイプ、公開日、信頼度を含むレポート

#### 10. `search_tools`
脅威アクターが使用する攻撃ツールを検索します。

**戻り値**: タイプ、バージョン、エイリアス、STIXメタデータを含むツール

**例**:
```
Claude: 「powershell」に関連するツールを見つけて
```

#### 11. `search_incidents`
OpenCTI内のセキュリティインシデントを検索します。

**戻り値**: 深刻度、タイプ、目的、時系列情報を含むインシデント

**例**:
```
Claude: ランサムウェアインシデントを検索して
```

### Observable管理ツール（2種類）

#### 12. `create_observable`
OpenCTI内に新しいObservable（IPアドレス、ドメイン名、またはファイルハッシュ）を作成します。

**パラメータ**:
- `value` (文字列、必須): Observable の値
- `value_type` (文字列、オプション): `ip`、`domain`、または`hash`を明示的に指定（省略時は自動検出）

**自動検出**:
- **IPアドレス**: IPv4およびIPv6形式の検証
- **ドメイン**: FQDN パターンマッチング
- **ハッシュ**: MD5 (32)、SHA-1 (40)、SHA-256 (64)、SHA-512 (128)

**戻り値**: ステータス（`created`または`exists`）とObservableの詳細

**例**:
```
Claude: IP 192.168.1.100のObservableを作成して
```

#### 13. `ask_virustotal_enrichment`
ObservableのVirusTotalエンリッチメントをリクエストします。

**パラメータ**:
- `value` (文字列、必須): Observableの値
- `value_type` (文字列、オプション): タイプ指定

**要件**: `VIRUSTOTAL_CONNECTOR_ID`が設定されている必要があります

**戻り値**: ワークID、コネクタID、Observable情報

**例**:
```
Claude: このハッシュをVirusTotalでエンリッチして: d41d8cd98f00b204e9800998ecf8427e
```

### エンティティとクエリツール（2種類）

#### 14. `get_entity`
IDで特定のエンティティの詳細情報を取得します。

**パラメータ**:
- `entity_type` (文字列、必須): エンティティタイプ（例: `Indicator`、`ThreatActor`）
- `entity_id` (文字列、必須): OpenCTI内部ID

**戻り値**: 関係性とメタデータを含む完全なエンティティデータ

**例**:
```
Claude: インジケーターID abc123...のエンティティ詳細を取得して
```

#### 15. `execute_graphql`
OpenCTI APIに対して任意のGraphQLクエリを実行します。

**パラメータ**:
- `query` (文字列、必須): GraphQLクエリ文字列
- `variables` (辞書、オプション): クエリ変数

**戻り値**: GraphQLレスポンスの生データ

**例**:
```
Claude: 過去7日間に作成されたすべてのインジケーターを見つけるGraphQLクエリを実行して
```

### 関係性と分析ツール（8種類）

#### 16. `get_entity_relationships`
特定のエンティティのすべての関係性を取得します。

**パラメータ**:
- `entity_id` (文字列、必須): OpenCTI内部ID
- `limit` (整数、デフォルト: 50): 関係性の最大数

**戻り値**: エンティティに接続されたすべての関係性（from/to）

**例**:
```
Claude: この脅威アクターのすべての関係性を表示して
```

#### 17. `get_indicators_by_entity`
特定のエンティティ（脅威アクター、マルウェア、キャンペーンなど）に関連するインジケーターを取得します。

**パラメータ**:
- `entity_id` (文字列、必須): OpenCTI内部ID
- `limit` (整数、デフォルト: 25): インジケーターの最大数

**戻り値**: エンティティに関連付けられたインジケーター

**例**:
```
Claude: このマルウェアファミリーのすべてのインジケーターを見つけて
```

#### 18. `get_attack_patterns_by_entity`
特定のエンティティが使用する攻撃パターン（TTP）を取得します。

**パラメータ**:
- `entity_id` (文字列、必須): OpenCTI内部ID
- `limit` (整数、デフォルト: 25): 攻撃パターンの最大数

**戻り値**: エンティティが使用するMITRE ATT&CKパターンおよびその他のTTP

**例**:
```
Claude: APT28はどの攻撃パターンを使用していますか?
```

#### 19. `get_entity_observables`
特定のエンティティに関連するObservable（IP、ドメイン、ハッシュ）を取得します。

**パラメータ**:
- `entity_id` (文字列、必須): OpenCTI内部ID
- `limit` (整数、デフォルト: 25): Observableの最大数

**戻り値**: エンティティに関連付けられたサイバーObservable

**例**:
```
Claude: このキャンペーンのすべてのObservableを表示して
```

#### 20. `get_entity_notes`
特定のエンティティの分析ノートとコメントを取得します。

**パラメータ**:
- `entity_id` (文字列、必須): OpenCTI内部ID
- `limit` (整数、デフォルト: 10): ノートの最大数

**戻り値**: 内容、著者、タイムスタンプを含むアナリストノート

**例**:
```
Claude: このインシデントのすべてのアナリストノートを取得して
```

#### 21. `search_by_stix_id`
STIX識別子を使用してエンティティを検索します。

**パラメータ**:
- `stix_id` (文字列、必須): STIX ID（例: `threat-actor--12345...`）

**戻り値**: STIXオブジェクトのエンティティデータ

**例**:
```
Claude: STIX ID threat-actor--12345... のエンティティを見つけて
```

#### 22. `list_connectors`
利用可能なすべてのエンリッチメントおよび統合コネクタを一覧表示します。

**戻り値**: タイプ、スコープ、ステータス、設定を含むコネクタの詳細

**例**:
```
Claude: OpenCTIで利用可能なコネクタは何ですか?
```

#### 23. `get_malware_analysis`
マルウェアファミリーの包括的な分析情報を取得します。

**パラメータ**:
- `malware_id` (文字列、必須): マルウェアのOpenCTI内部ID

**戻り値**: 機能、キルチェーンフェーズ、関係性を含む詳細なマルウェアデータ

**例**:
```
Claude: このマルウェアファミリーを詳細に分析して
```

## 📊 使用例

### 例1: 脅威アクター調査
```
ユーザー: APT28について教えて

Claudeが使用:
1. search_threat_actors(search="APT28")
2. get_entity(entity_type="ThreatActor", entity_id="...")
3. search_campaigns() で関連キャンペーンを検索

レスポンス: キャンペーン、TTP、ターゲットを含むAPT28の詳細プロファイル
```

### 例2: マルウェア分析
```
ユーザー: このファイルハッシュを分析して: 5d41402abc4b2a76b9719d911017c592

Claudeが使用:
1. create_observable(value="5d41402abc4b2a76b9719d911017c592")
2. ask_virustotal_enrichment(value="5d41402abc4b2a76b9719d911017c592")

レスポンス: Observableを作成しVT分析を開始
```

### 例3: キャンペーンリサーチ
```
ユーザー: 最新のランサムウェアキャンペーンは何ですか?

Claudeが使用:
1. search_campaigns(search="ransomware")
2. search_malware(search="ransomware")
3. search_indicators() で関連IoC を検索

レスポンス: 包括的なランサムウェアキャンペーンの概要
```

## 🏗️ アーキテクチャ

```
┌─────────────┐
│   Claude    │  ← MCPプロトコル
└──────┬──────┘
       │
┌──────▼──────────────┐
│  FastMCP Server     │  ← このプロジェクト
│  (opencti_mcp)      │
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│  OpenCTI GraphQL    │  ← 脅威インテリジェンス
│  & REST API         │     プラットフォーム
└─────────────────────┘
```

### モジュール構造

```
opencti_mcp/
├── __init__.py          # パッケージ初期化
├── server.py            # FastMCPサーバーとツール定義
├── client.py            # OpenCTI APIクライアント（GraphQL + REST）
├── config.py            # 設定管理
├── queries.py           # GraphQLクエリテンプレート
├── observables.py       # Observableタイプ検出
└── exceptions.py        # カスタム例外
```

## 🔒 セキュリティ

- **APIトークン**: トークンをバージョン管理にコミットしないでください
- **SSL検証**: デフォルトで有効（`OPENCTI_VERIFY_SSL=true`）
- **入力検証**: 多層検証（サーバー → クライアント → API）
- **ネットワークセグメンテーション**: OpenCTIアクセスの制限を検討してください
- **コネクタ権限**: エンリッチメントコネクタの権限を確認してください

## 🐛 トラブルシューティング

### インポートエラー
```bash
# パッケージがインストールされていることを確認
pip install -e .

# Pythonバージョンをチェック
python --version  # 3.10+である必要があります
```

### 接続の問題
```bash
# OpenCTI接続をテスト
curl -H "Authorization: Bearer YOUR_TOKEN" https://your-opencti.example.com/graphql

# テスト用にSSL検証を無効化（本番環境では非推奨）
export OPENCTI_VERIFY_SSL=false
```

### GraphQLエラー
- エンティティIDがOpenCTI内部ID（`standard_id`ではない）であることを確認してください
- 詳細なエラーメッセージについてはOpenCTIログを確認してください
- `execute_graphql`ツールを使用してクエリを対話的にテストしてください

### エンリッチメントが機能しない
- `VIRUSTOTAL_CONNECTOR_ID`が正しく設定されていることを確認してください
- OpenCTI設定でコネクタが有効になっていることを確認してください
- エンリッチメントをリクエストする前にObservableが存在することを確認してください

## 📚 開発

### コードスタイル
- 型ヒント付きPython 3.10+
- Googleスタイルのdocstring
- 不変性のためのfrozenデータクラス
- モジュラーアーキテクチャ（単一責任の原則）

### テスト
```bash
# テスト環境で実行
cp test.env .env
# テストインスタンスの詳細で.envを編集
opencti-mcp
```

### 新しい検索ツールの追加
1. `queries.py`にGraphQLクエリを追加
2. `server.py`に`@app.tool`デコレータ付きのツール関数を作成
3. クエリ設定で`_execute_collection_query()`を呼び出し
4. このREADMEを更新

## 🤝 コントリビューション

貢献を歓迎します！以下の手順に従ってください:

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを開く

## 📝 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細はLICENSEファイルを参照してください。

## 🙏 謝辞

- [OpenCTI](https://www.opencti.io/) - サイバー脅威インテリジェンスプラットフォーム
- [FastMCP](https://github.com/jlowin/fastmcp) - 高速モデルコンテキストプロトコルフレームワーク
- [Anthropic](https://www.anthropic.com/) - Claude AIとMCPプロトコル

## 📞 サポート

- **ドキュメント**: 詳細なプロジェクトガイドは[docs/CLAUDE.MD](docs/CLAUDE.MD)を参照してください
- **例**: 設定テンプレートについては[examples/](examples/)をチェックしてください
- **コントリビューション**: コントリビューションガイドラインは[CONTRIBUTING.md](CONTRIBUTING.md)をお読みください
- **変更履歴**: バージョン履歴は[CHANGELOG.md](CHANGELOG.md)を参照してください
- **問題**: [GitHub Issues](https://github.com/yourusername/OpenCTI_MCP_Claude/issues)経由でバグを報告してください
- **OpenCTIドキュメント**: https://docs.opencti.io/
- **MCPドキュメント**: https://modelcontextprotocol.io/

## 🗺️ ロードマップ

- [x] 関係性トラバーサルツール ✅
- [x] エンティティ固有のクエリ（インジケーター、攻撃パターン、Observable） ✅
- [x] インシデントとツール検索機能 ✅
- [x] マルウェア分析ツール ✅
- [ ] 複数IoC のバッチ操作
- [ ] STIXバンドルのインポート/エクスポート
- [ ] 高度なフィルタリング（信頼度スコア、TLPマーキング）
- [ ] エンティティの作成と更新操作
- [ ] パフォーマンス向上のためのキャッシュレイヤー
- [ ] レート制限とバックオフ戦略
- [ ] WebSocketトランスポートサポート
