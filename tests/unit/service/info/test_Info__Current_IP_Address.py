from unittest                                                               import TestCase
from osbot_utils.utils.Misc                                                 import list_set
from mgraph_ai_service_github_digest.service.info.Info__Current_IP_Address  import Info__Current_IP_Address
from osbot_utils.utils.Dev import pprint

class test_Info__Current_IP_Address(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.info__current_ip_address = Info__Current_IP_Address()

    def test___init__(self):
        with self.info__current_ip_address as _:
            assert type(_) == Info__Current_IP_Address

    def test_from__checkip__amazon_aws(self):
        with self.info__current_ip_address as _:
            result = _.from__checkip__amazon_aws()
            assert list_set(result)  == ['duration', 'headers', 'text']
            assert list_set(result.get('headers')) == ['Connection', 'Content-Length', 'Content-Type', 'Date', 'Server', 'Vary']

    def test_from__ip_ify(self):
        with self.info__current_ip_address as _:
            result = _.from__ip_ify()
            assert list_set(result.get('headers')) == ['CF-RAY', 'Connection', 'Content-Length', 'Content-Type',
                                                       'Date', 'Server', 'Vary', 'cf-cache-status', 'server-timing']