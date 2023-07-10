from socket import *
import threading
import json

movies = [
    {
        "Id": 1,
        "MovieName": "Dune",
        "LengthInMinutes": 155,
        "CountryOfOrigin": "USA"
    },
    {
        "Id": 2,
        "MovieName": "The Fifth Element",
        "LengthInMinutes": 126,
        "CountryOfOrigin": "USA"
    },
    {
        "Id": 3,
        "MovieName": "Martyrs",
        "LengthInMinutes": 99,
        "CountryOfOrigin": "France"
    }
]


def handle_client(connection_socket, address):
    print(address)
    request = connection_socket.recv(1024).decode()
    words = request.split()
    # Takes first word and converts to upper case, this is the command
    cmd = words[0].upper()
    print("Command: "+cmd)
    if (cmd == "GETALL"):
        response = json.dumps(movies)
    elif (cmd == "GETBYCOUNTRY"):
        searchstr = words[1].upper()
        matches = []
        for p in movies:
            if searchstr in p["CountryOfOrigin"].upper():
                matches.append(p)
        response = json.dumps(matches)
    else:
        response = "Invalid command, use GetAll or GetByCountry"
    print("Sending to client: "+response)

    connection_socket.send(response.encode())
    connection_socket.close()


serverPort = 43214

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server is ready to listen')


while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()

