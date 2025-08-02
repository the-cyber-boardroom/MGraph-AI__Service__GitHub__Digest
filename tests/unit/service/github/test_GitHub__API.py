from unittest                                                   import TestCase
from osbot_utils.utils.Misc                                     import list_set
from mgraph_ai_service_github_digest.service.github.GitHub__API import GitHub__API


class test_GitHub__API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_api = GitHub__API()

    def test_setUpClass(self):
        with self.github_api as _:
            assert type(_) == GitHub__API

    def test_rate_limit(self):
        with self.github_api as _:
            rate_limit = self.github_api.rate_limit()
            assert list_set(rate_limit) == ['rate', 'resources']