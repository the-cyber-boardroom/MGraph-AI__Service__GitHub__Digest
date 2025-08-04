from osbot_fast_api.api.Fast_API_Routes                                                  import Fast_API_Routes
from osbot_utils.helpers.Safe_Id                                                         import Safe_Id
from mgraph_ai_service_github_digest.service.github.GitHub__API                          import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter

TAG__GITHUB_API            = 'github-api'
ROUTES_PATHS__GIT_HUB__API = [f'/{TAG__GITHUB_API}/apis-available'         ,
                              f'/{TAG__GITHUB_API}/rate-limit'             ,
                              f'/{TAG__GITHUB_API}/repository'             ,
                              f'/{TAG__GITHUB_API}/repository-commits'     ,
                              f'/{TAG__GITHUB_API}/repository-issues'      ,
                              f'/{TAG__GITHUB_API}/repository-files-names' ,
                              f'/{TAG__GITHUB_API}/repository-text-files'  ,
                              ]

GIT_HUB__API__DEFAULT__OWNER              = 'owasp-sbot'
GIT_HUB__API__DEFAULT__REPO               = 'OSBot-Utils'
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

    def repository(self, owner: str = GIT_HUB__API__DEFAULT__OWNER,
                         repo : str=GIT_HUB__API__DEFAULT__REPO
                    ) -> dict:
        return self.github_api.repository(owner=Safe_Id(owner), repo=Safe_Id(repo))

    def repository_commits(self, owner: str = GIT_HUB__API__DEFAULT__OWNER,
                                    repo : str=GIT_HUB__API__DEFAULT__REPO
                               ) -> dict:
        return self.github_api.commits(owner=Safe_Id(owner), repo=Safe_Id(repo))

    def repository_issues(self, owner: str = GIT_HUB__API__DEFAULT__OWNER,
                                    repo : str=GIT_HUB__API__DEFAULT__REPO
                               ) -> dict:
        return self.github_api.issues(owner=Safe_Id(owner), repo=Safe_Id(repo))

    def repository_text_files(self, owner              : str = GIT_HUB__API__DEFAULT__OWNER,
                                    repo               : str = GIT_HUB__API__DEFAULT__REPO ,
                                    ref                : str = GIT_HUB__API__DEFAULT__REF  ,
                                    filter_starts_with : str = ''                          ,
                                    filter_contains    : str = ''                          ,
                                    filter_ends_with   : str = ''
                               ) -> dict:
        repo_filter = Schema__GitHub__Repo__Filter(owner              = owner               ,
                                                   repo               = repo                ,
                                                   ref                = ref                 ,
                                                   filter_starts_with = filter_starts_with  ,
                                                   filter_contains    = filter_contains     ,
                                                   filter_ends_with   = filter_ends_with    )
        return self.github_api.repository__contents__as_strings(repo_filter=repo_filter)

    def repository_files_names(self, owner: str = GIT_HUB__API__DEFAULT__OWNER,
                                     repo : str = GIT_HUB__API__DEFAULT__REPO
                                ) -> list:
        return self.github_api.repository__files__names(owner=Safe_Id(owner), repo=Safe_Id(repo))

    def setup_routes(self):
        self.add_route_get(self.rate_limit            )
        self.add_route_get(self.apis_available        )
        self.add_route_get(self.repository_commits    )
        self.add_route_get(self.repository_issues     )
        self.add_route_get(self.repository_files_names)
        self.add_route_get(self.repository_text_files )
        self.add_route_get(self.repository            )