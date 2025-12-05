from typing                                                                                             import List, Dict
from osbot_fast_api.api.routes.Fast_API__Routes                                                         import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name           import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner          import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                           import Safe_Str__Git__Ref
from starlette.responses                                                                                import PlainTextResponse
from mgraph_ai_service_github_digest.config                                                             import GIT_HUB__API__DEFAULT__REPO_OWNER, GIT_HUB__API__DEFAULT__REPO_NAME, GIT_HUB__API__DEFAULT__REF
from mgraph_ai_service_github_digest.service.github.GitHub__Stats                                       import GitHub__Stats
from mgraph_ai_service_github_digest.service.github.GitHub__Stats__Table                                import GitHub__Stats__Table
from mgraph_ai_service_github_digest.service.github.GitHub__Stats__Tree                                 import GitHub__Stats__Tree
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref                   import Schema__GitHub__Repo__Ref

TAG__GITHUB_STATS = 'github-stats'

ROUTES_PATHS__GITHUB__STATS = [f'/{TAG__GITHUB_STATS}/repo-stats'                    ,
                               f'/{TAG__GITHUB_STATS}/files-by-size'                 ,
                               f'/{TAG__GITHUB_STATS}/files-by-size/view/table'      ,
                               f'/{TAG__GITHUB_STATS}/folders-by-size'               ,
                               f'/{TAG__GITHUB_STATS}/folders-by-size/view/table'    ,
                               f'/{TAG__GITHUB_STATS}/folders-by-size/view/tree'     ,
                               f'/{TAG__GITHUB_STATS}/extension-breakdown'           ,
                               f'/{TAG__GITHUB_STATS}/extension-breakdown/view/table',
                               f'/{TAG__GITHUB_STATS}/folder-tree'                   ]


class Routes__GitHub__Stats(Fast_API__Routes):
    tag                : str                  = TAG__GITHUB_STATS
    github_stats       : GitHub__Stats
    github_stats_table : GitHub__Stats__Table
    github_stats_tree  : GitHub__Stats__Tree

    def repo_stats(self, owner        : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                         name         : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                         ref          : str = GIT_HUB__API__DEFAULT__REF        ,
                         folder_depth : int = 2
                   ) -> dict:
        """Get comprehensive repository statistics including file and folder sizes."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        stats           = self.github_stats.repo_stats(github_repo_ref=github_repo_ref, folder_depth=folder_depth)
        return stats.json()

    def files_by_size(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                            name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                            ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                            order : str = 'desc'                            ,
                            limit : int = 50
                      ) -> List[dict]:
        """Get files sorted by size. Use order='desc' for largest first, 'asc' for smallest."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        files           = self.github_stats.files_by_size(github_repo_ref=github_repo_ref, order=order, limit=limit)
        return [f.json() for f in files]

    def files_by_size__view__table(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                                       name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                                       ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                                       order : str = 'desc'                            ,
                                       limit : int = 50
                                 ) -> PlainTextResponse:
        """Get files sorted by size as a formatted text table."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        files           = self.github_stats.files_by_size(github_repo_ref=github_repo_ref, order=order, limit=limit)
        text_output     = self.github_stats_table.files_table(files=files, owner=owner, name=name, ref=ref)
        return PlainTextResponse(text_output, media_type='text/plain')

    def folders_by_size(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                              name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                              ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                              depth : int = 1                                 ,
                              order : str = 'desc'                            ,
                              limit : int = 20
                        ) -> List[dict]:
        """Get folders at specified depth sorted by size."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        folders         = self.github_stats.folders_by_size(github_repo_ref=github_repo_ref, depth=depth, order=order, limit=limit)
        return [f.json() for f in folders]

    def folders_by_size__view__table(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                                         name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                                         ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                                         depth : int = 1                                 ,
                                         order : str = 'desc'                            ,
                                         limit : int = 20
                                   ) -> PlainTextResponse:
        """Get folders at specified depth as a formatted text table."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        folders         = self.github_stats.folders_by_size(github_repo_ref=github_repo_ref, depth=depth, order=order, limit=limit)
        text_output     = self.github_stats_table.folders_table(folders=folders, owner=owner, name=name, ref=ref, depth=depth)
        return PlainTextResponse(text_output, media_type='text/plain')

    def folders_by_size__view__tree(self, owner     : str  = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                                        name      : str  = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                                        ref       : str  = GIT_HUB__API__DEFAULT__REF        ,
                                        max_depth : int  = 3                                 ,
                                        show_size : bool = True
                                  ) -> PlainTextResponse:
        """Get folder structure as an ASCII tree with sizes."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        stats           = self.github_stats.repo_stats(github_repo_ref=github_repo_ref, folder_depth=max_depth)
        text_output     = self.github_stats_tree.folder_tree(stats=stats, owner=owner, name=name, ref=ref, max_depth=max_depth, show_size=show_size)
        return PlainTextResponse(text_output, media_type='text/plain')

    def extension_breakdown(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                                  name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                                  ref   : str = GIT_HUB__API__DEFAULT__REF
                            ) -> Dict[str, Dict[str, int]]:
        """Get file count and total size grouped by extension."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        return self.github_stats.extension_breakdown(github_repo_ref=github_repo_ref)

    def extension_breakdown__view__table(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                                             name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                                             ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                                             order : str = 'size'
                                       ) -> PlainTextResponse:
        """Get extension breakdown as a formatted text table."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        breakdown       = self.github_stats.extension_breakdown(github_repo_ref=github_repo_ref)
        text_output     = self.github_stats_table.extensions_table(breakdown=breakdown, owner=owner, name=name, ref=ref, order=order)
        return PlainTextResponse(text_output, media_type='text/plain')

    def folder_tree(self, owner     : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                          name      : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                          ref       : str = GIT_HUB__API__DEFAULT__REF        ,
                          max_depth : int = 3
                    ) -> dict:
        """Get a nested tree structure of folders with sizes."""
        github_repo_ref = self._create_repo_ref(owner, name, ref)
        return self.github_stats.folder_tree(github_repo_ref=github_repo_ref, max_depth=max_depth)

    def _create_repo_ref(self, owner: str, name: str, ref: str) -> Schema__GitHub__Repo__Ref:
        """Helper to create repo ref schema."""
        return Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                         name  = Safe_Str__GitHub__Repo_Name (name ),
                                         ref   = Safe_Str__Git__Ref          (ref  ))

    def setup_routes(self):
        self.add_route_get(self.repo_stats                    )
        self.add_route_get(self.files_by_size                 )
        self.add_route_get(self.files_by_size__view__table    )
        self.add_route_get(self.folders_by_size               )
        self.add_route_get(self.folders_by_size__view__table    )
        self.add_route_get(self.folders_by_size__view__tree     )
        self.add_route_get(self.extension_breakdown           )
        self.add_route_get(self.extension_breakdown__view__table)
        self.add_route_get(self.folder_tree                   )