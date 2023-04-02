import vlc

# Create a VLC player using the URL to stream.
def createPlayer(streamURL):
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(streamURL)
    MediaList = Instance.media_list_new([streamURL])
    Media.get_mrl()
    player.set_media(Media)
    list_player = Instance.media_list_player_new()
    list_player.set_media_list(MediaList)
    return list_player

def prepStream(streamURI):
    stream = vlc.MediaPlayer(streamURI)
    return stream

def playStream(player):
    return player.play()
