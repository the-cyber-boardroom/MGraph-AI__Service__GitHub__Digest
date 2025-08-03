from unittest                                                   import TestCase

from osbot_utils.helpers.Safe_Id import Safe_Id
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_contents
from osbot_utils.utils.Functions import python_file
from osbot_utils.utils.Misc import list_set, bytes_to_str
from osbot_utils.utils.Zip import zip_bytes__file_list

from mgraph_ai_service_github_digest.service.github.GitHub__API import GitHub__API


# todo: we need to add support for caching the requests (at least per hour) so that we don't hit GitHub request limitations
class test_GitHub__API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_api = GitHub__API()
        cls.owner      = Safe_Id('owasp-sbot' )         # todo: add a class that represents the 'repo' and holds these values
        cls.repo       = Safe_Id('OSBot-Utils')

    def test_setUpClass(self):
        with self.github_api as _:
            assert type(_) == GitHub__API

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
            apis_available = self.github_api.repository(owner=owner, repo=repo).get('content')
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
            repo_files_contents = self.github_api.repository__contents__as_bytes(owner=self.owner, repo=self.repo)
            assert len(repo_files_contents) > 100
            assert '.gitignore'              in repo_files_contents
            assert 'osbot_utils/__init__.py' in repo_files_contents
            for file_name, file_contents in repo_files_contents.items():
                assert (type(file_contents) is bytes)

    def test_repository__contents__as_strings(self):
        with self.github_api as _:
            repo_files_contents = self.github_api.repository__contents__as_strings(owner=self.owner, repo=self.repo)
            assert len(repo_files_contents) > 100
            assert '.gitignore'              in repo_files_contents
            assert 'osbot_utils/__init__.py' in repo_files_contents
            for _, repo_file_contents in repo_files_contents.items():
                assert (type(repo_file_contents) is str)

            assert file_contents(python_file(Safe_Id)) == repo_files_contents.get('osbot_utils/helpers/Safe_Id.py')


    def test_repository__files__names(self):
        with self.github_api as _:
            files_names = self.github_api.repository__files__names(owner=self.owner, repo=self.repo)
            assert len(files_names) > 700
            assert  '.gitignore'                                     in files_names
            assert 'osbot_utils/decorators/methods/cache_on_self.py' in files_names
            assert 'osbot_utils/helpers/Random_Guid.py'              in files_names

    def test_repository__zip(self):
        with self.github_api as _:
            repository__zip = self.github_api.repository__zip(owner=self.owner, repo=self.repo)
            content         = repository__zip.get('content')
            assert list_set(repository__zip) == ['content', 'duration', 'headers']
            assert len(content) > 950000
            assert type(content) is bytes
            zip_files = zip_bytes__file_list(content)
            assert len(zip_files) > 900
