from typing                                                                                             import List, Dict
from osbot_fast_api.api.routes.Fast_API__Routes                                                         import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name           import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner          import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                           import Safe_Str__Git__Ref
from mgraph_ai_service_github_digest.config                                                             import GIT_HUB__API__DEFAULT__REPO_OWNER, GIT_HUB__API__DEFAULT__REPO_NAME, GIT_HUB__API__DEFAULT__REF
from mgraph_ai_service_github_digest.service.github.GitHub__Stats                                       import GitHub__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref                   import Schema__GitHub__Repo__Ref

TAG__GITHUB_STATS = 'github-stats'

ROUTES_PATHS__GITHUB__STATS = [f'/{TAG__GITHUB_STATS}/repo-stats'          ,
                               f'/{TAG__GITHUB_STATS}/files-by-size'       ,
                               f'/{TAG__GITHUB_STATS}/folders-by-size'     ,
                               f'/{TAG__GITHUB_STATS}/extension-breakdown' ,
                               f'/{TAG__GITHUB_STATS}/folder-tree'         ]


class Routes__GitHub__Stats(Fast_API__Routes):
    tag          : str           = TAG__GITHUB_STATS
    github_stats : GitHub__Stats

    def repo_stats(self, owner        : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                         name         : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                         ref          : str = GIT_HUB__API__DEFAULT__REF        ,
                         folder_depth : int = 2
                   ) -> dict:
        """Get comprehensive repository statistics including file and folder sizes."""
        github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                    name  = Safe_Str__GitHub__Repo_Name (name ),
                                                    ref   = Safe_Str__Git__Ref          (ref  ))

        stats = self.github_stats.repo_stats(github_repo_ref=github_repo_ref ,
                                             folder_depth   =folder_depth    )
        return stats.json()

    def files_by_size(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                            name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                            ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                            order : str = 'desc'                            ,
                            limit : int = 50
                      ) -> List[dict]:
        """Get files sorted by size. Use order='desc' for largest first, 'asc' for smallest."""
        github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                    name  = Safe_Str__GitHub__Repo_Name (name ),
                                                    ref   = Safe_Str__Git__Ref          (ref  ))

        files = self.github_stats.files_by_size(github_repo_ref = github_repo_ref ,
                                                order           = order           ,
                                                limit           = limit           )
        return [f.json() for f in files]

    def folders_by_size(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                              name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                              ref   : str = GIT_HUB__API__DEFAULT__REF        ,
                              depth : int = 1                                 ,
                              order : str = 'desc'                            ,
                              limit : int = 20
                        ) -> List[dict]:
        """Get folders at specified depth sorted by size."""
        github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                    name  = Safe_Str__GitHub__Repo_Name (name ),
                                                    ref   = Safe_Str__Git__Ref          (ref  ))

        folders = self.github_stats.folders_by_size(github_repo_ref = github_repo_ref ,
                                                    depth           = depth           ,
                                                    order           = order           ,
                                                    limit           = limit           )
        return [f.json() for f in folders]

    def extension_breakdown(self, owner : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                                  name  : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                                  ref   : str = GIT_HUB__API__DEFAULT__REF
                            ) -> Dict[str, Dict[str, int]]:
        """Get file count and total size grouped by extension."""
        github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                    name  = Safe_Str__GitHub__Repo_Name (name ),
                                                    ref   = Safe_Str__Git__Ref          (ref  ))

        return self.github_stats.extension_breakdown(github_repo_ref=github_repo_ref)

    def folder_tree(self, owner     : str = GIT_HUB__API__DEFAULT__REPO_OWNER ,
                          name      : str = GIT_HUB__API__DEFAULT__REPO_NAME  ,
                          ref       : str = GIT_HUB__API__DEFAULT__REF        ,
                          max_depth : int = 3
                    ) -> dict:
        """Get a nested tree structure of folders with sizes."""
        github_repo_ref = Schema__GitHub__Repo__Ref(owner = Safe_Str__GitHub__Repo_Owner(owner),
                                                    name  = Safe_Str__GitHub__Repo_Name (name ),
                                                    ref   = Safe_Str__Git__Ref          (ref  ))

        return self.github_stats.folder_tree(github_repo_ref = github_repo_ref ,
                                             max_depth       = max_depth       )

    def setup_routes(self):
        self.add_route_get(self.repo_stats         )
        self.add_route_get(self.files_by_size      )
        self.add_route_get(self.folders_by_size    )
        self.add_route_get(self.extension_breakdown)
        self.add_route_get(self.folder_tree        )