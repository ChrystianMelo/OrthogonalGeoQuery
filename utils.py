
import urllib.request

from typing import List, Tuple
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from typing import Dict, Tuple
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

class KDNode:
    __slots__ = ("point", "idx", "left", "right")
    def __init__(self, point: Tuple[float, float], idx: int):
        self.point, self.idx = point, idx
        self.left: "KDNode | None" = None
        self.right: "KDNode | None" = None

def build_kd(arr: List[Tuple[Tuple[float, float], int]], depth=0):
    if not arr:
        return None
    axis = depth % 2
    arr.sort(key=lambda p: p[0][axis])
    mid = len(arr) // 2
    node = KDNode(arr[mid][0], arr[mid][1])
    node.left = build_kd(arr[:mid], depth + 1)
    node.right = build_kd(arr[mid + 1 :], depth + 1)
    return node

def range_search(node: "KDNode | None", bbox: Tuple[float, float, float, float], depth=0, acc=None):
    if node is None:
        return acc or []
    if acc is None:
        acc = []
    x, y = node.point
    xmin, ymin, xmax, ymax = bbox
    if xmin <= x <= xmax and ymin <= y <= ymax:
        acc.append(node.idx)
    axis = depth % 2
    if (axis == 0 and xmin <= x) or (axis == 1 and ymin <= y):
        range_search(node.left, bbox, depth + 1, acc)
    if (axis == 0 and x <= xmax) or (axis == 1 and y <= ymax):
        range_search(node.right, bbox, depth + 1, acc)
    return acc