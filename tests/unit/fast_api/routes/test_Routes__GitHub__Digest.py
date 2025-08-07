from unittest                                                               import TestCase
from osbot_fast_api.api.Fast_API_Routes                                     import Fast_API_Routes
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.utils.Objects                                              import base_classes
from starlette.responses                                                    import PlainTextResponse
from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__Digest import Routes__GitHub__Digest

class test_Routes__GitHub__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_github__digest = Routes__GitHub__Digest()

    def test_setUpClass(self):
        with self.routes_github__digest as _:
            assert type(_)         == Routes__GitHub__Digest
            assert base_classes(_) == [Fast_API_Routes, Type_Safe, object]

    def test_repo_files_in_markdown(self):
        with self.routes_github__digest as _:
            response = _.repo_files_in_markdown()
            markdown = response.body.decode('utf-8')
            assert type(response) == PlainTextResponse
            assert '# Files from Repo'           in markdown
            assert '### osbot_utils/__init__.py' in markdown