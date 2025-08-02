from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

ROUTES_PATHS__GIT_HUB__DIGEST = ['/github-digest/ping']

class Routes__GitHub__Digest(Fast_API_Routes):
    tag = 'github-digest'

    def ping(self):
        return 'pong'

    def setup_routes(self):
        self.add_route_get(self.ping)