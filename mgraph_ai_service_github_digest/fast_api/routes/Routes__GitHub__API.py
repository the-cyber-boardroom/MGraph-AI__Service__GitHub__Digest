from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path               import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name   import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner  import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                   import Safe_Str__Git__Ref
from osbot_utils.utils.Misc                                                                     import date_time_now
from mgraph_ai_service_github_digest.service.github.GitHub__API                                 import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo                import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter        import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref           import Schema__GitHub__Repo__Ref

TAG__GITHUB_API            = 'github-api'
ROUTES_PATHS__GIT_HUB__API = [f'/{TAG__GITHUB_API}/apis-available'         ,
                              f'/{TAG__GITHUB_API}/rate-limit'             ,
                              f'/{TAG__GITHUB_API}/repository'             ,
                              f'/{TAG__GITHUB_API}/repository-commits'     ,
                              f'/{TAG__GITHUB_API}/repository-issues'      ,
                              f'/{TAG__GITHUB_API}/repository-files-names' ,
                              f'/{TAG__GITHUB_API}/repository-text-files'  ,
                              #f'/{TAG__GITHUB_API}/repository-refresh-cache',               # New endpoint for cache refresh
                              #f'/{TAG__GITHUB_API}/cache-status'           ,               # New endpoint for cache status
                              ]

GIT_HUB__API__DEFAULT__REPO_OWNER         = 'owasp-sbot'
GIT_HUB__API__DEFAULT__REPO_NAME          = 'OSBot-Utils'
GIT_HUB__API__DEFAULT__REF                = 'main'
GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH = 'osbot_utils'
GIT_HUB__API__DEFAULT__FILTER_CONTAINS    = ''
GIT_HUB__API__DEFAULT__FILTER_ENDS_WITH   = '.py'

class Routes__GitHub__API(Fast_API__Routes):
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
                                                   name  = Safe_Str__GitHub__Repo_Name (name ),
                                                   ref   = Safe_Str__Git__Ref          (ref  ))

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

    # def repository_refresh_cache(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,    # Repository owner
    #                                    name  : str = GIT_HUB__API__DEFAULT__REPO_NAME ,    # Repository name
    #                                    ref   : str = GIT_HUB__API__DEFAULT__REF                # Git ref to refresh
    #                               ) -> dict:                                                # Returns refresh status
    #     github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
    #                                                 name  = Safe_Str__GitHub__Repo_Name (name ),
    #                                                 ref   = Safe_Str__Git__Ref          (ref  ))
    #
    #     result = self.github_api.repository__zip__force_refresh(github_repo_ref=github_repo_ref)
    #
    #     # Return summary of refresh operation
    #     return dict(status       = 'refreshed'                              ,
    #                repository   = f'{owner}/{name}'                        ,
    #                ref          = ref                                      ,
    #                cache_id     = result.get('headers', {}).get('X-Cache-Id'),
    #                size_bytes   = len(result.get('content', b''))         ,
    #                refreshed_at = date_time_now()                          )

    # def cache_status(self) -> dict:                                                        # Returns cache service status
    #     return dict(cache_enabled = self.github_api.cache_enabled          ,
    #                cache_url     = self.github_api.cache_service.base_url ,
    #                namespace     = self.github_api.cache_service.namespace,
    #                strategy      = self.github_api.cache_service.strategy )

    def setup_routes(self):
        self.add_route_get (self.rate_limit            )
        self.add_route_get (self.apis_available        )
        self.add_route_get (self.repository_commits    )
        self.add_route_get (self.repository_issues     )
        self.add_route_get (self.repository_files_names)
        self.add_route_get (self.repository_text_files )
        self.add_route_get (self.repository            )
        #self.add_route_post(self.repository_refresh_cache)                                  # POST to trigger cache refresh
        #self.add_route_get (self.cache_status         )