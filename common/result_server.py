import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SplunkResultServer(object):
    def __init__(self, splunk_address=None, splunk_port=None, hec_token=None):
        self.address = splunk_address if splunk_address is not None else 'https://server'
        self.port = splunk_port if splunk_port is not None else '8088'
        self.url = self.address + ':' + self.port + '/services/collector'
        self.hec_token = hec_token

    def receive_data(self, body):
        content = requests.post(
                self.url,
                headers={
                    'X-Splunk-Request-Channel': '18654C68-B28B-4450-9CF0-6E7645CA60CA',
                    'Authorization': 'Splunk ' + self.hec_token
                },
                data=body,
                verify=False
        )
        if content.status_code != 200:
            print "HTTP ERROR CODE:" + str(content.status_code)
        # print content.status_code
