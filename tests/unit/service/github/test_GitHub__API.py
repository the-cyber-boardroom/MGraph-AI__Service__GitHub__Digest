from unittest                                                                                           import TestCase
from osbot_utils.helpers.ast.Ast_Load                                                                   import Ast_Load
from osbot_utils.testing.__ import __, __SKIP__
from osbot_utils.testing.__helpers import obj
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                       import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name           import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner          import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                           import Safe_Str__Git__Ref
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                                       import Safe_Id
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
            assert Safe_Str__File__Path('.gitignore'                                                         ) in files_names
            assert Safe_Str__File__Path('osbot_utils/decorators/methods/cache_on_self.py'                    ) in files_names
            #assert Safe_Str__File__Path('osbot_utils/type_safe/primitives/domains/identifiers/Random_Guid.py') in files_names  # todo: figure out why this is failing (since the file is there)

    def test_repository__zip(self):
        with self.github_api as _:
            repository__zip = self.github_api.repository__zip(self.github_repo_ref)
            content         = repository__zip.get('content')
            assert list_set(repository__zip) == ['content', 'duration', 'headers']
            assert len(content) > 950000
            assert type(content) is bytes
            zip_files = zip_bytes__file_list(content)
            assert len(zip_files) > 900

    # todo: review this test since it looks like that bug has been fixed
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



    def test__regression__repository__dict_error_in_repo__mgraph_semantic_text(self):
        owner           = Safe_Str__GitHub__Repo_Owner ('the-cyber-boardroom'              )
        name            = Safe_Str__GitHub__Repo_Name  ('MGraph-AI__Service__Semantic_Text')
        ref             = Safe_Str__Git__Ref           ('dev'              )
        github_repo_ref = Schema__GitHub__Repo__Ref(owner=owner, name=name, ref=ref)

        with GitHub__API() as _:
            repository  = _.repository(github_repo_ref).get('content')
            path_repo   = _.path__repo(github_repo_ref)
            #assert repository == { 'documentation_url': 'https://docs.github.com/rest/repos/repos#get-a-repository',
            #                       'message'          : 'Not Found'                                                ,
            #                       'status'           : '404'                                                      }
            #assert path_repo == '/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text'
            #files_names = _.repository__files__names(github_repo_ref)
            #assert repository.get('git_url') == 'git://github.com/DinisCruz/docs.diniscruz.ai.git'
            assert obj(repository) == __(   id                  = __SKIP__                                        ,
                                            node_id             = __SKIP__                                 ,
                                            name                = 'MGraph-AI__Service__Semantic_Text'             ,
                                            full_name           = 'the-cyber-boardroom/MGraph-AI__Service__Semantic_Text',
                                            private             = False                                           ,
                                            owner               = __(   login               = 'the-cyber-boardroom'                           ,
                                                                        id                  = __SKIP__                                        ,
                                                                        node_id             = __SKIP__                                  ,
                                                                        avatar_url          = __SKIP__,
                                                                        gravatar_id         = ''                                               ,
                                                                        url                 = 'https://api.github.com/users/the-cyber-boardroom',
                                                                        html_url            = 'https://github.com/the-cyber-boardroom'         ,
                                                                        followers_url       = 'https://api.github.com/users/the-cyber-boardroom/followers',
                                                                        following_url       = 'https://api.github.com/users/the-cyber-boardroom/following{/other_user}',
                                                                        gists_url           = 'https://api.github.com/users/the-cyber-boardroom/gists{/gist_id}',
                                                                        starred_url         = 'https://api.github.com/users/the-cyber-boardroom/starred{/owner}{/repo}',
                                                                        subscriptions_url   = 'https://api.github.com/users/the-cyber-boardroom/subscriptions',
                                                                        organizations_url   = 'https://api.github.com/users/the-cyber-boardroom/orgs',
                                                                        repos_url           = 'https://api.github.com/users/the-cyber-boardroom/repos',
                                                                        events_url          = 'https://api.github.com/users/the-cyber-boardroom/events{/privacy}',
                                                                        received_events_url = 'https://api.github.com/users/the-cyber-boardroom/received_events',
                                                                        type                = 'Organization'                                   ,
                                                                        user_view_type      = 'public'                                         ,
                                                                        site_admin          = False
                                                                    )                                     ,

                                            html_url            = 'https://github.com/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text'   ,
                                            description         = __SKIP__                                 ,
                                            fork                = False                                  ,
                                            url                 = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text',
                                            forks_url           = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/forks',
                                            keys_url            = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/keys{/key_id}',
                                            collaborators_url   = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/collaborators{/collaborator}',
                                            teams_url           = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/teams',
                                            hooks_url           = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/hooks',
                                            issue_events_url    = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/issues/events{/number}',
                                            events_url          = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/events',
                                            assignees_url       = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/assignees{/user}',
                                            branches_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/branches{/branch}',
                                            tags_url            = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/tags',
                                            blobs_url           = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/git/blobs{/sha}',
                                            git_tags_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/git/tags{/sha}',
                                            git_refs_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/git/refs{/sha}',
                                            trees_url           = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/git/trees{/sha}',
                                            statuses_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/statuses/{sha}',
                                            languages_url       = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/languages',
                                            stargazers_url      = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/stargazers',
                                            contributors_url    = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/contributors',
                                            subscribers_url     = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/subscribers',
                                            subscription_url    = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/subscription',
                                            commits_url         = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/commits{/sha}',
                                            git_commits_url     = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/git/commits{/sha}',
                                            comments_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/comments{/number}',
                                            issue_comment_url   = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/issues/comments{/number}',
                                            contents_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/contents/{+path}',
                                            compare_url         = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/compare/{base}...{head}',
                                            merges_url          = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/merges',
                                            archive_url         = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/{archive_format}{/ref}',
                                            downloads_url       = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/downloads',
                                            issues_url          = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/issues{/number}',
                                            pulls_url           = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/pulls{/number}',
                                            milestones_url      = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/milestones{/number}',
                                            notifications_url   = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/notifications{?since,all,participating}',
                                            labels_url          = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/labels{/name}',
                                            releases_url        = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/releases{/id}',
                                            deployments_url     = 'https://api.github.com/repos/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text/deployments',

                                            created_at          = __SKIP__        ,
                                            updated_at          = __SKIP__        ,
                                            pushed_at           = __SKIP__        ,

                                            git_url             = 'git://github.com/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text.git' ,
                                            ssh_url             = 'git@github.com:the-cyber-boardroom/MGraph-AI__Service__Semantic_Text.git'  ,
                                            clone_url           = 'https://github.com/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text.git',
                                            svn_url             = 'https://github.com/the-cyber-boardroom/MGraph-AI__Service__Semantic_Text'   ,
                                            homepage            = None                 ,
                                            size                = __SKIP__             ,
                                            stargazers_count    = __SKIP__                    ,
                                            watchers_count      = __SKIP__                    ,
                                            language            = 'Python'             ,
                                            has_issues          = True                 ,
                                            has_projects        = True                 ,
                                            has_downloads       = True                 ,
                                            has_wiki            = False                ,
                                            has_pages           = False                ,
                                            has_discussions     = False                ,
                                            forks_count         = __SKIP__                    ,
                                            mirror_url          = None                 ,
                                            archived            = False                ,
                                            disabled            = False                ,
                                            open_issues_count   = __SKIP__                    ,

                                            license             = __(
                                                                        key      = 'apache-2.0'               ,
                                                                        name     = 'Apache License 2.0'       ,
                                                                        spdx_id  = 'Apache-2.0'               ,
                                                                        url      = 'https://api.github.com/licenses/apache-2.0',
                                                                        node_id  = __SKIP__
                                                                    )          ,

                                            allow_forking       = True                 ,
                                            is_template         = False                ,
                                            web_commit_signoff_required = False        ,
                                            topics              = []                   ,
                                            visibility          = 'public'             ,
                                            forks               = __SKIP__                    ,
                                            open_issues         = __SKIP__                    ,
                                            watchers            = __SKIP__                    ,
                                            default_branch      = 'dev'                ,
                                            temp_clone_token    = None                 ,
                                            custom_properties   = __()                 ,

                                            organization        = __(
                                                                        login               = 'the-cyber-boardroom'                           ,
                                                                        id                  = __SKIP__                                        ,
                                                                        node_id             = __SKIP__                                  ,
                                                                        avatar_url          = __SKIP__,
                                                                        gravatar_id         = ''                                               ,
                                                                        url                 = 'https://api.github.com/users/the-cyber-boardroom',
                                                                        html_url            = 'https://github.com/the-cyber-boardroom'         ,
                                                                        followers_url       = 'https://api.github.com/users/the-cyber-boardroom/followers',
                                                                        following_url       = 'https://api.github.com/users/the-cyber-boardroom/following{/other_user}',
                                                                        gists_url           = 'https://api.github.com/users/the-cyber-boardroom/gists{/gist_id}',
                                                                        starred_url         = 'https://api.github.com/users/the-cyber-boardroom/starred{/owner}{/repo}',
                                                                        subscriptions_url   = 'https://api.github.com/users/the-cyber-boardroom/subscriptions',
                                                                        organizations_url   = 'https://api.github.com/users/the-cyber-boardroom/orgs',
                                                                        repos_url           = 'https://api.github.com/users/the-cyber-boardroom/repos',
                                                                        events_url          = 'https://api.github.com/users/the-cyber-boardroom/events{/privacy}',
                                                                        received_events_url = 'https://api.github.com/users/the-cyber-boardroom/received_events',
                                                                        type                = 'Organization'                                   ,
                                                                        user_view_type      = 'public'                                         ,
                                                                        site_admin          = False
                                                                    )                                     ,
                                            network_count       = __SKIP__     ,
                                            subscribers_count   = __SKIP__
                                    )

