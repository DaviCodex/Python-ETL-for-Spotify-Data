import  spotipy, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 

load_dotenv()

client_id = os.getenv('clientID')
client_secret = os.getenv('clientSecret')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

nombre_artista = 'YSY A'
resultado = sp.search( q='artist' + nombre_artista, type='artist')

artistas = resultado['artists']['items']

lista_artistas = []

for artista in artistas:
    nombre = artista['name']
    type = artista['type']
    id = artista['id']
    lista_artistas.append([nombre,type,id])

df_artists = pd.DataFrame(lista_artistas, columns=['nombre', 'type', 'id'])
print(df_artists)