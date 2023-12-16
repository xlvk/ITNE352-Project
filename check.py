import json
import urllib
from urllib.request import urlopen

# takes care of arrived flights only

api_key = "3f0e6c3e4a2674f4293af2ef40eefd58"


# Function to retrieve flight information from AviationStack API
def get_flight_info(airport_code):
    api_url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&limit=100&arr_icao={airport_code}"

    try:
        # Make a GET request to the API using urllib
        with urlopen(api_url) as response:
            # Read and parse the JSON response
            d = json.loads(response.read().decode("utf-8"))
            with open("flightinfo.json", "w") as json_file:
                json.dump(d, json_file, indent=4)
            return d

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
    vals = []
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

