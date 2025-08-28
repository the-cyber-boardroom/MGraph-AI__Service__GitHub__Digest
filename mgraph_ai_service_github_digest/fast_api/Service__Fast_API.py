from osbot_fast_api.api.routes.Routes__Set_Cookie                                import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                     import Serverless__Fast_API
from mgraph_ai_service_github_digest.config                                      import FAST_API__TITLE
from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__API         import Routes__GitHub__API
from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__Digest      import Routes__GitHub__Digest
from mgraph_ai_service_github_digest.fast_api.routes.Routes__Info                import Routes__Info
from mgraph_ai_service_github_digest.fast_api.routes.Routes__Threat_Intelligence import Routes__Threat_Intelligence
from mgraph_ai_service_github_digest.utils.Version                               import version__mgraph_ai_service_github_digest


class Service__Fast_API(Serverless__Fast_API):

    def fast_api__title(self):                                       # todo: move this to the Fast_API class
        return FAST_API__TITLE

    def setup(self):
        super().setup()
        self.setup_fast_api_title_and_version()
        return self

    def setup_fast_api_title_and_version(self):                     # todo: move this to the Fast_API class
        app       = self.app()
        app.title = self.fast_api__title()
        app.version = version__mgraph_ai_service_github_digest
        return self

    def setup_routes(self):
        self.add_routes(Routes__Info               )
        self.add_routes(Routes__Set_Cookie         )
        self.add_routes(Routes__GitHub__Digest     )
        self.add_routes(Routes__GitHub__API        )
        self.add_routes(Routes__Threat_Intelligence)