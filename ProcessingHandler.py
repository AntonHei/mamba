import gzip

from FileHandler import FileHandler
from General import General
from HeaderHandler import HeaderHandler


class ProcessingHandler():
    indexFileName = "index.html"

    http_status_codes_texts = {
        200: "OK",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
    }

    # Instances
    fileHandler = None

    # Runtime Variables
    l_socket = None

    def __init__(self):
        self.headerHandler = HeaderHandler()
        self.fileHandler = FileHandler()

    def getRequestedFilePath(self, r):
        filePath = None

        headData = r.getRequestHeadData()
        if "Request_File" in headData:
            r_file = headData["Request_File"]

            isFolder = self.fileHandler.isFolder(r_file)
            if isFolder:
                filePath = r_file + "/" + self.indexFileName
            else:
                filePath = r_file

        return filePath

    def getResponseStatusCode(self, r):
        file_path = self.getRequestedFilePath(r)

        if file_path:
            exists = self.fileHandler.doesFileExist(file_path)
            if exists:
                canAccess = self.fileHandler.canAccessFile(file_path)
                if not canAccess:
                    return 501
            else:
                return 404
        else:
            return 400

        return 200

    def validateRequest(self, r):
        valid = True

        headData = r.getRequestHeadData()
        if "Request_File" in headData:
            r_file = headData["Request_File"]
            isFolder = self.fileHandler.isFolder(r_file)

            if isFolder:
                if r_file[-1] != "/":
                    r.addCustomResponseHeader("status", "302 Found")
                    r.addCustomResponseHeader("location", r_file + "/")
                    valid = False

        return valid


    def getResponseStatusText(self, status_code):
        return self.http_status_codes_texts[status_code]

    def buildResponse(self, r):
        self.validateRequest(r)
        self.executeRequest(r)

        # Build Head/Body
        head = self.getResponseHead(r)
        body = self.getResponseBody(r)

        response = head + gzip.compress(body)

        return response

    def getResponseHead(self, r):
        headers = ""

        headers = self.headerHandler.buildResponseHeaders(r, self)
        headers = headers.encode()

        return headers

    def executeRequest(self, r):
        body = None

        requested_file_path = self.getRequestedFilePath(r)
        mimeType = self.fileHandler.getFileMimeType(requested_file_path)

        if mimeType == "application/php":
            phpOutput = self.fileHandler.executePHP(requested_file_path)
            phpOutputDecoded = phpOutput.decode()
            if "\r\n" in phpOutputDecoded:
                phpParts = phpOutputDecoded.split("\r\n\r\n", 1)
                phpHeadersBytes = phpParts[0].encode()
                body = phpParts[1].encode()

                phpHeaders = phpHeadersBytes.decode().split("\r\n")

                for phpHeader in phpHeaders:
                    if ":" in phpHeader:
                        h_parts = phpHeader.split(":", 1)
                        if len(h_parts) >= 2:
                            r.addCustomResponseHeader(h_parts[0].strip(), h_parts[1].strip())

            else:
                body = phpOutput
        else:
            body = self.fileHandler.loadRequestedFile(requested_file_path)

        r.setResponseBody(body)

    def getResponseBody(self, r):
        body = ""

        http_status_code = self.getResponseStatusCode(r)
        http_status_code_text = self.getResponseStatusText(http_status_code)

        webservice_name = General.getWSName()
        webservice_version = General.getWSVersion()

        if http_status_code == 200:
            body = r.getResponseBody()
        else:
            body = f'<!DOCTYPE html>\n' \
            f'<html>\n' \
            f'<head>\n' \
            f'<title>{http_status_code} - {http_status_code_text}</title>\n' \
            f'</head>\n' \
            f'<body>\n' \
            f'<h1>{http_status_code} - {http_status_code_text}</h1>\n' \
            f'<hr>\n' \
            f'<p>{webservice_name}/{webservice_version}</p>\n' \
            f'</body>\n' \
            f'</html>\n'

            body = body.encode()

        return body
