import socket
from ConfigHandler import ConfigHandler

class RequestHandler():

    socket_hostname = "127.0.0.1"
    socket_port = 8888

    r_mayBytes = 1024

    l_socket = None

    # Instances
    configHandler = None

    def __init__(self):
        self.configHandler = ConfigHandler()

    def start(self):
        socketConfigData = self.configHandler.getConfigData("socket")

        hostname = socketConfigData["hostname"]
        port = socketConfigData["port"]

        self.l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.l_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.l_socket.bind((hostname, int(port)))
        self.l_socket.listen(1)

        print('Listening on {:s}:{:s}'.format(str(hostname), str(port)))

    def waitForRequest(self):
        client_connection, client_address = self.l_socket.accept()
        r_data = client_connection.recv(self.r_mayBytes)

        return client_connection, r_data