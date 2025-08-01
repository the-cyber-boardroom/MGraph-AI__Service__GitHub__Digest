from unittest                               import TestCase
from mgraph_ai_service_github_digest.config import SERVICE_NAME, LAMBDA_NAME__SERVICE__GITHUB_DIGEST


class test_config(TestCase):

    def test__config_vars(self):
        assert SERVICE_NAME                        == 'mgraph_ai_service_github_digest'
        assert LAMBDA_NAME__SERVICE__GITHUB_DIGEST == f'service__{SERVICE_NAME}'