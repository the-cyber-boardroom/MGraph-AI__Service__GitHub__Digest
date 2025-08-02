import requests
from osbot_utils.helpers.duration.decorators.capture_duration import capture_duration
from osbot_utils.type_safe.Type_Safe                          import Type_Safe

URL__CHECKIP__AMAZON_AWS = 'https://checkip.amazonaws.com'
URL__IP_IFY              = "https://api.ipify.org"
URL__IF_CONFIG           = 'https://ifconfig.me/ip'
URL__IP_INFO             = 'https://ipinfo.io/ip'
class Info__Current_IP_Address(Type_Safe):

    def requests_get(self,url):
        with capture_duration(precision=3) as request_duration:
            response = requests.get(url)
            headers  = response.headers
            text     = response.text.strip()
        return dict(headers = dict(headers),
                    text     = text           ,
                    duration = request_duration.seconds)

    def from__all(self):
        return dict(check_ip__amazon_aws = self.from__checkip__amazon_aws(),
                    if_config            = self.from__if_config          (),
                    ip_ify               = self.from__ip_ify             (),
                    ip_info              = self.from__ip_info            ())

    def current_ip_address(self):
        data = self.from__checkip__amazon_aws()
        return dict(ip_address = data.get('text'        ),
                    duration   = data.get('duration'    ),
                    source     = 'checkip.amazonaws.com')

    def from__checkip__amazon_aws(self):
        return self.requests_get(URL__CHECKIP__AMAZON_AWS)

    def from__if_config(self):
        return self.requests_get(URL__IF_CONFIG)

    def from__ip_ify(self):
        return self.requests_get(URL__IP_IFY)

    def from__ip_info(self):
        return self.requests_get(URL__IP_INFO)