import spotipy, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pandasql as ps

if not load_dotenv():
    print("Advertencia: No se encontró el archivo .env")

client_id = os.getenv('clientID').strip()
client_secret = os.getenv('clientSecret').strip()
redirect_uri = os.getenv('redirectURI').strip()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope='user-top-read',
    open_browser=False
))

time_ranges = {
    'short_term':  'Último mes',
    'medium_term': 'Últimos 6 meses',
    'long_term':   'Histórico',
}

tracks_data = []

for time_range, label in time_ranges.items():
    results = sp.current_user_top_tracks(limit=50, time_range=time_range)
    for i, track in enumerate(results['items']):
        tracks_data.append({
            'Posicion':             i + 1,
            'Nombre_de_la_cancion': track['name'],
            'Artistas':             ', '.join(a['name'] for a in track['artists']),
            'Popularidad':          track.get('popularity', 0),
            'Periodo':              label,
        })

df_tracks = pd.DataFrame(tracks_data)
df_tracks.to_csv('my_top_tracks.csv', index=False)
print(f"✅ Exportado top_tracks_latam.csv — {len(df_tracks)} filas")


query="""
SELECT * FROM df_tracks 
WHERE Periodo='Último mes' AND Posicion IN (1,2,3,4,5)
ORDER BY Posicion
LIMIT 10;
"""

top_5_ultimomes= ps.sqldf(query, locals())
print(top_5_ultimomes)