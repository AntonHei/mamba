from General import General
from FileHandler import FileHandler

class HeaderHandler():

    def __init__(self):
        self.fileHandler = FileHandler()

    def buildResponseHeaders(self, r, processingHandler):
        file_path = processingHandler.getRequestedFilePath(r)

        http_status_code = processingHandler.getResponseStatusCode(r)
        http_status_code_text = processingHandler.getResponseStatusText(http_status_code)

        webservice_name = General.getWSName()
        webservice_version = General.getWSVersion()

        http_version = General.getHTTPVersion()

        # If File is found use file mime type otherwise default to text/html
        if processingHandler.getResponseStatusCode(r) == 200:
            file_mimetype = self.fileHandler.getFileMimeTypeForHeader(file_path)
        else:
            file_mimetype = "text/html"

        defaultHeaders = {
            f'Connection': f'Keep-Alive',
            f'Content-Encoding': f'gzip',
            f'Content-Type': f'{file_mimetype}; charset=utf-8',
            f'Server': f'{webservice_name}/{webservice_version}',
        }

        customHeaders = r.getCustomResponseHeaders()

        allHeaders = {}

        # Merge Headers with hierarchy
        for key in defaultHeaders:
            allHeaders[key.lower()] = defaultHeaders[key]

        for key in customHeaders:
            allHeaders[key.lower()] = customHeaders[key]

        if 'status' in allHeaders:
            customStatus = allHeaders['status']
            headers = f'HTTP/{http_version} {customStatus}\n'

            del allHeaders['status']
        else:
            headers = f'HTTP/{http_version} {http_status_code} {http_status_code_text}\n'

        for key in allHeaders:
            headers += f'{key}: {allHeaders[key]}\n'

        headers += f'\n'

        return headers
