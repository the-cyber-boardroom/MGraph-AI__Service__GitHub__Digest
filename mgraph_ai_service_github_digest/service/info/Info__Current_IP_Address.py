import requests
from osbot_utils.helpers.duration.decorators.capture_duration import capture_duration
from osbot_utils.type_safe.Type_Safe                          import Type_Safe

URL__CHECKIP__AMAZON_AWS = 'https://checkip.amazonaws.com'

class Info__Current_IP_Address(Type_Safe):

    def requests_get(self,url):
        with capture_duration(precision=3) as request_duration:
            response = requests.get(url)
            headers  = response.headers
            text     = response.text.strip()
        return dict(headers = dict(headers),
                    text     = text           ,
                    duration = request_duration.seconds)

    def from__checkip__amazon_aws(self):
        return self.requests_get(URL__CHECKIP__AMAZON_AWS)