# Este dashboard foi criado para analisar os dados do catálogo da Netflix de forma visual e interativa. 
# Ele permite que o usuário veja quantos conteúdos existem na plataforma, quantos são filmes e quantos são séries, 
# além de mostrar o ano do lançamento mais recente presente nos dados. Também é possível visualizar gráficos que mostram 
# a distribuição entre filmes e séries, a quantidade de lançamentos ao longo dos anos, os países que mais aparecem no 
# catálogo e os gêneros mais frequentes. O usuário pode filtrar as informações por tipo de conteúdo e por ano de 
# lançamento, fazendo com que todos os gráficos e métricas sejam atualizados automaticamente.

import streamlit as st
import pandas as pd  # tabelas e arquivos CSV
import plotly.express as px  # criar gráficos

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Netflix Dashboard",  # nome da aba do navegador
    layout="wide"  # largura da tela
)

# CSS

with open("style.css") as f:
    st.markdown(  # Permite escrever código HTML e CSS dentro do Streamlit
        f"<style>{f.read()}</style>",  # f.read() lê todo o conteúdo do arquivo.
        unsafe_allow_html=True  # Permite que o Streamlit interprete HTML e CSS
    )

# LEITURA DOS DADOS
# df significa DataFrame. É onde todos os dados ficam armazenados
df = pd.read_csv("netflix_titles.csv")  # Lê e transforma o arquivo em uma tabela do Pandas

# Barra Lateral

st.sidebar.title("Dashboard Netflix")  # Cria um título na barra lateral

tipo = st.sidebar.multiselect(  # Cria uma lista para o usuário poder escolher várias opções
    "Tipo",
    df["type"].dropna().unique(),  # Acessa a coluna "type", remove valores vazios, pega apenas valores únicos
    default=df["type"].dropna().unique()  # Deixa todas as opções selecionadas inicialmente como padrão configuração
)

anos = st.sidebar.slider(  # Cria uma barra deslizante
    "Ano de lançamento",
    int(df["release_year"].min()),  # Retorna o menor
    int(df["release_year"].max()),  # e maior ano
    (                               # o usuário pode escolher um intervalo
        int(df["release_year"].min()),
        int(df["release_year"].max())
    )
)

# FILTROS

df_filtrado = df[
    (df["type"].isin(tipo))  # verifica se o tipo está entre os selecionados
    &  # as duas condições devem ser verdadeiras
    (df["release_year"].between(anos[0], anos[1]))  # verifica se o ano está dentro do intervalo escolhido
]  # Cria uma nova tabela filtrada

# TÍTULO

st.title("Dashboard Netflix")
st.markdown("---")

# MÉTRICAS

total = len(df_filtrado)  # Conta quantas linhas existem

filmes = len(
    df_filtrado[df_filtrado["type"] == "Movie"]  # Conta quantos filmes existem
)

series = len(
    df_filtrado[df_filtrado["type"] == "TV Show"]  # Conta quantas séries existem
)

ultimo_ano = df_filtrado["release_year"].max()  # Pega o maior ano

c1,c2,c3,c4 = st.columns(4)  # Divide a tela em 4 partes

c1.metric("Total de Títulos", total)
c2.metric("Filmes", filmes)
c3.metric("Séries", series)
c4.metric("Ano Mais Recente", ultimo_ano)
st.markdown("---")

# PRIMEIRA LINHA DE GRÁFICOS
col1,col2 = st.columns(2)  # Divide a tela em duas partes.

with col1:

    tipo_count = (
        df_filtrado["type"]
        .value_counts() 
    )  # Conta quantas vezes cada tipo aparece (filme ou série)

    fig = px.pie(  # Cria um gráfico de pizza
        values=tipo_count.values,  # Valores do gráfico
        names=tipo_count.index,  # Nomes das fatias
        title="Filmes x Séries",  
        color_discrete_sequence=[
            "#E94F56",
            "#8B0D13"
        ]
    )

    fig.update_layout(
        paper_bgcolor="#1F1F1F",
        plot_bgcolor="#1F1F1F",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    ano_count = (
        df_filtrado["release_year"]
        .value_counts()
        .sort_index()  # Ordena os anos
    )  # Conta quantos títulos existem em cada ano

    fig = px.line(  # Cria um gráfico de linha
        x=ano_count.index,
        y=ano_count.values,
        title="Lançamentos por Ano"
    )

    fig.update_traces(
        line_color="#E50914"
    )

    fig.update_layout(
        paper_bgcolor="#1F1F1F",
        plot_bgcolor="#1F1F1F",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# SEGUNDA LINHA

col3,col4 = st.columns(2)  # Cria duas novas colunas

with col3:

    paises = (
        df_filtrado["country"]  # Pega a coluna de países
        .dropna()  # Remove vazios
        .str.split(", ")  # Divide os países que estão escritos juntos com vírgula
        .explode()  # Transforma a lista em linhas separadas
        .value_counts()  # Conta quantas vezes cada país aparece
        .head(10)  # Pega os 10 primeiros
    )

    fig = px.bar(  # Cria gráfico de barras
        x=paises.values,
        y=paises.index,
        orientation="h",
        title="Top 10 Países"
    )

    fig.update_traces(
        marker_color="#E50914"
    )

    fig.update_layout(
        paper_bgcolor="#1F1F1F",
        plot_bgcolor="#1F1F1F",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col4:

    generos = (
        df_filtrado["listed_in"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )

    fig = px.bar(
        x=generos.values,
        y=generos.index,
        orientation="h",
        title="Top 10 Gêneros"
    )

    fig.update_traces(
        marker_color="#B81D24"
    )

    fig.update_layout(
        paper_bgcolor="#1F1F1F",
        plot_bgcolor="#1F1F1F",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# TABELA

st.markdown("---")

st.subheader("Dados Filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)