
class General():

    ws_name = "Mamba"
    ws_version = "1.0.0"

    http_version = "1.1"

    @classmethod
    def getWSName(self):
        return self.ws_name

    @classmethod
    def getWSVersion(self):
        return self.ws_version

    @classmethod
    def getHTTPVersion(self):
        return self.http_version