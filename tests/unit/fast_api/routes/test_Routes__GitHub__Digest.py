from unittest                                                                            import TestCase
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter
from osbot_fast_api.api.routes.Fast_API__Routes                                          import Fast_API__Routes
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from starlette.responses                                                                 import PlainTextResponse
from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__Digest              import Routes__GitHub__Digest


class test_Routes__GitHub__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        with Routes__GitHub__Digest() as _:
            cls.routes_github__digest = _
            _.github_digest.github_api.cache_repo_zip = True

    def test_setUpClass(self):
        with self.routes_github__digest as _:
            assert type(_)         == Routes__GitHub__Digest
            assert base_classes(_) == [Fast_API__Routes, Type_Safe, object]

    def test_markdown(self):
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='')
            )
            markdown = response.body.decode('utf-8')

            assert type(response) == PlainTextResponse
            assert '# Files from Repo'           in markdown
            assert '### osbot_utils/__init__.py' in markdown

    def test_markdown__with_exclusions(self):                                 # Test exclusion parameters
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='' ,
                                              filter_exclude_paths=['test,__pycache__'])
            )
            markdown = response.body.decode('utf-8')

            assert type(response) == PlainTextResponse
            assert '## Exclusions:'  in markdown
            assert 'exclude_paths'   in markdown
            assert 'test'            in markdown

    def test_markdown__with_exclude_suffixes(self):                           # Test suffix exclusion
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='' ,
                                              filter_exclude_suffixes=['__init__.py,.pyc'])
            )
            markdown = response.body.decode('utf-8')

            assert 'exclude_suffixes' in markdown
            assert '__init__.py'      in markdown.split('## Files:')[0]                     # In header

    def test_markdown__with_exclude_prefixes(self):                           # Test prefix exclusion
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='' ,
                                              filter_exclude_prefixes=['osbot_utils/testing'] ,
                                              filter_starts_with='osbot_utils')
            )
            markdown = response.body.decode('utf-8')

            assert 'exclude_prefixes' in markdown

    def test_markdown__with_size_controls(self):                              # Test size control parameters
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains=''   ,
                                              max_file_size_bytes=5000 ,
                                              max_content_length=500)
            )
            markdown = response.body.decode('utf-8')

            assert '## Size Controls:' in markdown
            assert 'max_file_size'     in markdown
            assert '5,000'             in markdown
            assert 'max_content'       in markdown
            assert '500'               in markdown

    def test_markdown__with_truncate_patterns(self):                          # Test selective truncation
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains=''  ,
                                              max_content_length=100 ,
                                              truncate_patterns=['test_','_test'])
            )
            markdown = response.body.decode('utf-8')

            assert 'applies to:' in markdown
            assert 'test_'       in markdown.split('## Files:')[0]

    def test_markdown__with_starts_with_any(self):                            # Test multiple include paths
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='' ,
                                              filter_starts_with_any=['osbot_utils/helpers/flows','osbot_utils/helpers/duration'] ,
                                              filter_ends_with='.py')
            )
            markdown = response.body.decode('utf-8')

            assert 'starts_with_any:' in markdown
            assert 'osbot_utils/helpers/flows'    in markdown
            assert 'osbot_utils/helpers/duration' in markdown

    def test_markdown__combined_parameters(self):                             # Test all parameters together
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(
                    filter_contains=''                   ,
                    owner                  = 'owasp-sbot'       ,
                    name                   = 'OSBot-Utils'      ,
                    ref                    = 'dev'              ,
                    filter_starts_with     = 'osbot_utils/helpers' ,
                    filter_ends_with       = '.py'              ,
                    filter_starts_with_any = ['']               ,  # Empty = not used
                    filter_exclude_paths   = ['test']           ,
                    filter_exclude_prefixes= ['']               ,
                    filter_exclude_suffixes= ['__init__.py']    ,
                    max_file_size_bytes    = 10000              ,
                    max_content_length     = 1000               ,
                    truncate_patterns      = ['']                   # Empty = truncate all
                )
            )
            markdown = response.body.decode('utf-8')

            assert type(response) == PlainTextResponse
            assert '# Files from Repo'  in markdown
            assert 'owasp-sbot'         in markdown
            assert 'OSBot-Utils'        in markdown
            assert '## Exclusions:'     in markdown
            assert '## Size Controls:'  in markdown

    def test_markdown__truncation_visible(self):                              # Verify truncation marker appears
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='' ,
                                              filter_starts_with='osbot_utils/helpers' ,
                                              filter_ends_with='.py'                  ,
                                              max_content_length=200)
            )
            markdown = response.body.decode('utf-8')

            assert '[TRUNCATED:'    in markdown
            assert 'bytes remaining' in markdown

    def test_markdown__comma_parsing(self):                                   # Verify comma-separated lists work
        with self.routes_github__digest as _:
            response = _.markdown__filter(
                Schema__GitHub__Repo__Filter(filter_contains='' ,
                                              filter_exclude_paths=['test, __pycache__, .git'] ,
                                              filter_exclude_suffixes=['.pyc','.log,.tmp'])
            )
            markdown = response.body.decode('utf-8')

            header = markdown.split('## Files:')[0]
            assert 'test'        in header
            assert '__pycache__' in header
            assert '.git'        in header
            assert '.pyc'        in header
            assert '.log'        in header
            assert '.tmp'        in header
