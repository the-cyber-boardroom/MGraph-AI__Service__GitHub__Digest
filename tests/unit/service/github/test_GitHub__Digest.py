from unittest                                                                            import TestCase
from osbot_utils.helpers.Safe_Id                                                         import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                                   import Safe_Str__File__Path
from mgraph_ai_service_github_digest.service.github.GitHub__Digest                       import GitHub__Digest
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.git.Safe_Str__Git__Ref import Safe_Str__Git__Ref
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.github.Safe_Str__GitHub__Repo_Name import \
    Safe_Str__GitHub__Repo_Name
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.github.Safe_Str__GitHub__Repo_Owner import \
    Safe_Str__GitHub__Repo_Owner


class test_GitHub__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_digest = GitHub__Digest()
        cls.repo_filter    = Schema__GitHub__Repo__Filter(owner             = Safe_Str__GitHub__Repo_Owner ('owasp-sbot' ),
                                                          name               = Safe_Str__GitHub__Repo_Name  ('OSBot-Utils'),
                                                          ref                = Safe_Str__Git__Ref           ('dev'        ),
                                                          filter_starts_with = Safe_Str__File__Path('osbot_utils/helpers' ),
                                                          filter_contains    = Safe_Str__File__Path('d.py'                ),
                                                          filter_ends_with   = Safe_Str__File__Path())

    def test_repo_files__in_markdown(self):
        with self.github_digest as _:
            result = _.repo_files__in_markdown(repo_filter=self.repo_filter)
            assert "### osbot_utils/helpers/Guid.py" in result
            # # print()
            # print(result)