import socket

from ResponseHandler import ResponseHandler

class Request():

    c_connection = None
    r_data = None
    response = None
    response_body = None

    # Custom  Data
    response_custom_headers = {}

    def __init__(self, c_connection, r_data):
        # Clear
        self.c_connection = None
        self.r_data = None
        self.response = None
        self.response_body = None
        self.response_custom_headers = {}

        self.c_connection = c_connection
        self.r_data = r_data

        # Create Class Instances
        self.responseHandler = ResponseHandler()

    def setResponseBody(self, response_body):
        self.response_body = response_body

    def getResponseBody(self):
        return self.response_body

    def set_response(self, response):
        self.response = response

    def addCustomResponseHeader(self, key, value):
        self.response_custom_headers[key] = value

    def getCustomResponseHeaders(self):
        return self.response_custom_headers

    def getRequestHead(self):
        divider = "\r\n\r\n"
        r_parts = self.r_data.decode().split(divider)
        if r_parts:
            if r_parts[0]:
                return r_parts[0].encode()
        return b''

    def getRequestHeadData(self):
        head_data = {}

        divider = "\r\n"
        request_head = self.getRequestHead()
        r_parts = request_head.decode().split(divider)
        for line in r_parts:
            if ":" in line:
                # Head: Request Headers
                l_parts = line.split(":", 1)
                if len(l_parts) >= 2:
                    head_data[l_parts[0].strip()] = l_parts[1].strip()
            else:
                # Head: Request Line
                l_parts = line.split(" ")
                if len(l_parts) >= 1:
                    head_data['Request_Method'] = l_parts[0].strip()
                    if len(l_parts) >= 2:
                        head_data['Request_File'] = l_parts[1].strip()
                        if len(l_parts) >= 3:
                            p_parts = l_parts[2].split("/")
                            if len(p_parts) >= 1:
                                head_data['Request_Protocol'] = p_parts[0].strip()
                                if len(p_parts) >= 2:
                                    head_data['Request_Protocol_Version'] = p_parts[1].strip()
                            else:
                                head_data['Request_Protocol'] = l_parts[2].strip()

        return head_data

    def getRequestBody(self):
        divider = "\r\n\r\n"
        r_parts = self.r_data.decode().split(divider)
        if r_parts:
            if r_parts[1]:
                return r_parts[1].encode()
        return b''

    def getRequestBodyData(self):
        head_data = {}

        divider = "&"
        request_head = self.getRequestBody()
        r_parts = request_head.decode().split(divider)
        for line in r_parts:
            if "=" in line:
                # Body: Request Parameters
                l_parts = line.split("=", 1)
                if len(l_parts) >= 2:
                    head_data[l_parts[0].strip()] = l_parts[1].strip()

        return head_data

    def respond(self):
        # Respond
        self.responseHandler.client_respond(self.c_connection, self.response)
