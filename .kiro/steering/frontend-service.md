# Healthmate-Frontend サービス

## Service Overview

Healthmate-Frontend サービスは、Healthmate プロダクトのWebフロントエンドを担当し、ユーザーが健康管理機能にアクセスするためのモダンなReactアプリケーションを提供します。

### Primary Responsibilities

- **User Interface**: 健康データの入力・表示・管理のためのモダンWebUI
- **Authentication Flow**: Cognito OAuth 2.0による認証フロー管理
- **MCP API Integration**: HealthManagerMCP サービスとの連携
- **AI Agent Integration**: HealthCoachAI サービスとのチャット機能
- **Multi-language Support**: 日本語・英語対応

### Service Architecture

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: shadcn/ui + Tailwind CSS
- **State Management**: React Query + Zustand
- **Authentication**: Amazon Cognito OAuth 2.0 integration (Healthmate-Coreから継承)
- **API Communication**: Axios/Fetch for REST API calls
- **Deployment**: Static hosting (S3 + CloudFront or Vercel)

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
```typescript
// Cognito認証設定例
import { CognitoUserPool, CognitoUser, AuthenticationDetails } from 'amazon-cognito-identity-js';

const userPool = new CognitoUserPool({
  UserPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,
  ClientId: import.meta.env.VITE_COGNITO_CLIENT_ID,
});

export const authenticateUser = async (username: string, password: string): Promise<string> => {
  return new Promise((resolve, reject) => {
    const user = new CognitoUser({ Username: username, Pool: userPool });
    const authDetails = new AuthenticationDetails({ Username: username, Password: password });
    
    user.authenticateUser(authDetails, {
      onSuccess: (result) => {
        resolve(result.getAccessToken().getJwtToken());
      },
      onFailure: (err) => {
        reject(err);
      },
    });
  });
};
```

#### JWT Token Management
```typescript
// JWTトークンの管理と自動更新
class TokenManager {
  private accessToken: string | null = null;
  
  async getValidToken(): Promise<string> {
    // Token refresh logic
    // User session management
    if (!this.accessToken || this.isTokenExpired()) {
      await this.refreshToken();
    }
    return this.accessToken!;
  }
  
  private isTokenExpired(): boolean {
    // JWT expiration check
    return false;
  }
  
  private async refreshToken(): Promise<void> {
    // Token refresh implementation
  }
}
```

### API Integration Patterns

#### MCP API Calls
```typescript
// HealthManagerMCP サービスとの連携
class MCPClient {
  constructor(private baseUrl: string) {}
  
  async callMCPTool(toolName: string, parameters: Record<string, any>): Promise<any> {
    const token = await tokenManager.getValidToken();
    
    const response = await fetch(`${this.baseUrl}/${toolName}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(parameters),
    });
    
    return response.json();
  }
}
```

#### HealthCoachAI Integration
```typescript
// HealthCoachAI サービスとの連携
class HealthCoachClient {
  async sendMessage(message: string, sessionId: string, accessToken: string): Promise<string> {
    const payload = {
      prompt: message,
      sessionState: {
        sessionAttributes: {
          session_id: sessionId,
          timezone: "Asia/Tokyo",
          language: "ja"
        }
      }
    };
    
    const response = await fetch(this.agentCoreEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
        'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id': sessionId
      },
      body: JSON.stringify(payload)
    });
    
    // Handle streaming response
    return this.handleStreamingResponse(response);
  }
  
  private async handleStreamingResponse(response: Response): Promise<string> {
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let result = '';
    
    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const dataJson = line.substring(6);
            if (dataJson.trim()) {
              const eventData = JSON.parse(dataJson);
              if (eventData.event?.contentBlockDelta?.delta?.text) {
                result += eventData.event.contentBlockDelta.delta.text;
              }
            }
          } catch (e) {
            // JSON解析エラーは無視
          }
        }
      }
    }
    
    return result;
  }
}
```

#### Error Handling
```typescript
// 統一されたエラーハンドリング
export const handleApiError = (error: any): { error: string; message?: string; redirect?: string } => {
  if (error.response?.status === 401) {
    return { error: "AUTHENTICATION_REQUIRED", redirect: "/login" };
  } else if (error.response?.status === 403) {
    return { error: "INSUFFICIENT_PERMISSIONS" };
  }
  return { error: "INTERNAL_ERROR", message: error.message };
};
```

### UI/UX Patterns

#### Responsive Design
- **Mobile-First**: スマートフォンでの利用を優先
- **Progressive Web App**: PWA対応でネイティブアプリ体験
- **Accessibility**: WCAG 2.1 AA準拠のアクセシビリティ

#### Component Structure
```
src/
├── components/                 # 再利用可能なコンポーネント
│   ├── ui/                    # shadcn/ui コンポーネント
│   ├── auth/                  # 認証関連コンポーネント
│   ├── chat/                  # AIチャット機能
│   └── health/                # 健康管理機能
├── pages/                     # ページコンポーネント
├── hooks/                     # カスタムReactフック
├── services/                  # API サービス層
├── utils/                     # ユーティリティ関数
├── types/                     # TypeScript型定義
└── stores/                    # 状態管理 (Zustand)
```

### State Management Patterns

#### Health Data State
```typescript
// 健康データの状態管理 (Zustand)
interface HealthDataStore {
  userData: UserData | null;
  goals: Goal[];
  activities: Activity[];
  fetchUserData: (userId: string) => Promise<void>;
  updateGoal: (goalId: string, updates: Partial<Goal>) => Promise<void>;
}

export const useHealthDataStore = create<HealthDataStore>((set, get) => ({
  userData: null,
  goals: [],
  activities: [],
  
  fetchUserData: async (userId: string) => {
    const mcpClient = new MCPClient(import.meta.env.VITE_MCP_GATEWAY_ENDPOINT);
    const userData = await mcpClient.callMCPTool('getUser', { userId });
    set({ userData });
  },
  
  updateGoal: async (goalId: string, updates: Partial<Goal>) => {
    const mcpClient = new MCPClient(import.meta.env.VITE_MCP_GATEWAY_ENDPOINT);
    await mcpClient.callMCPTool('updateGoal', { goalId, ...updates });
    // Update local state
  },
}));
```

#### Chat State
```typescript
// AIチャットの状態管理
interface ChatStore {
  messages: ChatMessage[];
  sessionId: string;
  isLoading: boolean;
  sendMessage: (message: string) => Promise<void>;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  messages: [],
  sessionId: generateSessionId(),
  isLoading: false,
  
  sendMessage: async (message: string) => {
    set({ isLoading: true });
    
    const coachClient = new HealthCoachClient();
    const accessToken = await tokenManager.getValidToken();
    
    try {
      const response = await coachClient.sendMessage(message, get().sessionId, accessToken);
      
      set(state => ({
        messages: [
          ...state.messages,
          { role: 'user', content: message },
          { role: 'assistant', content: response }
        ],
        isLoading: false
      }));
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },
}));
```

### Development Patterns

#### Environment Configuration
```typescript
// 環境変数の型安全な管理
interface ImportMetaEnv {
  readonly VITE_AWS_REGION: string;
  readonly VITE_COGNITO_USER_POOL_ID: string;
  readonly VITE_COGNITO_CLIENT_ID: string;
  readonly VITE_MCP_GATEWAY_ENDPOINT: string;
  readonly VITE_AGENTCORE_ENDPOINT: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

export const config = {
  awsRegion: import.meta.env.VITE_AWS_REGION,
  cognito: {
    userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,
    clientId: import.meta.env.VITE_COGNITO_CLIENT_ID,
  },
  endpoints: {
    mcpGateway: import.meta.env.VITE_MCP_GATEWAY_ENDPOINT,
    agentCore: import.meta.env.VITE_AGENTCORE_ENDPOINT,
  },
};
```

#### Testing Strategy
- **Unit Tests**: Vitest + React Testing Library
- **Integration Tests**: API連携テスト
- **E2E Tests**: Playwright でのユーザーフロー全体テスト
- **Accessibility Tests**: axe-core による自動アクセシビリティテスト

### Integration Points

- **Healthmate-Core サービス**: Cognito認証の共有
- **HealthManagerMCP サービス**: MCP Gateway経由でのデータCRUD操作
- **HealthCoachAI サービス**: AgentCore経由でのリアルタイムチャット

### Development Commands

#### 環境セットアップ
```bash
cd Healthmate-Frontend
npm install
# または
yarn install
```

#### Development Server
```bash
# 開発サーバー起動
npm run dev
# または
yarn dev
```

#### Testing
```bash
# 単体テスト
npm run test
# または
yarn test

# E2Eテスト
npm run test:e2e
# または
yarn test:e2e

# カバレッジ付きテスト
npm run test:coverage
# または
yarn test:coverage
```

#### Build & Deploy
```bash
# プロダクションビルド
npm run build
# または
yarn build

# プレビュー
npm run preview
# または
yarn preview
```

#### Code Quality
```bash
# TypeScript型チェック
npm run type-check
# または
yarn type-check

# ESLint
npm run lint
# または
yarn lint

# Prettier
npm run format
# または
yarn format
```

### Service-Specific Best Practices

- **Security**: JWTトークンの安全な保存（メモリ内管理推奨）
- **Performance**: React Query による効率的なデータキャッシング
- **User Experience**: Suspense と Error Boundary による優れたローディング体験
- **Privacy**: 健康データの適切な暗号化と表示制御
- **Internationalization**: react-i18next による多言語対応（日本語優先）
- **Session Management**: AgentCore Memory との連携によるチャット継続性
- **Auto-Configuration**: 環境変数による柔軟な設定管理
- **Accessibility**: shadcn/ui による標準準拠のアクセシブルコンポーネント