import pytest
from unittest                                                                   import TestCase
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                                                      import load_dotenv
from osbot_utils.utils.Objects                                                  import obj
from mgraph_ai_service_github_digest.service.threat_intelligence.IP_Data        import IP_Data, ENV_VAR__IP_DATA__API_KEY
from mgraph_ai_service_github_digest.utils.for_osbot_utils.Safe_Str__IP_Address import Safe_Str__IP_Address


class test_IP_Data(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        with IP_Data() as _:
            cls.ip_data = _
            if not _.api_key():
                pytest.skip(f'Test needs {ENV_VAR__IP_DATA__API_KEY} API Key set')


    def test_api_key(self):
        assert self.ip_data.api_key() is not None

    def test_request_get(self):
        with self.ip_data as _:
            ip_address = Safe_Str__IP_Address('8.8.8.8')
            result     = _.ip_address__details(ip_address)
            with obj(result) as _:
                assert _.content.ip == ip_address