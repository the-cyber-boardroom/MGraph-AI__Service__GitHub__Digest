from typing                                                                                 import List
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Repo__Stats             import Schema__Repo__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats           import Schema__Folder__Stats


TREE_CHAR_BRANCH     = '├── '
TREE_CHAR_LAST       = '└── '
TREE_CHAR_VERTICAL   = '│   '
TREE_CHAR_SPACE      = '    '
TREE_ICON_FOLDER     = '📁'


class GitHub__Stats__Tree(Type_Safe):

    @type_safe
    def format_size(self, size_bytes: Safe_UInt) -> str:                                          # Format bytes to human readable
        if size_bytes >= 1024 * 1024:
            return f'{size_bytes / (1024*1024):.1f} MB'
        elif size_bytes >= 1024:
            return f'{size_bytes / 1024:.1f} KB'
        else:
            return f'{size_bytes} B'

    @type_safe
    def folder_tree(self, stats     : Schema__Repo__Stats ,                                 # Repository stats
                          owner     : str                 ,                                 # Repo owner for header
                          name      : str                 ,                                 # Repo name for header
                          ref       : str                 ,                                 # Git ref for header
                          max_depth : int                 ,                                 # Maximum depth to render
                          show_size : bool                = True                            # Show size info
                    ) -> str:                                                               # Returns formatted tree string

        lines = []
        lines.append(f'{TREE_ICON_FOLDER} {owner}/{name} ({ref})')
        lines.append(f'   Total: {stats.total_size_bytes:,} bytes ({stats.total_size_bytes/1024:.1f} KB) | {stats.total_files} files')
        lines.append('')

        folder_data = {}                                                                    # Build folder lookup
        for folder in stats.folders:
            folder_data[str(folder.path)] = folder

        root_folders = sorted([f for f in stats.folders if f.depth == 0],
                              key=lambda x: str(x.path))

        for i, folder in enumerate(root_folders):                                           # Render from root folders
            is_last = (i == len(root_folders) - 1)
            self._render_folder(folder_path   = str(folder.path)                         ,
                                folder_data   = folder_data                              ,
                                all_folders   = stats.folders                            ,
                                lines         = lines                                    ,
                                prefix        = ''                                       ,
                                is_last       = is_last                                  ,
                                current_depth = 0                                        ,
                                max_depth     = max_depth                                ,
                                show_size     = show_size                                )

        return '\n'.join(lines)

    def _render_folder(self, folder_path   : str                        ,                   # Current folder path
                             folder_data   : dict                       ,                   # Folder lookup dict
                             all_folders   : List[Schema__Folder__Stats],                   # All folders
                             lines         : List[str]                  ,                   # Output lines
                             prefix        : str                        ,                   # Current prefix
                             is_last       : bool                       ,                   # Is last sibling
                             current_depth : int                        ,                   # Current depth
                             max_depth     : int                        ,                   # Max depth to render
                             show_size     : bool                                           # Show size info
                       ) -> None:

        if current_depth > max_depth:
            return

        folder = folder_data.get(folder_path)
        if not folder:
            return

        connector   = TREE_CHAR_LAST if is_last else TREE_CHAR_BRANCH
        folder_name = folder_path.split('/')[-1] if '/' in folder_path else folder_path

        if show_size:
            size_str  = self.format_size(folder.size_bytes)
            file_info = f'{folder.file_count} files'
            line      = f'{prefix}{connector}{TREE_ICON_FOLDER} {folder_name} ({size_str}, {file_info})'
        else:
            line      = f'{prefix}{connector}{TREE_ICON_FOLDER} {folder_name}'

        lines.append(line)

        children = sorted([f for f in all_folders                                           # Find children
                           if str(f.path).startswith(folder_path + '/') and
                              f.depth == current_depth + 1],
                          key=lambda x: str(x.path))

        child_prefix = prefix + (TREE_CHAR_SPACE if is_last else TREE_CHAR_VERTICAL)

        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self._render_folder(folder_path   = str(child.path)                          ,
                                folder_data   = folder_data                              ,
                                all_folders   = all_folders                              ,
                                lines         = lines                                    ,
                                prefix        = child_prefix                             ,
                                is_last       = is_last_child                            ,
                                current_depth = current_depth + 1                        ,
                                max_depth     = max_depth                                ,
                                show_size     = show_size                                )

    @type_safe
    def folder_tree_simple(self, folders   : List[Schema__Folder__Stats] ,                  # Folders to render
                                 owner     : str                         ,                  # Repo owner for header
                                 name      : str                         ,                  # Repo name for header
                                 ref       : str                         ,                  # Git ref for header
                                 show_size : bool                        = True             # Show size info
                           ) -> str:                                                        # Returns formatted tree string
        """Simplified tree rendering without full stats context."""

        lines = []
        lines.append(f'{TREE_ICON_FOLDER} {owner}/{name} ({ref})')
        lines.append('')

        folder_data = {}
        for folder in folders:
            folder_data[str(folder.path)] = folder

        max_depth = max((f.depth for f in folders), default=0)

        root_folders = sorted([f for f in folders if f.depth == 0],
                              key=lambda x: str(x.path))

        for i, folder in enumerate(root_folders):
            is_last = (i == len(root_folders) - 1)
            self._render_folder(folder_path   = str(folder.path)                         ,
                                folder_data   = folder_data                              ,
                                all_folders   = folders                                  ,
                                lines         = lines                                    ,
                                prefix        = ''                                       ,
                                is_last       = is_last                                  ,
                                current_depth = 0                                        ,
                                max_depth     = max_depth                                ,
                                show_size     = show_size                                )

        return '\n'.join(lines)