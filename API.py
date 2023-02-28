import requests

# Set up Spotify API credentials
client_id = 'ba3be61013ee482fb007df10ea6ebae6'
client_secret = 'dbff0dcdee5740f6ab707a2af9205e02'

# Get an access token
auth_url = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
})
access_token = auth_response.json()['access_token']

# Set up headers with the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Get the tracks of the global top songs playlist
playlist_id = '37i9dQZEVXbMDoHDwVN2tF' # This is the playlist ID for the global top songs
response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers)

# Get the top 10 songs, artists and album images
top_songs = response.json()['items']
song_data = []
for i,song in enumerate(top_songs[:10]):
    song_name = song["track"]["name"]
    artist_name = song["track"]["artists"][0]["name"]
    album_id = song["track"]["album"]["id"]
    album_response = requests.get(f'https://api.spotify.com/v1/albums/{album_id}', headers=headers)
    album_image_url =album_response.json()['images'][0]['url']
    song_data.append({'song_name': song_name,'artist_name':artist_name,'album_image_url':album_image_url})

#print the song_data
print(song_data)

    

