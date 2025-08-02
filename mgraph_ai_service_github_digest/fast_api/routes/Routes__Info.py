from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from osbot_utils.utils.Http                         import GET

from mgraph_ai_service_github_digest.service.info.Info__Current_IP_Address import Info__Current_IP_Address
from mgraph_ai_service_github_digest.utils.Version  import version__mgraph_ai_service_github_digest

ROUTES_PATHS__INFO = ['/info/ip-address',
                      '/info/version'   ]

class Routes__Info(Fast_API_Routes):
    tag :str = 'info'
    info_current_ip_address : Info__Current_IP_Address

    def ip_address(self):
        with self.info_current_ip_address as _:
            sources = dict(check_ip__amazon_aws = _.from__checkip__amazon_aws())
        return { 'ip_address': GET('https://checkip.amazonaws.com').strip(),
                  'sources'  : sources}

    def version(self):
        return {'version': version__mgraph_ai_service_github_digest}

    
    def setup_routes(self):
        self.add_route_get(self.ip_address)
        self.add_route_get(self.version   )

