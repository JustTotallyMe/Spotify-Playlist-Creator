from webscraper_class import WebScrapeForBBC
from spotify_class import Spotifyer
from configHelper import ConfigHelper
import os
import json
from sys import argv

test = WebScrapeForBBC()
configFile = ConfigHelper(os.path.dirname(__file__) + '\\config.txt')
configJson = json.loads(configFile.readFromFile())['settings']

spot = Spotifyer(configJson['id_1'], configJson['id_2'])
selectedBBC_Show = test.GetSongListAsDict(argv[1])

songIds_1 = []
songIds_2 = []

for key in selectedBBC_Show:
    songIds_1.append(spot.GetTrackIdForSong(selectedBBC_Show[key], key, True))

for key in selectedBBC_Show:
    songIds_2.append(spot.GetTrackIdForSong(selectedBBC_Show[key], key, False))

for i in range(len(songIds_1)):
    if songIds_1[i]['id'] == '00':
        songIds_1[i] = songIds_2[i]

listWithIds = []

for entry in songIds_1:
    songId = entry['id']
    if songId != '00':
        listWithIds.append("spotify:track:" + entry['id'])
        print("spotify:track:" + entry['id'])

try:
    spot.ReplaceAllItemsInPlaylist(configJson['playlist_id'], listWithIds)
except BaseException:
    print('Error found')
finally:
    print('Es wurden ' + str(len(listWithIds)) + " Songs der Playlist " + configJson['playlist_id'] + " hinzugefuegt.")