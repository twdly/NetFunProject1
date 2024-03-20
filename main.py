import socket
from socket import *  # imports all objects from the socket module
import sys 


def main():  # main function to call on upon execution
    server_socket = socket(AF_INET, SOCK_STREAM)  # create new server socket
    server_socket.bind(("", 6789))  # binds sever socket to all available network interfaces " " with port number 6789
    server_socket.listen(1)  # allow for only 1 incoming connection

    while True:
        print('Ready to serve...')
        connection_socket, addr = server_socket.accept()  # creates a unique socket dedicated to the specific client

        try:
            message = connection_socket.recv(2048).decode()  # receives data through a http request & decodes it to a string
            filename = message.split()[1]  # splits message into parts and extracts second part which contains filename/path
            if filename == "/exit":
                break
            f = open(filename[1:])

            output_data = f.read() + "\r\n"
            status_header = "HTTP/1.1 200 OK\r\n"  # Indicates a 200 OK response
            content_type_header = "Content-Type: text/html; charset=UTF-8\r\n"  # Tells the browser that the response contains an html page
            content_length_header = f"Content-Length: {len(output_data.encode('utf-8'))}\r\n"  # Header to display the length of the content

            output_data = status_header + content_type_header + content_length_header + "\r\n" + output_data  # Construct the request by appending components
            connection_socket.send(output_data.encode())  # Send the constructed request

        except IOError:  # initiates an exception handler
            status_header = "HTTP/1.1 404 Not Found\r\n"  # Indicates a 404 Not found response
            f = open("404.html")  # opens the 404 html file

            error_output_data = f.read() + "\r\n"  # Reads the 404 html file and appends a carriage return
            content_type_header = "Content-Type: text/html; charset=UTF-8\r\n"  # Tells the browser that the response contains an html page
            content_length_header = f"Content-Length: {len(error_output_data.encode('utf-8'))}\r\n"  # Header to display the length of the content

            error_output_data = status_header + content_type_header + content_length_header + "\r\n" + error_output_data  # Construct the request by appending components
            connection_socket.send(error_output_data.encode())  # Send the constructed request

        finally:
            connection_socket.close()  # close connection socket
    server_socket.close()  # close server socket
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":  # ensure the script is executed directly
    main()
