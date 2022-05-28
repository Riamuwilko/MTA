from tracemalloc import stop
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from keys import api_key
from geopy.geocoders import Nominatim
from pprint import pprint
import time, requests, json

# Gets current location of the user
def getLocation(): 
    options = Options()

    #bypass location's permission request
    options.add_argument("--use--fake-ui-for-media-stream") 

    # allows selenium to open chrome 
    driver = webdriver.Chrome(executable_path = 'C:/Users/19294/Desktop/mta/chromedriver.exe', chrome_options=options) 
    timeout = 20

     # this websites shows the lat and lon
    driver.get("https://www.where-am-i.co")
    WebDriverWait(driver, timeout)
    time.sleep(2)

    #gets the coordinates in a string form ("lat , lon")
    fullcoords = driver.find_elements(By.ID,"geolocation_decimal")[0].text 
    driver.quit()

    #converts string coords to a set of coords {lat, lon}
    coords = fullcoords.split(",")
    return coords

# Gets coordinates from user's input of their address
def askLocation():
    geolocator = Nominatim(user_agent="MyApp")
    address = input("Input Address: (ex.111 8th Ave, New York): ") 

    #stores address in a location object
    location = geolocator.geocode(address) 
    coords = [str(location.latitude), str(location.longitude)] 
    return coords

#converts coordinates to real life address
def cordtoaddress(x,y): 
    locator = Nominatim(user_agent="myAwesomeCoolGeocoderThing")

    #stores address in a location object
    location = locator.reverse(x + ", " + y) 
    return str(location.address)

#ask user's which option
def intro():  
    coords = "C"  #filler string
    askorget = input("Use current location or custom address? Type 'Current' or 'Custom': ").lower()

    # two options: current or custom address 
    if askorget == 'current': 
        coords = getLocation()
        address = cordtoaddress(coords[0],coords[1])

        #this is asked because the website that uses to check location can be wonky at times 
        rigthaddress = input(f"Is {address} your current address? 'Y' for yes, 'N' for no: ").lower() 

        #in this case we ask the user to input their address for an more accurate data
        if rigthaddress == 'n': 
            print("Please enter a custom address instead!")
            coords = askLocation()
    elif askorget == 'custom':
        coords = askLocation() 

    return coords

#uses mta's onebusapi to access their data given location and an api key
def mta(key,lat,lon):

    #payload store the paramater for the request
    payload = {'lat': lat, 'lon': lon, 'lanSpan': 0.005, 'lonSpan': 0.005, 'key':key}
    r = requests.get('https://bustime.mta.info/api/where/stops-for-location.json', params=payload)

    #converts the json to a dictionary that we can draw data from
    data = r.json()
    pprint(data['data']['stops'])
    

if __name__ == "__main__":
    cord = intro()
    mta(api_key,cord[0],cord[1])

