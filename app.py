# app.py
import json
from pathlib import Path

import dash
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash import html, Output, Input, State   # ← importa daqui

# ------------------------------------------------------------------
# 1. GeoJSON dos estabelecimentos
# ------------------------------------------------------------------
with open(Path("data/bares_restaurantes.geojson"), encoding="utf-8") as f:
    geojson_data = json.load(f)

# ------------------------------------------------------------------
# 2. Camada GeoJSON com clustering nativo
# ------------------------------------------------------------------
geojson_layer = dl.GeoJSON(
    id="geojson",
    data=geojson_data,
    zoomToBounds=True,
    superClusterOptions=dict(radius=60, maxClusterRadius=80),
    children=[dl.Popup(id="popup")],      # popup reutilizável
)

# ------------------------------------------------------------------
# 3. Instancia o app Dash
# ------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder="assets",
)
server = app.server

# ------------------------------------------------------------------
# 4. Layout
# ------------------------------------------------------------------
app.layout = dbc.Container(
    [
        html.H2("Bares & Restaurantes de BH", className="my-2"),
        dl.Map(
            [dl.TileLayer(), geojson_layer],
            id="map",
            center=[-19.92, -43.94],
            zoom=12,
            style={"height": "70vh", "width": "100%", "margin": "auto"},
        ),
    ],
    fluid=True,
)

# ------------------------------------------------------------------
# 5. Callback 100 % client-side para popup
# ------------------------------------------------------------------
app.clientside_callback(
    """
    function (feature, latlng) {
        if (!feature) { return [window.dash_clientside.no_update,
                                window.dash_clientside.no_update]; }
        const p = feature.properties;
        return [latlng,
                `<b>${p.nome}</b><br>${p.endereco}`];
    }
    """,
    [Output("popup", "position"),
     Output("popup", "children")],
    Input("geojson", "click_feature"),
    State("geojson", "click_lat_lng"),
)

# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
