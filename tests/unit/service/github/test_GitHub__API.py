from unittest                                                                                           import TestCase
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                       import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name           import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner          import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                           import Safe_Str__Git__Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                                   import Type_Safe__Dict
from osbot_utils.utils.Misc                                                                             import list_set
from mgraph_ai_service_github_digest.service.github.GitHub__API                                         import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo                        import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter                import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref                   import Schema__GitHub__Repo__Ref

# todo: remove the cache_repo_zip=True once we have added the proper cache service support
class test_GitHub__API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_api      = GitHub__API(cache_repo_zip=True)                  # so that we don't make multiple requests to repo zip
        cls.owner           = Safe_Str__GitHub__Repo_Owner ('owasp-sbot' )
        cls.name            = Safe_Str__GitHub__Repo_Name  ('OSBot-Utils')
        cls.ref             = Safe_Str__Git__Ref           ('main'       )
        cls.github_repo     = Schema__GitHub__Repo     (owner=cls.owner, name=cls.name       )
        cls.github_repo_ref = Schema__GitHub__Repo__Ref(**cls.github_repo.json(), ref=cls.ref)

    def test_setUpClass(self):
        with self.github_api as _:
            assert type(_) == GitHub__API

        with self.github_repo as _:
            assert _.owner == self.owner
            assert _.name  == self.name

        with self.github_repo_ref as _:
            assert _.owner == self.owner
            assert _.name  == self.name
            assert _.ref   == self.ref

    def test_apis_available(self):
        with self.github_api as _:
            apis_available = self.github_api.apis_available().get('content')
            assert list_set(apis_available) == ['authorizations_url', 'code_search_url', 'commit_search_url',
                                                'current_user_authorizations_html_url', 'current_user_repositories_url',
                                                'current_user_url', 'emails_url', 'emojis_url', 'events_url', 'feeds_url',
                                                'followers_url', 'following_url', 'gists_url', 'hub_url', 'issue_search_url',
                                                'issues_url', 'keys_url', 'label_search_url', 'notifications_url',
                                                'organization_repositories_url', 'organization_teams_url', 'organization_url',
                                                'public_gists_url', 'rate_limit_url', 'repository_search_url', 'repository_url',
                                                'starred_gists_url', 'starred_url', 'topic_search_url', 'user_organizations_url',
                                                'user_repositories_url', 'user_search_url', 'user_url']


    def test_commits(self):
        with self.github_api as _:
            commits = self.github_api.commits(github_repo=self.github_repo).get('content')
            assert type(commits) is list                                                    # todo: this should be a strongly typed class
            for commit in commits:
                assert list_set(commit) == ['author', 'comments_url', 'commit', 'committer',
                                            'html_url', 'node_id', 'parents', 'sha', 'url']

    def test_issues(self):
        with self.github_api as _:
            issues = self.github_api.issues(github_repo=self.github_repo).get('content')
            assert type(issues) is list                                                    # todo: this should be a strongly typed class
            for issue in issues:
                assert list_set(issue) == sorted(['active_lock_reason', 'assignee', 'assignees', 'author_association',
                                           'body', 'closed_at', 'closed_by', 'comments', 'comments_url', 'created_at',
                                           'events_url', 'html_url', 'id', 'labels', 'labels_url', 'locked', 'milestone',
                                           'node_id', 'number', 'performed_via_github_app', 'reactions', 'repository_url',
                                           'state', 'state_reason', 'sub_issues_summary', 'timeline_url', 'title', 'type',
                                           'updated_at', 'url', 'user'] +
                                            ['issue_dependencies_summary'])

    def test_rate_limit(self):
        with self.github_api as _:
            rate_limit = self.github_api.rate_limit()
            content    = rate_limit.get('content')
            assert list_set(rate_limit) == ['content', 'duration', 'headers']
            assert list_set(content   ) == ['rate', 'resources']

    def test_repository(self):
        with self.github_api as _:
            repository = _.repository(github_repo=self.github_repo)
            assert list_set(repository) == ['content', 'duration', 'headers']

    def test_repository__zip(self):
        with self.github_api as _:
            repository_zip = _.repository__zip(self.github_repo_ref)
            assert list_set(repository_zip) == ['content', 'duration', 'headers']
            assert type(repository_zip.get('content')) is bytes

    def test_repository__files__names(self):
        with self.github_api as _:
            files_names = _.repository__files__names(self.github_repo_ref)
            assert type(files_names) is list
            assert len(files_names) > 0
            assert 'osbot_utils/__init__.py' in files_names

    def test_repository__contents__as_bytes(self):
        with self.github_api as _:
            contents = _.repository__contents__as_bytes(self.github_repo_ref)
            assert type(contents) is Type_Safe__Dict
            assert len(contents) > 0
            assert len(contents[Safe_Str__File__Path('osbot_utils/__init__.py')]) == 16
            assert type(contents['osbot_utils/__init__.py'])                      is bytes

    def test_repository__contents__as_strings(self):
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                              ,
                                                   name               = self.name                               ,
                                                   ref                = self.ref                                ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils'     ),
                                                   filter_ends_with   = Safe_Str__File__Path('.py'             ))
        with self.github_api as _:
            contents = _.repository__contents__as_strings(repo_filter=repo_filter)
            assert type(contents) is Type_Safe__Dict
            assert len(contents) > 0
            assert 'osbot_utils/type_safe/__init__.py' in contents
            assert type(contents['osbot_utils/type_safe/__init__.py']) is str

    # ==================== NEW FILTERING TESTS ====================

    def test_path_matches_filter__basic_includes(self):                                     # Test basic include filters (AND logic)
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_starts_with = Safe_Str__File__Path('osbot_utils'),
                                                       filter_ends_with   = Safe_Str__File__Path('.py'        ),
                                                       filter_contains    = Safe_Str__File__Path('helpers'    ))

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/Task.py'  ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/Flows.py' ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/Task.py'          ), repo_filter) is False   # Missing 'helpers'
            assert _.path_matches_filter(Safe_Str__File__Path('tests/helpers/Task.py'        ), repo_filter) is False   # Wrong prefix
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/Task.txt' ), repo_filter) is False   # Wrong suffix

    def test_path_matches_filter__exclude_paths(self):                                      # Test exclusion by path contains
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_starts_with   = Safe_Str__File__Path('osbot_utils'),
                                                       filter_contains      = ''                                 ,
                                                       filter_exclude_paths = ['test', '__pycache__'             ])

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/Task.py'     ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/test_Task.py'        ), repo_filter) is False  # Contains 'test'
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/__pycache__/Task.pyc'), repo_filter) is False  # Contains '__pycache__'
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/testing/Task.py'     ), repo_filter) is False  # Contains 'test'

    def test_path_matches_filter__exclude_prefixes(self):                                   # Test exclusion by prefix
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_exclude_prefixes = ['tests/', '.github/'],
                                                       filter_contains         = ''                    )

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/Task.py'    ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('tests/test_Task.py'     ), repo_filter) is False
            assert _.path_matches_filter(Safe_Str__File__Path('.github/workflows/ci.py'), repo_filter) is False

    def test_path_matches_filter__exclude_suffixes(self):                                   # Test exclusion by suffix
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_starts_with     = Safe_Str__File__Path('osbot_utils'),
                                                       filter_exclude_suffixes = ['.pyc', '.log', '.tmp'          ],
                                                       filter_contains         = ''                                )

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/Task.py'  ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/Task.pyc' ), repo_filter) is False
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/debug.log'), repo_filter) is False
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/temp.tmp' ), repo_filter) is False

    def test_path_matches_filter__exclusions_take_priority(self):                           # Verify exclusions override includes
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_starts_with   = Safe_Str__File__Path('osbot_utils'),
                                                       filter_ends_with     = Safe_Str__File__Path('.py'        ),
                                                       filter_exclude_paths = ['test'                           ])

            # File matches include filters but excluded by path
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/test_utils.py'), repo_filter) is False

    def test_path_matches_filter__starts_with_any_or_logic(self):                           # Test OR logic for multiple include paths
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_starts_with_any = ['osbot_utils/helpers'  ,
                                                                                 'osbot_utils/utils'   ,
                                                                                 'osbot_utils/testing'],
                                                       filter_contains         = ''                     )

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/Task.py' ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/utils/Files.py'  ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/testing/__.py'   ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/core/Base.py'    ), repo_filter) is False
            assert _.path_matches_filter(Safe_Str__File__Path('tests/unit/test_Task.py'     ), repo_filter) is False

    def test_path_matches_filter__combined_filters(self):                                   # Test complex filter combinations
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(filter_starts_with_any  = ['osbot_utils/helpers', 'osbot_utils/utils'],
                                                       filter_ends_with        = Safe_Str__File__Path('.py'                 ),
                                                       filter_contains         = ''                                          ,
                                                       filter_exclude_paths    = ['test'                                    ],
                                                       filter_exclude_suffixes = ['__init__.py'                             ])

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/Task.py'    ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/utils/Files.py'     ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/__init__.py'), repo_filter) is False  # Excluded suffix
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/helpers/test_x.py'  ), repo_filter) is False  # Contains 'test'
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/core/Base.py'       ), repo_filter) is False  # Wrong prefix

    def test_path_matches_filter__empty_filters(self):                                      # Test with no filters (should match all)
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter()

            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/type_safe/__init__.py'         ), repo_filter) is True
            assert _.path_matches_filter(Safe_Str__File__Path('osbot_utils/type_safe/Type_Safe.py' ), repo_filter) is True

    # ==================== TRUNCATION TESTS ====================

    def test_should_truncate_file__no_max_length(self):                                     # No truncation when max_content_length not set
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter()                                    # max_content_length defaults to None

            assert _.should_truncate_file(Safe_Str__File__Path('any/file.py'), repo_filter) is False

    def test_should_truncate_file__truncate_all(self):                                      # Truncate all files when no patterns specified
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(max_content_length = 500)

            assert _.should_truncate_file(Safe_Str__File__Path('any/file.py'  ), repo_filter) is True
            assert _.should_truncate_file(Safe_Str__File__Path('test/file.py' ), repo_filter) is True
            assert _.should_truncate_file(Safe_Str__File__Path('src/module.py'), repo_filter) is True

    def test_should_truncate_file__with_patterns(self):                                     # Truncate only files matching patterns
        with self.github_api as _:
            repo_filter = Schema__GitHub__Repo__Filter(max_content_length = 500              ,
                                                       truncate_patterns  = ['test_', '_test'])

            assert _.should_truncate_file(Safe_Str__File__Path('tests/test_utils.py'    ), repo_filter) is True
            assert _.should_truncate_file(Safe_Str__File__Path('tests/helpers_test.py'  ), repo_filter) is True
            assert _.should_truncate_file(Safe_Str__File__Path('src/module.py'          ), repo_filter) is False
            assert _.should_truncate_file(Safe_Str__File__Path('osbot_utils/testing.py' ), repo_filter) is False  # 'testing' != 'test_'

    def test_truncate_content__no_truncation_needed(self):                                  # Content shorter than max_length
        with self.github_api as _:
            content    = "Short content"
            max_length = 100
            result     = _.truncate_content(content=content, max_length=max_length, file_path='file.py')

            assert result == content                                                        # Unchanged

    def test_truncate_content__truncation_applied(self):                                    # Content longer than max_length
        with self.github_api as _:
            content    = "A" * 1000
            max_length = 100
            result     = _.truncate_content(content=content, max_length=max_length, file_path='file.py')

            assert result.startswith("A" * 100)
            assert "[TRUNCATED:" in result
            assert "900 bytes remaining" in result
            assert "file.py" in result

    def test_truncate_content__marker_format(self):                                         # Verify marker format
        with self.github_api as _:
            content    = "Hello World! " * 100                                              # 1300 chars
            max_length = 50
            result     = _.truncate_content(content=content, max_length=max_length, file_path='test/path.py')

            assert len(result) > max_length                                                 # Includes marker
            assert result[:50] == content[:50]
            assert "\n\n... [TRUNCATED:" in result
            assert "test/path.py" in result
            assert "bytes remaining" in result

    # ==================== SIZE FILTERING TESTS ====================

    def test_repository__contents__as_strings__max_file_size(self):                         # Test max_file_size_bytes filtering
        repo_filter = Schema__GitHub__Repo__Filter(owner               = self.owner                              ,
                                                   name                = self.name                               ,
                                                   ref                 = self.ref                                ,
                                                   filter_starts_with  = Safe_Str__File__Path('osbot_utils'     ),
                                                   filter_ends_with    = Safe_Str__File__Path('.py'             ),
                                                   max_file_size_bytes = 100                                     )  # Very small limit
        with self.github_api as _:
            contents = _.repository__contents__as_strings(repo_filter=repo_filter)
            # With 100 byte limit, most files should be excluded
            for file_path, content in contents.items():
                assert len(content) <= 100                                                  # All returned files are small

    def test_repository__contents__as_strings__content_truncation(self):                    # Test content truncation in real API call
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                              ,
                                                   name               = self.name                               ,
                                                   ref                = self.ref                                ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils'     ),
                                                   filter_ends_with   = Safe_Str__File__Path('.py'             ),
                                                   max_content_length = 200                                     )
        with self.github_api as _:
            contents = _.repository__contents__as_strings(repo_filter=repo_filter)
            assert len(contents) > 0

            truncated_count = 0
            for file_path, content in contents.items():
                if '[TRUNCATED:' in content:
                    truncated_count += 1
                    assert content[:200] == content.split('\n\n... [TRUNCATED:')[0][:200]   # Verify truncation point

            assert truncated_count > 0                                                      # At least some files truncated

    def test_repository__contents__as_strings__exclude_paths(self):                         # Test exclusion in real API call
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                              ,
                                                   name               = self.name                               ,
                                                   ref                = self.ref                                ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils'     ),
                                                   filter_exclude_paths = ['test', '__pycache__'               ])
        with self.github_api as _:
            contents = _.repository__contents__as_strings(repo_filter=repo_filter)

            for file_path in contents.keys():
                assert 'test' not in str(file_path).lower()
                assert '__pycache__' not in str(file_path)

    def test_repository__contents__as_strings__starts_with_any(self):                       # Test multiple include paths in real API call
        repo_filter = Schema__GitHub__Repo__Filter(owner                = self.owner                            ,
                                                   name                 = self.name                             ,
                                                   ref                  = self.ref                              ,
                                                   filter_contains      = ''                                    ,
                                                   filter_starts_with_any = ['osbot_utils/helpers/flows'        ,
                                                                             'osbot_utils/helpers/duration'     ],
                                                   filter_ends_with     = Safe_Str__File__Path('.py'            ))
        with self.github_api as _:
            contents = _.repository__contents__as_strings(repo_filter=repo_filter)
            assert len(contents) > 0

            for file_path in contents.keys():
                file_str = str(file_path)
                assert (file_str.startswith('osbot_utils/helpers/flows') or
                        file_str.startswith('osbot_utils/helpers/duration'))

    # ==================== HELPER METHOD TESTS ====================

    def test_fix_repo_file_name(self):
        with self.github_api as _:
            assert _.fix_repo_file_name('repo-name-abc123/src/file.py') == 'src/file.py'
            assert _.fix_repo_file_name('prefix/nested/path/file.py'  ) == 'nested/path/file.py'
            assert _.fix_repo_file_name('no-slash'                    ) is None                 # No slash
            assert _.fix_repo_file_name('folder/'                     ) is None                 # Ends with slash (directory)

    def test_fix_repo_files_names(self):
        with self.github_api as _:
            input_files = ['repo-abc/src/a.py', 'repo-abc/src/b.py', 'repo-abc/', 'no-slash']
            result = _.fix_repo_files_names(input_files)
            assert result == ['src/a.py', 'src/b.py']                                       # Sorted, invalid entries removed

    def test_path__repo(self):
        with self.github_api as _:
            path = _.path__repo(self.github_repo)
            assert path == '/repos/owasp-sbot/OSBot-Utils'

    def test_path__repo_ref(self):
        with self.github_api as _:
            path = _.path__repo_ref(self.github_repo_ref)
            assert path == '/repos/owasp-sbot/OSBot-Utils/zipball/main'