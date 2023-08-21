import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
URL = "https://www.popvortex.com/music/charts/top-reggaeton-songs.php"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
all_songs = soup.find_all(class_="title")
song_title = [song.getText() for song in all_songs]

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="CLIENT-ID",
        client_secret="CLIENT-SECRET",
        show_dialog=True,
        cache_path="token.txt",
        username="USERNAME",
    )
)

user_id = sp.current_user()["id"]

#Searching Spotify for songs by title
song_uris = []
for song in song_title:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
