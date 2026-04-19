import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "264a01a83a4546b3803999522500ca26"
CLIENT_SECRET = "82dad5576aa843138be3250ff32531f0"

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def get_recommendations(query):

    songs_result = sp.search(q=query, limit=10, type='track')
    songs = []

    for track in songs_result['tracks']['items']:
        if track and track.get('name') and track.get('artists'):
            songs.append({
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "url": track['external_urls']['spotify']
            })

    playlist_result = sp.search(q=query, limit=5, type='playlist')
    playlists = []

    for pl in playlist_result['playlists']['items']:
        if pl and pl.get('name') and pl.get('external_urls'):
            playlists.append({
                "name": pl['name'],
                "url": pl['external_urls']['spotify']
          })

    return songs, playlists