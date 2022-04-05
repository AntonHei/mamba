from RequestHandler import RequestHandler
from ProcessingHandler import ProcessingHandler
from ConfigHandler import ConfigHandler
from Request import Request

# Init
configHandler = ConfigHandler()
requestHandler = RequestHandler()
processingHandler = ProcessingHandler()

requestHandler.start()
print("---------------------------")

def waitForConnections():

    while True:
        processingHandler.reset()
        # Receive Request
        client_connection, r_data = requestHandler.waitForRequest()

        if len(r_data) <= 0:
            return waitForConnections()

        request = Request(client_connection, r_data)

        requestData = request.getRequestHeadData()
        print(requestData['Request_Method'] + " " + requestData['Request_File'] + " " + requestData['Request_Protocol'] + "/" + requestData['Request_Protocol_Version'])

        # Build Response
        response = processingHandler.buildResponse(request)
        request.set_response(response)

        http_response_status_code = processingHandler.getResponseStatusCode(request)
        http_response_status_code_text = processingHandler.getResponseStatusText(http_response_status_code)

        file_path = processingHandler.getRequestedFilePath(request)
        if processingHandler.getResponseStatusCode(request) == 200:
            file_mimetype = processingHandler.fileHandler.getFileMimeTypeForHeader(file_path)
        else:
            file_mimetype = "text/html"

        print(str(http_response_status_code) + " - " + http_response_status_code_text + " - " + str(file_mimetype))
        print()

        request.respond()

waitForConnections()
