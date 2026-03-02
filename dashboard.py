import pandas as pd
import streamlit as st
import os

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================
st.set_page_config(
    layout="wide",
    page_title="Gestao a vista Delly's",  # 🔹 Nome da aba do navegador
    initial_sidebar_state="collapsed"
)

# ==================================================
# ESTILO GLOBAL
# ==================================================
st.markdown("""
<style>

/* Remove barra superior inteira */
header {visibility: hidden;}
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Força modo escuro */
html {color-scheme: dark;}

/* Remove espaço lateral */
.block-container {
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Fundo com imagem */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Overlay escuro */
[data-testid="stAppViewContainer"] {
    background-color: rgba(0, 0, 0, 0.65);
}

/* Texto branco */
h1, h2, h3, h4, h5, h6, p, label, div, span {
    color: white !important;
}

/* Centralizar métricas */
[data-testid="metric-container"] {
    text-align: center;
}
[data-testid="stMetricValue"] {
    justify-content: center;
}

/* Cabeçalho personalizado */
.logo-title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 25px;
}

/* 🔵 Logo redonda */
.logo-title img {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
}

.logo-title h1 {
    margin: 0;
    font-size: 42px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CABEÇALHO COM LOGO
# ==================================================
st.markdown("""
<div class="logo-title">
    <img src="https://is4-ssl.mzstatic.com/image/thumb/Purple126/v4/13/93/57/139357e7-7bd2-43b9-1b59-8a6ffb9665a9/source/512x512bb.jpg">
    <h1>Gestão à vista Delly's</h1>
</div>
""", unsafe_allow_html=True)

# ==================================================
# LOCALIZAÇÃO DOS ARQUIVOS
# ==================================================
arquivo_xls = r"I:\dioney\GestaoVista\base8189.xls"
arquivo_xlsx = r"I:\dioney\GestaoVista\base8189.xlsx"

caminho = None
engine = None

if os.path.exists(arquivo_xls):
    caminho = arquivo_xls
    engine = "xlrd"
elif os.path.exists(arquivo_xlsx):
    caminho = arquivo_xlsx
    engine = "openpyxl"
else:
    st.error("Nenhum arquivo Excel válido encontrado!")
    st.stop()

# ==================================================
# CARREGAMENTO DE DADOS
# ==================================================
@st.cache_data(ttl=10)
def carregar_excel(caminho, engine):
    df = pd.read_excel(caminho, engine=engine)
    df = df.fillna(0)

    if "VLTOTAL" in df.columns:
        df["VLTOTAL"] = df["VLTOTAL"].astype(str).str.replace(",", ".", regex=False)
        df["VLTOTAL"] = pd.to_numeric(df["VLTOTAL"], errors="coerce").fillna(0)

    if "PESOBRUTOTOT" in df.columns:
        df["PESOBRUTOTOT"] = df["PESOBRUTOTOT"].astype(str).str.replace(",", ".", regex=False)
        df["PESOBRUTOTOT"] = pd.to_numeric(df["PESOBRUTOTOT"], errors="coerce").fillna(0)

    return df

df = carregar_excel(caminho, engine)

# ==================================================
# KPIs CENTRALIZADOS
# ==================================================
total_pedidos = len(df)
total_valor = df["VLTOTAL"].sum()
total_peso = df["PESOBRUTOTOT"].sum()

col_space1, col1, col2, col3, col_space2 = st.columns([1,2,2,2,1])

col1.metric("📦 Total de Pedidos", total_pedidos)
col2.metric(
    "💰 Valor Total",
    f"{total_valor:,.2f} R$".replace(",", "X").replace(".", ",").replace("X", ".")
)
col3.metric(
    "⚖️ Peso Total",
    f"{total_peso:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", ".")
)

# ==================================================
# FUNÇÕES
# ==================================================
def formatar_tabela(df):
    df = df.copy()
    df["VLTOTAL"] = df["VLTOTAL"].apply(
        lambda x: f"{x:,.2f} R$".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    df["PESOBRUTOTOT"] = df["PESOBRUTOTOT"].apply(
        lambda x: f"{x:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    return df

def resumo_por_cidade(df):
    resumo = df.groupby("CIDADE").agg(
        total_pedidos=("NUMPED", "count"),
        total_valor=("VLTOTAL", "sum"),
        total_peso=("PESOBRUTOTOT", "sum")
    ).reset_index()

    resumo["total_valor"] = resumo["total_valor"].apply(
        lambda x: f"{x:,.2f} R$".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    resumo["total_peso"] = resumo["total_peso"].apply(
        lambda x: f"{x:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    return resumo

# ==================================================
# ABAS
# ==================================================
tab1, tab2, tab3 = st.tabs(
    ["📍 POR MUNICÍPIO", "📄 DETALHES PEDIDOS", "🔎 PESQUISA PEDIDO"]
)

with tab1:
    st.subheader("Resumo por Município")
    st.dataframe(resumo_por_cidade(df), use_container_width=True)

with tab2:
    st.subheader("Todos os Pedidos")
    st.dataframe(formatar_tabela(df), use_container_width=True)

with tab3:
    st.subheader("Pesquisar Pedido")
    numero_pedido = st.text_input("Digite o número do pedido:")

    if numero_pedido:
        resultado = df[df["NUMPED"].astype(str) == numero_pedido]
        if not resultado.empty:
            st.success("Pedido encontrado ✅")
            st.dataframe(formatar_tabela(resultado), use_container_width=True)
        else:
            st.error("Pedido não encontrado ❌")