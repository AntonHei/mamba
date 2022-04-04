import socket

class ResponseHandler():

    l_socket = None

    def client_respond(self, client_connection, response):
        client_connection.send(response)
        client_connection.close()
