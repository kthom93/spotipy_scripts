import spotipy as sp
import csv
import sys
import spotify_credentials as sc
import spotipy.oauth2 as auth


#   Setup Credentials
credentials = auth.SpotifyClientCredentials(client_id=sc.getClientID(), client_secret=sc.getClientSecret())
token = credentials.get_access_token()
spotify = sp.Spotify(auth=token)

#   Grab the name and number of results
if len(sys.argv) > 2:
    name = sys.argv[1]
    total = int(sys.argv[2])
else:
    print('Usage: python %s <artist name> <number of results>' % sys.argv[0])
    exit()


#   Grab 50 results at a time because of a limit
resultsList = []
collected = 0

while (total > 0):
    if (total > 50):
        num = 50
        total = total - 50
    else:
        num = total
        total = 0
    
    try:
        results = spotify.search(q="artist:" + name, type="artist", limit=num, offset=collected)
    except:
        break
    collected = collected + num
    results = results['artists']['items']
    for item in results:
        genres = []
        for genre in item['genres']:
            genres.append(genre.encode('utf-8').strip())
        resultsList.append(([item['name'].encode('utf-8').strip(), item['popularity'], genres]))

#   Open csvfile
csvfile = open('artist_popularity_sorted.csv', 'w')
csvwriter = csv.writer(csvfile)

#   Write column names
csvwriter.writerow(("Artist Name", "Popularity", "Genres"))

#   Sort based on popularity
resultsList.sort(key= lambda x: x[1], reverse=True)
 
#   Write results to csv
for item in resultsList:
    csvwriter.writerow(item)

#   Close the file
csvfile.close()
