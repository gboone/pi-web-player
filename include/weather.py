from datetime import datetime, date, time
import requests

def convertKtoF(temp):
    tempInK = temp*9/5-459.67
    return round(tempInK,1)

def getTheWeather(token, location, baseurl):
  # Set up where we'll be fetching data from
  if len(token) == 0:
      raise RuntimeError(
              "You must register a token at https://home.openweathermap.org/users/sign_up then add it to config.yml under `other`, with the name openweather-token."
      )
  params = {"q": location, "appid": token}
  
  theWeather = requests.get(baseurl, params)
  theWeatherData = theWeather.json()
  
  currentTemp = convertKtoF(theWeather.json()['main']['temp'])
  highTemp = convertKtoF(theWeather.json()['main']['temp_max'])
  lowTemp = convertKtoF(theWeather.json()['main']['temp_min'])
  conditions = theWeather.json()['weather'][0]['main']
  conditionDescription = theWeather.json()['weather'][0]['description']
  conditionIcon = theWeather.json()['weather'][0]['icon']
  return (currentTemp,highTemp,lowTemp,conditions,conditionDescription,conditionIcon)
