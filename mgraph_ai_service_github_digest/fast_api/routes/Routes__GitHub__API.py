from osbot_fast_api.api.Fast_API_Routes                         import Fast_API_Routes
from mgraph_ai_service_github_digest.service.github.GitHub__API import GitHub__API

ROUTES_PATHS__GIT_HUB__API = ['/github-api/rate-limit']

class Routes__GitHub__API(Fast_API_Routes):
    tag        : str         = 'github-api'
    github_api : GitHub__API

    def rate_limit(self):
        return self.github_api.rate_limit()

    def setup_routes(self):
        self.add_route_get(self.rate_limit)