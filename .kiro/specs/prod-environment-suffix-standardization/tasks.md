# 実装計画: prod環境サフィックス標準化

## 概要

Healthmate App プロダクトの全サービスにおいて、「prod環境の場合はサフィックスを付けない」という条件分岐を削除し、全環境で一貫したサフィックス付与を実現する。デプロイとアンデプロイの両方を修正対象とする。

## タスク

- [x] 1. Healthmate-Core サービスの更新
- [x] 1.1 ConfigurationProviderクラスのprod判定削除
  - `healthmate_core/environment/configuration_provider.py`の`get_stack_name()`メソッドから`if self.environment == "prod"`条件分岐を削除
  - `get_environment_suffix()`メソッドから`if self.environment == "prod"`条件分岐を削除
  - _要件: 2.1, 2.2, 2.3_

- [x] 1.2 アンデプロイスクリプトの確認と修正
  - `destroy.sh`でConfigurationProviderを使用している場合は自動的に修正される
  - 直接的なprod判定がある場合は削除
  - _要件: 2.1, 2.2_

- [x] 2. Healthmate-HealthManager サービスの更新
- [x] 2.1 デプロイスクリプトのprod判定削除
  - `scripts/deploy-full-stack.sh`から`if [ "$HEALTHMATE_ENV" = "prod" ]`条件分岐を削除
  - スタック名とサフィックス生成を統一されたロジックに変更
  - _要件: 3.1, 3.2, 3.4_

- [x] 2.2 アンデプロイスクリプトのprod判定削除
  - `scripts/destroy-full-stack.sh`から`if [ "$HEALTHMATE_ENV" = "prod" ]`条件分岐を削除
  - `scripts/delete-credential-provider.sh`のprod判定も確認・修正
  - _要件: 3.1, 3.2_

- [x] 3. Healthmate-CoachAI サービスの更新
- [x] 3.1 デプロイスクリプトのprod判定削除
  - `deploy_to_aws.sh`から`if [ "$HEALTHMATE_ENV" = "prod" ]`条件分岐を削除
  - ENV_SUFFIX生成を統一されたロジックに変更
  - AgentCore Runtime名でアンダースコア、その他でハイフンを使用する既存ロジックを維持
  - _要件: 4.1, 4.2, 4.3, 4.4_

- [x] 3.2 アンデプロイスクリプトのprod判定削除
  - `destroy_from_aws.sh`から`if [ "$HEALTHMATE_ENV" = "prod" ]`条件分岐を削除
  - `create_custom_iam_role.py`のprod判定も確認・修正
  - _要件: 4.1, 4.2_

- [x] 4. Healthmate-Frontend サービスの確認
- [x] 4.1 デプロイ・アンデプロイスクリプトの確認
  - `deploy.sh`と`destroy.sh`でprod判定がないことを確認
  - `cdk/app.py`は既に統一されているため変更不要
  - _要件: 5.1, 5.2_

- [x] 5. 統合テストと検証
- [x] 5.1 Healthmate-App統合デプロイテスト
  - `deploy_all.sh prod`でprod環境の一括デプロイを実行
  - 全サービスが`{base_name}-prod`パターンでデプロイされることを確認
  - _要件: 1.1, 1.4, 6.2_

- [x] 5.2 Healthmate-App統合アンデプロイテスト
  - `undeploy_all.sh prod`でprod環境の一括アンデプロイを実行
  - 全サービスが正常にアンデプロイされることを確認
  - _要件: 6.2_

- [x] 5.3 問題発生時の修正
  - 統合テストで問題が発見された場合、該当サービスの修正を実行
  - 修正後、再度統合テストを実行
  - _要件: 7.1, 7.2, 7.4, 7.5_

## 注記

- 各サービスの個別テストは実行せず、最終的にHealthmate-Appでの統合テストのみ実行
- 変更は既存のdev/stage環境で正常に動作しているロジックをprod環境でも使用するだけの単純な修正
- アンデプロイスクリプトも同様にprod判定を削除し、一貫した命名規則を適用