import spotipy as sp
import csv
import sys
import spotify_credentials as sc
import spotipy.oauth2 as auth

#   Setup Credentials
credentials = auth.SpotifyClientCredentials(client_id=sc.getClientID(), client_secret=sc.getClientSecret())
token = credentials.get_access_token()
spotify = sp.Spotify(auth=token)

#   Grab the seed genre and number of results  or output application usage
if len(sys.argv) > 2:
    genre = sys.argv[1]
    total = int(sys.argv[2])
else:
    print('Usage: python %s <seed genre> <number of results>' % sys.argv[0])
    exit()

#   Grab 50 results at a time because of a limit
resultsList = []
collected = 0

while (total > 0):
    if (total > 0):
        num = 50
        total = total - 50
    else:
        num = total
        total = 0
    try:
        results = spotify.recommendations(seed_genres=[genre], limit=50, offset=collected)
    except:
        break
    collected = collected + num
    results = results['tracks']

    for track in results:
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'].encode('utf-8').strip())
        preview = track['preview_url']
        if (preview != None):
            preview = preview.encode('utf-8').strip()
        resultsList.append((track['name'].encode('utf-8').strip(), track['popularity'], artists, track['album']['name'].encode('utf-8').strip(), preview))

#   Sort based on track popularity
resultsList.sort(key= lambda x: x[1], reverse=True)
        
#   Open csvfile
csvfile = open('recommend_playlist_sorted.csv', 'w')
csvwriter = csv.writer(csvfile)

#   Write Column Headers
csvwriter.writerow(("Track Name", "Popularity", "Artists", "Album", "Preview URL"))

#   Write results
for item in resultsList:
    csvwriter.writerow(item)

#   Close the file
csvfile.close()
