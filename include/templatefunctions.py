from include import loadconfig, localnetwork, localsystem, localradio
from include import localtime, streamRadio
import subprocess


# return a tuple of players where is_playing() is True
def getActivePlayers(PLAYERS):
    activePlayers = []
    for player in PLAYERS:
        if PLAYERS[player].is_playing():
            activePlayers.append(player)
    return activePlayers


def getStoppedPlayers(PLAYERS):
    stoppedPlayers = []
    for player in PLAYERS:
        if not PLAYERS[player].is_playing():
            stoppedPlayers.append(player)
    return stoppedPlayers


def getSysInfo():
    return {
        "cpu": localsystem.getCPU(),
        "disk": localsystem.getDF(),
        "network": (localnetwork.isConnected(), localnetwork.currentIP())
    }


def getIndexData(PLAYERS):
    indexdata = {}
    indexdata['sysinfo'] = getSysInfo()
    indexdata['playing-stations'] = getActivePlayers(PLAYERS)
    indexdata['stopped-stations'] = getStoppedPlayers(PLAYERS)
    indexdata['all-stations'] = PLAYERS
    return indexdata


def radioStreamQueryArgs(request, status, player, UNSUPPORTED, PLATFORM):
    # Determine what to do. If "play" supplied, play the requested stream
    if 'play' in request.args.keys():
        if not player.is_playing():
            player.play()
    # if "stop" supplied, stop the requested stream
    elif 'stop' in request.args.keys():
        player.stop()
        status['status'] = "stopped"
    # if "volume" specified, set the volume to the requested value
    elif 'volume' in request.args.keys():
        volume = request.args.get('volume')
        status['volume'] = volume
        # Do nothing on Mac, Windows, other unsupported systems
        if PLATFORM in UNSUPPORTED:
            print("{}} Would have set to {}%".format(UNSUPPORTED, volume))
        # else adjust the volume.
        else:
            setVol = "amixer sset 'Headphone' {}%".format(volume)
            subprocess.check_output(setVol, shell=True)
    return status
