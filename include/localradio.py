from defusedxml import ElementTree as xmlparser
from include import localsystem
import requests
import vlc

# VLC controlling

def isVLC():
    return localsystem.processIsRunning('vlc')

def checkIsPlaying(player):
    if player.is_playing():
        return True
    else:
        return False

def stopAllPlayers(players):
    for station in players:
        if checkIsPlaying(players[station]) == True:
            player.stop()
    return True

# XSPF file parsing via defusedxml

# expect wyms to be a URL so we can gret fresh data
def getWYMSXML(wymsXML=""):
    xmlfile = requests.get(wymsXML)
    parsedXML = xmlparser.fromstring(xmlfile.text)
    return parsedXML

# get the track name from WYMS's XML file. This is specific to WYMS for now because
# there is no standard for how these XPSF files are meant to work. It could be
# different for other stations or even Radio Milwaukee streams.
#
# There are admittedly a lot of assumptions going on here, the main one being that
# the track information is the third item's (root[2]) only child's (root[2][0])
# second child (root[2][0][1]).

def getWYMSTrackInfo(parsedXML):
    return parsedXML[2][0][1].text

def getWYMSStationName(parsedXML):
    return parsedXML[2][0][2].text.split('\n')[0].split(' ')[2]