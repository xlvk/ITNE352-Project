import socket
import time
import threading
import urllib.error
from urllib.request import urlopen
import json
import flightUtils

# AviationStack API key
api_key = "ec9a339729e37e6f9dcb2531ca197d4e"


# Function to retrieve flight information from AviationStack API
def get_flight_info(airport_code):
    api_url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&limit=100&arr_icao={airport_code}"

    try:
        # Make a GET request to the API using urllib
        with urlopen(api_url) as response:
            # Read and parse the JSON response
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.URLError as e:
        print(f"Error: Unable to retrieve data from API. {e}")
        return None


# Socket setup
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 49999))
ss.listen(3)
sock_a, sockname = ss.accept()

# Send a prompt to the client
sock_a.send("Enter airport code (arr_icao)".encode())

# Receive the airport code from the client
airport_code = sock_a.recv(1024).decode()

# Retrieve flight information from AviationStack API
flight_info = get_flight_info(airport_code)

# Save the retrieved data in a JSON file
if flight_info:
    filename = "group_ID.json"
    with open(filename, "w") as json_file:
        json.dump(flight_info, json_file, indent=2)

    print(f"Flight information saved to {filename}")

# Receving the option to send (a,b,c,d)
OptionChose = -1
# Send a prompt to the client
sock_a.send("Server >> What option to choose?".encode())

# Receive the option from the client
OptionChose = sock_a.recv(1024).decode("ascii")
print(f"Option Choose : {OptionChose}")

match OptionChose:
    case 1:
        sock_a.send(json.dumps(flightUtils.searchForArrival(airport_code)))
    case 2:
        sock_a.send(json.dumps(flightUtils.searchForDelayed(airport_code)))
    case 3:
        sock_a.send("Server >> what is the desired ICAO for results?".encode())
        d_airport_code = sock_a.recv(1024).decode("ascii")
        sock_a.send(
            json.dumps(flightUtils.searchForSpecificCode(airport_code, d_airport_code))
        )
    case 4:
        sock_a.send("Server >> what is the desired IATA for the flight?".encode())
        d_IATA = sock_a.recv(1024).decode("ascii")
        sock_a.send(
            json.dumps(flightUtils.searchForSpecificFlight(airport_code, d_IATA))
        )
    case _:
        sock_a.send("Server >> 400 INVALID OPTION?".encode())

sock_a.close()
ss.close()
