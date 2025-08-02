from datetime                            import datetime
from unittest                            import TestCase
from osbot_utils.testing.Stderr          import Stderr
from osbot_utils.testing.Temp_Web_Server import Temp_Web_Server
from osbot_utils.utils.Misc              import list_set

from mgraph_ai_service_github_digest.service.shared.Http__Requests import Http__Requests


class test_Http__Requests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_web_server = Temp_Web_Server()
        cls.base_url        = cls.temp_web_server.url()
        cls.http_requests   = Http__Requests(base_url=cls.base_url)
        cls.temp_web_server.start()

    @classmethod
    def tearDownClass(cls):
        cls.temp_web_server.stop()

    def test_get(self):
        with Stderr() as stderr:
            with self.http_requests as _:
                response = _.get()
                headers  = response.get('headers')
                content  = response.get('content')
                assert list_set(response)        == ['content', 'duration', 'headers']
                assert list_set(headers )        == ['Content-Length', 'Content-type', 'Date', 'Server']
                assert "Directory listing for /" in content

        now__formatted = datetime.now().strftime('%d/%b/%Y %H:%M:%S')                           # Format the date

        assert stderr.value() == f'127.0.0.1 - - [{now__formatted}] "GET / HTTP/1.1" 200 -\n'   # confirm webserver output logs