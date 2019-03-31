# spotipy_scripts
Spotify api (spotipy) used to gather artist and music information.

In order to use, install spotipy

$pip install spotipy

Run scripts

$python artist_popularity.py <name> <number of results>
Enter any name and script will return the number of results of artists with that name sorted by popularity.
Exports to artist_popularity_sorted.csv

$python song_by_word_sorted.py <track hint> <number of results>
Enter a track hint and script will return the number of results of tracks with that hint included in it.
List is sorted by track length.
Exports to song_duration_sorted.csv

$python recommend_playlist_genre <seed genre> <number or results>
Enter a seed genre and script will return the number of results of playlists generated from the seed.
Tracks sorted by popularity.
Exports to recommend_playlist_sorted.cvs


Credentials

spotify_credentials
Simple helper script that stores the credentials of the developer.
