import dash
from dash import html, dcc, Input, Output, dash_table
import pandas as pd


df = pd.read_excel("ZFMR0003 Raporu Örnek.xlsx")

app = dash.Dash(__name__)
app.title = "SAP Raporu - Filtrelenmiş Tablo"

app.layout = html.Div([
    html.H2("SAP Raporu - Kişi ve Sütun Seçimli Tablo"),

    html.Label("Kişi(leri) Seç"),
    dcc.Dropdown(
        id="kisi-sec",
        options=[{"label": kisi, "value": kisi} for kisi in df["Defter"].unique()],
        multi=True,
        placeholder="Kişi Seçin"
    ),

    html.Label("Görmek istediğiniz sütun(ları) seçin"),
    dcc.Dropdown(
        id="sutun-sec",
        options=[{"label": col, "value": col} for col in df.columns if col not in [""]],  # boş sütunları at
        multi=True,
        placeholder="Sütun Seçin (örn: Şubat Bütçe)"
    ),

    html.Br(),
    html.H4("Sonuç Tablosu"),
    html.Div(id="filtreli-tablo")
])

@app.callback(
    Output("filtreli-tablo", "children"),
    [Input("kisi-sec", "value"),
     Input("sutun-sec", "value")]
)
def filtreli_tablo(secili_kisiler, secili_sutunlar):
    if not secili_kisiler or not secili_sutunlar:
        return html.Div("Lütfen kişi ve sütun seçiniz.", style={"color": "gray"})

    df_filtre = df[df["Defter"].isin(secili_kisiler)]

  
    secili_sutunlar = [col for col in secili_sutunlar if col in df_filtre.columns]

   
    gosterilecek_sutunlar = ["Defter"] + secili_sutunlar

    tablo = dash_table.DataTable(
        data=df_filtre[gosterilecek_sutunlar].to_dict("records"),
        columns=[{"name": i, "id": i} for i in gosterilecek_sutunlar],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
    )
    return tablo

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

