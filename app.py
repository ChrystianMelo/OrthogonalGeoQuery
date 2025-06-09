# app.py – mapa interativo com clustering, seleção retangular e busca ortogonal (k‑d tree)
# Funciona em dash‑leaflet ≥1.1.x (somente EditControl).
# EditControl deve ficar dentro de um FeatureGroup; usamos edit={"edit": False, "remove": True}.

import json
from pathlib import Path
from typing import List, Tuple

import utils

import dash
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash import html, Output, Input, State
from dash import dash_table

###########################################################################
# 1. Carrega GeoJSON dos estabelecimentos
###########################################################################
GEOJSON_PATH = Path("data/bares_restaurantes.geojson")
with GEOJSON_PATH.open(encoding="utf-8") as f:
    geojson_data = json.load(f)

points: List[Tuple[float, float]] = [
    (feat["geometry"]["coordinates"][0], feat["geometry"]["coordinates"][1])
    for feat in geojson_data["features"]
]

###########################################################################
# 2. Implementa k‑d tree e busca ortogonal
###########################################################################

root = utils.build_kd([(pt, i) for i, pt in enumerate(points)])

###########################################################################
# 3. Camadas Leaflet: GeoJSON + FeatureGroup + EditControl
###########################################################################
geojson_layer = dl.GeoJSON(
    id="geojson",
    data=geojson_data,
    zoomToBounds=True,
    superClusterOptions=dict(radius=60, maxClusterRadius=80),
    children=[dl.Popup(id="popup")],
)

edit_control = dl.EditControl(
    id="draw",
    position="topleft",
    draw={
        "rectangle": True,
        "polygon": False,
        "circle": False,
        "polyline": False,
        "marker": False,
        "circlemarker": False,
    },
    edit={"edit": False, "remove": True},
)

feature_group = dl.FeatureGroup([edit_control], id="draw-layer")

###########################################################################
# 4. Instancia o app Dash
###########################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

###########################################################################
# 5. Layout
###########################################################################
app.layout = dbc.Container(
    [
        html.H2("Bares & Restaurantes de BH", className="my-2"),
        dl.Map(
            [dl.TileLayer(), geojson_layer, feature_group],
            id="map",
            center=[-19.92, -43.94],
            zoom=12,
            style={"height": "70vh", "width": "100%", "margin": "auto"},
        ),
        html.Div(id="info", className="mt-2"),
    ],
    fluid=True,
)

###########################################################################
# 6. Popup client‑side
###########################################################################
app.clientside_callback(
    """
    function(feature, latlng){
      if(!feature) return [window.dash_clientside.no_update, window.dash_clientside.no_update];
      const p = feature.properties;
      return [latlng, `<b>${p.nome}</b><br>${p.endereco}`];
    }
    """,
    [Output("popup", "position"), Output("popup", "children")],
    Input("geojson", "click_feature"), State("geojson", "click_lat_lng"),
)

###########################################################################
# 7. Callback Python – busca ortogonal quando retângulo é criado
###########################################################################
@app.callback(Output("info", "children"), Input("draw", "geojson"), prevent_initial_call=True)
def on_rectangle(selection_geojson):
    if not selection_geojson or len(selection_geojson.get("features", [])) == 0:
        return dash.no_update
    coords = selection_geojson["features"][-1]["geometry"]["coordinates"][0]
    xs, ys = zip(*coords)
    bbox = (min(xs), min(ys), max(xs), max(ys))
    hits = utils.range_search(root, bbox)

    if not hits:
        return "Nenhum estabelecimento encontrado."

    selected_features = [geojson_data["features"][i]["properties"] for i in hits]

    columns = [{"name": col.capitalize(), "id": col} for col in selected_features[0].keys()]

    return dash_table.DataTable(
        data=selected_features,
        columns=columns,
        page_size=len(selected_features),  # Exibe todos os itens
        style_table={
            "overflowX": "auto",
            "overflowY": "auto",
            "height": "300px"  # Altura fixa para rolagem vertical
        },
        fixed_rows={'headers': True},  # Cabeçalho fixo ao rolar
    )

###########################################################################
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')