from typing                                                                              import Dict
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                                   import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                          import type_safe
from osbot_utils.utils.Http                                                              import url_join_safe
from osbot_utils.utils.Zip                                                               import zip_bytes__file_list, zip_bytes__files
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo         import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref    import Schema__GitHub__Repo__Ref
from mgraph_ai_service_github_digest.service.shared.Http__Requests                       import Http__Requests

SERVER__API_GITHUB_COM = "https://api.github.com"

# todo need to define a response schema for all these requests, so that we have a consistent way to return data to the caller
#      - it should contain: result, status, duration, cache_id (we might not need duration if that is already captured in the cache_id).
#      - should it be cache_ids? (since we could have more than one)

class GitHub__API(Type_Safe):
    http_request : Http__Requests

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
        zip_bytes           = repository_zip.get  ('content')
        repo_files_contents = zip_bytes__files    (zip_bytes)
        fixed_repo_files_contents = {}
        for file_name, file_contents in repo_files_contents.items():
            fixed_file_name = self.fix_repo_file_name(file_name)
            if fixed_file_name:
                fixed_repo_files_contents[fixed_file_name] = file_contents
        return fixed_repo_files_contents

    @type_safe
    def repository__contents__as_strings(self, repo_filter: Schema__GitHub__Repo__Filter) -> Dict:
        repo_files_contents = self.repository__contents__as_bytes(github_repo_ref=repo_filter)
        contents_as_strings = {}
        for file_path, file_contents in repo_files_contents.items():
            try:
                if self.path_matches_filter(path=file_path, repo_filter=repo_filter):
                    contents_as_strings[file_path] = file_contents.decode()                                                 # convert the file contents into a string
            except UnicodeDecodeError:
                pass                                                                                                    # todo: review if this is the best way to handle this situation, since the point of the method is to return strings
                #contents_as_strings[file_name] = f"ERROR: Failed to decode file: {error}"                              #        so it makes sense to not include the result in the response
        return contents_as_strings


    def path_matches_filter(self, path       : Safe_Str__File__Path         ,
                                  repo_filter: Schema__GitHub__Repo__Filter
                             ) -> bool:
        if repo_filter.filter_starts_with and not path.startswith(repo_filter.filter_starts_with):  return False
        if repo_filter.filter_ends_with   and not path.endswith  (repo_filter.filter_ends_with  ):  return False
        if repo_filter.filter_contains    and     repo_filter.filter_contains not in path        :  return False

        return True                                                                 # else we also have a match

    @type_safe
    def repository__zip(self, github_repo_ref: Schema__GitHub__Repo__Ref):
        path = self.path__repo_ref(github_repo_ref)
        return  self.http_request.get(path)

    def fix_repo_file_name(self, path: str) -> Safe_Str__File__Path:        #  Removes the first path segment from a repo file path.   Skips directories (paths ending with '/').
        if '/' not in path:
            return None                                                     # no slashes, can't strip root folder
        if path.endswith('/'):
            return None                                                     # it's a directory, skip
        fixed_path = path.partition('/')[2]                                 # get everything after first '/'
        return Safe_Str__File__Path(fixed_path)


    def fix_repo_files_names(self, repo_files_names: list[str]) -> list[str]:     # Processes a list of repo file paths: Strips the first directory (repo root folder),  Skips directories Returns a clean list of file paths
        fixed_files = []
        for path in repo_files_names:
            fixed_path = self.fix_repo_file_name(path)
            if fixed_path is not None:
                fixed_files.append(fixed_path)
        return sorted(fixed_files)