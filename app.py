from flask import Flask, render_template, request
import sys
import platform
from include import localradio, localsystem, localtime, localnetwork
from include import streamRadio, loadconfig, templatefunctions
import vlc
import subprocess
from flask_bootstrap import Bootstrap5
from flask import Flask

CONFIG = loadconfig.loadconfig("config.yml")
STATIONS = CONFIG['radio']['stations']
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
    now_playing = []
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
    status['status'] = "playing" if player.is_playing() else "stopped"
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
