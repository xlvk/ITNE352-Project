import socket
import time
import threading
import urllib.error
from urllib.request import urlopen
import json

# AviationStack API key
api_key = "ec9a339729e37e6f9dcb2531ca197d4e"


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
            # if flight landed, construct a object of data
            returns = {
                "flight_iata": data[i]["flight"]["iata"],
                "departure_airport": data[i]["departure"]["airport"],
                "arrival_actual": data[i]["arrival"]["actual"],
                "arrival_terminal": data[i]["arrival"]["terminal"],
                "arrival_gate": data[i]["arrival"]["gate"],
            }
            ## append to rest
            vals.append(returns)
        i += 1
    return {"data": vals}


## scan all flights for delayed flights in departure and arrival
## @param - ICAO code for source airport
## 5B
def searchForDelayed(ICAO_CODE):
    rawjsonData = get_flight_info(ICAO_CODE)
    vals = []
    data = rawjsonData.get("data", [])
    for i in range(0, len(data) - 1):
        if data[i]["arrival"]["delay"] != None:
            returns = {
                "flight_IATA": data[i]["flight"]["iata"],
                "departure_airport": data[i]["departure"]["airport"],
                "org_departure_time": data[i]["departure"]["scheduled"],
                "estimated_arrival_time": data[i]["arrival"]["estimated"],
                "arrival_terminal": data[i]["arrival"]["terminal"],
                "departure_delay": data[i]["departure"]["delay"],
                "arrival_delay": data[i]["arrival"]["delay"],
                "arrival_gate": data[i]["arrival"]["gate"],
            }
            vals.append(returns)

    return {"data": vals}


## Scan all flights from a specific airport
## @param - ICAO codes, one for source airport, and one for destination
## 5C
def searchForSpecificCode(ICAO_CODE_FOR_CURRENT, DESIRED_AIRPORT_ICAO):
    rawjsonData = get_flight_info(ICAO_CODE_FOR_CURRENT)
    vals = []
    data = rawjsonData.get("data", [])
    for i in range(0, len(data) - 1):
        if data[i]["departure"]["icao"] == DESIRED_AIRPORT_ICAO:
            returns = {
                "flight_iata": data[i]["flight"]["iata"],
                "departure_airport": data[i]["departure"]["airport"],
                "departure_scheduled": data[i]["departure"]["scheduled"],
                "arrival_estimated": data[i]["arrival"]["estimated"],
                "departure_gate": data[i]["departure"]["gate"],
                "arrival_gate": data[i]["arrival"]["gate"],
                "flight_status": data[i]["flight_status"],
            }
            vals.append(returns)
    return {"data": vals}


## scan for a specific flight
##@param - current ICAO + IATA code of flight needed
### 5D
def searchForSpecificFlight(CURRENT_AIRPORT_ICAO, IATA_CODE):
    rawjsonData = get_flight_info(CURRENT_AIRPORT_ICAO)
    data = rawjsonData.get("data", [])
    for i in range(0, len(data) - 1):
        if data[i]["flight"]["iata"] == IATA_CODE:
            return {
                "flight IATA": data[i]["flight"]["iata"],
                "departure airport": data[i]["departure"]["airport"],
                "departure gate": data[i]["departure"]["gate"],
                "departure terminal": data[i]["departure"]["terminal"],
                "arrival airport": data[i]["arrival"]["airport"],
                "arrival gate": data[i]["arrival"]["gate"],
                "arrival terminal": data[i]["arrival"]["terminal"],
                "departure scheduled": data[i]["departure"]["scheduled"],
                "arrival scheduled": data[i]["arrival"]["scheduled"],
            }


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

match int(OptionChose):
    case 1:
        # print(json.dumps(searchForArrival(airport_code)))
        for x in searchForArrival(airport_code).get("data"):
            print(json.dumps(x) + "\n\n")
        sock_a.send(json.dumps(searchForArrival(airport_code)).encode())
    case 2:
        # print(json.dumps(searchForDelayed(airport_code)))
        for x in searchForDelayed(airport_code).get("data"):
            print(json.dumps(x))
        sock_a.send(json.dumps(searchForDelayed(airport_code)).encode())
    case 3:
        sock_a.send("Server >> what is the desired ICAO for results?".encode())
        d_airport_code = sock_a.recv(1024).decode("ascii")
        # print(json.dumps(searchForSpecificCode(airport_code, d_airport_code)))
        for x in searchForSpecificCode(airport_code, d_airport_code).get("data"):
            print(json.dumps(x) + "\n\n")
        sock_a.send(
            json.dumps(searchForSpecificCode(airport_code, d_airport_code)).encode()
        )
    case 4:
        sock_a.send("Server >> what is the desired IATA for the flight?".encode())
        d_IATA = sock_a.recv(1024).decode("ascii")
        print(json.dumps(searchForSpecificFlight(airport_code, d_IATA)) + "\n\n")
        sock_a.send(json.dumps(searchForSpecificFlight(airport_code, d_IATA)).encode())
    case _:
        sock_a.send("Server >> 400 INVALID OPTION".encode())

sock_a.close()
ss.close()
