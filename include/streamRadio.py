import vlc


# Create a VLC list player for a stream URL. Returns the list player;
# use getState()/describeState() to inspect playback health.
def createPlayer(streamURL):
    Instance = vlc.Instance()
    MediaList = Instance.media_list_new([streamURL])
    list_player = Instance.media_list_player_new()
    list_player.set_media_list(MediaList)
    return list_player


# Map a player's VLC state to a simple status string for the UI/API.
def getStatus(player):
    state = player.get_state()
    if state == vlc.State.Error:
        return "error"
    if state in (vlc.State.Opening, vlc.State.Buffering):
        return "connecting"
    if player.is_playing():
        return "playing"
    return "stopped"


# After calling play(), wait briefly for VLC to either start playing or
# fail, so the API response can report a real outcome instead of a guess.
def waitForOutcome(player, timeout=3.0, interval=0.2):
    import time
    waited = 0.0
    while waited < timeout:
        state = player.get_state()
        if state == vlc.State.Error:
            return "error"
        if player.is_playing():
            return "playing"
        time.sleep(interval)
        waited += interval
    return getStatus(player)
