import socket
import time
import threading
import urllib.error
from urllib.request import urlopen
import json

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


## returns data for all landed flights
## returns are in the form of a 2d Array
## 5A
def searchForArrival(ICAO_CODE):
    rawjsonData = get_flight_info(ICAO_CODE)
    vals = []
    i = 0
    data = rawjsonData.get("data", [])
    for flight in data:
        if flight.get("flight_status") == "landed":
            # if flight landed, construct a array of data
            returns = [
                data[i]["flight"]["iata"],
                data[i]["departure"]["airport"],
                data[i]["arrival"]["actual"],
                data[i]["arrival"]["terminal"],
                data[i]["arrival"]["gate"],
            ]
            ## append to rest
            vals.append(returns)
        i += 1
    return vals


## Scan all flights from a specific airport
## @param - ICAO codes, one for source airport, and one for destination
## 5C
def searchForSpecificCode(ICAO_CODE_FOR_CURRENT, DESIRED_AIRPORT_ICAO):
    rawjsonData = get_flight_info(ICAO_CODE_FOR_CURRENT)
    vals = []
    data = rawjsonData.get("data", [])
    for i in range(0, len(data) - 1):
        if data[i]["departure"]["icao"] == DESIRED_AIRPORT_ICAO:
            returns = [
                data[i]["flight"]["iata"],
                data[i]["departure"]["airport"],
                data[i]["departure"]["scheduled"],
                data[i]["arrival"]["estimated"],
                data[i]["departure"]["gate"],
                data[i]["arrival"]["gate"],
                data[i]["flight_status"],
            ]
            vals.append(returns)
    return vals


## scan for a specific flight
## IATA code of flight needed
### 5D
def searchForSpecificFlight(CURRENT_AIRPORT_ICAO, IATA_CODE):
    rawjsonData = get_flight_info(CURRENT_AIRPORT_ICAO)
    data = rawjsonData.get("data", [])
    for i in range(0, len(data) - 1):
        if data[i]["flight"]["iata"] == IATA_CODE:
            return [
                data[i]["flight"]["iata"],
                data[i]["departure"]["airport"],
                data[i]["departure"]["gate"],
                data[i]["departure"]["terminal"],
                data[i]["arrival"]["airport"],
                data[i]["arrival"]["gate"],
                data[i]["arrival"]["terminal"],
                data[i]["departure"]["scheduled"],
                data[i]["arrival"]["scheduled"],
            ]


sock_a.close()
ss.close()
