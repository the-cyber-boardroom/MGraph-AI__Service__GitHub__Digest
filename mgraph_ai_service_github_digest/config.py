from mgraph_ai_service_github_digest import package_name

SERVICE_NAME                             = package_name
FAST_API__TITLE                          = "Github Digest - Service"
LAMBDA_NAME__SERVICE__GITHUB_DIGEST      = f'service__{SERVICE_NAME}'
LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS = ['osbot-fast-api-serverless==v1.2.0']
