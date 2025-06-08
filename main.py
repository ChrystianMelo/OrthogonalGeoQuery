import os
import urllib.request
import pandas as pd

import filtrar_csv

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from typing import Dict, Tuple
# (opcional) `pip install tqdm` para visual da barra
from tqdm import tqdm

def downloadFile(url, filename):
    """
    Baixa um arquivo da URL fornecida, caso ele ainda não exista localmente.

    Parâmetros:
        url (str): URL do arquivo a ser baixado.
        filename (str): Nome do arquivo local onde o conteúdo será salvo.
    """
    print(f"[↓] Baixando '{filename}'...")

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"[✔] Download concluído e salvo como '{filename}'")
    except Exception as e:
        print(f"[✗] Erro ao baixar: {e}")

def getCoordinates(csv_path: str,
                    progress: bool = True,
                    cache_ok: bool = True) -> Dict[int, Tuple[float, float]]:
    """
    Geocodifica endereços (coluna ENDERECO) usando Nominatim
    e devolve {ID: (lat, lon)} com barra de progresso.

    • `progress`   – exibe barra tqdm se True.
    • `cache_ok`   – evita repetir consultas p/ endereços já vistos.
    """
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8', on_bad_lines='skip')

    geolocator = Nominatim(user_agent="alg2_geocoder_bh", timeout=10)
    geocode    = RateLimiter(
        geolocator.geocode,
        min_delay_seconds=1,
        max_retries=5,
        error_wait_seconds=2,
    )

    coords: Dict[int, Tuple[float, float]] = {}
    cache:  Dict[str, Tuple[float, float]] = {}

    iterator = tqdm(df.itertuples(index=False), total=len(df)) if progress else df.itertuples(index=False)

    for row in iterator:
        ender = row.ENDERECO
        estid = row.ID_ATIV_ECON_ESTABELECIMENTO

        # cache simples p/ endereços duplicados
        if cache_ok and ender in cache:
            coords[estid] = cache[ender]
            continue

        loc = geocode(ender)
        if loc:
            coords[estid] = (loc.latitude, loc.longitude)
            if cache_ok:
                cache[ender] = coords[estid]

    return coords

def saveCoordinatesToCsv(coords: Dict[int, Tuple[float, float]],
                            output_path: str,
                            sep: str = ';') -> None:
    """
    Salva dicionário {ID: (lat, lon)} em `output_path`.

    Colunas: ID_ATIV_ECON_ESTABELECIMENTO, LATITUDE, LONGITUDE
    """
    df_out = pd.DataFrame(
        [(id_, lat, lon) for id_, (lat, lon) in coords.items()],
        columns=["ID_ATIV_ECON_ESTABELECIMENTO", "LATITUDE", "LONGITUDE"]
    )
    df_out.to_csv(output_path, sep=sep, index=False, encoding='utf-8')
    print(f"[✓] Coordenadas salvas em: {output_path}")


if __name__ == '__main__':
    import os
    print(os.getcwd())
    url = "https://ckan.pbh.gov.br/dataset/ec3efaac-0ca6-4846-9e32-0ffff2d76dbb/resource/a35a0ed3-c933-4919-b23f-b925c37b64b8/download/20250401_atividade_economica.csv"
    filename = "data/20250401_atividade_economica.csv"
    
    # Garante que a pasta 'data' existe
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists(filename):
        downloadFile(url, filename)
    else:
        print(f"[✓] O arquivo '{filename}' já existe. Nenhum download necessário.")

    filteredData = 'data/atividade_economica_filtrada.csv'
    if not os.path.exists(filteredData):
        filtrar_csv.main(filename, filteredData)
    else:
        print(f"[✓] O arquivo '{filteredData}' já existe. Nenhum processo necessário.")

    # 2) Salva em CSV separado
    coordinates = "data/cordenadas_bares_restaurantes.csv"
    if not os.path.exists(coordinates):
        saveCoordinatesToCsv(getCoordinates(filteredData), filteredData)
    else:
        print(f"[✓] O arquivo '{coordinates}' já existe. Nenhum processo necessário.")