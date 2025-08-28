from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Misc                                                              import date_time_now
from mgraph_ai_service_github_digest.service.github.GitHub__API                          import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter

class GitHub__Digest(Type_Safe):
    github_api : GitHub__API

    def repo_files__in_markdown(self, repo_filter: Schema__GitHub__Repo__Filter):
        files_in_repo = self.github_api.repository__contents__as_strings(repo_filter=repo_filter)
        with repo_filter as _:
            markdown = f"""
# Files from Repo
 
 - owner: {_.owner}
 - name: {_.name} 
 - ref: {_.ref}"

created at: { date_time_now()}

## Filtered by:
 - starts_with: {_.filter_starts_with}
 - contains   : {_.filter_contains}
 - ends_with  : {_.filter_ends_with}
 
 
## Files:

Showing {len(files_in_repo)} files that matched the filter(s) 

"""
        for file_path, file_contents in files_in_repo.items():
            markdown__file = f"""
### {file_path}

{file_contents}
---
"""
            markdown += markdown__file
        return markdown