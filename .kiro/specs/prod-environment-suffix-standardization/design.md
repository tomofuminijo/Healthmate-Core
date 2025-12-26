# 設計文書

## 概要

Healthmate App プロダクトの全サービスにおいて、現在実装されている「prod環境の場合はサフィックスを付けない」という条件分岐を削除する。dev/stageで正常に動作している既存のサフィックス付与ロジックをprod環境でも使用するだけの単純な変更。

## アーキテクチャ

### 現在の実装パターン

各サービスで以下のようなprod判定ロジックが実装されている：

```python
# Healthmate-Core/healthmate_core/environment/configuration_provider.py
def get_stack_name(self, base_stack_name: str) -> str:
    if self.environment == "prod":
        return base_stack_name  # ← この条件分岐を削除
    return f"{base_stack_name}-{self.environment}"

def get_environment_suffix(self) -> str:
    if self.environment == "prod":
        return ""  # ← この条件分岐を削除
    return f"-{self.environment}"
```

```bash
# Healthmate-HealthManager/scripts/deploy-full-stack.sh
if [ "$HEALTHMATE_ENV" = "prod" ]; then
    STACK_NAME="Healthmate-HealthManagerStack"  # ← この条件分岐を削除
    ENV_SUFFIX=""
else
    STACK_NAME="Healthmate-HealthManagerStack-${HEALTHMATE_ENV}"
    ENV_SUFFIX="-${HEALTHMATE_ENV}"
fi
```

```bash
# Healthmate-CoachAI/deploy_to_aws.sh
if [ "$HEALTHMATE_ENV" = "prod" ]; then
    ENV_SUFFIX=""  # ← この条件分岐を削除
else
    ENV_SUFFIX="-${HEALTHMATE_ENV}"
fi
```

### 変更後の実装パターン

prod判定を削除し、全環境で統一されたロジックを使用：

```python
# 修正後のPythonコード
def get_stack_name(self, base_stack_name: str) -> str:
    return f"{base_stack_name}-{self.environment}"

def get_environment_suffix(self) -> str:
    return f"-{self.environment}"
```

```bash
# 修正後のBashスクリプト
STACK_NAME="Healthmate-HealthManagerStack-${HEALTHMATE_ENV}"
ENV_SUFFIX="-${HEALTHMATE_ENV}"
```

## コンポーネントと インターフェース

### 変更対象ファイル

1. **Healthmate-Core**:
   - `healthmate_core/environment/configuration_provider.py`: `get_stack_name()`, `get_environment_suffix()`メソッドのprod判定削除

2. **Healthmate-HealthManager**:
   - `scripts/deploy-full-stack.sh`: スタック名とサフィックス生成のprod判定削除

3. **Healthmate-CoachAI**:
   - `deploy_to_aws.sh`: ENV_SUFFIX生成のprod判定削除

4. **Healthmate-Frontend**:
   - `cdk/app.py`: スタック名生成で既に統一されているため変更不要

5. **Healthmate-App**:
   - 統合デプロイスクリプトは各サービスの変更に追従するため変更不要

## データモデル

変更なし。既存のdev/stage環境で正常に動作しているロジックをそのまま使用。

## 正確性プロパティ

*プロパティとは、システムの全ての有効な実行において真であるべき特性や動作のことです。プロパティは、人間が読める仕様と機械で検証可能な正確性保証の橋渡しをします。*

### プロパティ1: 環境サフィックス一貫性

*すべての* 環境（dev、stage、prod）とベースリソース名の組み合わせにおいて、リソース名は `{base_name}-{environment}` のパターンに従う
**検証: 要件1.1, 1.2, 1.3, 1.4**

### プロパティ2: prod判定ロジック不存在

*すべての* デプロイスクリプトにおいて、prod環境を特別扱いする条件分岐（`if environment == "prod"`）が存在しない
**検証: 要件1.5**

### プロパティ3: AgentCore Runtime命名例外

*すべての* AgentCore Runtimeリソースにおいて、ハイフンの代わりにアンダースコアを使用し、`{base_name}_{environment}` のパターンに従う
**検証: 要件4.3**

## エラーハンドリング

変更なし。既存のdev/stage環境で正常に動作しているエラーハンドリングをそのまま使用。

## テスト戦略

### 単体テスト

既存のテストを更新してprod環境でもサフィックスが付与されることを確認：

```python
# Healthmate-Core/tests/unit/test_configuration_provider.py
def test_get_stack_name_prod_environment():
    """prod環境でもサフィックスが付与されることを確認"""
    config = ConfigurationProvider("healthmate-core")
    config.environment = "prod"
    
    result = config.get_stack_name("Healthmate-CoreStack")
    assert result == "Healthmate-CoreStack-prod"
```

### 統合テスト

既存の統合テストでprod環境のリソース名を確認：

```bash
# 統合テストでprod環境のリソース名確認
test_prod_resource_naming() {
    local environment="prod"
    local expected_stack="Healthmate-CoreStack-prod"
    
    # スタックが正しい名前で作成されていることを確認
    aws cloudformation describe-stacks --stack-name "$expected_stack"
    assert_equals $? 0
}
```

## 実装計画

### フェーズ1: Healthmate-Core サービス

1. `configuration_provider.py`のprod判定削除（2箇所の`if self.environment == "prod"`を削除）
2. 既存の単体テストを更新

### フェーズ2: Healthmate-HealthManager サービス

1. `deploy-full-stack.sh`のprod判定削除（1箇所の`if [ "$HEALTHMATE_ENV" = "prod" ]`を削除）

### フェーズ3: Healthmate-CoachAI サービス

1. `deploy_to_aws.sh`のprod判定削除（1箇所の`if [ "$HEALTHMATE_ENV" = "prod" ]`を削除）

### フェーズ4: 統合テストと検証

1. 全サービスでprod環境のデプロイテスト実行
2. リソース名の一貫性確認