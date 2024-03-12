import socket
from socket import *
import sys


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    # Fill in start
    server_socket.bind(("", 6789))
    server_socket.listen(1)
    # Fill in end
    while True:
        # Establish the connection
        print('Ready to serve...')
        connection_socket, addr = server_socket.accept()
        try:
            message = connection_socket.recv(2048).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            output_data = f.read()
            # Send one HTTP header line into socket
            # Fill in start
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())
            # Fill in end
            # Send the content of the requested file to the client
            for i in range(0, len(output_data)):
                connection_socket.send(output_data[i].encode())
            connection_socket.send("\r\n".encode())
        except IOError:
            # Send response message for file not found
            # Fill in start
            connection_socket.send("HTTP/1.1 404 Not Found\r\n".encode())
            f = open("404.html")
            error_page = f.read()
            for i in range(0, len(error_page)):
                connection_socket.send(error_page[i].encode())
            connection_socket.send("\r\n".encode())
            # Fill in end
        finally:
            # Close client socket
            connection_socket.close()
        server_socket.close()
        sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    main()
