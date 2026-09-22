from flask import Flask, render_template, request
import sys
import platform
from include import localradio, localsystem, localtime, localnetwork
from include import streamRadio, loadconfig, templatefunctions
from include import magtaghelper, weather
import vlc
import subprocess
from flask_bootstrap import Bootstrap5
from flask import Flask

CONFIG = loadconfig.loadconfig("config.yml")
STATIONS = CONFIG['radio']['stations']
OTHER = CONFIG['other']

# school URLs
lunch_url_base   = OTHER['school-cafe-baseurl']
lunch_url_paths  = OTHER['school-cafe-paths']
lunch_url_params = OTHER['school-cafe-params']
cal_url = OTHER['mps-calendar']

# weather URLs
#ow_token   = OTHER['openweather-token']
#ow_location= OTHER['openweather-location']
#ow_baseurl = OTHER['openweather-baseurl']

weather_baseurl = OTHER['weather-baseurl']
weather_latitude = OTHER['weather-latitude']
weather_longitude = OTHER['weather-longitude']
weather_params = OTHER['weather-forecast-params']

PLAYERS = {}
for station in STATIONS:
    streamURL = STATIONS[station]['stream']
    player = streamRadio.createPlayer(streamURL)
    PLAYERS[station] = player

PLATFORM = sys.platform
UNSUPPORTED = ("darwin", "win32", "cygwin", "wasi", "enscripten")
NOUPPORT = "Not available on this platform"
if PLATFORM == "darwin":
    FLASK_DEBUG = True
else:
    FLASK_DEBUG = False

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)

# Routes
@app.route("/")
def index():
    status = templatefunctions.getIndexData(STATIONS, request, PLAYERS)
    now_playing = templatefunctions.getActivePlayers(PLAYERS)
    return render_template(
        "index.html",
        status=status,
        now_playing=now_playing,
        bootstrap=bootstrap
    )


@app.route("/network/")
def network():
    return {
        "network": { 
            "IP": localnetwork.currentIP(), 
            "connected": localnetwork.isConnected() 
        },
        "related": ["/uptime/", "/sysinfo/"]
    }


@app.route("/time/")
def uptime():
    up = localtime.getUptime()
    local = localtime.getLocalTime()
    utcTime = localtime.getLocalTime(utc=True)
    return {
        "time": {
            "up": up, 
            "local": local[0], 
            "tz-local": local[1], 
            "local-utc": utcTime[0]
        },
        "related": ["/network/", "/sysinfo/"]
    }


@app.route("/sysinfo/")
def sysinfo():
    sysReport = {"disk": [], "cpu": []}
    dfValues = localsystem.getDF()
    dfJSON = [{
        "used": dfValues[0],
        "available": dfValues[1],
        "percent": dfValues[2]
    }]
    cpuValues = localsystem.getCPU()
    sysReport = {
        "disk": {
            "used": dfValues[0],
            "available": dfValues[1],
            "percent": dfValues[2],
        },
        "cpu": {
            "current": cpuValues
        }
    }

    return sysReport


@app.route("/radio/")
def radio():
    stream889 = CONFIG['radio']['stations']['889']
    xml889 = CONFIG['radio']['xspf']['889']
    station_status = localradio.getWYMSXML(xml889)
    station_info = {
        "vlc": localradio.isVLC(),
        "now_playing": localradio.getWYMSTrackInfo(station_status),
        "station": localradio.getWYMSStationName(station_status)
    }
    return station_info


@app.route("/radio/<stream>", methods=["GET"])
def streamPlayStop(stream):
    player = PLAYERS[stream]
    status = {
        "status": "",
        "station": stream,
        "url": STATIONS[stream],
        "last-played": "",
        "play": request.base_url + "?play",
        "stop": request.base_url + "?stop"
    }
    status = templatefunctions.radioStreamQueryArgs(
        request,
        status,
        player,
        UNSUPPORTED,
        PLATFORM
    )
    if status['status'] != "error":
        status['status'] = streamRadio.getStatus(player)
    return status


@app.route("/radio/stop-all/")
def radioStopAll():
    stopped = localradio.stopAllPlayers(PLAYERS)
    if stopped.__len__() > 0:
        return {"stopped": stopped}
    else:
        return {"stopped": "none"}


@app.route("/radio/streams/")
def radioStations():
    streams = templatefunctions.getStationData(STATIONS, request, PLAYERS)
    return streams

@app.route("/magtag/")
def magTag():
    todayLunch = magtaghelper.today_lunch(lunch_url_base, lunch_url_paths, lunch_url_params)
    timeOfDay = magtaghelper.time_of_day()
    weekday = magtaghelper.day_of_week()
    today = magtaghelper.today()
    check_no_school = magtaghelper.check_no_school(cal_url)
    theWeather = weather.getTheWeather(weather_baseurl, weather_latitude, weather_longitude, weather_params)
    return {
            "todayDay": today['Day'],
            "todayMonth": today['Month'],
            "todayYear": today['Year'],
            "timeOfDay": timeOfDay, 
            "weekend": weekday,
            "lunch": todayLunch,
            "schoolday": check_no_school[0],
            "weather": theWeather
            }
