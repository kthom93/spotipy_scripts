import spotipy as sp
import csv
import sys
import spotify_credentials as sc
import spotipy.oauth2 as auth

#   Setup Credentials
credentials = auth.SpotifyClientCredentials(client_id=sc.getClientID(), client_secret=sc.getClientSecret())
token = credentials.get_access_token()
spotify = sp.Spotify(auth=token)

#   Grab the track hint
if len(sys.argv) > 2:
    name = sys.argv[1]
    total = int(sys.argv[2])
else:
    print('Usage: python %s <track hint> <number of results>' % sys.argv[0])
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
        results = spotify.search(q="track:" + name, type="track", limit=50, offset=collected)
    except:
        break
    collected = collected + num
    results = results['tracks']['items']

    for track in results:
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'].encode('utf-8').strip())
        seconds = (track['duration_ms'] / 1000) % 60
        minutes = (track['duration_ms'] / (1000 * 60)) % 60
        resultsList.append((track['name'].encode('utf-8').strip(), track['duration_ms'], track['album']['name'].encode('utf-8').strip(), artists, track['album']['release_date'], ("%d:%d" % (minutes, seconds))))

#   Sort based on song length
resultsList.sort(key= lambda x: x[1], reverse=True)
        
#   Open csvfile
csvfile = open('song_duration_sorted.csv', 'w')
csvwriter = csv.writer(csvfile)

#   Write Column Headers
csvwriter.writerow(("Track Name", "Milliseconds", "Album",  "Artists", "Date Released", "Formatted Time"))

#   Write results
for item in resultsList:
    csvwriter.writerow(item)

#   Close the file
csvfile.close()
