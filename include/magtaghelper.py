from bs4 import BeautifulSoup
from datetime import datetime, time, date, timedelta
import requests
from icalendar import Calendar, Event

def time_of_day():
  now = datetime.now()
  if 4 < now.hour < 12:
      return "Morning"
  elif 12 < now.hour < 18:
      return "Afternoon"
  elif 18 < now.hour < 21:
      return "Evening"
  else:
      return "Night"

def day_of_week():
    now = today()
    weekday_int = now['weekday_int']
    weekday = now['weekday']
    if weekday_int in (0,6):
        return (weekday, True)
    else:
        return (weekday, False)
    
def today():
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    return {
            "Day": day,
            "Month": month,
            "Year": year,
            "weekday": f"{now:%A}",
            "weekday_int": f"{now:%w}",
            "ts": now
            }

def today_lunch(lunch_url, lunch_paths, lunch_params):
  lunch_params['ServingDate']= datetime.strftime(datetime.now(), "%m/%d/%Y")
  lunch_response = requests.get(f"{lunch_url}{lunch_paths}/", params=lunch_params)
  lunch_doc = lunch_response.json()
  
  try:
    entrees = [entree['MenuItemDescription'] for entree in lunch_doc['ENTREES']]
  except (NameError,KeyError):
      entrees = []
  try:
    veggies = [veggie['MenuItemDescription'] for veggie in lunch_doc['VEGETABLES']]
  except (NameError, KeyError):
    veggies = []
  try:
    fruits  = [fruits['MenuItemDescription'] for fruits in lunch_doc['FRUITS']]
  except (NameError, KeyError):
    fruits = []
  try:
    grains = [grain['MenuItemDescription'] for grain in lunch_doc['GRAINS']]
  except (NameError, KeyError):
      grains = []
  for entree in entrees:
        if "wow butter meal" in entree.lower():
          entrees.remove(entree)
        if "cheese stick" in entree.lower():
            entrees.remove(entree)
  theLunch = {"entrees": entrees, "veggies": veggies, "fruits": fruits, "grains": grains}
  return theLunch

def check_no_school(url, check_date=date.today()):
  school_calendar_data=requests.get(url).text
  school_calendar = Calendar.from_ical(school_calendar_data)
  events = school_calendar.events
  # If the date to check is a weekend, exit early.
  if date.weekday(check_date) in (5,6):
      return ("No School: Weekend", check_date)
  # Iterate through all the events in the calendar if any overlap with today
  # that means there's no school.
  for event in events:
      if event.DTSTART <= check_date < event.DTEND: 
          school_status = f"{check_date}, No school: {event['SUMMARY']}"
          return (school_status, check_date, event.DTSTART, event.DTEND)
  # If the loop does not match any days, then it is unforturnately a school day
  return ("School day", check_date)
