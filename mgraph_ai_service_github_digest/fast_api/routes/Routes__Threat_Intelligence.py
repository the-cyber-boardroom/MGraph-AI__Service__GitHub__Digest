from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from osbot_utils.helpers.safe_str.http.Safe_Str__IP_Address                     import Safe_Str__IP_Address
from mgraph_ai_service_github_digest.service.threat_intelligence.IP_Data        import IP_Data

ROUTES_PATHS__THREAT_INTELLIGENCE = ['/threat-intelligence/ip-address-details']

class Routes__Threat_Intelligence(Fast_API_Routes):
    tag     : str = 'threat-intelligence'
    ip_data : IP_Data

    def ip_address_details(self, ip_address='8.8.8.8'):
        return self.ip_data.ip_address__details(ip_address=Safe_Str__IP_Address(ip_address))

    def setup_routes(self):
        self.add_route_get(self.ip_address_details)