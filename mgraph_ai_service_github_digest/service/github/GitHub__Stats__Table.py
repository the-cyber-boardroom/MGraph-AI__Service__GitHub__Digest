from typing                                                                                 import List, Dict
from osbot_utils.helpers.Print_Table                                                        import Print_Table
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats             import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats           import Schema__Folder__Stats


class GitHub__Stats__Table(Type_Safe):

    @type_safe
    def files_table(self, files : List[Schema__File__Stats] ,                               # Files to render
                          owner : str                       ,                               # Repo owner for title
                          name  : str                       ,                               # Repo name for title
                          ref   : str                                                       # Git ref for title
                    ) -> str:                                                               # Returns formatted table string

        table = Print_Table()
        table.set_title(f'Files by Size: {owner}/{name} ({ref})')
        table.set_headers(['#', 'Path', 'Size (bytes)', 'Size (KB)', 'Extension'])

        for idx, file in enumerate(files, 1):
            size_kb = f'{file.size_bytes / 1024:.1f}'
            table.add_row([str(idx)            ,
                           str(file.path)      ,
                           str(file.size_bytes),
                           size_kb             ,
                           str(file.extension) or '(none)'])

        total_size = sum(f.size_bytes for f in files)
        table.set_footer(f'Total: {len(files)} files | {total_size:,} bytes ({total_size/1024:.1f} KB)')

        table.map_texts()
        return '\n'.join(table.text__all)

    @type_safe
    def folders_table(self, folders : List[Schema__Folder__Stats] ,                         # Folders to render
                            owner   : str                         ,                         # Repo owner for title
                            name    : str                         ,                         # Repo name for title
                            ref     : str                         ,                         # Git ref for title
                            depth   : int                                                   # Folder depth for title
                      ) -> str:                                                             # Returns formatted table string

        table = Print_Table()
        table.set_title(f'Folders by Size (depth={depth}): {owner}/{name} ({ref})')
        table.set_headers(['#', 'Path', 'Size (bytes)', 'Size (KB)', 'Files', 'Direct Files', 'Subfolders'])

        for idx, folder in enumerate(folders, 1):
            size_kb = f'{folder.size_bytes / 1024:.1f}'
            table.add_row([str(idx)                     ,
                           str(folder.path)             ,
                           str(folder.size_bytes)       ,
                           size_kb                      ,
                           str(folder.file_count)       ,
                           str(folder.direct_file_count),
                           str(folder.subfolder_count)  ])

        total_size  = sum(f.size_bytes for f in folders)
        total_files = sum(f.file_count for f in folders)
        table.set_footer(f'Total: {len(folders)} folders | {total_size:,} bytes ({total_size/1024:.1f} KB) | {total_files} files')

        table.map_texts()
        return '\n'.join(table.text__all)

    @type_safe
    def extensions_table(self, breakdown : Dict[str, Dict[str, int]] ,                      # Extension breakdown data
                               owner     : str                       ,                      # Repo owner for title
                               name      : str                       ,                      # Repo name for title
                               ref       : str                       ,                      # Git ref for title
                               order     : str                       = 'size'               # 'size' or 'count'
                         ) -> str:                                                          # Returns formatted table string

        items = list(breakdown.items())
        if order == 'count':
            items.sort(key=lambda x: x[1]['count'], reverse=True)
        else:                                                                               # Default to size
            items.sort(key=lambda x: x[1]['total_bytes'], reverse=True)

        table = Print_Table()
        table.set_title(f'Extension Breakdown: {owner}/{name} ({ref})')
        table.set_headers(['#', 'Extension', 'Count', 'Total Size (bytes)', 'Total Size (KB)', 'Avg Size (bytes)'])

        for idx, (ext, data) in enumerate(items, 1):
            avg_size = data['total_bytes'] // data['count'] if data['count'] > 0 else 0
            size_kb  = f"{data['total_bytes'] / 1024:.1f}"
            table.add_row([str(idx)               ,
                           ext                    ,
                           str(data['count'])     ,
                           str(data['total_bytes']),
                           size_kb                ,
                           str(avg_size)          ])

        total_count = sum(d['count']       for d in breakdown.values())
        total_size  = sum(d['total_bytes'] for d in breakdown.values())
        table.set_footer(f'Total: {len(breakdown)} extensions | {total_count} files | {total_size:,} bytes ({total_size/1024:.1f} KB)')

        table.map_texts()
        return '\n'.join(table.text__all)