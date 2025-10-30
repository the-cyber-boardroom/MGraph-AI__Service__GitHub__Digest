import hashlib
from typing                                                                              import Dict, Optional
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path        import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                           import type_safe
from osbot_utils.utils.Http                                                              import url_join_safe
from osbot_utils.utils.Json                                                              import json_to_str
from osbot_utils.utils.Zip                                                               import zip_bytes__file_list, zip_bytes__files
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo         import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref    import Schema__GitHub__Repo__Ref
from mgraph_ai_service_github_digest.service.shared.Http__Requests                       import Http__Requests
#from mgraph_ai_service_github_digest.service.cache.MGraph__Service__Cache                import MGraph__Service__Cache, Safe_Str__Cache_Hash

SERVER__API_GITHUB_COM = "https://api.github.com"

# todo need to define a response schema for all these requests, so that we have a consistent way to return data to the caller
#      - it should contain: result, status, duration, cache_id (we might not need duration if that is already captured in the cache_id).
#      - should it be cache_ids? (since we could have more than one)

class GitHub__API(Type_Safe):
    http_request  : Http__Requests                                                         # HTTP client for GitHub API
    #cache_service : MGraph__Service__Cache                                                 # Cache service client
    cache_enabled : bool                      = False                                       # Enable/disable caching

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.http_request.base_url = SERVER__API_GITHUB_COM

    def apis_available(self):
        return self.http_request.get('/')

    def rate_limit(self):
        return self.http_request.get('/rate_limit')

    @type_safe
    def commits(self, github_repo: Schema__GitHub__Repo):
        path = f'{self.path__repo(github_repo)}/commits'
        return self.http_request.get(path)

    @type_safe
    def issues(self, github_repo: Schema__GitHub__Repo):
        path = f'{self.path__repo(github_repo)}/issues'
        return self.http_request.get(path)

    def path__repo(self, github_repo: Schema__GitHub__Repo):
        return f'/repos/{github_repo.owner}/{github_repo.name}'

    def path__repo_ref(self, github_repo_ref: Schema__GitHub__Repo__Ref):
        repo_path = self.path__repo(github_repo_ref)
        ref       = github_repo_ref.ref
        path      = url_join_safe(f'{repo_path}/zipball/', ref)
        return path

    @type_safe
    def repository(self, github_repo: Schema__GitHub__Repo):
        return self.http_request.get(self.path__repo(github_repo))

    @type_safe
    def repository__files__names(self, github_repo_ref: Schema__GitHub__Repo__Ref):
        repository_zip         = self.repository__zip(github_repo_ref)
        zip_bytes              = repository_zip.get  ('content')
        repo_files_names       = zip_bytes__file_list(zip_bytes)
        fixed_repo_files_names = self.fix_repo_files_names(repo_files_names)

        return fixed_repo_files_names

    @type_safe
    def repository__contents__as_bytes(self, github_repo_ref: Schema__GitHub__Repo__Ref):
        repository_zip      = self.repository__zip(github_repo_ref=github_repo_ref)
        repo_zip_content    = repository_zip.get  ('content')
        if type(repo_zip_content) is bytes:
            fixed_repo_files_contents = {}
            repo_files_contents = zip_bytes__files(repo_zip_content)

            for file_name, file_contents in repo_files_contents.items():
                fixed_file_name = self.fix_repo_file_name(file_name)
                if fixed_file_name:
                    fixed_repo_files_contents[fixed_file_name] = file_contents
        else:
            error_message = dict(response__github_api     = repo_zip_content,
                                 request__github_repo_ref = github_repo_ref.json())
            fixed_repo_files_contents = {'__error__': json_to_str(error_message)}
        return fixed_repo_files_contents

    @type_safe
    def repository__contents__as_strings(self, repo_filter: Schema__GitHub__Repo__Filter) -> Dict:
        repo_files_contents = self.repository__contents__as_bytes(github_repo_ref=repo_filter)
        contents_as_strings = {}
        if len(repo_files_contents) == 1 and repo_files_contents.get('__error__'):
            return repo_files_contents
        else:
            for file_path, file_contents in repo_files_contents.items():
                try:
                    if self.path_matches_filter(path=file_path, repo_filter=repo_filter):
                        contents_as_strings[file_path] = file_contents.decode()
                except UnicodeDecodeError:
                    pass
            return contents_as_strings

    def path_matches_filter(self, path       : Safe_Str__File__Path         ,
                                  repo_filter: Schema__GitHub__Repo__Filter
                             ) -> bool:
        if repo_filter.filter_starts_with and not path.startswith(repo_filter.filter_starts_with):  return False
        if repo_filter.filter_ends_with   and not path.endswith  (repo_filter.filter_ends_with  ):  return False
        if repo_filter.filter_contains    and     repo_filter.filter_contains not in path        :  return False

        return True

    @type_safe
    def repository__zip(self, github_repo_ref : Schema__GitHub__Repo__Ref  ,                # Repository reference
                             force_refresh    : bool                       = False          # Force cache update
                        ) -> dict:                                                           # Returns zip content and metadata

        if not self.cache_enabled:                                                          # Skip cache if disabled
            return self._fetch_repository_zip_from_github(github_repo_ref)

        raise Exception("Cache Support is currently not supported")
        # # Generate cache key from repository details
        # cache_key = self._generate_cache_key(github_repo_ref)
        # cache_hash = self._generate_cache_hash(cache_key)
        #
        # # Try to retrieve from cache first
        # cached_response = self.cache_service.retrieve_by_hash(cache_hash=cache_hash)
        #
        # if cached_response and not force_refresh:                                           # Cache hit and not forcing refresh
        #     return dict(content      = cached_response.data                         ,
        #                headers      = {'X-Cache-Hit'  : 'true'                     ,
        #                               'X-Cached-At'   : cached_response.cached_at  ,
        #                               'X-Cache-Id'    : cached_response.cache_id   },
        #                duration     = 0.001                                         ,       # Minimal duration for cache hit
        #                cache_hit    = True                                          )
        #
        # # Cache miss or force refresh - fetch from GitHub
        # github_response = self._fetch_repository_zip_from_github(github_repo_ref)
        #
        # # Store in cache for future use
        # try:
        #     store_response = self.cache_service.store_binary(
        #         data          = github_response.get('content')     ,
        #         force_refresh = force_refresh                      )
        #
        #     # Add cache metadata to response
        #     github_response['headers']['X-Cache-Hit'] = 'false'
        #     github_response['headers']['X-Cache-Id']  = store_response.cache_id
        #     github_response['cache_hit']              = False
        #
        # except Exception as e:                                                              # Cache store failed, but continue
        #     # Log error but don't fail the request
        #     github_response['headers']['X-Cache-Error'] = str(e)
        #     github_response['cache_hit']                = False
        #
        # return github_response

    def _fetch_repository_zip_from_github(self, github_repo_ref: Schema__GitHub__Repo__Ref  # Repository to fetch
                                          ) -> dict:                                         # Returns GitHub response
        path = self.path__repo_ref(github_repo_ref)
        return self.http_request.get(path)

    def _generate_cache_key(self, github_repo_ref: Schema__GitHub__Repo__Ref                # Repository reference
                            ) -> str:                                                        # Returns cache key string
        # Create deterministic cache key
        cache_key = f"github:repo:{github_repo_ref.owner}:{github_repo_ref.name}:{github_repo_ref.ref}"
        return cache_key

    # def _generate_cache_hash(self, cache_key: str                                           # Cache key string
    #                          ) -> Safe_Str__Cache_Hash:                                     # Returns 16-char hash
    #     # Generate 16-character hash from cache key
    #     hash_object = hashlib.sha256(cache_key.encode())
    #     hash_hex    = hash_object.hexdigest()[:16]                                          # Take first 16 chars
    #     return Safe_Str__Cache_Hash(hash_hex)

    @type_safe
    def repository__zip__force_refresh(self, github_repo_ref: Schema__GitHub__Repo__Ref     # Repository to refresh
                                        ) -> dict:                                           # Returns fresh zip content
        # Convenience method to force cache refresh
        return self.repository__zip(github_repo_ref=github_repo_ref, force_refresh=True)

    def fix_repo_file_name(self, path: str) -> Safe_Str__File__Path:
        if '/' not in path:
            return None
        if path.endswith('/'):
            return None
        fixed_path = path.partition('/')[2]
        return Safe_Str__File__Path(fixed_path)

    def fix_repo_files_names(self, repo_files_names: list[str]) -> list[str]:
        fixed_files = []
        for path in repo_files_names:
            fixed_path = self.fix_repo_file_name(path)
            if fixed_path is not None:
                fixed_files.append(fixed_path)
        return sorted(fixed_files)