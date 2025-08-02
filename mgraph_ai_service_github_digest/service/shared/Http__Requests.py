import requests
from typing                                                   import Dict
from osbot_utils.helpers.duration.decorators.capture_duration import capture_duration
from osbot_utils.helpers.safe_str.Safe_Str__Url               import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                          import Type_Safe
from osbot_utils.utils.Http                                   import url_join_safe


class Http__Requests(Type_Safe):
    base_url : Safe_Str__Url = None
    headers  : Dict

    def get(self, path='', params=None):
        url      = self.url(path)
        with capture_duration() as request_duration:
            response     = requests.get(url, params=params, headers=self.headers)
            headers      = response.headers
            content_type = headers.get('Content-Type')
            if 'application/json' in content_type:
                content = response.json()
            elif 'text' in content_type:
                content = response.text
            else:
                content = response.content

        return dict(headers  = dict(headers)          ,
                    content  = content                ,
                    duration =request_duration.seconds)

    def url(self, path=''):
        if self.base_url is None:
            raise ValueError('No base url')
        return url_join_safe(base_path=self.base_url, path=path)