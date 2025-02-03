import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table

# Carregar os dados
file_path = "DashBoard.xlsx"
df = pd.read_excel(file_path, sheet_name="Folha1")

df.columns = [
    "Mediador", "Código Mediador", "Alínea A (Ano)", "Alínea B (Ano)", "Alínea C (Ano)", "Alínea D (Ano)",
    "Nº 2 do Art. 48º (Ano)", "Ignorar", "Alínea A (Triênio)", "Alínea B (Triênio)", "Alínea C (Triênio)",
    "Alínea D (Triênio)", "Nº 2 do Art. 48º (Triênio)"
]
df = df.iloc[1:].reset_index(drop=True)
df = df.drop(columns=["Ignorar"])
cols_numericas = df.columns[2:]
df[cols_numericas] = df[cols_numericas].apply(pd.to_numeric, errors="coerce")

# Criar a aplicação Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Supervisão de Corretores"),
    
    dash_table.DataTable(
        id='tabela-dados',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
    ),
    
    dcc.Graph(
        id="grafico-dispersao-ano",
        figure=px.scatter(df, x="Alínea A (Ano)", y="Alínea B (Ano)", 
                          color="Mediador", title="Dispersão da Carteira (Ano)",
                          hover_data=["Código Mediador"])
    ),
    
    dcc.Graph(
        id="grafico-dispersao-trienio",
        figure=px.scatter(df, x="Alínea A (Triênio)", y="Alínea B (Triênio)", 
                          color="Mediador", title="Dispersão da Carteira (Triênio)",
                          hover_data=["Código Mediador"])
    ),
    
    dcc.Graph(
        id="grafico-incumprimento",
        figure=go.Figure([
            go.Bar(x=df["Mediador"], y=df["Nº 2 do Art. 48º (Ano)"], name="Ano"),
            go.Bar(x=df["Mediador"], y=df["Nº 2 do Art. 48º (Triênio)"], name="Triênio")
        ]).update_layout(title="Casos de Incumprimento", barmode="group")
    ),
    
    html.Button("Exportar Relatório", id="botao-exportar", n_clicks=0),
    html.Div(id="notificacoes")
])

if __name__ == '__main__':
    app.run_server(debug=True)
