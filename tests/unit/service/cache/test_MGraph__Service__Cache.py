# from unittest                                                                                import TestCase
#
# import pytest
# from osbot_utils.testing.__                                                                  import __
# from osbot_utils.type_safe.primitives.core.Safe_Str                                          import Safe_Str
# from osbot_utils.type_safe.primitives.core.Safe_UInt                                         import Safe_UInt
# from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                        import Random_Guid
# from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                            import Safe_Id
# from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url                     import Safe_Str__Url
# from osbot_utils.utils.Objects                                                               import base_classes
# from osbot_utils.utils.Misc                                                                  import random_string
# from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
# from mgraph_ai_service_github_digest.service.cache.MGraph__Service__Cache                    import MGraph__Service__Cache
# from mgraph_ai_service_github_digest.service.cache.MGraph__Service__Requests                 import MGraph__Service__Requests
# from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Hash              import Safe_Str__Cache_Hash
# from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Id                import Safe_Str__Cache_Id
# from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Namespace         import Safe_Str__Cache_Namespace
# from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Delete__Response   import Schema__Cache__Delete__Response
# from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Retrieve__Response import Schema__Cache__Retrieve__Response
# from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Store__Response    import Schema__Cache__Store__Response
#
# class test_MGraph__Service__Cache(TestCase):
#
#     @classmethod
#     def setUpClass(cls):                                                                     # One-time setup for expensive operations
#
#         pytest.skip("Rewire tests when adding support for Cache_Service")
#         # Create unique test namespace to avoid conflicts
#         cls.test_namespace  = Safe_Str__Cache_Namespace(f"test-cache-{random_string(8)}")
#
#         # Setup cache service with test namespace
#         cls.cache_service = MGraph__Service__Cache(namespace=cls.test_namespace).setup()
#
#         # Track created cache IDs for cleanup
#         cls.created_cache_ids = []
#
#     @classmethod
#     def tearDownClass(cls):                                                                  # Clean up all created cache entries
#         # Delete all tracked cache entries
#         for cache_id in cls.created_cache_ids:
#             try:
#                 cls.cache_service.delete_by_id(cache_id=cache_id)
#             except:
#                 pass                                                                         # Ignore cleanup errors
#
#     def test__init__(self):                                                                  # Test auto-initialization of cache service
#         with MGraph__Service__Cache() as _:
#             assert type(_)                   is MGraph__Service__Cache
#             assert base_classes(_)           == [Type_Safe, object]
#
#             # Verify all attributes are initialized with correct types
#             assert type(_.base_url)          is Safe_Str__Url
#             assert type(_.namespace)         is Safe_Str__Cache_Namespace
#             assert type(_.strategy)          is Safe_Id
#             assert type(_.timeout)           is Safe_UInt
#             assert type(_.requests_service)  is type(None)                                  # Not initialized until setup()
#
#             # Verify default values using .obj()
#             assert _.obj() == __(base_url         = "https://cache.dev.mgraph.ai"          ,
#                                 namespace        = "github-digest"                         ,
#                                 strategy         = "temporal_latest"                       ,
#                                 timeout          = 30                                      ,
#                                 requests_service = None                                    )
#
#     def test__init__with_custom_values(self):                                               # Test initialization with custom values
#         custom_url       = "https://cache.dev.mgraph.ai"                                   # Must use real URL
#         custom_namespace = f"test-custom-{random_string(6)}"
#         custom_strategy  = "direct"
#         custom_timeout   = 60
#
#         with MGraph__Service__Cache(base_url  = custom_url      ,
#                                    namespace = custom_namespace,
#                                    strategy  = custom_strategy ,
#                                    timeout   = custom_timeout  ) as _:
#             assert _.base_url  == custom_url
#             assert _.namespace == custom_namespace
#             assert _.strategy  == custom_strategy
#             assert _.timeout   == custom_timeout
#
#     def test_setup(self):                                                                   # Test setup initializes requests service
#         with MGraph__Service__Cache() as _:
#             assert _.requests_service is None                                              # Not initialized before setup
#
#             result = _.setup()
#
#             assert result is _                                                             # Returns self for chaining
#             assert type(_.requests_service) is MGraph__Service__Requests                  # Now initialized
#             assert _.requests_service.base_url == _.base_url                              # Configured with cache URL
#             assert _.requests_service.timeout  == _.timeout                                # Configured with cache timeout
#
#     def test_setup__with_custom_requests_service(self):                                    # Test setup with pre-configured requests service
#         # Create custom requests service with auth
#         custom_requests = MGraph__Service__Requests(
#             base_url       = "https://cache.dev.mgraph.ai",
#             timeout        = 45,
#             auth_key_name  = "X-Custom-Auth",
#             auth_key_value = "custom-key-123"
#         ).setup()
#
#         with MGraph__Service__Cache(requests_service=custom_requests) as _:
#             _.setup()
#
#             assert _.requests_service is custom_requests                                   # Uses provided service
#             assert _.requests_service.auth_key_name == "X-Custom-Auth"                    # Auth preserved
#
#     def test_store_binary(self):                                                           # Test binary storage operation with live server
#         test_data = b"test binary data for refactored cache service"
#
#         with self.cache_service as _:
#             result = _.store_binary(data=test_data)
#
#             # Track for cleanup
#             self.created_cache_ids.append(result.cache_id)
#
#             # Verify response type and structure
#             assert type(result)           is Schema__Cache__Store__Response
#             assert type(result.cache_id)  is Safe_Str__Cache_Id
#             assert type(result.hash)      is Safe_Str__Cache_Hash
#             assert result.size            == len(test_data)
#             assert len(result.hash)       == 16                                            # 16-char hash
#             assert result.paths          is not None
#
#             # Verify we can retrieve what we stored
#             retrieved = _.retrieve_by_hash(cache_hash=result.hash)
#             assert retrieved is not None
#             assert retrieved.data == test_data
#
#     def test_store_binary__with_force_refresh(self):                                       # Test force refresh flag with live server
#         test_data = b"data for force refresh test"
#
#         with self.cache_service as _:
#             # Store initial version
#             result1 = _.store_binary(data=test_data)
#             self.created_cache_ids.append(result1.cache_id)
#
#             # Store again with force refresh (same data, should get new cache_id)
#             result2 = _.store_binary(data=test_data, force_refresh=True)
#             self.created_cache_ids.append(result2.cache_id)
#
#             # Same hash (same content) but different cache IDs
#             assert result1.hash     == result2.hash
#             assert result1.cache_id != result2.cache_id                                    # Different cache entries
#
#     def test_store_binary__different_strategies(self):                                     # Test different storage strategies
#         strategies = ["direct", "temporal", "temporal_latest"]
#         test_data = b"strategy test data for refactored service"
#
#         with self.cache_service as _:
#             for strategy in strategies:
#                 with self.subTest(strategy=strategy):
#                     # Store with specific strategy
#                     result = _.store_binary(data=test_data, strategy=strategy)
#                     self.created_cache_ids.append(result.cache_id)
#
#                     assert result.cache_id is not None
#                     assert result.hash is not None
#
#                     # Retrieve and verify
#                     retrieved = _.retrieve_by_hash(cache_hash=result.hash)
#                     assert retrieved.data == test_data
#
#     def test_retrieve_by_hash(self):                                                       # Test retrieval by hash with live server
#         test_content = b"test content for hash retrieval in refactored service"
#
#         with self.cache_service as _:
#             # Store first
#             store_result = _.store_binary(data=test_content)
#             self.created_cache_ids.append(store_result.cache_id)
#
#             # Retrieve by hash
#             result = _.retrieve_by_hash(cache_hash=store_result.hash)
#
#             # Verify response
#             assert type(result)       is Schema__Cache__Retrieve__Response
#             assert result.data        == test_content
#             assert result.data_type   == 'binary'
#             assert result.cache_hit   == True
#
#     def test_retrieve_by_hash__not_found(self):                                           # Test retrieval when item not in cache
#         non_existent_hash = Safe_Str__Cache_Hash("0000000000000000")                      # Unlikely to exist
#
#         with self.cache_service as _:
#             result = _.retrieve_by_hash(cache_hash=non_existent_hash)
#             assert result is None
#
#     def test_retrieve_by_id(self):                                                        # Test retrieval by ID with live server
#         test_content = b"test content for ID retrieval in refactored service"
#
#         with self.cache_service as _:
#             # Store first
#             store_result = _.store_binary(data=test_content)
#             self.created_cache_ids.append(store_result.cache_id)
#
#             # Retrieve by ID
#             result = _.retrieve_by_id(cache_id=store_result.cache_id)
#
#             # Verify response
#             assert type(result)     is Schema__Cache__Retrieve__Response
#             assert result.data      == test_content
#             assert result.cache_id  == store_result.cache_id
#
#     def test_retrieve_by_id__not_found(self):                                             # Test retrieval by ID when not found
#         non_existent_id = Safe_Str__Cache_Id(str(Random_Guid()))                          # Random GUID unlikely to exist
#
#         with self.cache_service as _:
#             result = _.retrieve_by_id(cache_id=non_existent_id)
#             assert result is None
#
#     def test_delete_by_id(self):                                                          # Test deletion by ID with live server
#         test_data = b"data to be deleted in refactored service"
#
#         with self.cache_service as _:
#             # Store first
#             store_result = _.store_binary(data=test_data)
#             cache_id = store_result.cache_id
#
#             # Verify it exists
#             exists_before = _.retrieve_by_id(cache_id=cache_id)
#             assert exists_before is not None
#             assert exists_before.data == test_data
#
#             # Delete it
#             result = _.delete_by_id(cache_id=cache_id)
#
#             # Verify response
#             assert type(result)           is Schema__Cache__Delete__Response
#             assert result.deleted         == True
#             assert result.cache_id        == cache_id
#             assert result.files_deleted   > 0                                             # At least 1 file deleted
#
#             # Verify it's gone
#             exists_after = _.retrieve_by_id(cache_id=cache_id)
#             assert exists_after is None
#
#     def test_delete_by_id__not_found(self):                                               # Test deletion of non-existent ID
#         non_existent_id = Safe_Str__Cache_Id(str(Random_Guid()))
#
#         with self.cache_service as _:
#             # Should handle gracefully
#             try:
#                 result = _.delete_by_id(cache_id=non_existent_id)
#                 # If no exception, check the response
#                 assert type(result) is Schema__Cache__Delete__Response
#                 # API might return success with 0 files deleted or deleted=False
#             except Exception as e:
#                 # API might return error for non-existent ID
#                 assert "404" in str(e) or "not found" in str(e).lower() or "Cache delete failed" in str(e)
#
#     def test_exists(self):                                                                # Test existence check with live server
#         test_data = b"data for existence check in refactored service"
#
#         with self.cache_service as _:
#             # Store data first
#             store_result = _.store_binary(data=test_data)
#             self.created_cache_ids.append(store_result.cache_id)
#
#             # Check it exists
#             result = _.exists(cache_hash=store_result.hash)
#             assert result is True
#
#             # Check non-existent hash
#             non_existent = _.exists(cache_hash=Safe_Str__Cache_Hash("ffffffffffffffff"))
#             assert non_existent is False
#
#     def test_generate_cache_key(self):                                                    # Test cache key generation
#         with self.cache_service as _:
#             result = _.generate_cache_key(owner = "test-owner"                           ,
#                                          name  = "test-repo"                             ,
#                                          ref   = "main"                                  )
#
#             assert type(result) is Safe_Str
#             assert result == "github:repo:test-owner:test-repo:main"
#
#     def test_generate_cache_key__with_special_chars(self):                                # Test cache key with special characters
#         with self.cache_service as _:
#             # Safe_Str will sanitize special characters
#             result = _.generate_cache_key(owner = "test@owner!"                          ,
#                                          name  = "test#repo$"                            ,
#                                          ref   = "feat/branch"                           )
#
#             # Special chars get removed/replaced by Safe_Str
#             assert type(result) is Safe_Str
#             assert "githubrepotestownertestrepofeatbranch" in result.replace(":", "")    # Sanitized version
#
#     def test__namespace_isolation(self):                                                  # Test that namespaces properly isolate data
#         test_data = b"namespace isolation test data"
#         namespace1 = Safe_Str__Cache_Namespace(f"test-ns1-{random_string(6)}")
#         namespace2 = Safe_Str__Cache_Namespace(f"test-ns2-{random_string(6)}")
#
#         with self.cache_service as _:
#             # Store in first namespace
#             result1 = _.store_binary(data=test_data, namespace=namespace1)
#             self.created_cache_ids.append(result1.cache_id)
#
#             # Store same data in second namespace
#             result2 = _.store_binary(data=test_data, namespace=namespace2)
#             self.created_cache_ids.append(result2.cache_id)
#
#             # Same hash but different cache IDs (isolated by namespace)
#             assert result1.hash == result2.hash
#
#             # Can retrieve from each namespace independently
#             retrieved1 = _.retrieve_by_hash(cache_hash=result1.hash, namespace=namespace1)
#             retrieved2 = _.retrieve_by_hash(cache_hash=result2.hash, namespace=namespace2)
#
#             assert retrieved1.data == test_data
#             assert retrieved2.data == test_data
#
#             # Delete from namespace1 doesn't affect namespace2
#             _.delete_by_id(cache_id=result1.cache_id, namespace=namespace1)
#
#             # namespace2 data still exists
#             still_exists = _.retrieve_by_hash(cache_hash=result2.hash, namespace=namespace2)
#             assert still_exists is not None
#             assert still_exists.data == test_data
#
#             # Clean up namespace2
#             _.delete_by_id(cache_id=result2.cache_id, namespace=namespace2)
#
#             # Remove from tracking since we already deleted
#             self.created_cache_ids.remove(result1.cache_id)
#             self.created_cache_ids.remove(result2.cache_id)
#
#     def test__large_binary_data(self):                                                    # Test with larger binary data
#         # Create 1MB of test data
#         large_data = b"x" * (1024 * 1024)
#
#         with self.cache_service as _:
#             # Store large data
#             result = _.store_binary(data=large_data)
#             self.created_cache_ids.append(result.cache_id)
#
#             assert result.size == len(large_data)
#
#             # Retrieve and verify size (not comparing full data for performance)
#             retrieved = _.retrieve_by_hash(cache_hash=result.hash)
#             assert len(retrieved.data) == len(large_data)
#             assert retrieved.data[:100] == large_data[:100]                              # Spot check beginning
#             assert retrieved.data[-100:] == large_data[-100:]                            # Spot check end
#
#     def test__requests_service_integration(self):                                         # Test that requests service is properly integrated
#         with self.cache_service as _:
#             # Verify requests service is used for all operations
#             assert _.requests_service is not None
#             assert type(_.requests_service) is MGraph__Service__Requests
#
#             # Test that auth headers would be passed through if configured
#             _.requests_service.auth_key_name  = Safe_Str("X-Test-Auth")
#             _.requests_service.auth_key_value = Safe_Str("test-key")
#             _.requests_service.setup()
#
#             # Make a request - auth headers should be included
#             test_data = b"auth header test"
#             result = _.store_binary(data=test_data)
#             self.created_cache_ids.append(result.cache_id)
#
#             # Verify the request succeeded (auth was properly passed)
#             assert result.cache_id is not None
#
#             # Verify retrieval also works with auth
#             retrieved = _.retrieve_by_id(cache_id=result.cache_id)
#             assert retrieved.data == test_data