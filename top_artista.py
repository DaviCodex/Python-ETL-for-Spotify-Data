import spotipy, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pandasql as ps

if not load_dotenv():
    print("Advertencia: No se encontró el archivo .env")

client_id     = os.getenv('clientID').strip()
client_secret = os.getenv('clientSecret').strip()
redirect_uri  = os.getenv('redirectURI').strip()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope='user-top-read',
    open_browser=False,
))

# Buscar el artista por nombre y obtener su ID
resultado = sp.search(q='Andrés Cepeda', type='artist', limit=1)
artista   = resultado['artists']['items'][0]
artist_id = artista['id']

# Buscar tracks del artista y ordenar por popularidad para simular el top
resultado_tracks = sp.search(q='Andrés Cepeda', type='track', limit=10)
tracks_raw = resultado_tracks['tracks']['items']

# Filtrar solo tracks donde el artista coincide por ID y ordenar por popularidad
tracks_artista = [
    t for t in tracks_raw
    if any(a['id'] == artist_id for a in t['artists'])
]
tracks_artista.sort(key=lambda t: t.get('popularity', 0), reverse=True)

tracks_data = []

for i, track in enumerate(tracks_artista[:5]):
    tracks_data.append({
        'Posicion':             i + 1,
        'Nombre_de_la_cancion': track['name'],
        'Album':                track['album']['name'],
        'Popularidad':          track.get('popularity', 0),
        'Duracion_seg':         track['duration_ms'] // 1000,
    })

df_tracks = pd.DataFrame(tracks_data)
df_tracks.to_csv('top_andres_cepeda.csv', index=False)
print(f"Exportado top_andres_cepeda.csv — {len(df_tracks)} filas\n")

query = """
SELECT Posicion, Nombre_de_la_cancion, Popularidad
FROM df_tracks
ORDER BY Popularidad DESC;
"""

ranking = ps.sqldf(query, locals())
print(ranking)
