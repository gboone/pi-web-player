from bs4 import BeautifulSoup
from datetime import datetime, time, date, timedelta
import requests
from icalendar import Calendar, Event

month = f"{datetime.today():%B}"
day = f"{datetime.today().day}"
year = f"{datetime.today().year}"
weekday = f"{datetime.now():%A}"
weekday_int = date.weekday(datetime.now())


def time_of_day():
  now = datetime.now()
  if now.hour < 12:
      return "Morning"
  elif now.hour > 12 & now.hour < 18:
      return "Afternoon"
  elif now.hour > 18 & now.hour < 22:
      return "Evening"
  else:
      return "Night"

def day_of_week():
    if weekday_int in (5,6):
        return (weekday,'weekend')
    else:
        return (weekday, 'weekday')
    
def today_lunch(lunch_url):
  lunch_response = requests.get(lunch_url)
  lunch_doc = lunch_response.text
  soup = BeautifulSoup(lunch_doc, 'html.parser')
  today_lunch = soup.find_all("strong", string=f"{month} {day}:")
  if today_lunch == []:
    return "No lunch today"
  else:
    return today_lunch[0].text

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
      if event.DTSTART <= check_date <= event.DTEND: 
          school_status = f"No school: {event['SUMMARY']}"
          return (school_status, check_date, event.DTSTART, event.DTEND)
  # If the loop does not match any days, then it is unforturnately a school day
  return ("School day", check_date)
