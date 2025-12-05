from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Misc                                                              import date_time_now
from mgraph_ai_service_github_digest.service.github.GitHub__API                          import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter import Schema__GitHub__Repo__Filter

class GitHub__Digest(Type_Safe):
    github_api : GitHub__API

    def repo_files__in_markdown(self, repo_filter: Schema__GitHub__Repo__Filter):
        files_in_repo = self.github_api.repository__contents__as_strings(repo_filter=repo_filter)
        with repo_filter as _:
            # Build exclusions section
            exclusions = []
            if _.filter_exclude_paths:
                exclusions.append(f"   - exclude_paths   : {', '.join(_.filter_exclude_paths)}")
            if _.filter_exclude_prefixes:
                exclusions.append(f"   - exclude_prefixes: {', '.join(_.filter_exclude_prefixes)}")
            if _.filter_exclude_suffixes:
                exclusions.append(f"   - exclude_suffixes: {', '.join(_.filter_exclude_suffixes)}")
            exclusions_str = '\n'.join(exclusions) if exclusions else '   (none)'

            # Build size controls section
            size_controls = []
            if _.max_file_size_bytes:
                size_controls.append(f"   - max_file_size  : {_.max_file_size_bytes:,} bytes")
            if _.max_content_length:
                patterns = ', '.join(_.truncate_patterns) if _.truncate_patterns else 'all files'
                size_controls.append(f"   - max_content    : {_.max_content_length:,} chars (applies to: {patterns})")

            size_str = '\n'.join(size_controls) if size_controls else '   (none)'

            markdown__before = f"""# Files from Repo
     
     - owner: {_.owner}
     - name: {_.name} 
     - ref: {_.ref}
    
    created at: {date_time_now()}"""

            markdown__after = f"""
    
    ## Filtered by:
     - starts_with    : {_.filter_starts_with or '(any)'}
     - contains       : {_.filter_contains or '(any)'}
     - ends_with      : {_.filter_ends_with or '(any)'}
     - starts_with_any: {', '.join(_.filter_starts_with_any) if _.filter_starts_with_any else '(not set)'}
    
    ## Exclusions:
    {exclusions_str}
    
    ## Size Controls:
    {size_str}
     
    ## Files:
    
    Showing {len(files_in_repo)} files that matched the filter(s) 
    
    """
        markdown__files = ""
        for file_path, file_contents in files_in_repo.items():
            if repo_filter.hide_file_contents:
                markdown__file = f"""
        - {file_path}"""
            else:
                markdown__file = f"""
    ### {file_path}
    
    {file_contents} 
    ---
    """
            markdown__files += markdown__file

        markdown_content = markdown__before + markdown__files + markdown__after
        text_size        = self.calculate_text_size  (markdown_content)
        text_tokens      = self.calculate_text_tokens(markdown_content)

        markdown__stats = f"""
        
## Output Stats:

   - text_size  : {text_size["formatted"]} ({text_size["bytes"]:,} bytes)')
   - text_tokens: ~{text_tokens:,} (estimated)')   
        """
        markdown = (markdown__before +
                    markdown__stats  +
                    markdown__after  +
                    markdown__files  )
        return markdown



    def calculate_text_size(self, text: str) -> dict:
        size_bytes = len(text.encode('utf-8'))
        if size_bytes >= 1024 * 1024:
            size_str = f'{size_bytes / (1024*1024):.1f} MB'
        elif size_bytes >= 1024:
            size_str = f'{size_bytes / 1024:.1f} KB'
        else:
            size_str = f'{size_bytes} B'
        return {'bytes': size_bytes, 'formatted': size_str}

    def calculate_text_tokens(self, text: str) -> int:
        # Simple approximation: ~4 chars per token (good enough for most uses)
        return len(text) // 5
