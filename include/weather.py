from datetime import datetime, date, time

import openmeteo_requests
from retry_requests import retry
import requests_cache
import requests

def convertKtoF(temp):
    tempInK = temp*9/5-459.67
    return round(tempInK,1)

def getTheWeather(baseurl, latitude, longitude, params):
  params['latitude'] = latitude
  params['longitude'] = longitude

  # Get the forecast from open-meteo. For what we're doing, the openmeteo
  # api python package is too intense. We just need the values, not to make 
  # complicated charts or track trends, etc. Just the facts, se we only
  # use requests.
  response = requests.get(baseurl, params)
  # The response contains keys for the different parts of the forecast we asked
  # the open-meteo API for. Current: current temp and weather code. And Daily:
  # The high, low, precipitation chance, and sunrise/sunset/daylight values.
  theWeather = response.json()
  current = theWeather['current']
  daily = theWeather['daily']
  current_temp = current['temperature_2m']
  current_weather_code = current['weather_code']
  # Map the above WMO codes to index of icon in 3x3 spritesheet
  WMO_CODE_TO_ICON = (
        (0,),  # 0 = sunny
        (1,),  # 1 = partly sunny/cloudy
        (2,),  # 2 = cloudy
        (3,),  # 3 = very cloudy
        (61, 63, 65),  # 4 = rain
        (51, 53, 55, 80, 81, 82),  # 5 = showers
        (95, 96, 99),  # 6 = storms
        (56, 57, 66, 67, 71, 73, 75, 77, 85, 86),  # 7 = snow
        (45, 48),  # 8 = fog and stuff
  )
  current_weather_icon = next(
    i for i, t in enumerate(WMO_CODE_TO_ICON) 
    if current_weather_code in t
  )
  # Daily forecast readout:
  # Same as with Current, the Daily variables appear in the order listed
  daily = theWeather['daily']
  highTemp = daily['temperature_2m_max'][0]
  lowTemp =  daily['temperature_2m_min'][0]
  precipProbability = daily['precipitation_probability_max'][0]
  precipHours = daily['precipitation_hours'][0]
  sunrise = daily['sunrise'][0]
  sunset = daily['sunset'][0]
  duration = daily['daylight_duration'][0]
  return {
          "current": {
              "temp": current_temp,
              "code": current_weather_code,
              "icon": current_weather_icon
              },
          "forecast": {
              "high": highTemp,
              "low": lowTemp,
              "precip": precipProbability,
              "sunrise": sunrise,
              "sunset": sunset,
              "daylight": duration
              }
          }
