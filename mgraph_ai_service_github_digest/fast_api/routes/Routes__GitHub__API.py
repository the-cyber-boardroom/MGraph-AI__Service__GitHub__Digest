from osbot_fast_api.api.Fast_API_Routes                                                                 import Fast_API_Routes
from mgraph_ai_service_github_digest.service.github.GitHub__API                                         import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo                        import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter                import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref                   import Schema__GitHub__Repo__Ref
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.git.Safe_Str__Git__Ref              import Safe_Str__Git__Ref
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.github.Safe_Str__GitHub__Repo_Name  import Safe_Str__GitHub__Repo_Name
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.github.Safe_Str__GitHub__Repo_Owner import Safe_Str__GitHub__Repo_Owner
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                                                  import Safe_Str__File__Path

TAG__GITHUB_API            = 'github-api'
ROUTES_PATHS__GIT_HUB__API = [f'/{TAG__GITHUB_API}/apis-available'         ,
                              f'/{TAG__GITHUB_API}/rate-limit'             ,
                              f'/{TAG__GITHUB_API}/repository'             ,
                              f'/{TAG__GITHUB_API}/repository-commits'     ,
                              f'/{TAG__GITHUB_API}/repository-issues'      ,
                              f'/{TAG__GITHUB_API}/repository-files-names' ,
                              f'/{TAG__GITHUB_API}/repository-text-files'  ,
                              ]

GIT_HUB__API__DEFAULT__REPO_OWNER         = 'owasp-sbot'
GIT_HUB__API__DEFAULT__REPO_NAME          = 'OSBot-Utils'
GIT_HUB__API__DEFAULT__REF                = 'main'
GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH = 'osbot_utils'
GIT_HUB__API__DEFAULT__FILTER_CONTAINS    = ''
GIT_HUB__API__DEFAULT__FILTER_ENDS_WITH   = '.py'

class Routes__GitHub__API(Fast_API_Routes):
    tag        : str         = TAG__GITHUB_API
    github_api : GitHub__API

    def apis_available(self):
        return self.github_api.apis_available()

    def rate_limit(self):
        return self.github_api.rate_limit()

    def repository(self, owner: str = GIT_HUB__API__DEFAULT__REPO_OWNER,
                        name : str = GIT_HUB__API__DEFAULT__REPO_NAME
                   ) -> dict:
        github_repo = Schema__GitHub__Repo(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                           name  = Safe_Str__GitHub__Repo_Name (name ))
        return self.github_api.repository(github_repo=github_repo)

    def repository_commits(self, owner: str = GIT_HUB__API__DEFAULT__REPO_OWNER,
                                 name : str = GIT_HUB__API__DEFAULT__REPO_NAME
                           ) -> dict:
        github_repo = Schema__GitHub__Repo(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                           name  = Safe_Str__GitHub__Repo_Name (name ))
        return self.github_api.commits(github_repo=github_repo)

    def repository_issues(self, owner: str = GIT_HUB__API__DEFAULT__REPO_OWNER,
                               name : str = GIT_HUB__API__DEFAULT__REPO_NAME
                          ) -> dict:
        github_repo = Schema__GitHub__Repo(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                           name  = Safe_Str__GitHub__Repo_Name (name ))
        return self.github_api.issues(github_repo=github_repo)

    def repository_text_files(self, owner              : str = GIT_HUB__API__DEFAULT__REPO_OWNER,
                                    name               : str = GIT_HUB__API__DEFAULT__REPO_NAME,
                                    ref                : str = GIT_HUB__API__DEFAULT__REF,
                                    filter_starts_with : str = '',
                                    filter_contains    : str = '',
                                    filter_ends_with   : str = ''
                              ) -> dict:


        repo_filter = Schema__GitHub__Repo__Filter(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                   name  = Safe_Str__GitHub__Repo_Name(name),
                                                   ref   = Safe_Str__Git__Ref(ref))

        # Only set filter fields if they have values (not empty strings)
        if filter_starts_with:
            repo_filter.filter_starts_with = Safe_Str__File__Path(filter_starts_with)
        if filter_contains:
            repo_filter.filter_contains = Safe_Str__File__Path(filter_contains)
        if filter_ends_with:
            repo_filter.filter_ends_with = Safe_Str__File__Path(filter_ends_with)

        return self.github_api.repository__contents__as_strings(repo_filter=repo_filter)

    def repository_files_names(self, owner: str = GIT_HUB__API__DEFAULT__REPO_OWNER,
                                     name : str = GIT_HUB__API__DEFAULT__REPO_NAME,
                                     ref  : str = GIT_HUB__API__DEFAULT__REF
                                ) -> list:
        github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                    name  = Safe_Str__GitHub__Repo_Name (name ),
                                                    ref   = Safe_Str__Git__Ref          (ref  ))
        return self.github_api.repository__files__names(github_repo_ref=github_repo_ref)

    def setup_routes(self):
        self.add_route_get(self.rate_limit            )
        self.add_route_get(self.apis_available        )
        self.add_route_get(self.repository_commits    )
        self.add_route_get(self.repository_issues     )
        self.add_route_get(self.repository_files_names)
        self.add_route_get(self.repository_text_files )
        self.add_route_get(self.repository            )