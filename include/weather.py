from datetime import datetime, date, time
import requests
import loadconfig

CONFIG = loadconfig.loadconfig("config.yml")
OPEN_WEATHER_TOKEN=CONFIG['other']['openweather-token']
LOCATION=CONFIG['other']['openweather-location']
DATA_SOURCE_URL = CONFIG['other']['openweather-baseurl']


if len(OPEN_WEATHER_TOKEN) == 0:
    raise RuntimeError(
        "You need to set your token first. If you don't already have one, you can register for a free account at https://home.openweathermap.org/users/sign_up"
    )

def convertKtoF(temp):
    tempInK = temp*9/5-459.67
    return round(tempInK,1)

def getTheWeather():
  # Set up where we'll be fetching data from
  params = {"q": LOCATION, "appid": OPEN_WEATHER_TOKEN}
  
  theWeather = requests.get(DATA_SOURCE_URL, params)
  theWeatherData = theWeather.json()
  
  currentTemp = convertKtoF(theWeather.json()['main']['temp'])
  highTemp = convertKtoF(theWeather.json()['main']['temp_max'])
  lowTemp = convertKtoF(theWeather.json()['main']['temp_min'])
  conditions = theWeather.json()['weather'][0]['main']
  conditionDescription = theWeather.json()['weather'][0]['description']
  conditionIcon = theWeather.json()['weather'][0]['icon']
  return (currentTemp,highTemp,lowTemp,conditions,conditionDescription,conditionIcon)
