"""
ANÁLISE DE DADOS DE E-COMMERCE COM DASH
=======================================

Este código cria um painel interativo para análise de dados de produtos de e-commerce.
Ele utiliza a biblioteca Dash (baseada em Flask) para criar uma aplicação web com gráficos interativos.

ESTRUTURA DO CÓDIGO:
1. Importações de bibliotecas
2. Configurações iniciais e carregamento de dados
3. Funções auxiliares para criação de gráficos
4. Inicialização da aplicação Dash
5. Definição do layout da interface
6. Callbacks para interatividade
7. Configurações para deploy

Autor: [Seu Nome]
Data: [Data]
Versão: 1.0
"""

# ==============================================
# 1. IMPORTAÇÕES DE BIBLIOTECAS
# ==============================================

# Bibliotecas para manipulação de arquivos e dados
import os  # Para operações com sistema de arquivos
import pandas as pd  # Para manipulação de dados em DataFrames

# Bibliotecas para criação da aplicação web e visualizações
import dash  # Framework principal
from dash import dcc, html  # Componentes de interface
from dash.dependencies import Input, Output  # Para interatividade
import plotly.express as px  # Para gráficos de alto nível
import plotly.graph_objects as go  # Para gráficos de baixo nível
from plotly.subplots import make_subplots  # Para gráficos múltiplos

# ==============================================
# 2. CONFIGURAÇÕES INICIAIS E CARREGAMENTO DE DADOS
# ==============================================

"""
ETAPAS DO PROCESSAMENTO DE DADOS:
1. Definir caminho para o arquivo CSV
2. Carregar os dados em um DataFrame
3. Converter colunas para tipos numéricos
4. Remover valores nulos
"""

# Caminho absoluto para o arquivo CSV (compatível com Render)
current_dir = os.path.dirname(__file__)  # Pega o diretório atual do script
csv_path = os.path.join(current_dir, 'ecommerce_estatistica.csv')  # Monta o caminho completo

try:
    # Carrega os dados do arquivo CSV
    df = pd.read_csv(csv_path)
    
    # Conversão de tipos numéricos (evita problemas com gráficos)
    # 'errors=coerce' transforma valores inválidos em NaN
    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')
    
    # Remove linhas com valores nulos nas colunas numéricas
    df = df.dropna(subset=['Preço', 'Qtd_Vendidos'])

except Exception as e:
    # Tratamento de erro robusto para evitar falhas na aplicação
    print(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame()  # Cria um DataFrame vazio para evitar erros

# ==============================================
# 3. FUNÇÕES AUXILIARES PARA CRIAÇÃO DE GRÁFICOS
# ==============================================

def criar_histograma():
    """
    Cria um histograma mostrando a distribuição dos preços dos produtos.
    
    Retorna:
        Figure: Objeto de figura do Plotly contendo o histograma
    """
    fig = px.histogram(
        df,
        x='Preço',  # Eixo X: preços dos produtos
        nbins=30,  # Número de intervalos (bins)
        title="Distribuição dos Preços dos Produtos",
        labels={'Preço': 'Preço (R$)'},  # Rótulos personalizados
        color_discrete_sequence=['#636EFA'],  # Cor azul padrão
        template="plotly_white"  # Template de fundo branco
    )
    
    # Personalização adicional do layout
    fig.update_layout(
        bargap=0.1,  # Espaço entre as barras
        xaxis_title="Preço (R$)",  # Título do eixo X
        yaxis_title="Quantidade de Produtos"  # Título do eixo Y
    )
    return fig

def criar_dispersao():
    """
    Cria um gráfico de dispersão mostrando a relação entre preço, avaliações e quantidade vendida.
    
    Retorna:
        Figure: Objeto de figura do Plotly contendo o gráfico de dispersão
    """
    fig = px.scatter(
        df,
        x='Preço',  # Eixo X: preço
        y='N_Avaliações',  # Eixo Y: número de avaliações
        color='Qtd_Vendidos',  # Cor dos pontos: quantidade vendida
        title="Relação entre Preço, Avaliações e Quantidade Vendida",
        labels={
            'Preço': 'Preço (R$)',
            'N_Avaliações': 'Número de Avaliações',
            'Qtd_Vendidos': 'Quantidade Vendida'
        },
        color_continuous_scale='Viridis'  # Escala de cores
    )
    
    # Personalização do fundo do gráfico
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',  # Cor de fundo do gráfico
        paper_bgcolor='rgba(240,240,240,0.5)'  # Cor de fundo ao redor do gráfico
    )
    return fig

def criar_heatmap():
    """
    Cria um mapa de calor mostrando as correlações entre variáveis numéricas.
    
    Retorna:
        Figure: Objeto de figura do Plotly contendo o mapa de calor
    """
    # Seleciona apenas colunas numéricas
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calcula a matriz de correlação
    correlation_matrix = numerical_df.corr()

    fig = px.imshow(
        correlation_matrix,
        title="Mapa de Calor das Correlações entre Variáveis Numéricas",
        color_continuous_scale='Blues',  # Escala de cores azuis
        text_auto=True,  # Mostra os valores nas células
        aspect="auto"  # Ajuste automático de aspecto
    )
    
    # Personalização dos eixos
    fig.update_layout(
        xaxis_title="Variáveis",
        yaxis_title="Variáveis"
    )
    return fig

def criar_barras():
    """
    Cria um gráfico de barras mostrando as marcas mais populares (top 7).
    
    Retorna:
        Figure: Objeto de figura do Plotly contendo o gráfico de barras
    """
    # Conta a frequência de cada marca e pega as 7 mais comuns
    marcas = df['Marca'].value_counts().head(7)
    
    fig = px.bar(
        marcas,
        x=marcas.index,  # Eixo X: nomes das marcas
        y=marcas.values,  # Eixo Y: contagem de produtos
        title="Top 7 Marcas mais Populares",
        labels={'x': 'Marca', 'y': 'Quantidade de Produtos'},
        color=marcas.index,  # Cores baseadas nas marcas
        color_discrete_sequence=px.colors.qualitative.Pastel  # Cores pastel
    )
    
    # Remove a legenda (não necessária para este gráfico)
    fig.update_layout(showlegend=False)
    return fig

def criar_pizza():
    """
    Cria um gráfico de pizza mostrando a distribuição de gêneros (top 3).
    
    Retorna:
        Figure: Objeto de figura do Plotly contendo o gráfico de pizza
    """
    # Conta a frequência de cada gênero e pega os 3 mais comuns
    generos = df['Gênero'].value_counts().head(3)
    
    fig = px.pie(
        generos,
        values=generos.values,  # Valores: contagem
        names=generos.index,  # Nomes: gêneros
        title="Distribuição dos Produtos por Gênero (Top 3)",
        hole=0.3,  # Cria um buraco no meio (gráfico de rosca)
        color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de cores
    )
    return fig

def criar_densidade():
    """
    Cria um gráfico de densidade mostrando a distribuição dos preços.
    
    Retorna:
        Figure: Objeto de figura do Plotly contendo o gráfico de densidade
    """
    fig = px.density_contour(
        df,
        x="Preço",
        title="Densidade dos Preços",
        color_discrete_sequence=['#00CC96']  # Cor verde
    )
    
    # Preenche as curvas de nível com cores
    fig.update_traces(contours_coloring="fill", contours_showlabels=True)
    
    # Personalização dos eixos
    fig.update_layout(
        xaxis_title="Preço (R$)",
        yaxis_title="Densidade"
    )
    return fig

def criar_regressao():
    """
    Cria um gráfico de dispersão com linha de regressão linear.
    
    Retorna:
        Figure ou html.Div: Retorna o gráfico ou mensagem de erro se statsmodels não estiver instalado
    """
    try:
        fig = px.scatter(
            df,
            x="Preço",
            y="Qtd_Vendidos",
            trendline="ols",  # Adiciona linha de regressão linear
            title="Regressão Linear: Preço vs Quantidade Vendida",
            labels={
                'Preço': 'Preço (R$)',
                'Qtd_Vendidos': 'Quantidade Vendida'
            },
            color_discrete_sequence=['#EF553B']  # Cor vermelha
        )
        
        # Personalização do fundo
        fig.update_layout(
            plot_bgcolor='rgba(240,240,240,0.8)',
            paper_bgcolor='rgba(240,240,240,0.5)'
        )
        return fig
    except Exception as e:
        # Mensagem de erro amigável se statsmodels não estiver instalado
        return html.Div([
            html.H4("Erro ao gerar gráfico de regressão"),
            html.P("Por favor, instale a biblioteca statsmodels:"),
            html.Pre("pip install statsmodels"),
            html.P(f"Detalhes do erro: {str(e)}")
        ], style={'color': 'red', 'padding': '20px'})

# ==============================================
# 4. INICIALIZAÇÃO DA APLICAÇÃO DASH
# ==============================================

"""
CONFIGURAÇÃO DA APLICAÇÃO:
- __name__: Necessário para o Dash identificar recursos estáticos
- external_stylesheets: Carrega uma folha de estilo CSS externa para melhor aparência
"""

app = dash.Dash(
    __name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

# ==============================================
# 5. LAYOUT DA APLICAÇÃO
# ==============================================

"""
ESTRUTURA DA INTERFACE:
1. Cabeçalho com título
2. Linha com controles (dropdown) e informações
3. Área para exibição do gráfico selecionado

ESTILIZAÇÃO:
- Usa classes CSS do framework (como 'row', 'six columns')
- Estilos inline para personalização específica
"""

app.layout = html.Div([
    # Container principal com estilo
    html.Div([
        # Título principal
        html.H1(
            "📊 Painel de Análise de E-commerce",
            style={
                'textAlign': 'center',
                'color': '#2a3f5f',
                'marginBottom': '30px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),

        # Linha com controles e informações
        html.Div([
            # Coluna para o dropdown de seleção
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
                    value='histograma',  # Valor padrão
                    clearable=False,  # Não permite limpar a seleção
                    style={'width': '100%'}
                )
            ], className="six columns", style={'marginBottom': '30px'}),

            # Coluna para informações do dataset
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
        ], className="row"),  # row: organiza as colunas lado a lado

        # Área de exibição do gráfico
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
# 6. CALLBACKS PARA INTERATIVIDADE
# ==============================================

"""
FUNCIONAMENTO DO CALLBACK:
1. O decorador @app.callback define a relação entre entrada e saída
2. Quando o dropdown (Input) muda, a função é acionada
3. A função retorna o gráfico correspondente para a área de exibição (Output)
"""

@app.callback(
    Output('output-grafico', 'children'),  # Saída: conteúdo da div 'output-grafico'
    [Input('grafico-selecionado', 'value')]  # Entrada: valor do dropdown
)
def atualizar_grafico(grafico):
    """
    Atualiza o gráfico exibido com base na seleção do usuário.
    
    Parâmetros:
        grafico (str): Valor do dropdown indicando qual gráfico mostrar
        
    Retorna:
        dcc.Graph ou html.Div: O gráfico selecionado ou mensagem de erro
    """
    # Verifica se o DataFrame está vazio (erro no carregamento)
    if df.empty:
        return html.Div("Erro: Não foi possível carregar os dados.", style={'color': 'red'})

    # Dicionário mapeando valores do dropdown para funções de gráfico
    graficos = {
        'histograma': criar_histograma,
        'dispersao': criar_dispersao,
        'heatmap': criar_heatmap,
        'barras': criar_barras,
        'pizza': criar_pizza,
        'densidade': criar_densidade,
        'regressao': criar_regressao
    }

    # Obtém a função correspondente ao gráfico selecionado
    # Se não existir, usa uma função que retorna uma figura vazia
    figura = graficos.get(grafico, lambda: go.Figure())()

    # Se a função retornar um componente HTML (como no caso de erro da regressão)
    if isinstance(figura, html.Div):
        return figura

    # Retorna o gráfico com estilos aplicados
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
# 7. CONFIGURAÇÕES PARA DEPLOY
# ==============================================

"""
IMPORTANTE PARA DEPLOY NO RENDER:
- A variável 'server' é necessária para o Gunicorn identificar a aplicação
- O bloco if __name__ é usado para execução local
"""

# Esta linha é essencial para o Gunicorn no Render
server = app.server

# Execução local (não usado no Render)
if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',  # Permite acesso de qualquer IP
        port=8050,  # Porta padrão do Dash
        debug=True  # Modo debug para desenvolvimento
    )