# import pytest
# from unittest                                                                    import TestCase
# from osbot_utils.testing.__                                                      import __
# from osbot_utils.type_safe.primitives.core.Safe_UInt                             import Safe_UInt
# from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text     import Safe_Str__Text
# from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key import Safe_Str__Key
# from osbot_utils.utils.Env                                                       import set_env, get_env
# from osbot_utils.utils.Objects                                                   import base_classes
# from osbot_utils.utils.Misc                                                      import random_string
# from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
# from mgraph_ai_service_github_digest.service.cache.MGraph__Service__Requests     import MGraph__Service__Requests
#
#
# class test_MGraph__Service__Requests(TestCase):
#
#     @classmethod
#     def setUpClass(cls):                                                                  # One-time setup for all tests
#         pytest.skip("Rewire tests when adding support for Cache_Service")
#         cls.httpbin_url      = "https://httpbin.org"                                     # Use httpbin for testing
#         cls.test_auth_key    = "X-Test-API-Key"
#         cls.test_auth_value  = f"test-api-key-{random_string(6)}"
#         cls.requests_service = MGraph__Service__Requests(base_url=cls.httpbin_url).setup()
#
#         # Store original env values to restore later
#         cls.original_env_key_name  = get_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME')
#         cls.original_env_key_value = get_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE')
#
#     @classmethod
#     def tearDownClass(cls):                                                               # Restore original env values
#         if cls.original_env_key_name:
#             set_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME', cls.original_env_key_name)
#         if cls.original_env_key_value:
#             set_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE', cls.original_env_key_value)
#
#     def setUp(self):                                                                      # Per-test lightweight setup
#         # Reset service to clean state
#         self.requests_service.auth_key_name   = None
#         self.requests_service.auth_key_value  = None
#         self.requests_service.default_headers = {}
#         #self.requests_service.setup()                                                    # Rebuild headers
#
#     def test__init__(self):                                                               # Test auto-initialization
#         with MGraph__Service__Requests() as _:
#             assert type(_)                is MGraph__Service__Requests
#             assert base_classes(_)        == [Type_Safe, object]
#
#             # Verify all attributes initialized with correct types
#             assert type(_.base_url)       is type(None)                                  # Optional, starts as None
#             assert type(_.timeout)        is Safe_UInt
#             assert type(_.auth_key_name)  is type(None)
#             assert type(_.auth_key_value) is type(None)
#             assert type(_.default_headers) is type(None)
#
#             # Verify defaults using .obj()
#             assert _.obj() == __(base_url         = None   ,
#                                  timeout          = 30     ,
#                                  auth_key_name    = None   ,
#                                  auth_key_value   = None   ,
#                                  default_headers  = None   )
#
#     def test__init__with_custom_values(self):                                            # Test initialization with custom values
#         with MGraph__Service__Requests(base_url       = self.httpbin_url              ,
#                                       timeout        = 10                             ,
#                                       auth_key_name  = self.test_auth_key             ,
#                                       auth_key_value = self.test_auth_value           ) as _:
#             assert _.base_url       == self.httpbin_url
#             assert _.timeout        == 10
#             assert _.auth_key_name  == self.test_auth_key
#             assert _.auth_key_value == self.test_auth_value
#
#     def test_setup(self):                                                                # Test setup method initialization
#         with MGraph__Service__Requests() as _:
#             result = _.setup()
#             assert result is _                                                           # Returns self for chaining
#             assert _.default_headers == {}                                              # Empty when no auth configured
#
#     def test_setup__with_env_vars(self):                                                # Test setup with environment variables
#         # Set environment variables
#         env_key_name  = f'X-Env-API-Key-{random_string(4)}'
#         env_key_value = f'env-api-key-{random_string(8)}'
#         set_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME', env_key_name)
#         set_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE', env_key_value)
#
#         try:
#             with MGraph__Service__Requests() as _:
#                 _.setup()
#
#                 assert _.auth_key_name   == env_key_name
#                 assert _.auth_key_value  == env_key_value
#                 assert _.default_headers == {env_key_name: env_key_value}
#         finally:
#             # Clean up env vars
#             set_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME', None)
#             set_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE', None)
#
#     def test_setup__with_existing_auth(self):                                           # Test setup preserves existing auth
#         with MGraph__Service__Requests(auth_key_name  = "X-Custom-Key"                ,
#                                       auth_key_value = "custom-value"                 ) as _:
#             # Set env vars that should be ignored
#             set_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME', 'X-Env-Key')
#             set_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE', 'env-value')
#
#             try:
#                 _.setup()
#
#                 # Should keep the explicitly set values
#                 assert _.auth_key_name   == 'X-Custom-Key'
#                 assert _.auth_key_value  == 'custom-value'
#                 assert _.default_headers == {'X-Custom-Key': 'custom-value'}
#             finally:
#                 # Clean up
#                 set_env('ENV_VAR__FAST_API__AUTH__API_KEY__NAME', None)
#                 set_env('ENV_VAR__FAST_API__AUTH__API_KEY__VALUE', None)
#
#     def test__build_default_headers(self):                                              # Test header building logic
#         with MGraph__Service__Requests() as _:
#             # No auth configured
#             _._build_default_headers()
#             assert _.default_headers == {}
#
#             # With auth configured
#             _.auth_key_name  = Safe_Str__Key("Authorization")
#             _.auth_key_value = Safe_Str__Text("Bearer token123")
#             _._build_default_headers()
#             assert _.default_headers == {"Authorization": "Bearer token123"}
#
#     def test_get_headers(self):                                                         # Test header merging logic
#         with MGraph__Service__Requests() as _:
#             _.auth_key_name  = Safe_Str__Key("X-API-Key")
#             _.auth_key_value = Safe_Str__Text("api-key-123")
#             _._build_default_headers()
#
#             # No additional headers
#             result = _.get_headers()
#             assert result == {"X-API-Key": "api-key-123"}
#
#             # With additional headers
#             additional = {"Content-Type": "application/json", "X-Custom": "value"}
#             result = _.get_headers(additional)
#             assert result == {"X-API-Key"   : "api-key-123"                           ,
#                             "Content-Type" : "application/json"                       ,
#                             "X-Custom"     : "value"                                  }
#
#             # Additional headers override defaults
#             override = {"X-API-Key": "different-key"}
#             result = _.get_headers(override)
#             assert result == {"X-API-Key": "different-key"}                            # Override wins
#
#     def test_post(self):                                                                # Test POST request with httpbin
#         with self.requests_service as _:
#             # Test with form data
#             test_data = b"test binary data"
#             response = _.post(endpoint="post", data=test_data)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['data'] == test_data.decode('utf-8')                  # httpbin echoes back the data
#             assert response_json['url'] == f"{self.httpbin_url}/post"
#
#     def test_post__with_json(self):                                                     # Test POST with JSON payload
#         with self.requests_service as _:
#             _.auth_key_name = Safe_Str__Key("X-Custom-Auth")
#             _.auth_key_value = Safe_Str__Text(f"test-{random_string(6)}")
#             _.setup()
#
#             json_payload = {"key": "value", "number": 123, "list": [1, 2, 3]}
#             response = _.post(endpoint="post", json_data=json_payload)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['json'] == json_payload                               # httpbin echoes JSON
#             assert response_json['headers']['X-Custom-Auth'] == str(_.auth_key_value)  # Auth header present
#
#     def test_post__with_custom_headers(self):                                          # Test POST with custom headers
#         with self.requests_service as _:
#             custom_headers = {"X-Test-Header": "test-value", "X-Request-Id": random_string(8)}
#             response = _.post(endpoint="post",
#                             json_data={"test": "data"},
#                             headers=custom_headers)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['headers']['X-Test-Header'] == "test-value"
#             assert 'X-Request-Id' in response_json['headers']
#
#     def test_get(self):                                                                 # Test GET request with httpbin
#         with self.requests_service as _:
#             # Test with query parameters
#             params = {"param1": "value1", "param2": 123, "param3": "test"}
#             response = _.get(endpoint="get", params=params)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['args'] == {"param1": "value1", "param2": "123", "param3": "test"}
#             assert response_json['url'].startswith(f"{self.httpbin_url}/get")
#
#     def test_get__with_auth_headers(self):                                             # Test GET with auth headers
#         with self.requests_service as _:
#             _.auth_key_name = Safe_Str__Key("Authorization")
#             _.auth_key_value = Safe_Str__Text(f"Bearer {random_string(16)}")
#             _.setup()
#
#             response = _.get(endpoint="get")
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['headers']['Authorization'] == str(_.auth_key_value)
#
#     def test_get__with_custom_timeout(self):                                           # Test GET with custom timeout
#         with self.requests_service as _:
#             # httpbin has a /delay endpoint for testing timeouts
#             # Use a short timeout that should succeed
#             response = _.get(endpoint="delay/1", timeout=5)                            # 1 second delay, 5 second timeout
#             assert response.status_code == 200
#
#             # Test timeout failure (delay longer than timeout)
#             with pytest.raises(Exception):                                             # requests.Timeout wrapped in Exception
#                 _.get(endpoint="delay/5", timeout=1)                                   # 5 second delay, 1 second timeout
#
#     def test_delete(self):                                                             # Test DELETE request with httpbin
#         with self.requests_service as _:
#             response = _.delete(endpoint="delete")
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['url'] == f"{self.httpbin_url}/delete"
#
#     def test_delete__with_params(self):                                                # Test DELETE with query parameters
#         with self.requests_service as _:
#             params = {"id": "123", "confirm": "true"}
#             response = _.delete(endpoint="delete", params=params)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['args'] == params
#
#     def test_put(self):                                                                # Test PUT request with httpbin
#         with self.requests_service as _:
#             put_data = {"updated": "value", "timestamp": random_string(10)}
#             response = _.put(endpoint="put", json_data=put_data)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['json'] == put_data
#
#     def test_put__with_raw_data(self):                                                 # Test PUT with raw data
#         with self.requests_service as _:
#             raw_data = b"raw binary content for PUT"
#             response = _.put(endpoint="put", data=raw_data)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['data'] == raw_data.decode('utf-8')
#
#     def test_patch(self):                                                              # Test PATCH request with httpbin
#         with self.requests_service as _:
#             patch_data = {"field": "patched_value"}
#             response = _.patch(endpoint="patch", json_data=patch_data)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['json'] == patch_data
#
#     def test_head(self):                                                               # Test HEAD request with httpbin
#         with self.requests_service as _:
#             response = _.head(endpoint="get")                                          # HEAD on /get endpoint
#
#             assert response.status_code == 200
#             assert response.content == b''                                             # HEAD returns no body
#             assert 'Content-Type' in response.headers                                  # But has headers
#
#     def test_options(self):                                                            # Test OPTIONS request with httpbin
#         with self.requests_service as _:
#             response = _.options(endpoint="get")                                       # OPTIONS on /get endpoint
#
#             assert response.status_code == 200
#             assert 'Allow' in response.headers or response.status_code == 200          # httpbin returns 200 for OPTIONS
#
#     def test__without_base_url(self):                                                  # Test using full URLs without base_url
#         with MGraph__Service__Requests() as _:                                         # No base_url set
#             _.setup()
#
#             # Should work with full URL as endpoint
#             full_url = f"{self.httpbin_url}/get"
#             response = _.get(endpoint=full_url)
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert response_json['url'] == full_url
#
#     def test__status_codes(self):                                                      # Test various HTTP status codes
#         with self.requests_service as _:
#             # Test different status codes using httpbin's /status endpoint
#             test_codes = [200, 201, 400, 404, 500]
#
#             for code in test_codes:
#                 with self.subTest(status_code=code):
#                     response = _.get(endpoint=f"status/{code}")
#                     assert response.status_code == code
#
#     def test__user_agent(self):                                                        # Test that requests are made with python-requests user agent
#         with self.requests_service as _:
#             response = _.get(endpoint="user-agent")
#
#             assert response.status_code == 200
#             response_json = response.json()
#             assert 'python-requests' in response_json['user-agent'].lower()
#
#     def test__response_formats(self):                                                  # Test different response formats
#         with self.requests_service as _:
#             # JSON response
#             response = _.get(endpoint="json")
#             assert response.status_code == 200
#             assert isinstance(response.json(), dict)
#
#             # HTML response
#             response = _.get(endpoint="html")
#             assert response.status_code == 200
#             assert b'<!DOCTYPE html>' in response.content
#
#             # XML response
#             response = _.get(endpoint="xml")
#             assert response.status_code == 200
#             assert b'<?xml' in response.content