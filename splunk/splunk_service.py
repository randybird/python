from splunklib import client


class SplunkService(object):
    def __init__(self, host, port, username, password, scheme, app_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.scheme = scheme
        self.app_name = app_name

    def get_service(self):
        service = client.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                app=self.app_name,
                scheme='http'
        )
        return service
