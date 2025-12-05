from starlette.responses                                                                    import PlainTextResponse
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from mgraph_ai_service_github_digest.config                                                 import GIT_HUB__API__DEFAULT__REPO_OWNER, GIT_HUB__API__DEFAULT__REPO_NAME, GIT_HUB__API__DEFAULT__REF, GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH
from mgraph_ai_service_github_digest.service.github.GitHub__Digest                          import GitHub__Digest
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Filter    import Schema__GitHub__Repo__Filter

TAG__GIT_HUB__DIGEST = 'github-digest'
ROUTES_PATHS__GIT_HUB__DIGEST = [f'/{TAG__GIT_HUB__DIGEST}/markdown',
                                 f'/{TAG__GIT_HUB__DIGEST}/markdown/filter']


class Routes__GitHub__Digest(Fast_API__Routes):
    tag          = TAG__GIT_HUB__DIGEST
    github_digest: GitHub__Digest


    def markdown(self, owner              : str = GIT_HUB__API__DEFAULT__REPO_OWNER        ,
                       name               : str = GIT_HUB__API__DEFAULT__REPO_NAME         ,
                       ref                : str = GIT_HUB__API__DEFAULT__REF               ,
                       filter_starts_with : str = GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH,
                       filter_contains    : str = '',
                       filter_ends_with   : str = ''):
        repo_filter = Schema__GitHub__Repo__Filter(owner              = owner              ,
                                                   name               = name               ,
                                                   ref                = ref                ,
                                                   filter_starts_with = filter_starts_with ,
                                                   filter_contains    = filter_contains    ,
                                                   filter_ends_with   = filter_ends_with   )
        markdown = self.github_digest.repo_files__in_markdown(repo_filter=repo_filter)
        return PlainTextResponse(markdown, media_type="text/markdown")

    def markdown__filter(self, repo_filter        : Schema__GitHub__Repo__Filter):
        markdown = self.github_digest.repo_files__in_markdown(repo_filter=repo_filter)
        return PlainTextResponse(markdown, media_type="text/markdown")

    def setup_routes(self):
        self.add_route_get (self.markdown        )
        self.add_route_post(self.markdown__filter)