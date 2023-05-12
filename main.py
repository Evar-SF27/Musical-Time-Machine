import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_id = "49589c0674f642b585a71a4980da951a"
spotify_secret = "95fdf9683b954e7eab79911fa1c48939"
redirect_URI = "https://www.localhost:3000/musical_time_machine/"
scope = "playlist-modify-private"

auth_manager = SpotifyOAuth(
    client_id=spotify_id,
    client_secret=spotify_secret,
    redirect_uri=redirect_URI,
    scope=scope,
    cache_path='token.txt'
)
sp = spotipy.Spotify(oauth_manager=auth_manager)

spotify_user_id = "31upvcct7ubf53bvpvqpbqyycegu"

date = input("Which year are you interested in? Type the date in the format YYYY-MM-DD: ")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
billboard_res = requests.get(billboard_url)
billboard_page = billboard_res.text

soup = BeautifulSoup(billboard_page, 'html.parser')

song_title_class = "c-title"
song_artist_class = "c-label"
song_title = soup.select(selector='li h3', class_=song_title_class, id='title-of-a-story')
song_artist = soup.find_all(name="span", class_=song_artist_class)
top_20 = [song.string[14:][0:-5] for song in song_title[:20]]
top_20_artist = [artist.string[4:][0:-1] for artist in song_artist[4:][0:160:4][::2]]

track_dict = {}
for number in range(20):
    track = {'name': top_20[number], 'artist': top_20_artist[number], 'year': date[:4]}
    track_dict[number] = track

song_uri_list = []
for t in track_dict:
    track = track_dict[t]
    name = track['name']
    artist = track['artist']
    year = track['year']
    query = f"track:{name} artist:{artist} year:{year}"
    result = sp.search(q=query, type="track")
    track_found = result['tracks']['items']
    if len(track_found) > 0:
        song_uri = track_found[0]['uri']
        song_uri_list.append(song_uri)

# Creating a new Spotify Playlist
my_playlist = sp.user_playlist_create(
    user=spotify_user_id,
    name=f"{date} Billboard - 20",
    description=f"New Playlist for top 20 songs as of {date}",
    public='false'
)
playlist_id = my_playlist['id']

# Adding tracks to playlist
add_track = sp.playlist_add_items(playlist_id=playlist_id, items=song_uri_list)




