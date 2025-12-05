# import requests
# from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
# from osbot_utils.type_safe.primitives.core.Safe_Str                                import Safe_Str
# from osbot_utils.type_safe.primitives.core.Safe_UInt                               import Safe_UInt
# from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text       import Safe_Str__Text
# from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key   import Safe_Str__Key
# from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url           import Safe_Str__Url
# from osbot_utils.type_safe.type_safe_core.decorators.type_safe                     import type_safe
# from osbot_utils.utils.Env                                                         import get_env
# from typing                                                                        import Dict, Any
#
#
# class MGraph__Service__Requests(Type_Safe):                         # HTTP request handler for MGraph services
#     base_url         : Safe_Str__Url       = None                   # Base URL for requests
#     timeout          : Safe_UInt           = 30                     # Request timeout in seconds
#     auth_key_name    : Safe_Str__Key       = None                   # Auth header key name
#     auth_key_value   : Safe_Str__Text      = None                   # Auth header key value
#     default_headers  : Dict[str, str]      = None                   # Default headers for all requests
#
#     def setup(self) -> 'MGraph__Service__Requests':                 # Initialize with auth from environment
#         # Load auth configuration from environment if not set
#         if not self.auth_key_name:
#             env_key_name = get_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME')
#             if env_key_name:
#                 self.auth_key_name = Safe_Str(env_key_name)
#
#         if not self.auth_key_value:
#             env_key_value = get_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE')
#             if env_key_value:
#                 self.auth_key_value = Safe_Str(env_key_value)
#
#         # Build default headers
#         self._build_default_headers()
#         return self
#
#     def _build_default_headers(self) -> None:                      # Build default headers including auth
#         self.default_headers = {}
#         if self.auth_key_name and self.auth_key_value:
#             self.default_headers[str(self.auth_key_name)] = str(self.auth_key_value)
#
#     @type_safe
#     def get_headers(self, additional_headers: Dict[str, str] = None) -> Dict[str, str]:  # Merge default and additional headers
#         headers = self.default_headers.copy() if self.default_headers else {}
#         if additional_headers:
#             headers.update(additional_headers)
#         return headers
#
#     @type_safe
#     def post(self, endpoint      : Safe_Str                ,        # Endpoint path (relative to base_url)
#                    data          : Any              = None ,        # Request body data
#                    headers       : Dict[str, str]   = None ,        # Additional headers
#                    json_data     : Dict[str, Any]   = None ,        # JSON payload
#                    timeout       : Safe_UInt        = None          # Override default timeout
#              ) -> requests.Response:                                # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         kwargs = {
#             'headers': merged_headers,
#             'timeout': int(request_timeout)
#         }
#
#         if json_data is not None:
#             kwargs['json'] = json_data
#         elif data is not None:
#             kwargs['data'] = data
#
#         return requests.post(url, **kwargs)
#
#     @type_safe
#     def get(self, endpoint      : Safe_Str                ,         # Endpoint path (relative to base_url)
#                   params        : Dict[str, Any]   = None ,         # Query parameters
#                   headers       : Dict[str, str]   = None ,         # Additional headers
#                   timeout       : Safe_UInt        = None           # Override default timeout
#             ) -> requests.Response:                                 # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         return requests.get(url,
#                           params  = params,
#                           headers = merged_headers,
#                           timeout = int(request_timeout))
#
#     @type_safe
#     def delete(self, endpoint      : Safe_Str                ,      # Endpoint path (relative to base_url)
#                      params        : Dict[str, Any]   = None ,      # Query parameters
#                      headers       : Dict[str, str]   = None ,      # Additional headers
#                      timeout       : Safe_UInt        = None        # Override default timeout
#                ) -> requests.Response:                              # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         return requests.delete(url,
#                              params  = params,
#                              headers = merged_headers,
#                              timeout = int(request_timeout))
#
#     @type_safe
#     def put(self, endpoint      : Safe_Str                ,         # Endpoint path (relative to base_url)
#                   data          : Any              = None ,         # Request body data
#                   headers       : Dict[str, str]   = None ,         # Additional headers
#                   json_data     : Dict[str, Any]   = None ,         # JSON payload
#                   timeout       : Safe_UInt        = None           # Override default timeout
#             ) -> requests.Response:                                 # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         kwargs = {
#             'headers': merged_headers,
#             'timeout': int(request_timeout)
#         }
#
#         if json_data is not None:
#             kwargs['json'] = json_data
#         elif data is not None:
#             kwargs['data'] = data
#
#         return requests.put(url, **kwargs)
#
#     @type_safe
#     def patch(self, endpoint      : Safe_Str                ,       # Endpoint path (relative to base_url)
#                     data          : Any              = None ,       # Request body data
#                     headers       : Dict[str, str]   = None ,       # Additional headers
#                     json_data     : Dict[str, Any]   = None ,       # JSON payload
#                     timeout       : Safe_UInt        = None         # Override default timeout
#               ) -> requests.Response:                               # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         kwargs = {
#             'headers': merged_headers,
#             'timeout': int(request_timeout)
#         }
#
#         if json_data is not None:
#             kwargs['json'] = json_data
#         elif data is not None:
#             kwargs['data'] = data
#
#         return requests.patch(url, **kwargs)
#
#     @type_safe
#     def head(self, endpoint      : Safe_Str                ,        # Endpoint path (relative to base_url)
#                    headers       : Dict[str, str]   = None ,        # Additional headers
#                    timeout       : Safe_UInt        = None          # Override default timeout
#              ) -> requests.Response:                                # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         return requests.head(url,
#                            headers = merged_headers,
#                            timeout = int(request_timeout))
#
#     @type_safe
#     def options(self, endpoint      : Safe_Str                ,     # Endpoint path (relative to base_url)
#                       headers       : Dict[str, str]   = None ,     # Additional headers
#                       timeout       : Safe_UInt        = None       # Override default timeout
#                 ) -> requests.Response:                             # Returns requests Response object
#
#         url = f"{self.base_url}/{endpoint}" if self.base_url else str(endpoint)
#         merged_headers = self.get_headers(headers)
#         request_timeout = timeout or self.timeout
#
#         return requests.options(url,
#                               headers = merged_headers,
#                               timeout = int(request_timeout))