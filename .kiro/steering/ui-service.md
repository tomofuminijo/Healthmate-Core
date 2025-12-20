# HealthmateUI サービス

## Service Overview

HealthmateUI サービスは、Healthmate プロダクトのWebフロントエンドを担当し、ユーザーが健康管理機能にアクセスするためのインターフェースを提供します。

### Primary Responsibilities

- **User Interface**: 健康データの入力・表示・管理のためのWebUI
- **Authentication Flow**: Cognito OAuth 2.0による認証フロー管理
- **MCP API Integration**: HealthManagerMCP サービスとの連携
- **AI Agent Integration**: HealthCoachAI サービスとのチャット機能
- **Multi-language Support**: 日本語・英語対応

### Service Architecture

- **Framework**: FastAPI + htmx
- **Runtime**: AWS Lambda (Python 3.12)
- **Container**: Docker + Amazon ECR
- **Static Hosting**: Amazon S3 + CloudFront
- **Authentication**: Amazon Cognito OAuth 2.0 integration (Healthmate-Coreから継承)
- **API Communication**: RESTful API calls to MCP Gateway
- **State Management**: Session-based state management

### Key Features

#### Health Data Management
- **User Profile**: ユーザー情報の表示・編集
- **Goal Setting**: 健康目標の作成・管理・進捗表示
- **Policy Management**: 健康ポリシーの設定・管理
- **Activity Logging**: 日々の活動記録（食事、運動、体重等）

#### AI Integration
- **Health Coach Chat**: HealthCoachAI サービスとのリアルタイムチャット
- **Personalized Advice**: AIからの健康アドバイス表示
- **Progress Analysis**: AIによる健康データ分析結果の可視化
- **Session Continuity**: 会話の継続性を保持したチャット体験

### Authentication Patterns

#### Cognito OAuth 2.0 Flow
```python
# FastAPI認証設定例
from app.auth.cognito import CognitoAuth

cognito_auth = CognitoAuth(
    user_pool_id=config.COGNITO_USER_POOL_ID,
    client_id=config.COGNITO_CLIENT_ID,
    client_secret=config.COGNITO_CLIENT_SECRET,
    region=config.AWS_REGION
)
```

#### JWT Token Management
```python
# JWTトークンの管理と自動更新
class SessionManager:
    def __init__(self):
        self.token_store = {}
    
    async def get_valid_token(self, session_id: str) -> str:
        # Token refresh logic
        # User session management
        pass
```

### API Integration Patterns

#### MCP API Calls
```python
# HealthManagerMCP サービスとの連携
class MCPClient:
    def __init__(self, gateway_endpoint: str):
        self.base_url = gateway_endpoint
    
    async def call_mcp_tool(self, tool_name: str, parameters: dict) -> dict:
        token = await self.get_valid_token()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{tool_name}",
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                },
                json=parameters
            )
            return response.json()
```

#### HealthCoachAI Integration
```python
# HealthCoachAI サービスとの連携
class HealthCoachClient:
    async def send_message(self, message: str, session_id: str, jwt_token: str) -> str:
        payload = {
            "prompt": message,
            "sessionState": {
                "sessionAttributes": {
                    "session_id": session_id,
                    "jwt_token": jwt_token,
                    "timezone": "Asia/Tokyo",
                    "language": "ja"
                }
            }
        }
        # AgentCore invoke call
        return await self.invoke_agent(payload)
```

#### Error Handling
```python
# 統一されたエラーハンドリング
async def handle_api_error(error: Exception) -> dict:
    if isinstance(error, httpx.HTTPStatusError):
        if error.response.status_code == 401:
            # Token expired - redirect to login
            return {"error": "AUTHENTICATION_REQUIRED", "redirect": "/login"}
        elif error.response.status_code == 403:
            # Insufficient permissions
            return {"error": "INSUFFICIENT_PERMISSIONS"}
    return {"error": "INTERNAL_ERROR", "message": str(error)}
```

### UI/UX Patterns

#### Responsive Design
- **Mobile-First**: スマートフォンでの利用を優先
- **Progressive Web App**: PWA対応でネイティブアプリ体験
- **Accessibility**: WCAG 2.1 AA準拠のアクセシビリティ

#### Component Structure
```
app/
├── auth/                       # 認証関連
│   ├── cognito.py             # Cognito認証クライアント
│   ├── session.py             # セッション管理
│   ├── middleware.py          # 認証ミドルウェア
│   └── routes.py              # 認証APIルート
├── chat/                      # AIチャット機能
├── health/                    # 健康管理機能
├── models/                    # データモデル
│   └── auth.py               # 認証関連モデル
└── utils/                     # ユーティリティ
    ├── config.py             # 設定管理
    └── logger.py             # ログ設定
```

### State Management Patterns

#### Health Data State
```python
# 健康データの状態管理
class HealthDataManager:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.cache = {}
    
    async def get_user_data(self, user_id: str) -> dict:
        # Cache management
        # MCP API calls
        pass
    
    async def update_goal(self, user_id: str, goal_id: str, updates: dict) -> dict:
        # Update operations
        pass
```

#### Chat State
```python
# AIチャットの状態管理
class ChatManager:
    def __init__(self, coach_client: HealthCoachClient):
        self.coach_client = coach_client
        self.sessions = {}
    
    async def send_message(self, session_id: str, message: str) -> dict:
        # Message handling
        # Session continuity
        pass
```

### Development Patterns

#### Environment Configuration
```python
# 環境別設定
class Config:
    def __init__(self):
        self.AWS_ACCOUNT_ID = os.getenv('AWS_ACCOUNT_ID')
        self.COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
        self.COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
        self.COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')
        self.HEALTH_COACH_AI_RUNTIME_ID = os.getenv('HEALTH_COACH_AI_RUNTIME_ID')
        self.MCP_GATEWAY_ENDPOINT = os.getenv('MCP_GATEWAY_ENDPOINT')
```

#### Auto-Configuration
```python
# 自動設定機能
class AutoConfig:
    async def get_cognito_config_from_cloudformation(self) -> dict:
        # CloudFormationスタックから設定を取得
        pass
    
    async def get_agentcore_runtime_id(self) -> str:
        # AgentCore CLIから設定を取得
        pass
```

#### Testing Strategy
- **Unit Tests**: コンポーネント単体テスト
- **Integration Tests**: API連携テスト
- **E2E Tests**: ユーザーフロー全体のテスト
- **Accessibility Tests**: アクセシビリティ自動テスト

### Integration Points

- **Healthmate-Core サービス**: Cognito認証の共有
- **HealthManagerMCP サービス**: MCP Gateway経由でのデータCRUD操作
- **HealthCoachAI サービス**: AgentCore経由でのリアルタイムチャット

### Development Commands

#### 仮想環境セットアップ
```bash
cd HealthmateUI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Development Server
```bash
# 自動設定付き開発サーバー
python run_dev.py
```

#### Testing
```bash
# 単体テスト
pytest tests/unit/ -v

# 統合テスト
pytest tests/integration/ -v

# カバレッジ付きテスト
pytest --cov=app --cov-report=html
```

#### Code Quality
```bash
# フォーマット
black app/ tests/

# リント
flake8 app/ tests/

# 型チェック
mypy app/
```

### Service-Specific Best Practices

- **Security**: JWTトークンの安全な保存（HttpOnly cookies推奨）
- **Performance**: 健康データの効率的なキャッシング
- **User Experience**: オフライン対応とデータ同期
- **Privacy**: 健康データの適切な暗号化と表示制御
- **Internationalization**: 多言語対応の実装パターン（日本語優先）
- **Session Management**: AgentCore Memoryとの連携によるチャット継続性
- **Auto-Configuration**: CloudFormationとAgentCoreからの自動設定取得