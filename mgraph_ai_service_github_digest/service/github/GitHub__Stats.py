from collections                                                                            import defaultdict
from typing                                                                                 import Dict, List, Optional
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path           import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_github_digest.service.github.GitHub__API                             import GitHub__API
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref       import Schema__GitHub__Repo__Ref
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats             import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats           import Schema__Folder__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Repo__Stats             import Schema__Repo__Stats


class GitHub__Stats(Type_Safe):
    github_api: GitHub__API

    @type_safe
    def repo_stats(self, github_repo_ref : Schema__GitHub__Repo__Ref   ,            # Repository to analyze
                         folder_depth    : int                         = 2          # Depth for folder stats (0=root only)
                   ) -> Schema__Repo__Stats:                                        # Returns complete stats

        repo_contents = self.github_api.repository__contents__as_bytes(github_repo_ref=github_repo_ref)

        if repo_contents.get('__error__'):                                          # Handle error case
            return Schema__Repo__Stats(owner = github_repo_ref.owner ,
                                       name  = github_repo_ref.name  ,
                                       ref   = github_repo_ref.ref   )

        file_stats_list   = []
        folder_sizes      = defaultdict(lambda: {'size': 0, 'file_count': 0, 'direct_files': 0, 'extensions': set()})
        extensions_data   = defaultdict(lambda: {'count': 0, 'total_bytes': 0})
        max_depth         = 0

        for file_path, file_bytes in repo_contents.items():
            file_path_str = str(file_path)
            file_size     = len(file_bytes)

            file_stats = self._create_file_stats(file_path_str, file_size)          # Create file stats
            file_stats_list.append(file_stats)

            ext = str(file_stats.extension) if file_stats.extension else '(none)'   # Track extension stats
            extensions_data[ext]['count']       += 1
            extensions_data[ext]['total_bytes'] += file_size

            depth = self._update_folder_stats(file_path_str  ,                      # Update folder aggregations
                                              file_size      ,
                                              folder_sizes   ,
                                              str(file_stats.extension))
            max_depth = max(max_depth, depth)

        folder_stats_list = self._build_folder_stats(folder_sizes, folder_depth)    # Build folder stats at requested depth

        total_size = sum(len(b) for b in repo_contents.values())

        return Schema__Repo__Stats(owner              = github_repo_ref.owner                                         ,
                                   name               = github_repo_ref.name                                          ,
                                   ref                = github_repo_ref.ref                                           ,
                                   total_files        = Safe_UInt(len(file_stats_list))                               ,
                                   total_size_bytes   = Safe_UInt(total_size)                                         ,
                                   total_folders      = Safe_UInt(len([f for f in folder_sizes if f]))                ,
                                   files              = file_stats_list                                               ,
                                   folders            = folder_stats_list                                             ,
                                   extensions_summary = dict(extensions_data)                                         ,
                                   max_depth          = Safe_UInt(max_depth)                                          ,
                                   requested_depth    = Safe_UInt(folder_depth)                                       )

    def _create_file_stats(self, file_path: str, file_size: int) -> Schema__File__Stats:
        parts     = file_path.rsplit('/', 1)
        folder    = parts[0] if len(parts) > 1 else ''
        file_name = parts[-1]

        ext_parts = file_name.rsplit('.', 1)
        extension = f'.{ext_parts[-1]}' if len(ext_parts) > 1 and ext_parts[0] else ''

        return Schema__File__Stats(path       = Safe_Str__File__Path(file_path) ,
                                   name       = Safe_Str__File__Path(file_name) ,
                                   extension  = Safe_Str__File__Path(extension) ,
                                   size_bytes = Safe_UInt(file_size)            ,
                                   folder     = Safe_Str__File__Path(folder)    )

    def _update_folder_stats(self, file_path    : str                                    ,
                                   file_size    : int                                    ,
                                   folder_sizes : Dict                                   ,
                                   extension    : str
                             ) -> int:                                                    # Returns depth
        parts = file_path.split('/')
        depth = len(parts) - 1                                                            # Depth is number of folders

        current_path = ''                                                                 # Update all parent folders
        for i, part in enumerate(parts[:-1]):                                             # Exclude file name
            current_path = f'{current_path}/{part}' if current_path else part
            folder_sizes[current_path]['size']       += file_size
            folder_sizes[current_path]['file_count'] += 1
            folder_sizes[current_path]['extensions'].add(extension)

            if i == len(parts) - 2:                                                       # Direct parent
                folder_sizes[current_path]['direct_files'] += 1

        return depth

    def _build_folder_stats(self, folder_sizes : Dict ,
                                  max_depth    : int
                            ) -> List[Schema__Folder__Stats]:

        folder_stats   = []
        subfolder_count = defaultdict(int)

        for folder_path in folder_sizes.keys():                                           # Count subfolders for each folder
            parts = folder_path.split('/')
            if len(parts) > 1:
                parent = '/'.join(parts[:-1])
                subfolder_count[parent] += 1

        for folder_path, stats in folder_sizes.items():
            depth = folder_path.count('/')

            if depth <= max_depth:
                folder_stat = Schema__Folder__Stats(
                    path              = Safe_Str__File__Path(folder_path)                ,
                    depth             = Safe_UInt(depth)                                 ,
                    size_bytes        = Safe_UInt(stats['size'])                         ,
                    file_count        = Safe_UInt(stats['file_count'])                   ,
                    direct_file_count = Safe_UInt(stats['direct_files'])                 ,
                    subfolder_count   = Safe_UInt(subfolder_count.get(folder_path, 0))   ,
                    extensions        = list(stats['extensions'])                        )
                folder_stats.append(folder_stat)

        folder_stats.sort(key=lambda x: (x.depth, str(x.path)))                           # Sort by depth, then path

        return folder_stats

    @type_safe
    def files_by_size(self, github_repo_ref : Schema__GitHub__Repo__Ref   ,               # Repository to analyze
                            order           : str                         = 'desc' ,      # 'asc' or 'desc'
                            limit           : int                         = 50            # Max files to return
                      ) -> List[Schema__File__Stats]:                                     # Returns sorted file list

        stats = self.repo_stats(github_repo_ref=github_repo_ref, folder_depth=0)
        files = stats.files

        reverse = order.lower() == 'desc'
        sorted_files = sorted(files, key=lambda f: f.size_bytes, reverse=reverse)

        return sorted_files[:limit] if limit > 0 else sorted_files

    @type_safe
    def folders_by_size(self, github_repo_ref : Schema__GitHub__Repo__Ref   ,             # Repository to analyze
                              depth           : int                         = 1    ,      # Folder depth to analyze
                              order           : str                         = 'desc',     # 'asc' or 'desc'
                              limit           : int                         = 20          # Max folders to return
                        ) -> List[Schema__Folder__Stats]:                                 # Returns sorted folder list

        stats   = self.repo_stats(github_repo_ref=github_repo_ref, folder_depth=depth)
        folders = [f for f in stats.folders if f.depth == depth]

        reverse = order.lower() == 'desc'
        sorted_folders = sorted(folders, key=lambda f: f.size_bytes, reverse=reverse)

        return sorted_folders[:limit] if limit > 0 else sorted_folders

    @type_safe
    def extension_breakdown(self, github_repo_ref: Schema__GitHub__Repo__Ref              # Repository to analyze
                            ) -> Dict[str, Dict[str, int]]:                               # Returns extension -> {count, total_bytes}
        stats = self.repo_stats(github_repo_ref=github_repo_ref, folder_depth=0)
        return stats.extensions_summary

    @type_safe
    def folder_tree(self, github_repo_ref : Schema__GitHub__Repo__Ref   ,                 # Repository to analyze
                          max_depth       : int                         = 3               # Max depth to show
                    ) -> Dict:                                                            # Returns nested folder structure

        stats = self.repo_stats(github_repo_ref=github_repo_ref, folder_depth=max_depth)

        tree = {'name': '/', 'size_bytes': stats.total_size_bytes, 'file_count': stats.total_files, 'children': {}}

        for folder in stats.folders:
            parts        = str(folder.path).split('/')
            current_node = tree['children']

            for i, part in enumerate(parts):
                if part not in current_node:
                    current_node[part] = {'name'      : part                          ,
                                          'path'      : '/'.join(parts[:i+1])         ,
                                          'children'  : {}                            }

                if i == len(parts) - 1:                                                   # Leaf folder
                    current_node[part]['size_bytes']        = folder.size_bytes
                    current_node[part]['file_count']        = folder.file_count
                    current_node[part]['direct_file_count'] = folder.direct_file_count
                    current_node[part]['subfolder_count']   = folder.subfolder_count

                current_node = current_node[part]['children']

        return tree