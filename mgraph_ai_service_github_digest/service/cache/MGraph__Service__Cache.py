# from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
# from osbot_utils.type_safe.primitives.core.Safe_Str                                             import Safe_Str
# from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt
# from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name   import Safe_Str__GitHub__Repo_Name
# from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner  import Safe_Str__GitHub__Repo_Owner
# from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                   import Safe_Str__Git__Ref
# from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                               import Safe_Id
# from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url                        import Safe_Str__Url
# from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                  import type_safe
# from mgraph_ai_service_github_digest.service.cache.MGraph__Service__Requests                    import MGraph__Service__Requests
# from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Hash                 import Safe_Str__Cache_Hash
# from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Id                   import Safe_Str__Cache_Id
# from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Namespace            import Safe_Str__Cache_Namespace
# from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Delete__Response      import Schema__Cache__Delete__Response
# from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Retrieve__Response    import Schema__Cache__Retrieve__Response
# from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Store__Response       import Schema__Cache__Store__Response
#
#
# class MGraph__Service__Cache(Type_Safe):                                         # Main cache service client
#     base_url        : Safe_Str__Url             = "https://cache.dev.mgraph.ai"  # Cache service endpoint
#     namespace       : Safe_Str__Cache_Namespace = "github-digest"                # Default namespace
#     strategy        : Safe_Id                   = "temporal_latest"              # Default storage strategy
#     timeout         : Safe_UInt                 = 30                             # Request timeout in seconds
#     requests_service: MGraph__Service__Requests = None                           # HTTP requests handler
#
#     def setup(self) -> 'MGraph__Service__Cache':                                 # Initialize service with request handler
#         if not self.requests_service:
#             self.requests_service = MGraph__Service__Requests(base_url = self.base_url, timeout  = self.timeout).setup()
#         return self
#
#     @type_safe
#     def store_binary(self, data          : bytes                           ,  # Binary data to cache
#                           namespace      : Safe_Str__Cache_Namespace = None,  # Override namespace
#                           strategy       : Safe_Str                  = None,  # Override strategy
#                           force_refresh  : bool                      = False  # Force cache update
#                      ) -> Schema__Cache__Store__Response:                     # Returns store response
#
#         namespace = namespace or self.namespace
#         strategy  = strategy  or self.strategy
#         endpoint = f"cache/store/binary/{strategy}/{namespace}"
#
#         headers = {}
#         if force_refresh:                                                   # Add header to force cache refresh
#             headers['X-Force-Refresh'] = 'true'
#
#         response = self.requests_service.post(endpoint = endpoint,
#                                              data     = data      ,
#                                              headers  = headers   )
#
#         if response.status_code == 200:
#             response_data = response.json()
#             return Schema__Cache__Store__Response(**response_data)
#         else:
#             raise Exception(f"Cache store failed: {response.status_code}")
#
#     @type_safe
#     def retrieve_by_hash(self, cache_hash : Safe_Str__Cache_Hash            ,   # Hash to retrieve
#                               namespace   : Safe_Str__Cache_Namespace = None    # Override namespace
#                          ) -> Schema__Cache__Retrieve__Response:                # Returns retrieve response or None
#         namespace = namespace or self.namespace
#         endpoint = f"cache/retrieve/binary/by-hash/{cache_hash}/{namespace}"
#         response = self.requests_service.get(endpoint)
#
#         if response.status_code == 200:
#             return Schema__Cache__Retrieve__Response(
#                 data      = response.content                         ,
#                 metadata  = response.headers.get('X-Cache-Metadata') ,
#                 data_type = 'binary'                                 ,
#                 cache_hit = True                                     ,
#                 cached_at = response.headers.get('X-Cached-At')     ,
#                 cache_id  = response.headers.get('X-Cache-Id')      )
#         elif response.status_code == 404:
#             return None                                                     # Not in cache
#         else:
#             raise Exception(f"Cache retrieve failed: {response.status_code}")
#
#     @type_safe
#     def retrieve_by_id(self, cache_id  : Safe_Str__Cache_Id            ,     # ID to retrieve
#                              namespace  : Safe_Str__Cache_Namespace = None   # Override namespace
#                         ) -> Schema__Cache__Retrieve__Response:              # Returns retrieve response or None
#         namespace = namespace or self.namespace
#         endpoint = f"cache/retrieve/binary/by-id/{cache_id}/{namespace}"
#         response = self.requests_service.get(endpoint)
#
#         if response.status_code == 200:
#             return Schema__Cache__Retrieve__Response(
#                 data      = response.content                         ,
#                 metadata  = response.headers.get('X-Cache-Metadata') ,
#                 data_type = 'binary'                                 ,
#                 cache_hit = True                                     ,
#                 cached_at = response.headers.get('X-Cached-At')     ,
#                 cache_id  = cache_id                                 )
#         elif response.status_code == 404:
#             return None
#         else:
#             raise Exception(f"Cache retrieve failed: {response.status_code}")
#
#     @type_safe
#     def delete_by_id(self, cache_id : Safe_Str__Cache_Id              ,    # ID to delete
#                            namespace : Safe_Str__Cache_Namespace = None      # Override namespace
#                     ) -> Schema__Cache__Delete__Response:                 # Returns delete response
#         namespace = namespace or self.namespace
#         endpoint = f"cache/delete/by-id/{cache_id}/{namespace}"
#         response = self.requests_service.delete(endpoint)
#
#         if response.status_code == 200:
#             response_data = response.json()
#             return Schema__Cache__Delete__Response(**response_data)
#         else:
#             raise Exception(f"Cache delete failed: {response.status_code}")
#
#     @type_safe
#     def exists(self, cache_hash : Safe_Str__Cache_Hash               ,     # Hash to check
#                      namespace   : Safe_Str__Cache_Namespace = None         # Override namespace
#                 ) -> bool:                                                  # Returns True if exists
#         namespace = namespace or self.namespace
#         endpoint = f"cache/exists/{cache_hash}/{namespace}"
#         response = self.requests_service.get(endpoint)
#
#         if response.status_code == 200:
#             result = response.json()
#             return result.get('exists', False)
#         else:
#             return False
#
#     @type_safe
#     def generate_cache_key(self, owner : Safe_Str__GitHub__Repo_Owner ,       # Repository owner
#                                  name  : Safe_Str__GitHub__Repo_Name  ,       # Repository name
#                                  ref   : Safe_Str__Git__Ref                   # Git ref
#                             ) -> Safe_Str__Cache_Id:                          # Returns cache key
#         cache_key = f"github:repo:{owner}:{name}:{ref}"                       # Generate deterministic cache key for repository
#         return Safe_Str__Cache_Id(cache_key)                                  # todo: see if we shouldn't add support to Safe_Str__Cache_Id for : (since at the moment  it is basically Safe_Id)