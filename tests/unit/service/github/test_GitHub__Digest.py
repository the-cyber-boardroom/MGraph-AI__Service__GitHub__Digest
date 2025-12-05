from unittest                                                                                   import TestCase
from mgraph_ai_service_github_digest.service.github.GitHub__API                                 import GitHub__API
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path               import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name   import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner  import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                   import Safe_Str__Git__Ref
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_github_digest.service.github.GitHub__Digest                              import GitHub__Digest
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter        import Schema__GitHub__Repo__Filter


class test_GitHub__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_api    = GitHub__API(cache_repo_zip = True)
        cls.github_digest = GitHub__Digest(github_api=cls.github_api)
        cls.owner         = Safe_Str__GitHub__Repo_Owner ('owasp-sbot' )
        cls.name          = Safe_Str__GitHub__Repo_Name  ('OSBot-Utils')
        cls.ref           = Safe_Str__Git__Ref           ('dev'        )

    def test_setUpClass(self):
        with self.github_digest as _:
            assert type(_)         is GitHub__Digest
            assert base_classes(_) == [Type_Safe, object]

    def test_repo_files__in_markdown(self):
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                              ,
                                                   name               = self.name                               ,
                                                   ref                = self.ref                                ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils/helpers'),
                                                   filter_contains    = Safe_Str__File__Path('d.py'             ),
                                                   filter_ends_with   = Safe_Str__File__Path()                  )
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)
            assert "### osbot_utils/helpers/Random_Seed.py" in result
            assert "# Files from Repo" in result

    def test_repo_files__in_markdown__with_exclusions(self):                                # Test markdown shows exclusion info
        repo_filter = Schema__GitHub__Repo__Filter(owner                = self.owner                            ,
                                                   name                 = self.name                             ,
                                                   ref                  = self.ref                              ,
                                                   filter_contains    = ''                                      ,
                                                   filter_starts_with   = Safe_Str__File__Path('osbot_utils'   ),
                                                   filter_ends_with     = Safe_Str__File__Path('.py'           ),
                                                   filter_exclude_paths = ['test', '__pycache__'               ])
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "# Files from Repo"         in result
            assert "## Exclusions:"            in result
            assert "exclude_paths"             in result
            assert "test"                      in result                                    # Shows excluded pattern
            assert "__pycache__"               in result                                    # Shows excluded pattern

            # Verify excluded files are not in output
            assert "test/" not in result.split("## Files:")[1]                              # No test files after Files section

    def test_repo_files__in_markdown__with_exclude_suffixes(self):                          # Test exclude_suffixes in output
        repo_filter = Schema__GitHub__Repo__Filter(owner                  = self.owner                          ,
                                                   name                   = self.name                           ,
                                                   ref                    = self.ref                            ,
                                                   filter_starts_with     = Safe_Str__File__Path('osbot_utils' ),
                                                   filter_exclude_suffixes = ['__init__.py', '.pyc'            ])
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "exclude_suffixes"  in result
            assert "__init__.py"       in result.split("## Files:")[0]                      # In header, not content

    def test_repo_files__in_markdown__with_size_controls(self):                             # Test size controls in output
        repo_filter = Schema__GitHub__Repo__Filter(owner               = self.owner                             ,
                                                   name                = self.name                              ,
                                                   ref                 = self.ref                               ,
                                                   filter_starts_with  = Safe_Str__File__Path('osbot_utils/helpers'),
                                                   filter_ends_with    = Safe_Str__File__Path('.py'            ),
                                                   max_file_size_bytes = 5000                                   ,
                                                   max_content_length  = 500                                    )
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "## Size Controls:" in result
            assert "max_file_size"     in result
            assert "5,000 bytes"       in result
            assert "max_content"       in result
            assert "500"               in result

    def test_repo_files__in_markdown__truncation_visible(self):                             # Verify truncated content shows marker
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                                 ,
                                                   name               = self.name                                  ,
                                                   ref                = self.ref                                   ,
                                                   filter_contains    = ''                                         ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils/helpers'),
                                                   filter_ends_with   = Safe_Str__File__Path('.py'                ),
                                                   max_content_length = 200                                        )
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "[TRUNCATED:" in result                                                  # Truncation marker visible
            assert "bytes remaining" in result

    def test_repo_files__in_markdown__truncate_patterns(self):                              # Test selective truncation with patterns
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                              ,
                                                   name               = self.name                               ,
                                                   ref                = self.ref                                ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils'     ),
                                                   filter_ends_with   = Safe_Str__File__Path('.py'             ),
                                                   max_content_length = 100                                     ,
                                                   truncate_patterns  = ['__init__'                            ])
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "applies to:" in result
            assert "__init__"    in result.split("## Files:")[0]                            # In size controls section

    def test_repo_files__in_markdown__starts_with_any(self):                                # Test OR logic for multiple paths
        repo_filter = Schema__GitHub__Repo__Filter(owner                = self.owner                            ,
                                                   name                 = self.name                             ,
                                                   ref                  = self.ref                              ,
                                                   filter_starts_with_any = ['osbot_utils/helpers/flows'       ,
                                                                             'osbot_utils/helpers/duration'    ],
                                                   filter_ends_with     = Safe_Str__File__Path('.py'           ))
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "starts_with_any:" in result
            assert "osbot_utils/helpers/flows" in result
            assert "osbot_utils/helpers/duration" in result

            # Verify only matching paths in Files section
            files_section = result.split("## Files:")[1]
            for line in files_section.split('\n'):
                if line.startswith('### '):
                    file_path = line.replace('### ', '').strip()
                    assert (file_path.startswith('osbot_utils/helpers/flows') or
                            file_path.startswith('osbot_utils/helpers/duration'))

    def test_repo_files__in_markdown__no_filters(self):                                     # Test output with minimal filters
        repo_filter = Schema__GitHub__Repo__Filter(owner              = self.owner                              ,
                                                   name               = self.name                               ,
                                                   ref                = self.ref                                ,
                                                   filter_starts_with = Safe_Str__File__Path('osbot_utils/__init__'),
                                                   filter_ends_with   = Safe_Str__File__Path('.py'             ))
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            assert "## Exclusions:"    in result
            assert "(none)"            in result                                            # No exclusions set
            assert "## Size Controls:" in result

    def test_repo_files__in_markdown__file_count(self):                                     # Verify file count in header matches content
        repo_filter = Schema__GitHub__Repo__Filter(owner                = self.owner                            ,
                                                   name                 = self.name                             ,
                                                   ref                  = self.ref                              ,
                                                   filter_starts_with_any = ['osbot_utils/helpers/flows'       ],
                                                   filter_ends_with     = Safe_Str__File__Path('.py'           ))
        with self.github_digest as _:
            result       = _.repo_files__in_markdown(repo_filter=repo_filter)
            files_section = result.split("## Files:")[1]
            file_headers  = [line for line in files_section.split('\n') if line.startswith('### ')]

            # Extract count from "Showing X files"
            for line in result.split('\n'):
                if 'Showing' in line and 'files' in line:
                    count_str = line.split('Showing')[1].split('files')[0].strip()
                    expected_count = int(count_str)
                    assert len(file_headers) == expected_count
                    break

    def test_repo_files__in_markdown__combined_filters(self):                               # Test complex filter combination
        repo_filter = Schema__GitHub__Repo__Filter(owner                  = self.owner                          ,
                                                   name                   = self.name                           ,
                                                   ref                    = self.ref                            ,
                                                   filter_starts_with_any  = ['osbot_utils/helpers'             ],
                                                   filter_ends_with       = Safe_Str__File__Path('.py'         ),
                                                   filter_exclude_paths   = ['test'                            ],
                                                   filter_exclude_suffixes = ['__init__.py'                    ],
                                                   max_file_size_bytes    = 10000                               ,
                                                   max_content_length     = 1000                                )
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=repo_filter)

            # Verify all sections present
            assert "# Files from Repo"  in result
            assert "## Filtered by:"    in result
            assert "## Exclusions:"     in result
            assert "## Size Controls:"  in result
            assert "## Files:"          in result

            # Verify filters shown
            assert "starts_with_any:"   in result
            assert "exclude_paths"      in result
            assert "exclude_suffixes"   in result
            assert "max_file_size"      in result
            assert "max_content"        in result