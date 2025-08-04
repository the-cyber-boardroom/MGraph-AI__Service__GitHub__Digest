from unittest                                                            import TestCase

from osbot_utils.utils.Dev import pprint

from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__API import Routes__GitHub__API


class test_Routes__GitHub__API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_github_api = Routes__GitHub__API()

    def test_repository_files_names(self):
        with self.routes_github_api as _:
            assert 'osbot_utils/helpers/flows/Task.py' in _.repository_files_names()