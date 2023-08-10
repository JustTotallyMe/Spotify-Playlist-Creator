from webscraper_class import WebScrapeForBBC
from spotify_class import Spotifyer
from configHelper import ConfigHelper
import os
import json

webscraper = WebScrapeForBBC()
configFile = ConfigHelper(os.path.dirname(__file__) + '\\config.txt')
configJson = json.loads(configFile.readFromFile())['settings']

spot = Spotifyer(configJson['id_1'], configJson['id_2'])
selectedBBC_Show = webscraper.GetSongListAsDict(webscraper.GetCorrectUrl())

songIds_1 = [spot.GetTrackIdForSong(selectedBBC_Show[key], key, True) for key in selectedBBC_Show]
songIds_2 = [spot.GetTrackIdForSong(selectedBBC_Show[key], key, False) for key in selectedBBC_Show]

songIds_1 = list(map(lambda songLst1, songsLst2: songsLst2 if songLst1['id'] == '00' else songLst1, songIds_1, songIds_2))

listWithIds = ["spotify:track:" + entry['id'] for entry in songIds_1 if entry['id'] != '00']

for track in listWithIds:
    print(track)

try:
    spot.ReplaceAllItemsInPlaylist(configJson['playlist_id'], listWithIds)
except BaseException:
    print('Error found')
finally:
    print('Es wurden ' + str(len(listWithIds)) + " Songs der Playlist " + configJson['playlist_id'] + " hinzugefuegt.")