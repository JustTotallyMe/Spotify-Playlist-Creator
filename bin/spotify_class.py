import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import re


class Spotifyer:
    def __init__(self, clientId, clientSecret):
        self.userID = None
        # self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret))
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId, client_secret=clientSecret,
                                                            redirect_uri='http://localhost:9000',
                                                            scope='playlist-modify-private'))

    def GetTrackIdForSong(self, title, artist, searchWithArtist):
        if searchWithArtist:
            queryString = "track: " + title + " artist:" + artist
        else:
            queryString = "track: " + title

        result = self.sp.search(q=queryString, type='track', limit=50)

        for song in result['tracks']['items']:
            foundArtist = song['artists'][0]['name']
            url = song['external_urls']['spotify']
            foundTitle = song['name']

            regExedTitle = re.sub(r"[^a-zA-Z0-9]", "", title).lower()
            regExedArtist = re.sub(r"[^a-zA-Z0-9]", "", artist).lower()
            regExedFoundArtist = re.sub(r"[^a-zA-Z0-9]", "", foundArtist).lower()
            regExedFoundTitle = re.sub(r"[^a-zA-Z0-9]", "", foundTitle).lower()

            if \
                    (
                            regExedFoundTitle == regExedTitle or regExedTitle in regExedFoundTitle or regExedFoundTitle in regExedTitle) \
                            and \
                            (
                                    regExedFoundArtist == regExedArtist or regExedFoundArtist in regExedArtist or regExedArtist in regExedFoundArtist):
                return {'id': song['id'], 'url': url}
        else:
            return {'id': '00', 'url': ""}

    def GetUserID(self):
        self.userID = self.sp.current_user()["id"]
        print(self.userID)

    def GetCurUsersPlaylists(self):
        return self.sp.current_user_playlists()

    def ReplaceAllItemsInPlaylist(self, playlistId, listOfTracks):
        self.sp.playlist_replace_items(playlistId, listOfTracks)
