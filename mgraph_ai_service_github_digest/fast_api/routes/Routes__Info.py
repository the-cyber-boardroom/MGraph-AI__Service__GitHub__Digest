from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from mgraph_ai_service_github_digest.utils.Version  import version__mgraph_ai_service_github_digest

ROUTES_PATHS__INFO = ['/info/version']

class Routes__Info(Fast_API_Routes):
    tag :str = 'info'


    def version(self):
        return {'version': version__mgraph_ai_service_github_digest}

    
    def setup_routes(self):
        self.add_route_get(self.version)

