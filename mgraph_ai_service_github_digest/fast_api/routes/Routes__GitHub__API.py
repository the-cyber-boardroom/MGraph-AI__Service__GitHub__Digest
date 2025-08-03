from osbot_fast_api.api.Fast_API_Routes                         import Fast_API_Routes
from osbot_utils.helpers.Safe_Id                                import Safe_Id
from mgraph_ai_service_github_digest.service.github.GitHub__API import GitHub__API

TAG__GITHUB_API            = 'github-api'
ROUTES_PATHS__GIT_HUB__API = [f'/{TAG__GITHUB_API}/apis-available'        ,
                              f'/{TAG__GITHUB_API}/rate-limit'            ,
                              f'/{TAG__GITHUB_API}/repository'            ,
                              f'/{TAG__GITHUB_API}/repository-text-files' ,
                              f'/{TAG__GITHUB_API}/repository-files-names']

GIT_HUB__API__DEFAULT__OWNER = 'owasp-sbot'
GIT_HUB__API__DEFAULT__REPO  = 'OSBot-Utils'

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

    def repository_text_files(self, owner: str = GIT_HUB__API__DEFAULT__OWNER,
                                    repo : str=GIT_HUB__API__DEFAULT__REPO
                               ) -> dict:
        return self.github_api.repository__contents__as_strings(owner=Safe_Id(owner), repo=Safe_Id(repo))

    def repository_files_names(self, owner: str = GIT_HUB__API__DEFAULT__OWNER,
                                     repo : str=GIT_HUB__API__DEFAULT__REPO
                                ) -> dict:
        return self.github_api.repository__files__names(owner=Safe_Id(owner), repo=Safe_Id(repo))

    def setup_routes(self):
        self.add_route_get(self.rate_limit            )
        self.add_route_get(self.apis_available        )
        self.add_route_get(self.repository_text_files )
        self.add_route_get(self.repository_files_names)
        self.add_route_get(self.repository            )