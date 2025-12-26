# Healthmate-App サービス - 統合管理

## Service Overview

Healthmate-App サービスは、Healthmate App プロダクトの統合デプロイメント管理を担当するメタリポジトリです。4つの独立したHealthmateサービスを効率的に管理し、一括デプロイメント機能を提供します。

### Primary Responsibilities

- **統合デプロイメント管理**: 4サービスの一括デプロイ・アンデプロイ
- **依存関係管理**: サービス間の正しいデプロイ順序の自動管理
- **前提条件チェック**: 環境セットアップの自動検証
- **統合テスト**: 全サービス連携の動作確認
- **運用管理**: ログ監視、エラーハンドリング、ロールバック支援

### Service Architecture

- **管理対象**: 4つの独立したHealthmateサービス
- **技術スタック**: Bash スクリプト + 統合テスト
- **デプロイツール**: AWS CLI + CDK + AgentCore CLI
- **ログ管理**: 構造化ログとサマリーレポート
- **エラーハンドリング**: 段階的フォールバックとリトライ機能

### Key Technologies

#### Core Tools
- **Bash**: デプロイメントスクリプトの実行環境
- **AWS CLI**: AWSリソースの管理とステータス確認
- **jq**: JSON処理とCloudFormation出力解析
- **Git**: バージョン管理とリポジトリ操作

#### Integration Tools
- **AWS CDK**: Infrastructure as Code（各サービス）
- **bedrock-agentcore-control**: CoachAIエージェント管理
- **npm**: Frontend依存関係管理
- **Python venv**: 仮想環境管理

### Management Patterns

#### Service Orchestration
```bash
# デプロイ順序の管理
DEPLOY_ORDER=(
    "Healthmate-Core"      # 認証基盤
    "Healthmate-HealthManager"  # データ基盤
    "Healthmate-CoachAI"   # AI エージェント
    "Healthmate-Frontend"  # フロントエンド
)

# アンデプロイは逆順
UNDEPLOY_ORDER=(
    "Healthmate-Frontend"
    "Healthmate-CoachAI"
    "Healthmate-HealthManager"
    "Healthmate-Core"
)
```

#### Prerequisites Validation
```bash
# 必須ソフトウェアチェック
check_required_software() {
    local required_tools=("aws" "python3" "node" "npm" "jq" "git")
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool が見つかりません"
            return 1
        fi
    done
}

# AWS認証チェック
check_aws_authentication() {
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS認証が無効です"
        return 1
    fi
}

# Python仮想環境チェック
check_python_environments() {
    local services=("Healthmate-Core" "Healthmate-HealthManager" "Healthmate-CoachAI")
    for service in "${services[@]}"; do
        if [[ ! -d "../$service/.venv" ]]; then
            log_warning "$service の仮想環境が見つかりません"
        fi
    done
}
```

#### Error Handling and Retry
```bash
# CoachAI用のリトライ機能
wait_for_service_ready() {
    local service_name="$1"
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if check_service_status "$service_name"; then
            log_success "$service_name の準備が完了しました"
            return 0
        fi
        
        log_info "待機中... ($attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    
    log_error "$service_name の準備がタイムアウトしました"
    return 1
}

# HealthManager Credential Provider用のリトライ
retry_with_backoff() {
    local max_retries=30
    local delay=1
    local attempt=1
    
    while [[ $attempt -le $max_retries ]]; do
        if "$@"; then
            return 0
        fi
        
        if [[ $? -eq 2 ]]; then  # ConflictException
            log_warning "ConflictException発生、リトライします ($attempt/$max_retries)"
            sleep $delay
            ((attempt++))
        else
            return 1
        fi
    done
    
    log_error "最大リトライ回数に達しました"
    return 1
}
```

### Directory Structure

```
Healthmate-App/
├── deploy_all.sh              # 一括デプロイスクリプト
├── undeploy_all.sh            # 一括アンデプロイスクリプト
├── check_prerequisites.sh     # 前提条件チェック
├── test_integration.sh        # 統合テスト
├── lib/                       # 共通ライブラリ
│   ├── common.sh             # 共通関数とログ機能
│   └── services.sh           # サービス固有の処理
├── logs/                     # 実行ログ
├── tests/                    # テストスクリプト
└── README.md                 # 詳細なドキュメント
```

### Command Patterns

#### Deploy All Services
```bash
使用方法: ./deploy_all.sh [environment] [options]

環境:
    dev     開発環境（デフォルト）
    stage   ステージング環境  
    prod    本番環境

オプション:
    --region REGION    AWSリージョンを指定
    --help, -h         ヘルプを表示

例:
    ./deploy_all.sh                              # dev環境
    ./deploy_all.sh prod --region ap-northeast-1 # prod環境
```

#### Undeploy All Services
```bash
使用方法: ./undeploy_all.sh [environment] [options]

# 逆順でアンデプロイ（依存関係を考慮）
# エラーが発生しても他のサービスのアンデプロイは継続
```

#### Prerequisites Check
```bash
./check_prerequisites.sh

チェック項目:
- 必須ソフトウェア（AWS CLI, Python, Node.js, npm, jq, Git）
- AWS認証設定
- ディレクトリ構造
- Python仮想環境
- Node.js依存関係
- デプロイスクリプトの実行権限
```

### Integration Points

#### Service Dependencies
```bash
# 各サービスとの統合ポイント
CORE_DEPLOY_SCRIPT="../Healthmate-Core/deploy.sh"
HEALTHMANAGER_DEPLOY_SCRIPT="../Healthmate-HealthManager/scripts/deploy.sh"
COACHAI_DEPLOY_SCRIPT="../Healthmate-CoachAI/deploy_to_aws.sh"
FRONTEND_DEPLOY_SCRIPT="../Healthmate-Frontend/deploy.sh"
```

#### Environment Configuration
```bash
# 環境変数の統一管理
export HEALTHMATE_ENV="${environment}"
export AWS_REGION="${region}"

# 各サービスに環境変数を渡す
deploy_service() {
    local service_name="$1"
    
    cd "../$service_name" || return 1
    
    # 環境変数を設定してデプロイ実行
    HEALTHMATE_ENV="$HEALTHMATE_ENV" \
    AWS_REGION="$AWS_REGION" \
    ./deploy.sh
}
```

### Logging and Monitoring

#### Structured Logging
```bash
# ログレベル管理
LOG_LEVELS=("INFO" "SUCCESS" "WARNING" "ERROR")

log_with_timestamp() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# 実行サマリー
generate_summary() {
    local total_time="$1"
    local successful_services=("$@")
    
    log_info "=== 実行サマリー ==="
    log_info "実行時間: $total_time"
    log_info "成功したサービス: ${successful_services[*]}"
    log_info "ログファイル: $LOG_FILE"
}
```

#### Performance Monitoring
```bash
# デプロイ時間の測定
measure_deployment_time() {
    local service_name="$1"
    local start_time=$(date +%s)
    
    deploy_service "$service_name"
    local exit_code=$?
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log_info "$service_name のデプロイ時間: ${duration}秒"
    return $exit_code
}
```

### Development Commands

#### 環境セットアップ
```bash
# リポジトリクローン
mkdir healthmate-workspace && cd healthmate-workspace
git clone https://github.com/tomofuminijo/Healthmate-Core.git
git clone https://github.com/tomofuminijo/Healthmate-HealthManager.git
git clone https://github.com/tomofuminijo/Healthmate-CoachAI.git
git clone https://github.com/tomofuminijo/Healthmate-Frontend.git
git clone https://github.com/tomofuminijo/Healthmate-App.git

# 前提条件チェック
cd Healthmate-App
./check_prerequisites.sh
```

#### デプロイメント
```bash
# 開発環境デプロイ
./deploy_all.sh dev

# 本番環境デプロイ
./deploy_all.sh prod --region ap-northeast-1

# アンデプロイ
./undeploy_all.sh dev
```

#### テスト
```bash
# 統合テスト
./test_integration.sh

# 個別サービステスト
cd ../Healthmate-Core && ./test.sh
cd ../Healthmate-HealthManager && python test_mcp_client.py
cd ../Healthmate-CoachAI && python manual_test_deployed_agent.py
```

### Service-Specific Best Practices

- **Dependency Management**: 正しいデプロイ順序の厳守
- **Error Recovery**: 段階的フォールバックとリトライ機能
- **Environment Isolation**: 環境ごとの設定分離
- **Logging**: 構造化ログと詳細なエラー情報
- **Validation**: デプロイ前の前提条件チェック
- **Monitoring**: リアルタイムステータス監視
- **Documentation**: 包括的なREADMEとトラブルシューティング
- **Security**: 認証情報の安全な管理
- **Performance**: デプロイ時間の最適化
- **Rollback**: 問題発生時の迅速なロールバック支援

### Troubleshooting Patterns

#### Common Issues
1. **AWS認証エラー**: `aws configure` または `aws sso login`
2. **Python仮想環境エラー**: 各サービスで `.venv` の作成と依存関係インストール
3. **Node.js依存関係エラー**: Frontend で `npm install`
4. **CoachAI デプロイタイムアウト**: IAMロール作成の確認
5. **HealthManager Credential Provider競合**: 自動リトライ機能で解決

#### Debug Commands
```bash
# ログ確認
cat logs/healthmate-app-*.log

# AWS リソース確認
aws cloudformation list-stacks
aws bedrock-agentcore-control list-agent-runtimes

# 個別サービステスト
cd ../Healthmate-Core && ./deploy.sh
```