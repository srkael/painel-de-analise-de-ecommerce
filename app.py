"""
PAINEL INTERATIVO DE ANÁLISE DE DADOS DE E-COMMERCE

Este script cria um dashboard interativo para análise de dados de produtos de e-commerce,
permitindo visualizar diferentes aspectos dos dados através de gráficos selecionáveis.

Tecnologias utilizadas:
- Python (linguagem de programação)
- Pandas (manipulação de dados)
- Dash (framework para criação de web apps)
- Plotly (criação de gráficos interativos)

Estrutura do código:
1. Importação de bibliotecas
2. Configuração inicial e carregamento de dados
3. Funções para criação de gráficos
4. Layout da aplicação
5. Sistema de callbacks (interatividade)
6. Execução da aplicação
"""

# ==============================================
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ==============================================

# Pandas: biblioteca para manipulação e análise de dados
import pandas as pd

# Dash: framework para criar aplicações web analíticas
import dash
from dash import dcc  # Componentes core do Dash (dropdowns, gráficos, etc.)
from dash import html  # Componentes HTML (divs, headings, etc.)
from dash.dependencies import Input, Output  # Para criar interatividade

# Plotly: biblioteca para criação de gráficos interativos
import plotly.express as px  # Interface simplificada
import plotly.graph_objects as go  # Interface mais personalizável
from plotly.subplots import make_subplots  # Para criar gráficos com múltiplas partes

# ==============================================
# 2. CONFIGURAÇÃO INICIAL E CARREGAMENTO DE DADOS
# ==============================================

"""
ETAPA DE CARREGAMENTO E PREPARAÇÃO DOS DADOS

Nesta seção, vamos:
1. Ler os dados de um arquivo CSV
2. Garantir que as colunas numéricas estão no formato correto
3. Lidar com possíveis erros durante o carregamento
"""

try:
    # Carrega os dados do arquivo CSV para um DataFrame (tabela de dados)
    df = pd.read_csv('ecommerce_estatistica.csv')

    # Converte as colunas numéricas para o tipo correto
    # 'errors=coerce' transforma valores inválidos em NaN (Not a Number)
    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')

    # Remove linhas onde 'Preço' ou 'Qtd_Vendidos' são NaN
    df = df.dropna(subset=['Preço', 'Qtd_Vendidos'])

except Exception as e:
    # Se ocorrer algum erro, imprime a mensagem e cria um DataFrame vazio
    print(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame()  # DataFrame vazio para evitar erros nas visualizações

# ==============================================
# 3. FUNÇÕES PARA CRIAÇÃO DE GRÁFICOS
# ==============================================

"""
FUNÇÕES DE VISUALIZAÇÃO DE DADOS

Cada função abaixo cria um tipo específico de gráfico usando os dados carregados.
Todas retornam um objeto 'figure' que pode ser exibido no dashboard.
"""


def criar_histograma():
    """
    Cria um histograma mostrando a distribuição dos preços dos produtos.

    Histograma: gráfico que mostra a frequência de valores em intervalos (bins).
    Útil para entender a distribuição de uma variável numérica.
    """
    fig = px.histogram(
        df,  # DataFrame com os dados
        x='Preço',  # Coluna para o eixo X
        nbins=30,  # Número de intervalos (bins)
        title="Distribuição dos Preços dos Produtos",
        labels={'Preço': 'Preço (R$)'},  # Rótulos mais amigáveis
        color_discrete_sequence=['#636EFA'],  # Cor das barras
        template="plotly_white"  # Template visual limpo
    )

    # Personalizações adicionais do layout
    fig.update_layout(
        bargap=0.1,  # Espaço entre as barras
        xaxis_title="Preço (R$)",  # Título do eixo X
        yaxis_title="Quantidade de Produtos"  # Título do eixo Y
    )
    return fig


def criar_dispersao():
    """
    Cria um gráfico de dispersão entre preço, avaliações e quantidade vendida.

    Gráfico de dispersão: mostra a relação entre duas variáveis numéricas.
    Aqui usamos cores para representar uma terceira variável (Qtd_Vendidos).
    """
    fig = px.scatter(
        df,
        x='Preço',  # Eixo X: preço do produto
        y='N_Avaliações',  # Eixo Y: número de avaliações
        color='Qtd_Vendidos',  # Cor representa quantidade vendida
        title="Relação entre Preço, Avaliações e Quantidade Vendida",
        labels={  # Rótulos mais descritivos
            'Preço': 'Preço (R$)',
            'N_Avaliações': 'Número de Avaliações',
            'Qtd_Vendidos': 'Quantidade Vendida'
        },
        color_continuous_scale='Viridis'  # Escala de cores
    )

    # Personaliza o fundo do gráfico
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',  # Cor de fundo do gráfico
        paper_bgcolor='rgba(240,240,240,0.5)'  # Cor de fundo ao redor do gráfico
    )
    return fig


def criar_heatmap():
    """
    Cria um mapa de calor (heatmap) mostrando correlações entre variáveis numéricas.

    Heatmap: representa valores através de cores. Neste caso, mostra como as variáveis
    se relacionam entre si (-1 a 1, onde 1 é correlação perfeita positiva).
    """
    # Seleciona apenas colunas numéricas
    numerical_df = df.select_dtypes(include=['float64', 'int64'])

    # Calcula a matriz de correlação
    correlation_matrix = numerical_df.corr()

    fig = px.imshow(
        correlation_matrix,  # Matriz de correlação
        title="Mapa de Calor das Correlações entre Variáveis Numéricas",
        color_continuous_scale='Blues',  # Escala de cores azuis
        text_auto=True,  # Mostra os valores nas células
        aspect="auto"  # Ajusta automaticamente a proporção
    )

    # Adiciona títulos aos eixos
    fig.update_layout(
        xaxis_title="Variáveis",
        yaxis_title="Variáveis"
    )
    return fig


def criar_barras():
    """
    Cria um gráfico de barras das marcas mais populares (com mais produtos).

    Gráfico de barras: ideal para comparar quantidades entre categorias.
    Mostra as 7 marcas com maior número de produtos no catálogo.
    """
    # Conta quantos produtos há por marca e pega as 7 mais frequentes
    marcas = df['Marca'].value_counts().head(7)

    fig = px.bar(
        marcas,  # Dados já processados (séries com marcas e contagens)
        x=marcas.index,  # Marcas no eixo X
        y=marcas.values,  # Contagens no eixo Y
        title="Top 7 Marcas mais Populares",
        labels={'x': 'Marca', 'y': 'Quantidade de Produtos'},
        color=marcas.index,  # Cores diferentes para cada marca
        color_discrete_sequence=px.colors.qualitative.Pastel  # Cores pastéis
    )

    # Remove a legenda (desnecessária pois já temos os rótulos no eixo X)
    fig.update_layout(showlegend=False)
    return fig


def criar_pizza():
    """
    Cria um gráfico de pizza (pie chart) mostrando a distribuição por gênero.

    Gráfico de pizza: mostra proporções de um todo.
    Aqui limitamos aos 3 gêneros mais comuns para não poluir a visualização.
    """
    # Conta produtos por gênero e pega os 3 mais frequentes
    generos = df['Gênero'].value_counts().head(3)

    fig = px.pie(
        generos,
        values=generos.values,  # Valores (quantidades)
        names=generos.index,  # Nomes (gêneros)
        title="Distribuição dos Produtos por Gênero (Top 3)",
        hole=0.3,  # Cria um buraco no meio (donut chart)
        color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de cores
    )
    return fig


def criar_densidade():
    """
    Cria um gráfico de densidade dos preços.

    Gráfico de densidade: mostra onde os valores se concentram.
    Áreas mais escuras indicam maior concentração de produtos naquela faixa de preço.
    """
    fig = px.density_contour(
        df,
        x="Preço",  # Variável a ser analisada
        title="Densidade dos Preços",
        color_discrete_sequence=['#00CC96']  # Cor verde-água
    )

    # Preenche as curvas de nível com cor
    fig.update_traces(
        contours_coloring="fill",  # Preenche entre as curvas
        contours_showlabels=True  # Mostra rótulos nas curvas
    )

    fig.update_layout(
        xaxis_title="Preço (R$)",
        yaxis_title="Densidade"
    )
    return fig


def criar_regressao():
    """
    Cria um gráfico de dispersão com linha de regressão linear.

    Mostra a relação entre preço e quantidade vendida, com uma linha que tenta
    modelar essa relação (mínimos quadrados ordinários - OLS).
    """
    try:
        fig = px.scatter(
            df,
            x="Preço",  # Variável independente
            y="Qtd_Vendidos",  # Variável dependente
            trendline="ols",  # Adiciona linha de regressão
            title="Regressão Linear: Preço vs Quantidade Vendida",
            labels={
                'Preço': 'Preço (R$)',
                'Qtd_Vendidos': 'Quantidade Vendida'
            },
            color_discrete_sequence=['#EF553B']  # Cor vermelha
        )

        fig.update_layout(
            plot_bgcolor='rgba(240,240,240,0.8)',
            paper_bgcolor='rgba(240,240,240,0.5)'
        )
        return fig

    except Exception as e:
        # Se houver erro (geralmente por falta da biblioteca statsmodels)
        # Retorna uma mensagem de erro amigável
        return html.Div([
            html.H4("Erro ao gerar gráfico de regressão"),
            html.P("Por favor, instale a biblioteca statsmodels:"),
            html.Pre("pip install statsmodels"),
            html.P(f"Detalhes do erro: {str(e)}")
        ], style={'color': 'red', 'padding': '20px'})


# ==============================================
# 4. LAYOUT DA APLICAÇÃO
# ==============================================

"""
CONFIGURAÇÃO DA INTERFACE DO USUÁRIO

Aqui definimos como o dashboard será exibido no navegador, com:
- Um título
- Um menu dropdown para seleção de gráficos
- Informações sobre o dataset
- Área para exibição do gráfico selecionado
"""

# Cria a aplicação Dash
app = dash.Dash(
    __name__,  # Nome do módulo
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']  # Estilo CSS
)

# Define a estrutura do layout
app.layout = html.Div([
    # Container principal
    html.Div([
        # Título do dashboard
        html.H1(
            "📊 Painel de Análise de E-commerce",
            style={
                'textAlign': 'center',  # Centraliza o texto
                'color': '#2a3f5f',  # Cor do texto
                'marginBottom': '30px',  # Espaço abaixo
                'fontFamily': 'Arial, sans-serif'  # Fonte
            }
        ),

        # Linha com dois componentes: dropdown e informações
        html.Div([
            # Coluna para o dropdown (6 colunas de 12)
            html.Div([
                html.Label(
                    "Selecione o tipo de análise:",
                    style={
                        'fontWeight': 'bold',  # Texto em negrito
                        'marginBottom': '10px'  # Espaço abaixo
                    }
                ),
                # Dropdown para seleção do gráfico
                dcc.Dropdown(
                    id='grafico-selecionado',  # ID para referência
                    options=[  # Opções disponíveis
                        {'label': '📈 Histograma de Preços', 'value': 'histograma'},
                        {'label': '🟢 Dispersão: Preço vs Avaliações', 'value': 'dispersao'},
                        {'label': '🔥 Mapa de Calor de Correlações', 'value': 'heatmap'},
                        {'label': '📊 Barras: Marcas Populares', 'value': 'barras'},
                        {'label': '🍕 Pizza: Distribuição de Gêneros', 'value': 'pizza'},
                        {'label': '🌊 Densidade de Preços', 'value': 'densidade'},
                        {'label': '📉 Regressão Linear (Preço vs Qtd Vendida)', 'value': 'regressao'}
                    ],
                    value='histograma',  # Valor padrão selecionado
                    clearable=False,  # Não permite desmarcar
                    style={'width': '100%'}  # Ocupa toda a largura
                )
            ], className="six columns", style={'marginBottom': '30px'}),

            # Coluna para informações do dataset (6 colunas de 12)
            html.Div([
                html.Label(
                    "📌 Informações do Dataset:",
                    style={'fontWeight': 'bold'}
                ),
                # Lista não ordenada com informações
                html.Ul([
                    html.Li(f"Total de produtos: {len(df)}"),
                    html.Li(f"Média de preço: R${df['Preço'].mean():.2f}"),
                    html.Li(f"Produto mais caro: R${df['Preço'].max():.2f}")
                ])
            ], className="six columns", style={'paddingLeft': '20px'})
        ], className="row"),  # Fim da linha

        # Div que conterá o gráfico selecionado
        html.Div(id='output-grafico', style={'marginTop': '20px'})
    ], style={  # Estilo do container principal
        'maxWidth': '1200px',  # Largura máxima
        'margin': '0 auto',  # Centraliza na página
        'padding': '20px',  # Espaçamento interno
        'backgroundColor': 'white',  # Cor de fundo
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',  # Sombra
        'borderRadius': '5px'  # Bordas arredondadas
    })
])

# ==============================================
# 5. SISTEMA DE CALLBACKS (INTERATIVIDADE)
# ==============================================

"""
MECANISMO DE INTERATIVIDADE

O callback abaixo é o que torna o dashboard interativo. Ele:
1. Observa o dropdown (Input)
2. Quando o valor muda, executa a função
3. Atualiza a área do gráfico (Output) com o novo gráfico selecionado
"""


@app.callback(
    Output('output-grafico', 'children'),  # Saída: atualiza a div do gráfico
    [Input('grafico-selecionado', 'value')]  # Entrada: valor do dropdown
)
def atualizar_grafico(grafico):
    """
    Função chamada sempre que o valor do dropdown muda.
    Recebe o valor selecionado e retorna o gráfico correspondente.
    """
    # Verifica se há dados carregados
    if df.empty:
        return html.Div("Erro: Não foi possível carregar os dados.", style={'color': 'red'})

    # Dicionário que mapeia valores do dropdown para funções de gráfico
    graficos = {
        'histograma': criar_histograma,
        'dispersao': criar_dispersao,
        'heatmap': criar_heatmap,
        'barras': criar_barras,
        'pizza': criar_pizza,
        'densidade': criar_densidade,
        'regressao': criar_regressao
    }

    # Obtém a função correspondente ao gráfico selecionado e executa
    figura = graficos.get(grafico, lambda: go.Figure())()

    # Se a função retornar uma Div (como no caso de erro da regressão)
    if isinstance(figura, html.Div):
        return figura

    # Retorna o gráfico dentro de um componente dcc.Graph
    return dcc.Graph(
        figure=figura,
        style={
            'height': '600px',  # Altura fixa
            'border': '1px solid #eee',  # Borda sutil
            'borderRadius': '5px',  # Bordas arredondadas
            'padding': '10px'  # Espaçamento interno
        }
    )


# ==============================================
# 6. EXECUÇÃO DA APLICAÇÃO
# ==============================================

"""
INICIALIZAÇÃO DO SERVIDOR

Este bloco só é executado quando o script é rodado diretamente
(não quando importado como módulo).
"""

# Estas linhas são ESSENCIAIS para o deploy no Render
# Estas linhas devem ser as últimas do arquivo, ANTES do if __name__...
app = dash.Dash(__name__)  # Já deve existir no seu código
server = app.server        # Esta linha é crucial

if __name__ == '__main__':
    app.run(debug=True)