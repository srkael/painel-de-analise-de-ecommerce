import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================
# CONFIGURAÇÕES INICIAIS E CARREGAMENTO DE DADOS
# ==============================================

# Caminho absoluto para o arquivo CSV (compatível com Render)
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'ecommerce_estatistica.csv')

try:
    df = pd.read_csv(csv_path)
    
    # Conversão de tipos numéricos
    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')
    
    # Remoção de valores nulos
    df = df.dropna(subset=['Preço', 'Qtd_Vendidos'])

except Exception as e:
    print(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame()  # DataFrame vazio para evitar erros

# ==============================================
# FUNÇÕES AUXILIARES PARA GRÁFICOS (mantidas originais)
# ==============================================

def criar_histograma():
    """Cria histograma de preços com intervalo personalizado"""
    fig = px.histogram(
        df,
        x='Preço',
        nbins=30,
        title="Distribuição dos Preços dos Produtos",
        labels={'Preço': 'Preço (R$)'},
        color_discrete_sequence=['#636EFA'],
        template="plotly_white"
    )
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Preço (R$)",
        yaxis_title="Quantidade de Produtos"
    )
    return fig

def criar_dispersao():
    """Cria gráfico de dispersão entre preço e avaliações"""
    fig = px.scatter(
        df,
        x='Preço',
        y='N_Avaliações',
        color='Qtd_Vendidos',
        title="Relação entre Preço, Avaliações e Quantidade Vendida",
        labels={
            'Preço': 'Preço (R$)',
            'N_Avaliações': 'Número de Avaliações',
            'Qtd_Vendidos': 'Quantidade Vendida'
        },
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

def criar_heatmap():
    """Cria mapa de calor de correlações"""
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numerical_df.corr()

    fig = px.imshow(
        correlation_matrix,
        title="Mapa de Calor das Correlações entre Variáveis Numéricas",
        color_continuous_scale='Blues',
        text_auto=True,
        aspect="auto"
    )
    fig.update_layout(
        xaxis_title="Variáveis",
        yaxis_title="Variáveis"
    )
    return fig

def criar_barras():
    """Cria gráfico de barras das marcas mais populares"""
    marcas = df['Marca'].value_counts().head(7)
    fig = px.bar(
        marcas,
        x=marcas.index,
        y=marcas.values,
        title="Top 7 Marcas mais Populares",
        labels={'x': 'Marca', 'y': 'Quantidade de Produtos'},
        color=marcas.index,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(showlegend=False)
    return fig

def criar_pizza():
    """Cria gráfico de pizza da distribuição de gêneros"""
    generos = df['Gênero'].value_counts().head(3)
    fig = px.pie(
        generos,
        values=generos.values,
        names=generos.index,
        title="Distribuição dos Produtos por Gênero (Top 3)",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def criar_densidade():
    """Cria gráfico de densidade de preços"""
    fig = px.density_contour(
        df,
        x="Preço",
        title="Densidade dos Preços",
        color_discrete_sequence=['#00CC96']
    )
    fig.update_traces(contours_coloring="fill", contours_showlabels=True)
    fig.update_layout(
        xaxis_title="Preço (R$)",
        yaxis_title="Densidade"
    )
    return fig

def criar_regressao():
    """Cria gráfico de regressão linear"""
    try:
        fig = px.scatter(
            df,
            x="Preço",
            y="Qtd_Vendidos",
            trendline="ols",
            title="Regressão Linear: Preço vs Quantidade Vendida",
            labels={
                'Preço': 'Preço (R$)',
                'Qtd_Vendidos': 'Quantidade Vendida'
            },
            color_discrete_sequence=['#EF553B']
        )
        fig.update_layout(
            plot_bgcolor='rgba(240,240,240,0.8)',
            paper_bgcolor='rgba(240,240,240,0.5)'
        )
        return fig
    except Exception as e:
        return html.Div([
            html.H4("Erro ao gerar gráfico de regressão"),
            html.P("Por favor, instale a biblioteca statsmodels:"),
            html.Pre("pip install statsmodels"),
            html.P(f"Detalhes do erro: {str(e)}")
        ], style={'color': 'red', 'padding': '20px'})

# ==============================================
# INICIALIZAÇÃO DO APP DASH - ORDEM CORRIGIDA
# ==============================================

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# ==============================================
# LAYOUT DA APLICAÇÃO
# ==============================================

app.layout = html.Div([
    html.Div([
        html.H1(
            "📊 Painel de Análise de E-commerce",
            style={
                'textAlign': 'center',
                'color': '#2a3f5f',
                'marginBottom': '30px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),

        html.Div([
            html.Div([
                html.Label(
                    "Selecione o tipo de análise:",
                    style={
                        'fontWeight': 'bold',
                        'marginBottom': '10px'
                    }
                ),
                dcc.Dropdown(
                    id='grafico-selecionado',
                    options=[
                        {'label': '📈 Histograma de Preços', 'value': 'histograma'},
                        {'label': '🟢 Dispersão: Preço vs Avaliações', 'value': 'dispersao'},
                        {'label': '🔥 Mapa de Calor de Correlações', 'value': 'heatmap'},
                        {'label': '📊 Barras: Marcas Populares', 'value': 'barras'},
                        {'label': '🍕 Pizza: Distribuição de Gêneros', 'value': 'pizza'},
                        {'label': '🌊 Densidade de Preços', 'value': 'densidade'},
                        {'label': '📉 Regressão Linear (Preço vs Qtd Vendida)', 'value': 'regressao'}
                    ],
                    value='histograma',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], className="six columns", style={'marginBottom': '30px'}),

            html.Div([
                html.Label(
                    "📌 Informações do Dataset:",
                    style={'fontWeight': 'bold'}
                ),
                html.Ul([
                    html.Li(f"Total de produtos: {len(df)}"),
                    html.Li(f"Média de preço: R${df['Preço'].mean():.2f}"),
                    html.Li(f"Produto mais caro: R${df['Preço'].max():.2f}")
                ])
            ], className="six columns", style={'paddingLeft': '20px'})
        ], className="row"),

        html.Div(id='output-grafico', style={'marginTop': '20px'})
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': 'white',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
        'borderRadius': '5px'
    })
])

# ==============================================
# CALLBACKS
# ==============================================

@app.callback(
    Output('output-grafico', 'children'),
    [Input('grafico-selecionado', 'value')]
)
def atualizar_grafico(grafico):
    if df.empty:
        return html.Div("Erro: Não foi possível carregar os dados.", style={'color': 'red'})

    graficos = {
        'histograma': criar_histograma,
        'dispersao': criar_dispersao,
        'heatmap': criar_heatmap,
        'barras': criar_barras,
        'pizza': criar_pizza,
        'densidade': criar_densidade,
        'regressao': criar_regressao
    }

    figura = graficos.get(grafico, lambda: go.Figure())()

    if isinstance(figura, html.Div):
        return figura

    return dcc.Graph(
        figure=figura,
        style={
            'height': '600px',
            'border': '1px solid #eee',
            'borderRadius': '5px',
            'padding': '10px'
        }
    )

# ==============================================
# CONFIGURAÇÃO PARA DEPLOY NO RENDER - PARTE CRÍTICA
# ==============================================

# Esta linha é essencial para o Gunicorn no Render
server = app.server

# Execução local (não usado no Render)
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)