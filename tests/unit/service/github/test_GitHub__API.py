from unittest                                                                                           import TestCase
from osbot_utils.helpers.ast.Ast_Load                                                                   import Ast_Load
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path                          import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Git__Ref                                   import Safe_Str__Git__Ref
from osbot_utils.type_safe.primitives.safe_str.github.Safe_Str__GitHub__Repo_Name                       import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.safe_str.github.Safe_Str__GitHub__Repo_Owner                      import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id                                      import Safe_Id
from osbot_utils.utils.Files                                                                            import file_contents
from osbot_utils.utils.Functions                                                                        import python_file
from osbot_utils.utils.Misc                                                                             import list_set
from osbot_utils.utils.Zip                                                                              import zip_bytes__file_list
from mgraph_ai_service_github_digest.service.github.GitHub__API                                         import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo                        import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter                import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref                   import Schema__GitHub__Repo__Ref

from osbot_utils.utils.Dev  import pprint

# todo: we need to add support for caching the requests (at least per hour) so that we don't hit GitHub request limitations
class test_GitHub__API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_api      = GitHub__API()
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

    def test_apis_repository(self):
        owner = Safe_Id('owasp-sbot')
        repo  = Safe_Id('OSBot-Utils')
        with self.github_api as _:
            apis_available = self.github_api.repository(github_repo=self.github_repo).get('content')
            assert list_set(apis_available) == ['allow_forking', 'archive_url', 'archived', 'assignees_url', 'blobs_url', 'branches_url',
                                                'clone_url', 'collaborators_url', 'comments_url', 'commits_url', 'compare_url', 'contents_url',
                                                'contributors_url', 'created_at', 'custom_properties', 'default_branch', 'deployments_url',
                                                'description', 'disabled', 'downloads_url', 'events_url', 'fork', 'forks', 'forks_count', 'forks_url',
                                                'full_name', 'git_commits_url', 'git_refs_url', 'git_tags_url', 'git_url', 'has_discussions',
                                                'has_downloads', 'has_issues', 'has_pages', 'has_projects', 'has_wiki', 'homepage', 'hooks_url',
                                                'html_url', 'id', 'is_template', 'issue_comment_url', 'issue_events_url', 'issues_url', 'keys_url',
                                                'labels_url', 'language', 'languages_url', 'license', 'merges_url', 'milestones_url', 'mirror_url',
                                                'name', 'network_count', 'node_id', 'notifications_url', 'open_issues', 'open_issues_count', 'organization',
                                                'owner', 'private', 'pulls_url', 'pushed_at', 'releases_url', 'size', 'ssh_url', 'stargazers_count',
                                                'stargazers_url', 'statuses_url', 'subscribers_count', 'subscribers_url', 'subscription_url', 'svn_url',
                                                'tags_url', 'teams_url', 'temp_clone_token', 'topics', 'trees_url', 'updated_at', 'url', 'visibility',
                                                'watchers', 'watchers_count', 'web_commit_signoff_required']

    def test_repository__contents__as_bytes(self):
        with self.github_api as _:
            repo_files_contents = self.github_api.repository__contents__as_bytes(github_repo_ref=self.github_repo_ref)
            assert len(repo_files_contents) > 100
            assert Safe_Str__File__Path('.gitignore')              in repo_files_contents
            assert Safe_Str__File__Path('osbot_utils/__init__.py') in repo_files_contents
            for file_name, file_contents in repo_files_contents.items():
                assert (type(file_contents) is bytes)

    def test_repository__contents__as_strings(self):
        with self.github_api as _:

            repo_filter = Schema__GitHub__Repo__Filter(**self. github_repo_ref.json()                                  ,
                                                       filter_starts_with = Safe_Str__File__Path('osbot_utils/helpers'),
                                                       filter_contains    = Safe_Str__File__Path('ast/'               ),
                                                       filter_ends_with   = Safe_Str__File__Path("d.py"               ))

            repo_files_contents = self.github_api.repository__contents__as_strings(repo_filter=repo_filter)
            assert len(repo_files_contents) == 8

            assert Safe_Str__File__Path('osbot_utils/helpers/ast/Ast_Load.py'         ) in repo_files_contents
            assert Safe_Str__File__Path('osbot_utils/helpers/ast/nodes/Ast_Keyword.py') in repo_files_contents
            assert Safe_Str__File__Path('osbot_utils/helpers/ast/nodes/Ast_Yield.py'  ) in repo_files_contents

            for _, repo_file_contents in repo_files_contents.items():
                assert (type(repo_file_contents) is str)

            assert file_contents(python_file(Ast_Load)) == repo_files_contents.get(Safe_Str__File__Path('osbot_utils/helpers/ast/Ast_Load.py'))


    def test_repository__files__names(self):
        with self.github_api as _:
            files_names = self.github_api.repository__files__names(self.github_repo_ref)
            assert len(files_names) > 700
            assert Safe_Str__File__Path('.gitignore'                                                          ) in files_names
            assert Safe_Str__File__Path('osbot_utils/decorators/methods/cache_on_self.py'                     ) in files_names
            assert Safe_Str__File__Path('osbot_utils/type_safe/primitives/safe_str/identifiers/Random_Guid.py') in files_names

    def test_repository__zip(self):
        with self.github_api as _:
            repository__zip = self.github_api.repository__zip(self.github_repo_ref)
            content         = repository__zip.get('content')
            assert list_set(repository__zip) == ['content', 'duration', 'headers']
            assert len(content) > 950000
            assert type(content) is bytes
            zip_files = zip_bytes__file_list(content)
            assert len(zip_files) > 900

    def test__bug__dict_error_in_dinis_cruz_docs_site(self):
        owner           = Safe_Str__GitHub__Repo_Owner ('DinisCruz'        )
        name            = Safe_Str__GitHub__Repo_Name  ('docs.diniscruz.ai')
        ref             = Safe_Str__Git__Ref           ('dev'              )
        github_repo_ref = Schema__GitHub__Repo__Ref(owner=owner, name=name, ref=ref)

        with GitHub__API() as _:
            repository  = _.repository              (github_repo_ref).get('content')
            files_names = _.repository__files__names(github_repo_ref)
            assert repository.get('git_url') == 'git://github.com/DinisCruz/docs.diniscruz.ai.git'

            assert 'setup.py'                       in files_names
            assert 'overrides/partials/footer.html' in files_names
            assert 'docs/research/projects.md'      in files_names


