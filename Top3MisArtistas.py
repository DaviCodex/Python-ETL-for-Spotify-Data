import spotipy, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pandasql as ps
# Cargamos el .env
if not load_dotenv():
    print("Advertencia: No se encontró el archivo .env")

#Credenciales
client_id     = os.getenv('clientID').strip()
client_secret = os.getenv('clientSecret').strip()
redirect_uri  = os.getenv('redirectURI').strip()

#OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope='user-top-read',
    open_browser=False,
))
#Mi top 5 artistas
top5_artistas = sp.current_user_top_artists(limit=5)

tracks_data = []

for pos_artista, artista in enumerate(top5_artistas['items'], start=1):
    #El id y nombre de mi top 5 artistas
    id_artista     = artista['id']
    nombre_artista = artista['name']
    #Search de 10 resultados con el nombre del artista
    tracks_artista = sp.search(q=nombre_artista, type='track', limit=10)
    tracks = [
        t for t in tracks_artista['tracks']['items']
        if any(a['id'] == id_artista for a in t['artists'])
    ]
    tracks.sort(key=lambda t: t.get('popularity', 0), reverse=True)
    top_3 = tracks[:3]

    for pos_track, track in enumerate(top_3, start=1):
        tracks_data.append({
            'Posicion_artista':     pos_artista,
            'Artista':              nombre_artista,
            'Posicion_cancion':     pos_track,
            'Cancion':              track['name'],
            'Album':                track['album']['name'],
            'Popularidad':          track.get('popularity', 0),
            'Duracion_seg':         track['duration_ms'] // 1000,
        })

df_tracks = pd.DataFrame(tracks_data)
df_tracks.to_csv('top3_mis_artistas.csv', index=False)
print(f"Exportado top3_mis_artistas.csv — {len(df_tracks)} filas\n")
print(df_tracks.to_string(index=False))