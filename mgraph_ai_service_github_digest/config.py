from mgraph_ai_service_github_digest import package_name
import os

SERVICE_NAME                             = package_name
FAST_API__TITLE                          = "Github Digest - Service"
LAMBDA_NAME__SERVICE__GITHUB_DIGEST      = f'service__{SERVICE_NAME}'
LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS = ['osbot-fast-api-serverless==v1.31.0']

# Cache Service Configuration
CACHE_SERVICE_URL         = os.getenv('CACHE_SERVICE_URL'  , 'https://cache.dev.mgraph.ai')    # Cache service endpoint
CACHE_NAMESPACE           = os.getenv('CACHE_NAMESPACE'    , 'github-digest'             )    # Cache namespace
CACHE_STRATEGY            = os.getenv('CACHE_STRATEGY'     , 'temporal_latest'           )    # Storage strategy
CACHE_ENABLED             = os.getenv('CACHE_ENABLED'      , 'true').lower() == 'true'        # Enable/disable caching
CACHE_TTL_HOURS           = int(os.getenv('CACHE_TTL_HOURS', '24'))                         # Cache TTL in hours


GIT_HUB__API__DEFAULT__REPO_OWNER         = 'owasp-sbot'
GIT_HUB__API__DEFAULT__REPO_NAME          = 'OSBot-Utils'
GIT_HUB__API__DEFAULT__REF                = 'main'
GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH = 'osbot_utils'
GIT_HUB__API__DEFAULT__FILTER_CONTAINS    = 'type_safe'
GIT_HUB__API__DEFAULT__FILTER_ENDS_WITH   = '.py'