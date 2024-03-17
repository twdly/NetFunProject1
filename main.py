import socket
from socket import * # imports all objects from the socket module
import sys 


def main(): #main function to call on upon execution
    server_socket = socket(AF_INET, SOCK_STREAM)#create new server socket
    server_socket.bind(("", 6789)) #binds sever socket to all available network intrefaces " " with port number 6789
    server_socket.listen(1) #allow for only 1 incoming connection

    while True:
        print('Ready to serve...')
        connection_socket, addr = server_socket.accept()#creates a unique socket dedictaed to the specific client

        try:
            message = connection_socket.recv(2048).decode()#receives data through a http request & decodes it to a string
            filename = message.split()[1]#splits message into parts and extracts second part which contains filename/path
            f = open(filename[1:])
            output_data = f.read()
            connection_socket.send("HTTP/1.1 200 OK\r\n".encode())#sends http response indicating a 200 ok message
            
            for i in range(0, len(output_data)): #iterates over every character in the string 
                connection_socket.send(output_data[i].encode())
            connection_socket.send("\r\n".encode())#indicated end of message

        except IOError: #initiates an exception handler
            connection_socket.send("HTTP/1.1 404 Not Found\r\n".encode())#sends http response indicating a 404 Not found message
            f = open("404.html")
            error_page = f.read()
            
            for i in range(0, len(error_page)):
                connection_socket.send(error_page[i].encode())
            connection_socket.send("\r\n".encode())

        finally:
            connection_socket.close() #close connection socket
        server_socket.close()#close server socket
        sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__": #ensure the script is executed directly 
    main()

