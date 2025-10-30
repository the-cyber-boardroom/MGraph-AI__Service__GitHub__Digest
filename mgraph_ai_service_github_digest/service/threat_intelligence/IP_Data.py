from osbot_utils.decorators.methods.cache_on_self                                   import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.network.safe_str.Safe_Str__IP_Address import Safe_Str__IP_Address
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                      import type_safe
from osbot_utils.utils.Env                                                          import get_env
from mgraph_ai_service_github_digest.service.shared.Http__Requests                  import Http__Requests


IP_DATA__API_NAME          = 'api-key'
ENV_VAR__IP_DATA__API_KEY  = 'IP_DATA__API_KEY'
URL__API_IP_DATA           = 'https://api.ipdata.co/'


class IP_Data(Type_Safe):                                               # todo: add support for caching the data received from the ipdata.co API since it shouldn't change that often
    http_request : Http__Requests

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.http_request.base_url = URL__API_IP_DATA

    @cache_on_self
    def api_key(self):
        return get_env(ENV_VAR__IP_DATA__API_KEY, '')

    @type_safe
    def ip_address__details(self, ip_address: Safe_Str__IP_Address):
        with self.http_request as _:
            return _.get(ip_address, params={IP_DATA__API_NAME : self.api_key()})
