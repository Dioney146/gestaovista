# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import io
import re
import json
import time
import datetime
import urllib.request
import plotly.express as px
import plotly.graph_objects as go
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    layout="wide",
    page_title="Gestao a Vista - Delly's",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ==================================================
# DESIGN SYSTEM - CSS PREMIUM
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0&display=block');

:root {
    --bg-base: #05070A;
    --bg-card: #0E1117;
    --bg-card-soft: rgba(14,17,23,0.72);
    --border-soft: rgba(255,255,255,0.08);
    --accent: #F59E0B;
    --accent-soft: #FDBA74;
    --text-main: #FFFFFF;
    --text-sub: #B8C0CC;
    --radius-lg: 20px;
    --radius-md: 16px;
    --shadow-card: 0 8px 30px rgba(0,0,0,0.45);
    --shadow-glow: 0 0 24px rgba(245,158,11,0.25);
}

* { box-sizing: border-box; }

header {visibility: hidden;}
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

html, body, .stApp {
    background-color: var(--bg-base) !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 100vh;
}

/* ---------- FUNDO EM CAMADAS ---------- */
.stApp {
    position: relative;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    background-image:
        radial-gradient(circle at 15% 10%, rgba(59,130,246,0.10), transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(245,158,11,0.08), transparent 45%),
        linear-gradient(180deg, rgba(5,7,10,0.75) 0%, rgba(5,7,10,0.92) 55%, rgba(5,7,10,0.98) 100%),
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    filter: blur(3px) saturate(0.9);
    transform: scale(1.03);
}
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.65) 100%);
}
[data-testid="stAppViewContainer"] { background: transparent !important; position: relative; z-index: 1; min-height: 100vh; }
[data-testid="stMain"], [data-testid="stMainBlockContainer"], .main, .main > div { background-color: transparent !important; }
.block-container { padding: 1rem 1.6rem 1.4rem 1.6rem !important; max-width: 100% !important; position: relative; z-index: 1; min-height: 100vh; }

/* Particulas discretas */
.particulas { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.particulas span {
    position: absolute; width: 3px; height: 3px; border-radius: 50%;
    background: rgba(245,158,11,0.35); animation: subir 14s linear infinite;
}
@keyframes subir { from { transform: translateY(100vh); opacity: 0; } 10% { opacity:.6; } to { transform: translateY(-10vh); opacity: 0; } }

/* ---------- TIPOGRAFIA GERAL ---------- */
h1, h2, h3, h4, h5, h6, p, label, li, a { color: var(--text-main) !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text-sub) !important; }
[data-testid="stCaptionContainer"] p { color: var(--text-sub) !important; font-size: 12.5px !important; }

/* Icones - protegidos contra sobreposicao */
[data-testid="stIconMaterial"], .material-symbols-outlined, .material-icons, span[class*="material-symbols"] {
    font-family: 'Material Symbols Outlined' !important;
    line-height: 1 !important; display: inline-block !important;
    overflow: hidden !important; white-space: nowrap !important; flex-shrink: 0 !important;
}
[data-testid="stExpander"] summary { display: flex !important; align-items: center !important; gap: 8px !important; flex-wrap: nowrap !important; }
[data-testid="stExpander"] summary span { position: static !important; }
[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] { overflow: visible !important; white-space: normal !important; }
[data-testid="stFileUploaderDropzone"] { flex-wrap: wrap !important; }

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(9,11,15,0.97), rgba(5,7,10,0.99)) !important;
    border-right: 1px solid var(--border-soft) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--text-sub) !important; }
.sb-logo { display:flex; align-items:center; gap:12px; padding: 6px 4px 22px 4px; border-bottom: 1px solid var(--border-soft); margin-bottom: 18px; }
.sb-logo img { width: 40px; height: 40px; border-radius: 10px; border: 2px solid rgba(245,158,11,0.6); }
.sb-logo .t1 { font-family:'Bebas Neue',sans-serif; font-size: 20px; letter-spacing: 1.5px; color: #fff; line-height:1; }
.sb-logo .t2 { font-size: 11px; color: var(--text-sub); }

[data-testid="stSidebar"] .stButton button {
    width: 100%; text-align: left; background: transparent !important; color: var(--text-sub) !important;
    border: 1px solid transparent !important; border-left: 3px solid transparent !important;
    border-radius: 10px !important; padding: 10px 14px !important; font-weight: 500 !important;
    font-size: 14px !important; transition: all .2s ease !important; margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(245,158,11,0.08) !important; color: #fff !important;
    border-left: 3px solid rgba(245,158,11,0.5) !important; transform: translateX(2px);
}
[data-testid="stSidebar"] .stButton button:focus { box-shadow: none !important; }
.sb-ativo button {
    background: linear-gradient(90deg, rgba(245,158,11,0.22), rgba(245,158,11,0.04)) !important;
    color: #fff !important; border-left: 3px solid var(--accent) !important;
    box-shadow: var(--shadow-glow); font-weight: 700 !important;
}
.sb-secao { font-size: 10.5px; text-transform: uppercase; letter-spacing: 1.4px; color: var(--text-sub); font-weight: 700; margin: 14px 4px 6px 4px; opacity: .75; }

/* ---------- CABECALHO ---------- */
.topo-header {
    display:flex; justify-content:space-between; align-items:center; flex-wrap: wrap; gap: 14px;
    padding: 18px 24px; margin-bottom: 22px; border-radius: var(--radius-lg);
    background: var(--bg-card-soft); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-soft); box-shadow: var(--shadow-card);
    animation: fadeInUp .5s ease;
}
.topo-header h2 { margin:0; font-size: 21px !important; font-weight: 800 !important; }
.topo-header .sub { color: var(--text-sub) !important; font-size: 13px; margin-top: 2px; }
.topo-meta { text-align:right; }
.topo-meta .lbl { font-size: 11px; color: var(--text-sub); text-transform:uppercase; letter-spacing: .6px;}
.topo-meta .val { font-size: 13px; color: #fff; font-weight:600; }

/* ---------- BLOCOS / CARDS GLASS GERAIS ---------- */
.glass-box {
    background: var(--bg-card-soft); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--border-soft); border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card); padding: 18px 20px; margin-bottom: 18px;
    animation: fadeInUp .5s ease;
}
@keyframes fadeInUp { from { opacity:0; transform: translateY(10px);} to {opacity:1; transform:translateY(0);} }

.filter-title { font-size: 12px !important; text-transform: uppercase; letter-spacing: 1.6px; color: var(--accent-soft) !important; margin-bottom: 10px; font-weight:700; display:flex; align-items:center; gap:6px; }

.painel {
    background: var(--bg-card-soft); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border-soft); border-radius: var(--radius-md);
    box-shadow: var(--shadow-card); padding: 14px 16px; margin-bottom: 14px;
}
.painel-titulo { display:flex; align-items:center; gap:8px; font-size: 14.5px !important; font-weight:700 !important; color:#fff !important; margin: 0 0 10px 0 !important; }
.painel-titulo .ic { font-size: 15px; }

/* ---------- INPUTS / FILTROS PREMIUM ---------- */
input, textarea, select { background-color: rgba(255,255,255,0.04) !important; border: 1px solid var(--border-soft) !important; border-radius: 12px !important; color: #fff !important; -webkit-text-fill-color: #fff !important; }
[data-testid="stSelectbox"] > div > div, [data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.04) !important; border: 1px solid var(--border-soft) !important;
    border-radius: 12px !important; color: #fff !important; min-height: 46px !important;
    transition: box-shadow .2s ease, border-color .2s ease !important;
}
[data-baseweb="select"]:focus-within > div { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(245,158,11,0.18) !important; }
[data-baseweb="popover"], [data-baseweb="menu"], ul[data-baseweb="menu"] { background-color: #12151C !important; border: 1px solid var(--border-soft) !important; border-radius: 12px !important; }
[data-baseweb="menu"] li, [role="option"] { background-color: #12151C !important; color: #fff !important; }
[data-baseweb="menu"] li:hover, [role="option"]:hover { background-color: rgba(245,158,11,0.15) !important; }
[data-testid="stMultiSelect"] > div > div { background-color: rgba(255,255,255,0.04) !important; border: 1px solid var(--border-soft) !important; border-radius: 12px !important; min-height: 46px !important; }
[data-baseweb="tag"] { background-color: rgba(245,158,11,0.22) !important; border-radius: 6px !important; border: 1px solid rgba(245,158,11,0.45) !important; }
[data-testid="stTextInput"] input { min-height: 46px !important; }

/* ---------- BOTOES ---------- */
.stButton button, [data-testid="stDownloadButton"] button {
    border-radius: 12px !important; font-weight: 700 !important; transition: all .2s ease !important;
}
div[data-testid="column"] .stButton button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), #d97706) !important; border: none !important;
    color: #0a0a0a !important; box-shadow: 0 4px 18px rgba(245,158,11,0.35) !important;
}
div[data-testid="column"] .stButton button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(245,158,11,0.5) !important; }
[data-testid="stDownloadButton"] button {
    background: rgba(245,158,11,0.12) !important; border: 1px solid rgba(245,158,11,0.5) !important;
    color: var(--accent-soft) !important; width: 100% !important;
}
[data-testid="stDownloadButton"] button:hover { background: rgba(245,158,11,0.22) !important; transform: translateY(-1px); }

/* ---------- ABAS PREMIUM ---------- */
[data-testid="stTabs"] [data-baseweb="tab-list"] { background: transparent !important; gap: 6px; border-bottom: 1px solid var(--border-soft); }
[data-testid="stTabs"] button {
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 13.5px !important;
    color: var(--text-sub) !important; border-radius: 10px 10px 0 0 !important; background: transparent !important;
    padding: 12px 18px !important; transition: all .25s ease !important; position: relative;
}
[data-testid="stTabs"] button:hover { color: #fff !important; background: rgba(255,255,255,0.04) !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #fff !important; background: rgba(245,158,11,0.08) !important;
}
[data-testid="stTabs"] button[aria-selected="true"]::after {
    content:""; position:absolute; left:14px; right:14px; bottom:-1px; height:3px; border-radius: 3px 3px 0 0;
    background: linear-gradient(90deg, var(--accent), var(--accent-soft)); box-shadow: 0 0 10px rgba(245,158,11,0.7);
}

/* ---------- KPI CARDS ---------- */
.kpi-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap: 18px; margin-bottom: 6px; }
.kpi-card-premium {
    position: relative; background: linear-gradient(155deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
    border: 1px solid var(--border-soft); border-radius: var(--radius-lg); padding: 20px 22px;
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    box-shadow: var(--shadow-card); overflow:hidden; transition: transform .25s ease, box-shadow .25s ease;
    animation: fadeInUp .5s ease;
}
.kpi-card-premium:hover { transform: translateY(-4px); box-shadow: var(--shadow-card), var(--shadow-glow); }
.kpi-card-premium::before {
    content:""; position:absolute; top:-40%; right:-30%; width:180px; height:180px; border-radius:50%;
    background: radial-gradient(circle, rgba(245,158,11,0.16), transparent 70%); pointer-events:none;
}
.kpi-top { display:flex; align-items:center; justify-content:space-between; margin-bottom: 14px; }
.kpi-icon-circ {
    width: 42px; height:42px; border-radius: 50%; display:flex; align-items:center; justify-content:center;
    font-size: 19px; background: linear-gradient(135deg, rgba(245,158,11,0.28), rgba(245,158,11,0.06));
    border: 1px solid rgba(245,158,11,0.4); box-shadow: 0 0 14px rgba(245,158,11,0.25);
}
.kpi-label-p { font-size: 11.5px; text-transform: uppercase; letter-spacing: 1.2px; color: var(--text-sub); font-weight:700; }
.kpi-valor-p { font-size: 27px; font-weight: 800; color: #fff; line-height:1.15; margin-bottom: 2px; }
.kpi-desc-p { font-size: 12px; color: var(--text-sub); }
.kpi-spark { margin-top: 10px; opacity: .9; }

/* ---------- TABELA PREMIUM ---------- */
.tabela-premium-wrap { border-radius: var(--radius-md); overflow:hidden; border: 1px solid var(--border-soft); background: var(--bg-card-soft); backdrop-filter: blur(10px); }
.tabela-premium { width:100%; border-collapse: collapse; font-family:'Inter',sans-serif; font-size: 13px; }
.tabela-premium thead th {
    background: rgba(255,255,255,0.045); color: var(--accent-soft); text-transform: uppercase;
    font-size: 11px; letter-spacing: .8px; font-weight: 700; text-align:left; padding: 12px 16px;
    border-bottom: 1px solid rgba(245,158,11,0.25); white-space: nowrap; position: sticky; top:0;
}
.tabela-premium tbody td { padding: 10px 16px; color: #E8ECF1; border-bottom: 1px solid rgba(255,255,255,0.04); white-space: nowrap; }
.tabela-premium tbody tr:nth-child(even) { background: rgba(255,255,255,0.02); }
.tabela-premium tbody tr:hover td { background: rgba(245,158,11,0.07); }
.tabela-premium tr.linha-total td { background: rgba(245,158,11,0.14) !important; color:#fff !important; font-weight:800; border-top: 2px solid rgba(245,158,11,0.5); }
.barra-peso-track { position: relative; width: 90px; height: 8px; background: rgba(255,255,255,0.08); border-radius: 6px; overflow:hidden; display:inline-block; vertical-align:middle; margin-left:8px;}
.barra-peso-fill { position:absolute; left:0; top:0; bottom:0; border-radius:6px; background: linear-gradient(90deg, var(--accent), var(--accent-soft)); }

/* ---------- RODAPE ---------- */
.rodape-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 16px; margin-top: 24px; }
.rodape-card {
    background: var(--bg-card-soft); border: 1px solid var(--border-soft); border-radius: var(--radius-md);
    padding: 16px 18px; backdrop-filter: blur(10px); display:flex; gap:12px; align-items:center;
    transition: transform .2s ease;
}
.rodape-card:hover { transform: translateY(-3px); }
.rodape-ic { font-size: 20px; }
.rodape-t { font-size: 12.5px; font-weight:700; color:#fff; }
.rodape-s { font-size: 11px; color: var(--text-sub); }

hr { border-color: var(--border-soft) !important; }
[data-testid="stAlert"] { background-color: rgba(14,17,23,0.85) !important; border-radius: 14px !important; border: 1px solid var(--border-soft) !important; }
[data-testid="stMetric"] { background: var(--bg-card-soft) !important; border: 1px solid var(--border-soft) !important; border-radius: var(--radius-md) !important; padding: 14px !important; }

[data-testid="stDataFrame"] { background: var(--bg-card-soft) !important; border-radius: var(--radius-md) !important; border: 1px solid var(--border-soft) !important; overflow: hidden; }

/* ---------- RESPONSIVO ---------- */
@media (max-width: 1366px) {
    .kpi-valor-p { font-size: 23px; }
    .block-container { padding: 1rem 1.2rem 1.6rem 1.2rem !important; }
}
@media (max-width: 900px) {
    .kpi-grid { grid-template-columns: 1fr 1fr; }
    .topo-header { flex-direction: column; align-items: flex-start; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="particulas">' + "".join(
    [f'<span style="left:{7+i*11}%; animation-delay:{i*1.3}s;"></span>' for i in range(9)]
) + '</div>', unsafe_allow_html=True)

# ==================================================
# CONFIGURACAO DOS ESTADOS
# ==================================================
ESTADOS_LABELS = {
    "AM":    "Amazonas (AM)",
    "BA":    "Bahia (BA)",
    "DF":    "Distrito Federal (DF)",
    "MG":    "Minas Gerais (MG)",
    "ES":    "Espirito Santo (ES)",
    "SP":    "Sao Paulo (SP)",
    "SPW":   "Sao Paulo WFS (SPW)",
}

# UF real no mapa -> sigla(s) usada(s) no nosso sistema
MAPA_UF_PARA_ESTADO = {
    "AM": ["AM"],
    "BA": ["BA"],
    "DF": ["DF"],
    "MG": ["MG"],
    "ES": ["ES"],
    "SP": ["SP", "SPW"],
}

# ==================================================
# PERSISTENCIA COMPARTILHADA (GOOGLE SHEETS)
# ==================================================
# Apenas DUAS abas gerais na planilha: "LIBERADOS" e "MONTADOS", com todos os
# estados juntos e uma coluna DATA_IMPORTACAO marcando o dia em que cada leva de
# pedidos foi importada. Isso cria um historico: cada dia de importacao fica
# guardado, em vez de sobrescrever o anterior.
#
# Reimportar o mesmo estado no mesmo dia (ex: corrigiu o arquivo e subiu de novo)
# remove automaticamente as linhas antigas daquele estado com a MESMA
# DATA_IMPORTACAO antes de gravar as novas — ou seja, so descarta duplicados do
# dia corrente; o historico de dias anteriores nunca e mexido.
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
ABAS_GERAIS = {"LIBERADOS": "LIBERADOS", "MONTADOS": "MONTADOS", "CARGAS": "CARGAS"}

def planilha_configurada():
    """Verifica se as credenciais do Google Sheets foram configuradas em st.secrets."""
    return "gcp_service_account" in st.secrets and "GOOGLE_SHEET_ID" in st.secrets

@st.cache_resource(show_spinner=False)
def obter_cliente_planilha():
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=GOOGLE_SCOPES
    )
    return gspread.authorize(creds)

@st.cache_resource(show_spinner=False)
def obter_planilha():
    return obter_cliente_planilha().open_by_key(st.secrets["GOOGLE_SHEET_ID"])

def obter_ou_criar_aba_geral(tipo):
    planilha = obter_planilha()
    nome = ABAS_GERAIS[tipo]
    try:
        return planilha.worksheet(nome)
    except gspread.WorksheetNotFound:
        return planilha.add_worksheet(title=nome, rows="200", cols="20")

def carregar_geral_da_planilha(tipo):
    """Le a aba geral inteira (LIBERADOS ou MONTADOS) — todos os estados, todas as
    datas de importacao ja gravadas."""
    aba = obter_ou_criar_aba_geral(tipo)
    valores = aba.get_all_values()
    if len(valores) < 2:
        return pd.DataFrame()

    df = pd.DataFrame(valores[1:], columns=valores[0])
    for col in ["VLTOTAL", "PESOBRUTOTOT"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    for col in ["DATA", "DTENTREGA"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    if "DATA_IMPORTACAO" in df.columns:
        df["DATA_IMPORTACAO"] = normalizar_data_importacao(df["DATA_IMPORTACAO"])
    return df

def salvar_estado_na_planilha(estado, tipo, df, data_importacao=None):
    """Acrescenta os pedidos ao historico geral (aba LIBERADOS/MONTADOS/CARGAS),
    marcando a data de importacao (hoje, por padrao, ou a data escolhida na tela de
    importacao). Remove antes as linhas do MESMO estado com a MESMA data de
    importacao, para nao duplicar caso o arquivo seja reenviado para aquela data."""
    data_alvo = data_importacao or time.strftime(FORMATO_DATA_IMPORTACAO)

    df_novo = df.copy()
    df_novo["DATA_IMPORTACAO"] = data_alvo

    df_historico = carregar_geral_da_planilha(tipo)
    if not df_historico.empty:
        mascara_manter = ~(
            (df_historico["ESTADO"].astype(str) == estado) &
            (df_historico["DATA_IMPORTACAO"].astype(str) == data_alvo)
        )
        df_historico = df_historico[mascara_manter]
        df_final = pd.concat([df_historico, df_novo], ignore_index=True)
    else:
        df_final = df_novo

    df_export = df_final.copy()
    for col in ["DATA", "DTENTREGA"]:
        if col in df_export.columns and pd.api.types.is_datetime64_any_dtype(df_export[col]):
            df_export[col] = df_export[col].dt.strftime("%Y-%m-%d").fillna("")
    df_export = df_export.fillna("").astype(str)

    valores = [df_export.columns.tolist()] + df_export.values.tolist()
    aba = obter_ou_criar_aba_geral(tipo)
    aba.clear()
    aba.resize(rows=max(len(valores) + 20, 200), cols=max(len(df_export.columns) + 2, 15))
    aba.update(values=valores)

def apagar_estado_na_planilha(estado, tipo=None):
    """Remove do historico geral todas as linhas do estado informado.
    tipo=None apaga em LIBERADOS e MONTADOS."""
    for t in ([tipo] if tipo else ["LIBERADOS", "MONTADOS", "CARGAS"]):
        df_historico = carregar_geral_da_planilha(t)
        if df_historico.empty:
            continue
        df_restante = df_historico[df_historico["ESTADO"].astype(str) != estado]
        if len(df_restante) == len(df_historico):
            continue

        df_export = df_restante.copy()
        for col in ["DATA", "DTENTREGA"]:
            if col in df_export.columns and pd.api.types.is_datetime64_any_dtype(df_export[col]):
                df_export[col] = df_export[col].dt.strftime("%Y-%m-%d").fillna("")
        df_export = df_export.fillna("").astype(str)

        aba = obter_ou_criar_aba_geral(t)
        aba.clear()
        if df_export.empty:
            continue
        valores = [df_export.columns.tolist()] + df_export.values.tolist()
        aba.resize(rows=max(len(valores) + 20, 200), cols=max(len(df_export.columns) + 2, 15))
        aba.update(values=valores)

@st.cache_data(ttl=120, show_spinner="Carregando dados salvos da planilha...")
def carregar_todos_os_dados_da_planilha():
    """Le as tres abas gerais e separa o resultado por estado, para alimentar
    st.session_state['dados_por_estado'] como antes — cada estado enxerga so o
    proprio historico (todas as datas de importacao ja gravadas)."""
    df_lib_geral = carregar_geral_da_planilha("LIBERADOS")
    df_mont_geral = carregar_geral_da_planilha("MONTADOS")
    df_cargas_geral = carregar_geral_da_planilha("CARGAS")

    dados = {}
    estados_presentes = set()
    if not df_lib_geral.empty and "ESTADO" in df_lib_geral.columns:
        estados_presentes |= set(df_lib_geral["ESTADO"].astype(str).unique())
    if not df_mont_geral.empty and "ESTADO" in df_mont_geral.columns:
        estados_presentes |= set(df_mont_geral["ESTADO"].astype(str).unique())
    if not df_cargas_geral.empty and "ESTADO" in df_cargas_geral.columns:
        estados_presentes |= set(df_cargas_geral["ESTADO"].astype(str).unique())

    for estado in estados_presentes:
        df_lib_e = df_lib_geral[df_lib_geral["ESTADO"].astype(str) == estado].copy() if not df_lib_geral.empty else pd.DataFrame()
        df_mont_e = df_mont_geral[df_mont_geral["ESTADO"].astype(str) == estado].copy() if not df_mont_geral.empty else pd.DataFrame()
        df_cargas_e = df_cargas_geral[df_cargas_geral["ESTADO"].astype(str) == estado].copy() if not df_cargas_geral.empty else pd.DataFrame()
        dados[estado] = {"liberados": df_lib_e, "montados": df_mont_e, "cargas": df_cargas_e}
    return dados

def parse_numero_brl(valor):
    """Converte valores numericos vindos da planilha (formato BR ou US) para float."""
    if pd.isna(valor):
        return 0.0
    s = str(valor).strip()
    if s == "":
        return 0.0
    s = s.replace(" ", "").replace("R$", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0

def tratar_dataframe(df):
    """Aplica a limpeza padrao (numeros, datas, textos) em um dataframe de uma aba."""
    df = df.copy()
    df = df.fillna(0)

    for col in ["VLTOTAL", "PESOBRUTOTOT"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_numero_brl)

    for col in ["DATA", "DTENTREGA"]:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
            except Exception:
                pass

    cols_texto = ["NOMECLIENTE", "POSICAO", "NOMERCA", "NOMESUP", "CIDADE",
                  "TIPOVENDA", "PRACA", "DESTINO", "PLACA"]
    for col in cols_texto:
        if col in df.columns:
            df[col] = df[col].replace(0, "").astype(str)

    if "POSICAO" in df.columns:
        posicao_valida = df["POSICAO"].astype(str).str.strip().str.upper().isin(["L", "M"])
        df = df[posicao_valida]

    if "NUMPED" in df.columns:
        numped_valido = pd.to_numeric(df["NUMPED"], errors="coerce").notna()
        df = df[numped_valido]

    df = df.reset_index(drop=True)
    return df

# Mapeamento das colunas da planilha de MONTADOS (RoadNet) para os nomes padrao do sistema
COLUNAS_MONTADOS = {
    "Número do pedido": "NUMPED",
    "Entrega Valor":    "VLTOTAL",
    "Entrega Peso":     "PESOBRUTOTOT",
    "Cliente":          "NOMECLIENTE",
    "Cidade":           "CIDADE",
    "Data de término":  "DATA",
    "Gerenciado Por":   "NOMESUP",
    "FILIAL":           "CODFILIAL",
    "Tipo":             "TIPO_MONTADO",
    "Estado da Ordem":  "STATUS_MONTADO",
}

def tratar_dataframe_montados(df):
    """Limpeza dedicada para a planilha de MONTADOS, que usa colunas diferentes da de Liberados."""
    df = df.copy()
    df = df.rename(columns={k: v for k, v in COLUNAS_MONTADOS.items() if k in df.columns})
    df = df.fillna(0)

    for col in ["VLTOTAL", "PESOBRUTOTOT"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_numero_brl)

    if "DATA" in df.columns:
        try:
            df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True)
        except Exception:
            pass

    cols_texto = ["NOMECLIENTE", "CIDADE", "NOMESUP", "STATUS_MONTADO", "TIPO_MONTADO", "CODFILIAL"]
    for col in cols_texto:
        if col in df.columns:
            df[col] = df[col].replace(0, "").astype(str).str.strip()

    if "NUMPED" in df.columns:
        df["NUMPED"] = normalizar_numped(df["NUMPED"])
        df = df[df["NUMPED"] != ""]
        df = df.drop_duplicates(subset=["NUMPED"])

    df = df.reset_index(drop=True)
    return df

# Mapeamento das colunas da planilha de CARGAS (rotas do RoadNet) para os nomes padrao do sistema
COLUNAS_CARGAS = {
    "ID":                       "IDROTA",
    "Descrição":                "DESCRICAOROTA",
    "Número de paradas":        "NUMPARADAS",
    "Número de Ordens":         "NUMORDENS",
    "Entrega Total Peso":       "PESOBRUTOTOT",
    "Entrega Total Valor":      "VLTOTAL",
    "Capacidade Peso":          "CAPACIDADEPESO",
    "Equipamento":              "PLACA",
    "Distância total":          "DISTANCIATOTAL",
    "Tipos de equipamento":     "TIPOEQUIPAMENTO",
    "Sessão de roteirização":   "SESSAOROTEIRIZACAO",
    "Estado":                   "STATUS_ROTA",
    "Horário Criado":           "DATA",
}

def tratar_dataframe_cargas(df):
    """Limpeza dedicada para a planilha de CARGAS (rotas/equipamentos do RoadNet).
    Usa colunas totalmente diferentes das de Liberados/Montados."""
    df = df.copy()
    df = df.rename(columns={k: v for k, v in COLUNAS_CARGAS.items() if k in df.columns})
    df = df.fillna("")

    # A ultima linha do relatorio costuma ser uma linha de TOTAL (sem descricao da rota) — descarta.
    if "DESCRICAOROTA" in df.columns:
        df = df[df["DESCRICAOROTA"].astype(str).str.strip() != ""]

    for col in ["NUMPARADAS", "NUMORDENS"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce").fillna(0).astype(int)

    for col in ["PESOBRUTOTOT", "VLTOTAL", "CAPACIDADEPESO", "DISTANCIATOTAL"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_numero_brl)

    if "DATA" in df.columns:
        try:
            df["DATA"] = df["DATA"].astype(str).str.replace(r"\s+[A-Z]{2,4}$", "", regex=True)
            df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True)
        except Exception:
            pass

    cols_texto = ["IDROTA", "DESCRICAOROTA", "PLACA", "TIPOEQUIPAMENTO", "SESSAOROTEIRIZACAO", "STATUS_ROTA"]
    for col in cols_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "TIPOEQUIPAMENTO" in df.columns:
        df["TIPOEQUIPAMENTO"] = df["TIPOEQUIPAMENTO"].replace("", "Nao informado")

    if "IDROTA" in df.columns:
        df = df[df["IDROTA"] != ""]
        df = df.drop_duplicates(subset=["IDROTA"])

    df = df.reset_index(drop=True)
    return df

def normalizar_numped(serie):
    """Normaliza numeros de pedido para string, sem sufixo '.0' e sem espacos,
    para permitir comparar Montados x Liberados com seguranca."""
    numeros = pd.to_numeric(serie, errors="coerce")
    resultado = numeros.astype("Int64").astype(str)
    resultado = resultado.where(numeros.notna(), serie.astype(str).str.strip())
    resultado = resultado.replace("<NA>", "").str.strip()
    return resultado

FORMATO_DATA_IMPORTACAO = "%d/%m/%Y"

def normalizar_data_importacao(serie):
    """Converte a coluna DATA_IMPORTACAO para o padrao dd/mm/aaaa, aceitando tanto
    esse formato quanto o antigo aaaa-mm-dd (usado antes desse ajuste) - assim as
    linhas antigas ja gravadas na planilha sao exibidas certas tambem."""
    s = serie.astype(str).str.strip()
    dt = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    faltando = dt.isna()
    if faltando.any():
        dt.loc[faltando] = pd.to_datetime(s[faltando], format=FORMATO_DATA_IMPORTACAO, errors="coerce")
    return dt.dt.strftime(FORMATO_DATA_IMPORTACAO).where(dt.notna(), s)

def ordenar_datas_importacao_desc(lista_datas):
    """Ordena uma lista de datas no formato dd/mm/aaaa da mais recente para a mais antiga."""
    return sorted(
        lista_datas,
        key=lambda d: pd.to_datetime(d, format=FORMATO_DATA_IMPORTACAO, errors="coerce"),
        reverse=True,
    )

def ler_arquivo_upload(arquivo):
    """Le um arquivo enviado pelo usuario (.xlsx, .xls ou .csv) para um DataFrame."""
    nome = arquivo.name.lower()
    if nome.endswith(".csv"):
        return pd.read_csv(arquivo)
    elif nome.endswith(".xls"):
        return pd.read_excel(arquivo, engine="xlrd")
    else:
        return pd.read_excel(arquivo, engine="openpyxl")

def detectar_estado_pelo_nome(nome_arquivo):
    """Tenta identificar a sigla do estado a partir do nome do arquivo enviado."""
    nome = nome_arquivo.upper()

    def tem(padrao):
        return re.search(padrao, nome) is not None

    if tem(r'(?<![A-Z0-9])(WFS|SPW)(?![A-Z0-9])'):
        return "SPW"
    if tem(r'(?<![A-Z0-9])ES(?![A-Z0-9])') or "ESPIRITO SANTO" in nome:
        return "ES"
    if tem(r'(?<![A-Z0-9])MG(?![A-Z0-9])') or "MINAS GERAIS" in nome:
        return "MG"
    if tem(r'D[\.\-_ ]?F(?![A-Z0-9])') or "DISTRITO FEDERAL" in nome:
        return "DF"
    if tem(r'(?<![A-Z0-9])BA(?![A-Z0-9])') or "BAHIA" in nome:
        return "BA"
    if tem(r'(?<![A-Z0-9])AM(?![A-Z0-9])') or "AMAZONAS" in nome:
        return "AM"
    if tem(r'(?<![A-Z0-9])SP(?![A-Z0-9])') or "SAO PAULO" in nome:
        return "SP"
    return None

def detectar_tipo_pelo_nome(nome_arquivo):
    """Identifica se o arquivo enviado e de pedidos LIBERADOS, MONTADOS ou CARGAS."""
    nome = nome_arquivo.upper()
    if "MONTAD" in nome:
        return "MONTADOS"
    if "LIBERAD" in nome:
        return "LIBERADOS"
    if "CARGA" in nome or "ROTA" in nome:
        return "CARGAS"
    return None

def detectar_tipo_pelo_conteudo(colunas):
    """Quando o nome do arquivo nao da nenhuma pista (ex: 'AM.xlsx'), tenta
    identificar o tipo pelas proprias colunas do arquivo — cada tipo de relatorio
    do RoadNet usa um conjunto de colunas bem diferente."""
    cols = {str(c).strip() for c in colunas}
    if {"Tipos de equipamento", "Sessão de roteirização", "Número de paradas"} & cols:
        return "CARGAS"
    if {"Número do pedido", "Estado da Ordem", "Entrega Valor"} & cols:
        return "MONTADOS"
    if {"NUMPED", "VLTOTAL", "POSICAO"} & cols:
        return "LIBERADOS"
    return None

# ==================================================
# FUNCOES DE FORMATACAO
# ==================================================
def fmt_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_kg(valor):
    return f"{valor:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_int(valor):
    return f"{valor:,}".replace(",", ".")

def fmt_data_col(df):
    """Formata colunas de data (datetime) para dd/mm/aaaa para exibicao."""
    df = df.copy()
    for col in ["DATA", "DTENTREGA"]:
        if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%d/%m/%Y").fillna("")
    return df

# ==================================================
# SPARKLINE (SVG LEVE, SEM DEPENDENCIA EXTRA)
# ==================================================
def gerar_sparkline_svg(valores, cor="#F59E0B", largura=110, altura=32):
    """Gera um mini-grafico de tendencia em SVG puro a partir de uma lista de valores reais."""
    valores = [v for v in valores if v is not None]
    if len(valores) < 2 or all(v == valores[0] for v in valores):
        return f'<svg width="{largura}" height="{altura}"></svg>'

    vmin, vmax = min(valores), max(valores)
    faixa = (vmax - vmin) or 1
    n = len(valores)
    passo_x = largura / (n - 1)

    pontos = []
    for i, v in enumerate(valores):
        x = i * passo_x
        y = altura - ((v - vmin) / faixa) * (altura - 4) - 2
        pontos.append((x, y))

    path_linha = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pontos)
    path_area = path_linha + f" L {pontos[-1][0]:.1f},{altura} L 0,{altura} Z"
    uid = f"spk{abs(hash(str(valores)))}"

    return (
        f'<svg width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">'
        f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{cor}" stop-opacity="0.45"/>'
        f'<stop offset="100%" stop-color="{cor}" stop-opacity="0"/>'
        f'</linearGradient></defs>'
        f'<path d="{path_area}" fill="url(#{uid})" stroke="none"/>'
        f'<path d="{path_linha}" fill="none" stroke="{cor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg>'
    )

def serie_diaria(df, coluna, agregacao="sum"):
    """Agrega uma coluna por dia (usando DATA) para alimentar as sparklines reais."""
    if "DATA" not in df.columns or df.empty:
        return []
    tmp = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(tmp["DATA"]):
        tmp["DATA"] = pd.to_datetime(tmp["DATA"], errors="coerce", dayfirst=True)
    tmp = tmp.dropna(subset=["DATA"])
    if tmp.empty:
        return []
    if agregacao == "count":
        serie = tmp.groupby(tmp["DATA"].dt.date)[coluna].count()
    else:
        serie = tmp.groupby(tmp["DATA"].dt.date)[coluna].sum()
    serie = serie.sort_index()
    return serie.tolist()

# ==================================================
# KPI CARD PREMIUM
# ==================================================
def kpi_card_premium(icone, label, valor, descricao, valores_tendencia, cor=None):
    cor = cor or "#F59E0B"
    spark = gerar_sparkline_svg(valores_tendencia, cor=cor)
    return (
        f'<div class="kpi-card-premium">'
        f'<div class="kpi-top"><div class="kpi-icon-circ">{icone}</div></div>'
        f'<div class="kpi-label-p">{label}</div>'
        f'<div class="kpi-valor-p">{valor}</div>'
        f'<div class="kpi-desc-p">{descricao}</div>'
        f'<div class="kpi-spark">{spark}</div>'
        f'</div>'
    )

# ==================================================
# TABELA PREMIUM (com barra de peso/valor e linha de total)
# ==================================================
def tabela_premium_html(df, coluna_barra=None, rotulo_total="Total Geral", max_height=480):
    df = df.copy()
    cols = df.columns.tolist()
    header = "".join(f'<th>{c}</th>' for c in cols)

    max_barra = None
    if coluna_barra and coluna_barra in df.columns:
        try:
            max_barra = df[coluna_barra].max() or 1
        except Exception:
            max_barra = None

    linhas = ""
    for _, row in df.iterrows():
        cells = ""
        for c in cols:
            valor_cel = row[c]
            if c == coluna_barra and max_barra:
                pct = min(100, (float(valor_cel) / max_barra) * 100) if max_barra else 0
                cells += f'<td>{valor_cel}<span class="barra-peso-track"><span class="barra-peso-fill" style="width:{pct:.1f}%;"></span></span></td>'
            else:
                cells += f"<td>{valor_cel}</td>"
        linhas += f"<tr>{cells}</tr>"

    uid = f"tblp_{abs(hash(str(cols) + str(len(df))))}"
    altura_css = f"max-height:{max_height}px;overflow-y:auto;" if max_height else ""

    return f"""
    <div class="tabela-premium-wrap" style="{altura_css}">
    <table class="tabela-premium" id="{uid}">
        <thead><tr>{header}</tr></thead>
        <tbody>{linhas}</tbody>
    </table>
    </div>
    """

def formatar_tabela(df):
    df = fmt_data_col(df)
    df = df.copy()
    if "VLTOTAL"      in df.columns: df["VLTOTAL"]      = df["VLTOTAL"].apply(fmt_brl)
    if "PESOBRUTOTOT" in df.columns: df["PESOBRUTOTOT"] = df["PESOBRUTOTOT"].apply(fmt_kg)
    return df

def resumo_por_cidade(df):
    resumo = df.groupby("CIDADE").agg(
        Pedidos=("NUMPED",       "count"),
        Valor  =("VLTOTAL",      "sum"),
        Peso   =("PESOBRUTOTOT", "sum")
    ).reset_index().sort_values("Valor", ascending=False)
    resumo.rename(columns={"CIDADE": "Cidade"}, inplace=True)
    return resumo

def resumo_por_estado(df):
    resumo = df.groupby("ESTADO").agg(
        Pedidos=("NUMPED",       "count"),
        Valor  =("VLTOTAL",      "sum"),
        Peso   =("PESOBRUTOTOT", "sum")
    ).reset_index().sort_values("Valor", ascending=False)
    resumo.rename(columns={"ESTADO": "Estado"}, inplace=True)
    return resumo

def montar_tabela_com_total(df_num, col_rotulo, col_barra=None, max_height=480):
    """Recebe um dataframe numerico (Pedidos/Valor/Peso) e devolve o HTML premium
    ja formatado, com linha de Total Geral destacada."""
    df_fmt = df_num.copy()
    total_pedidos = int(df_fmt["Pedidos"].sum())
    total_valor   = df_fmt["Valor"].sum()
    total_peso    = df_fmt["Peso"].sum()

    df_fmt["Peso_num"] = df_fmt["Peso"]
    df_fmt["Valor"] = df_fmt["Valor"].apply(fmt_brl)
    df_fmt["Peso"]  = df_fmt["Peso"].apply(fmt_kg)

    cols = [col_rotulo, "Pedidos", "Valor", "Peso"]
    header = "".join(f"<th>{c}</th>" for c in cols)

    max_peso = df_fmt["Peso_num"].max() or 1
    linhas = ""
    for _, row in df_fmt.iterrows():
        pct = min(100, (row["Peso_num"] / max_peso) * 100) if max_peso else 0
        linhas += (
            f"<tr><td>{row[col_rotulo]}</td><td>{fmt_int(int(row['Pedidos']))}</td>"
            f"<td>{row['Valor']}</td>"
            f"<td>{row['Peso']}<span class='barra-peso-track'><span class='barra-peso-fill' style='width:{pct:.1f}%;'></span></span></td></tr>"
        )

    linha_total = (
        f"<tr class='linha-total'><td>Total Geral</td><td>{fmt_int(total_pedidos)}</td>"
        f"<td>{fmt_brl(total_valor)}</td><td>{fmt_kg(total_peso)}</td></tr>"
    )

    uid = f"tbltot_{abs(hash(str(cols)+str(len(df_fmt))))}"
    return (
        f'<div class="tabela-premium-wrap" style="max-height:{max_height}px;overflow-y:auto;">'
        f'<table class="tabela-premium" id="{uid}"><thead><tr>{header}</tr></thead>'
        f'<tbody>{linhas}{linha_total}</tbody></table></div>'
    )

# ==================================================
# TEMA PREMIUM PARA GRAFICOS PLOTLY
# ==================================================
def aplicar_tema_grafico(fig, titulo_size=14):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E8ECF1",
        font_family="Inter, sans-serif",
        title_font_size=titulo_size,
        title_font_color="#FFFFFF",
        margin=dict(l=0, r=10, t=45, b=10),
        legend=dict(font=dict(color="#B8C0CC")),
        hoverlabel=dict(bgcolor="#12151C", font_color="#FFFFFF", bordercolor="rgba(245,158,11,0.4)"),
    )
    fig.update_xaxes(showgrid=False, color="#B8C0CC")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", color="#B8C0CC")
    try:
        fig.update_traces(marker_cornerradius=8, selector=dict(type="bar"))
    except Exception:
        pass
    return fig

GRADIENTE_LARANJA = ["#7c3d00", "#F59E0B", "#FDBA74"]

# ==================================================
# GEOJSON DOS ESTADOS DO BRASIL (para o mapa)
# ==================================================
@st.cache_data(ttl=86400, show_spinner=False)
def obter_geojson_brasil():
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.load(resp)
    except Exception:
        return None

# ==================================================
# SIDEBAR - NAVEGACAO
# ==================================================
ITENS_MENU = [
    ("Dashboard",      "📊"),
    ("Pedidos",        "📦"),
    ("Estados",        "🗺️"),
    ("Cargas",         "🚛"),
    ("Mapas",          "📍"),
    ("Relatorios",     "📈"),
    ("Alertas",        "🔔"),
    ("Configuracoes",  "⚙️"),
]

if "pagina_ativa" not in st.session_state:
    st.session_state["pagina_ativa"] = "Dashboard"

# Dados guardados de forma individual/separada por estado:
# { "AM": {"liberados": df, "montados": df}, "BA": {...}, ... }
# Fonte de verdade: planilha Google Sheets compartilhada (quando configurada em st.secrets).
if "dados_por_estado" not in st.session_state:
    if planilha_configurada():
        st.session_state["dados_por_estado"] = carregar_todos_os_dados_da_planilha()
    else:
        st.session_state["dados_por_estado"] = {}

def tela_login():
    """Login simples por estado: cada pessoa so ve/envia os dados do proprio estado.
    ADMIN enxerga e importa todos os estados. As senhas ficam em
    st.secrets['SENHAS_ESTADOS'], nunca no codigo."""
    senhas_cfg = st.secrets.get("SENHAS_ESTADOS", {})
    if not senhas_cfg:
        st.warning("Login ainda nao configurado. Adicione as senhas em st.secrets['SENHAS_ESTADOS'].")
        return

    opcoes_login = [e for e in ESTADOS_LABELS.keys() if e in senhas_cfg]
    if "ADMIN" in senhas_cfg:
        opcoes_login = ["ADMIN"] + opcoes_login

    col1, col2, col3 = st.columns([1.3, 1.3, 1])
    with col1:
        estado_login = st.selectbox(
            "Quem esta acessando?", opcoes_login,
            format_func=lambda e: "Administrador (todos os estados)" if e == "ADMIN" else ESTADOS_LABELS.get(e, e),
            key="estado_login_sel"
        )
    with col2:
        senha_login = st.text_input("Senha", type="password", key="senha_login_input")
    with col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Entrar", use_container_width=True, type="primary"):
            if senha_login and senha_login == senhas_cfg.get(estado_login):
                st.session_state["usuario_logado"] = estado_login
                st.rerun()
            else:
                st.error("Senha incorreta.")

def dados_visiveis():
    """Retorna somente os dados que o usuario logado tem permissao de ver:
    ADMIN enxerga todos os estados; um login de estado enxerga somente o proprio."""
    todos = st.session_state.get("dados_por_estado", {})
    usuario = st.session_state.get("usuario_logado")
    if usuario == "ADMIN":
        return todos
    if usuario and usuario in todos:
        return {usuario: todos[usuario]}
    return {}

with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <img src="https://is4-ssl.mzstatic.com/image/thumb/Purple126/v4/13/93/57/139357e7-7bd2-43b9-1b59-8a6ffb9665a9/source/512x512bb.jpg">
        <div>
            <div class="t1">DELLY'S</div>
            <div class="t2">Gestao a Vista</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for nome, icone in ITENS_MENU:
        ativo = st.session_state["pagina_ativa"] == nome
        wrapper_class = "sb-ativo" if ativo else ""
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(f"{icone}   {nome}", key=f"nav_{nome}", use_container_width=True):
            st.session_state["pagina_ativa"] = nome
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    estados_com_dados = sorted(dados_visiveis().keys())
    if estados_com_dados:
        st.markdown('<div class="sb-secao">Paginas por estado</div>', unsafe_allow_html=True)
        for estado in estados_com_dados:
            chave_pagina = f"ESTADO::{estado}"
            ativo = st.session_state["pagina_ativa"] == chave_pagina
            wrapper_class = "sb-ativo" if ativo else ""
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(f"🟠   {estado}", key=f"nav_estado_{estado}", use_container_width=True):
                st.session_state["pagina_ativa"] = chave_pagina
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    usuario_logado_sb = st.session_state.get("usuario_logado")
    if usuario_logado_sb:
        st.markdown('<div class="sb-secao">Sessao</div>', unsafe_allow_html=True)
        rotulo_sb = "Administrador" if usuario_logado_sb == "ADMIN" else ESTADOS_LABELS.get(usuario_logado_sb, usuario_logado_sb)
        st.caption(f"Logado como: **{rotulo_sb}**")
        if st.button("Sair", key="sair_sidebar", use_container_width=True):
            st.session_state.pop("usuario_logado", None)
            st.rerun()

pagina_ativa = st.session_state["pagina_ativa"]

# ==================================================
# ACESSO — exige login para ver qualquer dado (ADMIN ve tudo, cada estado ve so o seu)
# ==================================================
usuario_logado = st.session_state.get("usuario_logado")
is_admin = usuario_logado == "ADMIN"

if not usuario_logado:
    st.markdown("""
    <div class="topo-header">
        <div>
            <h2>🔒 Acesso restrito</h2>
            <div class="sub">Faca login com a senha do seu estado (ou do administrador) para acessar o painel</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    tela_login()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================================================
# IMPORTACAO DE DADOS (upload manual, direto no site)
# ==================================================
def processar_lote(arquivos, mapa_estado_manual, mapa_tipo_manual, data_importacao=None):
    """Processa uma lista de arquivos ja enviados e MESCLA o resultado dentro de
    st.session_state['dados_por_estado'], por (estado, tipo). Reprocessar um
    estado/tipo substitui somente aquele par - os demais estados ja carregados
    permanecem intactos. data_importacao (dd/mm/aaaa) marca com que data o lote
    fica salvo no historico - por padrao, hoje."""
    agrupados = {}
    erros = []
    for arquivo in arquivos:
        try:
            estado = detectar_estado_pelo_nome(arquivo.name) or mapa_estado_manual.get(arquivo.name)
            if estado is None:
                erros.append(f"{arquivo.name}: nao foi possivel identificar o estado.")
                continue

            df_bruto = ler_arquivo_upload(arquivo)
            tipo = (
                detectar_tipo_pelo_nome(arquivo.name)
                or mapa_tipo_manual.get(arquivo.name)
                or detectar_tipo_pelo_conteudo(df_bruto.columns)
                or "LIBERADOS"
            )

            if tipo == "MONTADOS":
                df_arquivo = tratar_dataframe_montados(df_bruto)
            elif tipo == "CARGAS":
                df_arquivo = tratar_dataframe_cargas(df_bruto)
            else:
                df_arquivo = tratar_dataframe(df_bruto)
            df_arquivo["ESTADO"] = estado
            agrupados.setdefault((estado, tipo), []).append(df_arquivo)
        except Exception as e:
            erros.append(f"{arquivo.name}: {e}")

    data_alvo = data_importacao or time.strftime(FORMATO_DATA_IMPORTACAO)

    resumo_ok = []
    for (estado, tipo), lista_dfs in agrupados.items():
        df_concat = pd.concat(lista_dfs, ignore_index=True)
        df_concat["DATA_IMPORTACAO"] = data_alvo
        chave = {"LIBERADOS": "liberados", "MONTADOS": "montados", "CARGAS": "cargas"}[tipo]
        st.session_state["dados_por_estado"].setdefault(estado, {})[chave] = df_concat
        if planilha_configurada():
            try:
                salvar_estado_na_planilha(estado, tipo, df_concat, data_importacao=data_alvo)
            except Exception as e:
                erros.append(f"Nao foi possivel salvar {estado} ({tipo}) na planilha compartilhada: {e}")
        resumo_ok.append(f"{estado} ({tipo.title()}): {len(df_concat)} registro(s)")

    if planilha_configurada() and resumo_ok:
        carregar_todos_os_dados_da_planilha.clear()

    return erros, resumo_ok

with st.expander("📥 Importar dados", expanded=(not dados_visiveis())):
    col_info, col_logout = st.columns([4, 1])
    with col_info:
        rotulo_login = "Administrador" if is_admin else ESTADOS_LABELS.get(usuario_logado, usuario_logado)
        st.caption(f"Logado como: **{rotulo_login}**")
    with col_logout:
        if st.button("Sair", use_container_width=True, key="sair_importar"):
            st.session_state.pop("usuario_logado", None)
            st.rerun()

    if is_admin:
        modo_importacao = st.radio(
            "Modo de importacao",
            ["Individual (um estado por vez)", "Combinada (varios arquivos/estados de uma vez)"],
            horizontal=True,
        )
    else:
        modo_importacao = "Individual (um estado por vez)"

    if modo_importacao.startswith("Individual"):
        if is_admin:
            estado_individual = st.selectbox(
                "Estado", list(ESTADOS_LABELS.keys()),
                format_func=lambda e: ESTADOS_LABELS[e], key="estado_individual_sel"
            )
        else:
            estado_individual = usuario_logado
            st.write(f"Enviando dados de: **{ESTADOS_LABELS.get(estado_individual, estado_individual)}**")

        data_individual = st.date_input(
            "🗓️ Data de importacao (use uma data anterior se estiver importando com atraso)",
            value=datetime.date.today(), format="DD/MM/YYYY", key="data_individual_sel"
        )

        arquivos_individual = st.file_uploader(
            f"Liberados, Montados e Cargas - {estado_individual}", type=["xlsx", "xls", "csv"],
            accept_multiple_files=True, key=f"up_individual_{estado_individual}"
        )

        if st.button(f"Processar dados de {estado_individual}", type="primary", use_container_width=True):
            if not arquivos_individual:
                st.warning("Envie ao menos um arquivo (Liberados, Montados e/ou Cargas) para processar.")
            else:
                mapa_estado_manual = {a.name: estado_individual for a in arquivos_individual}
                data_str = data_individual.strftime(FORMATO_DATA_IMPORTACAO)
                erros, resumo_ok = processar_lote(arquivos_individual, mapa_estado_manual, {}, data_importacao=data_str)
                st.session_state["erros_importacao"] = erros
                if resumo_ok:
                    st.success(f"Dados de {estado_individual} atualizados com data de importacao {data_str}! " + " | ".join(resumo_ok))
                    st.rerun()
                elif not erros:
                    st.warning("Nenhum arquivo valido foi processado.")

    else:
        data_combinada = st.date_input(
            "🗓️ Data de importacao (use uma data anterior se estiver importando com atraso)",
            value=datetime.date.today(), format="DD/MM/YYYY", key="data_combinada_sel"
        )

        arquivos = st.file_uploader(
            "Arraste os arquivos de LIBERADOS, MONTADOS e CARGAS de todos os estados aqui — estado e tipo sao identificados automaticamente",
            type=["xlsx", "xls", "csv"],
            accept_multiple_files=True,
            key="up_combinado",
        )

        mapa_estado_manual = {}
        mapa_tipo_manual = {}

        if arquivos:
            estado_indef = [a for a in arquivos if detectar_estado_pelo_nome(a.name) is None]
            tipo_indef = []
            for a in arquivos:
                if detectar_tipo_pelo_nome(a.name):
                    continue
                try:
                    if detectar_tipo_pelo_conteudo(ler_arquivo_upload(a).columns):
                        a.seek(0)
                        continue
                    a.seek(0)
                except Exception:
                    pass
                tipo_indef.append(a)

            if estado_indef or tipo_indef:
                st.caption("Nao identifiquei automaticamente alguns arquivos — confirme manualmente:")
                for arq in arquivos:
                    precisa_estado = arq in estado_indef
                    precisa_tipo = arq in tipo_indef
                    if not precisa_estado and not precisa_tipo:
                        continue
                    col_nome, col_tipo, col_est = st.columns([2.4, 1, 1])
                    with col_nome:
                        st.write(arq.name)
                    with col_tipo:
                        if precisa_tipo:
                            mapa_tipo_manual[arq.name] = st.selectbox(
                                "Tipo", ["LIBERADOS", "MONTADOS", "CARGAS"],
                                key=f"tipo_{arq.name}", label_visibility="collapsed"
                            )
                    with col_est:
                        if precisa_estado:
                            mapa_estado_manual[arq.name] = st.selectbox(
                                "Estado", list(ESTADOS_LABELS.keys()),
                                key=f"manual_{arq.name}", label_visibility="collapsed"
                            )

        processar = st.button("Processar dados", type="primary", use_container_width=True)

        if processar:
            if not arquivos:
                st.warning("Nenhum arquivo foi enviado. Selecione ao menos um arquivo e clique em processar novamente.")
            else:
                data_str_comb = data_combinada.strftime(FORMATO_DATA_IMPORTACAO)
                erros, resumo_ok = processar_lote(arquivos, mapa_estado_manual, mapa_tipo_manual, data_importacao=data_str_comb)
                st.session_state["erros_importacao"] = erros
                if resumo_ok:
                    st.success(f"Dados importados com sucesso com data de importacao {data_str_comb}! " + " | ".join(resumo_ok))
                    st.rerun()
                elif not erros:
                    st.warning("Nenhum arquivo valido foi processado.")

    if is_admin:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.caption("Apagar dados salvos (acao definitiva — remove da planilha compartilhada tambem).")
        estados_para_limpar = ["Todos os estados"] + sorted(st.session_state["dados_por_estado"].keys())
        col_limp1, col_limp2 = st.columns([2, 1])
        with col_limp1:
            alvo_limpeza = st.selectbox("Apagar dados de:", estados_para_limpar, key="alvo_limpeza")
        with col_limp2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Apagar", use_container_width=True):
                if alvo_limpeza == "Todos os estados":
                    for est in list(st.session_state["dados_por_estado"].keys()):
                        if planilha_configurada():
                            apagar_estado_na_planilha(est)
                    st.session_state["dados_por_estado"] = {}
                else:
                    if planilha_configurada():
                        apagar_estado_na_planilha(alvo_limpeza)
                    st.session_state["dados_por_estado"].pop(alvo_limpeza, None)
                if planilha_configurada():
                    carregar_todos_os_dados_da_planilha.clear()
                st.session_state.pop("erros_importacao", None)
                st.rerun()

if st.session_state.get("erros_importacao"):
    with st.expander(f"⚠️ {len(st.session_state['erros_importacao'])} erro(s) na importacao"):
        for e in st.session_state["erros_importacao"]:
            st.write(e)

def montar_df_geral(chave):
    """Concatena os dados dos estados VISIVEIS ao usuario logado (ADMIN ve todos,
    um login de estado ve so o proprio) em um unico DataFrame, para alimentar as
    visoes gerais/agregadas do dashboard."""
    partes = [
        v[chave] for v in dados_visiveis().values()
        if chave in v and v[chave] is not None and not v[chave].empty
    ]
    if not partes:
        return pd.DataFrame()
    return pd.concat(partes, ignore_index=True)

if not dados_visiveis():
    if is_admin:
        st.info("Envie os arquivos de LIBERADOS acima (individual ou combinado) e clique em 'Processar dados' para comecar.")
    else:
        st.info(f"Ainda nao ha dados importados para {ESTADOS_LABELS.get(usuario_logado, usuario_logado)}. Envie os arquivos acima em 'Importar dados'.")
    st.stop()

df = montar_df_geral("liberados")
df_montados_bruto = montar_df_geral("montados")
df_cargas_bruto = montar_df_geral("cargas")

if df.empty:
    st.warning("Os arquivos importados nao geraram nenhum pedido de LIBERADOS valido. Confira os arquivos e tente novamente.")
    st.stop()

# ==================================================
# ACOES DO TOPO
# ==================================================
col_espaco, col_atualiza = st.columns([5, 1.1])
with col_atualiza:
    if st.button("🔄  Atualizar Dados", use_container_width=True):
        if planilha_configurada():
            carregar_todos_os_dados_da_planilha.clear()
            st.session_state["dados_por_estado"] = carregar_todos_os_dados_da_planilha()
        st.rerun()

# ==================================================
# FILTROS GLOBAIS
# ==================================================
estados_carregados = sorted(df["ESTADO"].unique().tolist()) if "ESTADO" in df.columns else []

st.markdown('<div class="glass-box">', unsafe_allow_html=True)
st.markdown('<p class="filter-title">🔎 Filtros</p>', unsafe_allow_html=True)

col_f0, col_f1, col_f2, col_f3, col_f4 = st.columns([1.2, 1.7, 1.3, 1, 1])

with col_f0:
    if is_admin:
        estados_sel = st.multiselect("🌎 Estado", options=estados_carregados, placeholder="Todos os estados",
                                      default=st.session_state.get("estados_sel_mapa", []))
    else:
        estados_sel = [usuario_logado] if usuario_logado in estados_carregados else []
        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
        st.markdown(f"🌎 **Estado:** {ESTADOS_LABELS.get(usuario_logado, usuario_logado)}")

with col_f1:
    cidades_disp = sorted(df["CIDADE"].astype(str).unique().tolist()) if "CIDADE" in df.columns else []
    cidades_sel  = st.multiselect("🏙️ Cidade", options=cidades_disp, placeholder="Todas as cidades")

with col_f2:
    if "DATA_IMPORTACAO" in df.columns:
        datas_disp = ordenar_datas_importacao_desc(df["DATA_IMPORTACAO"].astype(str).unique().tolist())
        datas_sel = st.multiselect("🗓️ Data de Importacao", options=datas_disp, placeholder="Todo o historico")
    else:
        datas_sel = []

with col_f3:
    if "POSICAO" in df.columns:
        posicoes_disp = ["Todas"] + sorted(df["POSICAO"].astype(str).unique().tolist())
        posicao_sel = st.selectbox("📋 Posicao", posicoes_disp)
    else:
        posicao_sel = "Todas"

with col_f4:
    if "TIPOVENDA" in df.columns:
        tipos_disp = ["Todos"] + sorted(df["TIPOVENDA"].astype(str).unique().tolist())
        tipo_sel = st.selectbox("🏷️ Tipo Venda", tipos_disp)
    else:
        tipo_sel = "Todos"
st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# APLICA FILTROS GLOBAIS
# ==================================================
df_filtrado = df.copy()

if estados_sel:
    df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estados_sel)]
if cidades_sel:
    df_filtrado = df_filtrado[df_filtrado["CIDADE"].isin(cidades_sel)]
if datas_sel and "DATA_IMPORTACAO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["DATA_IMPORTACAO"].astype(str).isin(datas_sel)]
if posicao_sel != "Todas" and "POSICAO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["POSICAO"].astype(str) == posicao_sel]
if tipo_sel != "Todos" and "TIPOVENDA" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["TIPOVENDA"].astype(str) == tipo_sel]

# Mesmos filtros de Estado/Cidade/Data aplicados aos MONTADOS (quando importados)
df_montados_filtrado = df_montados_bruto.copy()
if not df_montados_filtrado.empty:
    if estados_sel and "ESTADO" in df_montados_filtrado.columns:
        df_montados_filtrado = df_montados_filtrado[df_montados_filtrado["ESTADO"].isin(estados_sel)]
    if cidades_sel and "CIDADE" in df_montados_filtrado.columns:
        df_montados_filtrado = df_montados_filtrado[df_montados_filtrado["CIDADE"].isin(cidades_sel)]
    if datas_sel and "DATA_IMPORTACAO" in df_montados_filtrado.columns:
        df_montados_filtrado = df_montados_filtrado[df_montados_filtrado["DATA_IMPORTACAO"].astype(str).isin(datas_sel)]

# Mesmos filtros de Estado/Data aplicados as CARGAS (nao tem coluna CIDADE)
df_cargas_filtrado = df_cargas_bruto.copy()
if not df_cargas_filtrado.empty:
    if estados_sel and "ESTADO" in df_cargas_filtrado.columns:
        df_cargas_filtrado = df_cargas_filtrado[df_cargas_filtrado["ESTADO"].isin(estados_sel)]
    if datas_sel and "DATA_IMPORTACAO" in df_cargas_filtrado.columns:
        df_cargas_filtrado = df_cargas_filtrado[df_cargas_filtrado["DATA_IMPORTACAO"].astype(str).isin(datas_sel)]

# ==================================================
# KPIs PREMIUM
# ==================================================
def renderizar_kpis():
    total_pedidos = len(df_filtrado)
    total_valor   = df_filtrado["VLTOTAL"].sum()       if "VLTOTAL"      in df_filtrado.columns else 0
    total_peso    = df_filtrado["PESOBRUTOTOT"].sum()  if "PESOBRUTOTOT" in df_filtrado.columns else 0

    serie_pedidos = serie_diaria(df_filtrado, "NUMPED", "count")
    serie_valor   = serie_diaria(df_filtrado, "VLTOTAL", "sum")
    serie_peso    = serie_diaria(df_filtrado, "PESOBRUTOTOT", "sum")

    n_dias = len([d for d in serie_pedidos if d is not None]) or 0
    desc_pedidos = f"{n_dias} dia(s) no periodo filtrado" if n_dias else "Sem historico diario"

    cards = [
        ("📦", "Total de Pedidos", fmt_int(total_pedidos), desc_pedidos, serie_pedidos),
        ("💰", "Valor Total", fmt_brl(total_valor), "Somatorio do periodo filtrado", serie_valor),
        ("⚖️", "Peso Total", fmt_kg(total_peso), "Somatorio do periodo filtrado", serie_peso),
    ]

    colunas = st.columns(3)
    for coluna, (icone, label, valor, descricao, serie) in zip(colunas, cards):
        with coluna:
            st.markdown(kpi_card_premium(icone, label, valor, descricao, serie), unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ==================================================
# RENDERIZADORES DE CADA VISAO
# ==================================================
def renderizar_por_estados():
    if "ESTADO" not in df_filtrado.columns or df_filtrado.empty:
        st.info("Nenhum dado disponivel.")
        return

    estado_df = resumo_por_estado(df_filtrado)
    estado_ordenado = estado_df.sort_values("Valor")

    col_tabela, col_grafico, col_mapa = st.columns([1.05, 1.05, 0.95])

    with col_tabela:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">📄</span>Resumo por Estado</p>', unsafe_allow_html=True)
        st.markdown(montar_tabela_com_total(estado_df, "Estado", max_height=340), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_grafico:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">📈</span>Valor por Estado</p>', unsafe_allow_html=True)
        fig_estado = px.bar(
            estado_ordenado, x="Valor", y="Estado", orientation="h",
            title="", color="Valor", color_continuous_scale=GRADIENTE_LARANJA,
            custom_data=["Pedidos"],
        )
        fig_estado.update_traces(
            marker_line_width=0,
            text=estado_ordenado["Valor"].apply(fmt_brl),
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=11),
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Valor: R$ %{x:,.2f}<br>Pedidos: %{customdata[0]}<extra></extra>",
        )
        fig_estado.update_layout(
            yaxis=dict(autorange="reversed", title=""),
            xaxis=dict(title="", tickprefix="R$ ", separatethousands=True, range=[0, estado_ordenado["Valor"].max() * 1.3]),
            coloraxis_showscale=False,
            height=340,
            margin=dict(l=0, r=10, t=5, b=10),
        )
        aplicar_tema_grafico(fig_estado, titulo_size=1)
        st.plotly_chart(fig_estado, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_mapa:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">🗺️</span>Distribuicao por Estado</p>', unsafe_allow_html=True)
        renderizar_mapa_interativo(chave="aba_estados", mostrar_titulo=False, altura=340)
        st.markdown('</div>', unsafe_allow_html=True)

def renderizar_por_municipio():
    st.subheader("Resumo por Municipio")
    if df_filtrado.empty:
        st.info("Nenhum dado disponivel.")
        return
    col_tabela, col_grafico = st.columns([1.2, 1])
    with col_tabela:
        st.markdown(montar_tabela_com_total(resumo_por_cidade(df_filtrado), "Cidade"), unsafe_allow_html=True)
    with col_grafico:
        dados_grafico = df_filtrado.groupby("CIDADE")["VLTOTAL"].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(dados_grafico, x="VLTOTAL", y="CIDADE", orientation="h", title="Top 10 Cidades por Valor",
                     color="VLTOTAL", color_continuous_scale=GRADIENTE_LARANJA)
        fig.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Valor: R$ %{x:,.2f}<extra></extra>")
        fig.update_layout(yaxis=dict(autorange="reversed", title=""), xaxis=dict(title="", tickprefix="R$ ", separatethousands=True), coloraxis_showscale=False)
        aplicar_tema_grafico(fig)
        st.plotly_chart(fig, use_container_width=True)

def renderizar_por_praca():
    st.subheader("Quantitativo por Praca")
    if "PRACA" not in df_filtrado.columns or df_filtrado.empty:
        st.info("Nenhum dado disponivel.")
        return

    praca_df = df_filtrado.groupby("PRACA").agg(
        Pedidos=("NUMPED", "count"), Valor=("VLTOTAL", "sum"), Peso=("PESOBRUTOTOT", "sum")
    ).reset_index().sort_values("Valor", ascending=False)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_pr = px.bar(praca_df.sort_values("Valor"), x="Valor", y="PRACA", orientation="h", title="Valor por Praca",
                         color="Valor", color_continuous_scale=GRADIENTE_LARANJA, custom_data=["Pedidos"])
        fig_pr.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Valor: R$ %{x:,.2f}<br>Pedidos: %{customdata[0]}<extra></extra>")
        fig_pr.update_layout(yaxis=dict(autorange="reversed", title=""), xaxis=dict(title="", tickprefix="R$ ", separatethousands=True), coloraxis_showscale=False)
        aplicar_tema_grafico(fig_pr)
        st.plotly_chart(fig_pr, use_container_width=True)

    with col_g2:
        if "TIPOVENDA" in df_filtrado.columns:
            tipo_df = df_filtrado.groupby("TIPOVENDA").agg(Pedidos=("NUMPED", "count"), Valor=("VLTOTAL", "sum")).reset_index()
            fig_tipo = px.pie(tipo_df, names="TIPOVENDA", values="Valor", title="Distribuicao por Tipo de Venda",
                               color_discrete_sequence=GRADIENTE_LARANJA, custom_data=["Pedidos"], hole=0.45)
            fig_tipo.update_traces(textposition="inside", textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Pedidos: %{customdata[0]}<extra></extra>")
            aplicar_tema_grafico(fig_tipo)
            st.plotly_chart(fig_tipo, use_container_width=True)

    st.subheader("Tabela por Praca")
    st.markdown(montar_tabela_com_total(praca_df, "Praca" if "Praca" in praca_df.columns else "PRACA"), unsafe_allow_html=True)

def renderizar_detalhes():
    st.subheader("Todos os Pedidos")
    COLUNAS_EXIB = [c for c in [
        "NUMPED", "ESTADO", "DATA_IMPORTACAO", "DATA", "NOMECLIENTE", "CIDADE", "PRACA",
        "NOMESUP", "NOMERCA", "POSICAO", "TIPOVENDA",
        "VLTOTAL", "PESOBRUTOTOT", "DTENTREGA",
        "NUMCARREGAMENTO", "PLACA", "DESTINO"
    ] if c in df_filtrado.columns]

    col_busca, col_ordem, col_export = st.columns([3, 1, 1])
    with col_busca:
        busca = st.text_input("🔍 Busca rapida (qualquer campo):", placeholder="Digite para filtrar...")
    with col_ordem:
        ordem = st.selectbox("Ordenar por", ["Padrao", "Maior Valor", "Menor Valor"]) if "VLTOTAL" in df_filtrado.columns else "Padrao"

    df_exib = df_filtrado[COLUNAS_EXIB].copy()

    if busca:
        mask = df_exib.astype(str).apply(lambda row: row.str.contains(busca, case=False).any(), axis=1)
        df_exib = df_exib[mask]

    if "VLTOTAL" in df_exib.columns:
        if ordem == "Maior Valor":
            df_exib = df_exib.sort_values("VLTOTAL", ascending=False)
        elif ordem == "Menor Valor":
            df_exib = df_exib.sort_values("VLTOTAL", ascending=True)

    with col_export:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            formatar_tabela(df_exib).to_excel(writer, index=False, sheet_name="Pedidos")
        st.download_button("⬇️ Exportar Excel", data=buffer.getvalue(), file_name="pedidos_filtrados.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.caption(f"{fmt_int(len(df_exib))} pedidos encontrados")
    st.markdown(tabela_premium_html(formatar_tabela(df_exib), coluna_barra=None), unsafe_allow_html=True)

def tabela_comparativo_estado(df_montados, df_liberados, df_pendentes):
    """Monta uma tabela premium comparando Montados x Liberados x Pendentes (Pedidos/Valor/Peso) por estado.
    Pendentes = pedidos LIBERADOS cujo NUMPED nao foi encontrado em Montados do mesmo estado
    (comparacao feita pedido a pedido em calcular_pendentes_montados)."""
    def resumo(df):
        if df.empty or "ESTADO" not in df.columns or "NUMPED" not in df.columns:
            return pd.DataFrame(columns=["Pedidos", "Valor", "Peso"])
        return df.groupby("ESTADO").agg(
            Pedidos=("NUMPED", "count"), Valor=("VLTOTAL", "sum"), Peso=("PESOBRUTOTOT", "sum")
        )

    r_mont = resumo(df_montados)
    r_lib  = resumo(df_liberados)
    r_pend = resumo(df_pendentes)

    estados = sorted(set(r_mont.index) | set(r_lib.index) | set(r_pend.index))
    if not estados:
        return None

    def valor_total(e):
        v = 0.0
        if e in r_mont.index: v += r_mont.loc[e, "Valor"]
        if e in r_lib.index:  v += r_lib.loc[e, "Valor"]
        return v

    estados_ordenados = sorted(estados, key=valor_total, reverse=True)

    tot_mp = tot_mv = tot_mw = tot_lp = tot_lv = tot_lw = tot_pp = tot_pv = tot_pw = 0
    linhas = ""
    for e in estados_ordenados:
        mp = int(r_mont.loc[e, "Pedidos"]) if e in r_mont.index else 0
        mv = float(r_mont.loc[e, "Valor"]) if e in r_mont.index else 0.0
        mw = float(r_mont.loc[e, "Peso"])  if e in r_mont.index else 0.0
        lp = int(r_lib.loc[e, "Pedidos"])  if e in r_lib.index else 0
        lv = float(r_lib.loc[e, "Valor"])  if e in r_lib.index else 0.0
        lw = float(r_lib.loc[e, "Peso"])   if e in r_lib.index else 0.0
        pp = int(r_pend.loc[e, "Pedidos"]) if e in r_pend.index else 0
        pv = float(r_pend.loc[e, "Valor"]) if e in r_pend.index else 0.0
        pw = float(r_pend.loc[e, "Peso"])  if e in r_pend.index else 0.0

        tot_mp += mp; tot_mv += mv; tot_mw += mw
        tot_lp += lp; tot_lv += lv; tot_lw += lw
        tot_pp += pp; tot_pv += pv; tot_pw += pw

        cor_pend = "color:#fca5a5;font-weight:700;" if pp > 0 else ""
        linhas += (
            f"<tr><td>{e}</td>"
            f"<td>{fmt_int(mp)}</td><td>{fmt_brl(mv)}</td><td>{fmt_kg(mw)}</td>"
            f"<td>{fmt_int(lp)}</td><td>{fmt_brl(lv)}</td><td>{fmt_kg(lw)}</td>"
            f"<td style='{cor_pend}'>{fmt_int(pp)}</td><td style='{cor_pend}'>{fmt_brl(pv)}</td><td style='{cor_pend}'>{fmt_kg(pw)}</td></tr>"
        )

    linha_total = (
        f"<tr class='linha-total'><td>Total Geral</td>"
        f"<td>{fmt_int(tot_mp)}</td><td>{fmt_brl(tot_mv)}</td><td>{fmt_kg(tot_mw)}</td>"
        f"<td>{fmt_int(tot_lp)}</td><td>{fmt_brl(tot_lv)}</td><td>{fmt_kg(tot_lw)}</td>"
        f"<td>{fmt_int(tot_pp)}</td><td>{fmt_brl(tot_pv)}</td><td>{fmt_kg(tot_pw)}</td></tr>"
    )

    header = (
        "<tr><th rowspan='2'>Estado</th>"
        "<th colspan='3' style='text-align:center;background:rgba(245,158,11,0.16);'>MONTADOS</th>"
        "<th colspan='3' style='text-align:center;background:rgba(34,197,94,0.16);'>LIBERADOS</th>"
        "<th colspan='3' style='text-align:center;background:rgba(239,68,68,0.16);'>FICARAM PARA TRAS</th></tr>"
        "<tr><th>Pedidos</th><th>Valor</th><th>Peso</th><th>Pedidos</th><th>Valor</th><th>Peso</th>"
        "<th>Pedidos</th><th>Valor</th><th>Peso</th></tr>"
    )

    uid = f"tblcmp_{abs(hash(str(estados_ordenados) + str(tot_mv) + str(tot_pv)))}"
    return (
        f'<div class="tabela-premium-wrap" style="max-height:420px;overflow-y:auto;">'
        f'<table class="tabela-premium" id="{uid}"><thead>{header}</thead>'
        f'<tbody>{linhas}{linha_total}</tbody></table></div>'
    )

def calcular_pendentes_montados(df_liberados, df_montados):
    """Compara Liberados x Montados (por ESTADO + NUMPED) e devolve os pedidos
    LIBERADOS que ainda NAO aparecem como montados (ou seja, ainda nao foram montados).

    Pedidos que existem apenas em Montados (sem estar em Liberados) sao desconsiderados
    de proposito — geralmente sao pedidos encaixados apos o corte de liberados, ou cancelados."""
    if df_liberados.empty or "NUMPED" not in df_liberados.columns:
        return df_liberados.iloc[0:0]

    if df_montados.empty or "NUMPED" not in df_montados.columns:
        return df_liberados.copy()

    numped_lib  = normalizar_numped(df_liberados["NUMPED"])
    numped_mont = normalizar_numped(df_montados["NUMPED"])

    chave_mont = set(zip(df_montados["ESTADO"].astype(str), numped_mont))
    chave_lib  = list(zip(df_liberados["ESTADO"].astype(str), numped_lib))
    mascara_nao_montado = [c not in chave_mont for c in chave_lib]
    return df_liberados[mascara_nao_montado].copy()

def tabela_cargas_resumo_estado(df_cargas):
    """Tabela premium com o resumo de CARGAS por estado: quantidade de rotas,
    quantidade de veiculos (equipamentos) usados e ocupacao (peso carregado vs
    capacidade total), no mesmo estilo das demais tabelas com linha de Total Geral."""
    if df_cargas.empty or "ESTADO" not in df_cargas.columns:
        return None

    resumo = df_cargas.groupby("ESTADO").agg(
        Rotas=("IDROTA", "count"),
        Veiculos=("PLACA", pd.Series.nunique),
        PesoCarregado=("PESOBRUTOTOT", "sum"),
        Capacidade=("CAPACIDADEPESO", "sum"),
    ).reset_index().sort_values("Rotas", ascending=False)
    resumo["Ocupacao"] = resumo.apply(
        lambda r: (r["PesoCarregado"] / r["Capacidade"] * 100) if r["Capacidade"] else 0, axis=1
    )

    tot_rotas = int(resumo["Rotas"].sum())
    tot_veic = int(df_cargas["PLACA"].nunique()) if "PLACA" in df_cargas.columns else 0
    tot_peso = resumo["PesoCarregado"].sum()
    tot_cap = resumo["Capacidade"].sum()
    tot_ocup = (tot_peso / tot_cap * 100) if tot_cap else 0

    linhas = ""
    for _, row in resumo.iterrows():
        linhas += (
            f"<tr><td>{row['ESTADO']}</td><td>{fmt_int(int(row['Rotas']))}</td>"
            f"<td>{fmt_int(int(row['Veiculos']))}</td><td>{fmt_kg(row['PesoCarregado'])}</td>"
            f"<td>{fmt_kg(row['Capacidade'])}</td><td>{row['Ocupacao']:.1f}%</td></tr>"
        )
    linha_total = (
        f"<tr class='linha-total'><td>Total Geral</td><td>{fmt_int(tot_rotas)}</td>"
        f"<td>{fmt_int(tot_veic)}</td><td>{fmt_kg(tot_peso)}</td>"
        f"<td>{fmt_kg(tot_cap)}</td><td>{tot_ocup:.1f}%</td></tr>"
    )
    header = "<tr><th>Estado</th><th>Rotas</th><th>Veiculos</th><th>Peso Carregado</th><th>Capacidade Total</th><th>Ocupacao</th></tr>"

    uid = f"tblcarg_{abs(hash(str(tot_rotas) + str(tot_veic)))}"
    return (
        f'<div class="tabela-premium-wrap" style="max-height:360px;overflow-y:auto;">'
        f'<table class="tabela-premium" id="{uid}"><thead>{header}</thead>'
        f'<tbody>{linhas}{linha_total}</tbody></table></div>'
    )

def tabela_rotas_por_tipo_equipamento(df_cargas):
    """Tabela premium com a quantidade de rotas por tipo de equipamento — uma
    coluna por estado quando ha mais de um estado nos dados, senao uma coluna
    unica de Total."""
    if df_cargas.empty or "TIPOEQUIPAMENTO" not in df_cargas.columns:
        return None

    tem_varios_estados = "ESTADO" in df_cargas.columns and df_cargas["ESTADO"].nunique() > 1
    if tem_varios_estados:
        pivot = df_cargas.pivot_table(index="TIPOEQUIPAMENTO", columns="ESTADO", values="IDROTA", aggfunc="count", fill_value=0)
        pivot["Total"] = pivot.sum(axis=1)
    else:
        pivot = df_cargas.groupby("TIPOEQUIPAMENTO").agg(Total=("IDROTA", "count"))
    pivot = pivot.sort_values("Total", ascending=False)
    colunas = list(pivot.columns)

    header = "<tr><th>Tipo de Equipamento</th>" + "".join(f"<th>{c}</th>" for c in colunas) + "</tr>"
    linhas = ""
    totais = {c: 0 for c in colunas}
    for tipo, row in pivot.iterrows():
        cells = ""
        for c in colunas:
            valor = int(row[c])
            totais[c] += valor
            cells += f"<td>{fmt_int(valor)}</td>"
        linhas += f"<tr><td>{tipo}</td>{cells}</tr>"
    linha_total = "<tr class='linha-total'><td>Total Geral</td>" + "".join(f"<td>{fmt_int(totais[c])}</td>" for c in colunas) + "</tr>"

    uid = f"tbltipo_{abs(hash(str(colunas) + str(totais)))}"
    return (
        f'<div class="tabela-premium-wrap" style="max-height:360px;overflow-y:auto;">'
        f'<table class="tabela-premium" id="{uid}"><thead>{header}</thead>'
        f'<tbody>{linhas}{linha_total}</tbody></table></div>'
    )

def renderizar_montados():
    st.subheader("Montados x Liberados")

    if df_montados_bruto.empty:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.write("Nenhum arquivo de **MONTADOS** foi importado ainda. Abra 'Importar dados' no topo da pagina e envie os arquivos "
                  "(ex: MONTADOS_AM, MONTADOS_SP, MONTADOS_D.F...) junto com os de LIBERADOS — o tipo de cada arquivo e identificado "
                  "automaticamente pelo nome.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df_pendentes = calcular_pendentes_montados(df_filtrado, df_montados_filtrado)

    total_montados  = len(df_montados_filtrado)
    total_liberados = len(df_filtrado)
    total_pendentes = len(df_pendentes)
    pct_atendido = ((total_liberados - total_pendentes) / total_liberados * 100) if total_liberados else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card_premium("🧩", "Total Montados", fmt_int(total_montados), "Pedidos montados no periodo", []), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card_premium("🚚", "Total Liberados", fmt_int(total_liberados), "Pedidos liberados no periodo", []), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card_premium("⏳", "Ficaram para Tras", fmt_int(total_pendentes), "Liberados que ainda nao foram montados", [], cor="#ef4444"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card_premium("✅", "% Atendimento", f"{pct_atendido:.1f}%", "Liberados que ja foram montados", []), unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="painel">', unsafe_allow_html=True)
    st.markdown('<p class="painel-titulo"><span class="ic">🌎</span>Montados x Liberados por Estado</p>', unsafe_allow_html=True)

    tabela_cmp = tabela_comparativo_estado(df_montados_filtrado, df_filtrado, df_pendentes)
    if tabela_cmp is None:
        st.info("Sem dados suficientes para montar a comparacao por estado.")
    else:
        st.markdown(tabela_cmp, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    col_carg1, col_carg2 = st.columns(2)
    with col_carg1:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">🚛</span>Cargas por Estado</p>', unsafe_allow_html=True)
        tabela_carg = tabela_cargas_resumo_estado(df_cargas_filtrado)
        if tabela_carg is None:
            st.info("Nenhum arquivo de CARGAS foi importado ainda. Envie em 'Importar dados' (ex: AM.xlsx).")
        else:
            st.markdown(tabela_carg, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_carg2:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">🚚</span>Rotas por Tipo de Equipamento</p>', unsafe_allow_html=True)
        tabela_tipo = tabela_rotas_por_tipo_equipamento(df_cargas_filtrado)
        if tabela_tipo is None:
            st.info("Nenhum arquivo de CARGAS foi importado ainda. Envie em 'Importar dados' (ex: AM.xlsx).")
        else:
            st.markdown(tabela_tipo, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def renderizar_cargas(df_cargas, titulo_geo="por Estado", mostrar_estado=True):
    """Renderiza os indicadores de CARGAS (rotas/equipamentos do RoadNet):
    tipo de equipamentos, quantidade de rotas, quantidade de rotas por tipo de
    equipamento e medias de paradas. Recebe o DataFrame ja filtrado (geral ou de
    um unico estado)."""
    if df_cargas.empty:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.write("Nenhum arquivo de **CARGAS** foi importado ainda. Abra 'Importar dados' no topo da pagina, "
                  "na secao '🚛 Cargas (rotas)', e envie o relatorio de rotas do RoadNet (ex: AM.xlsx).")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total_rotas = len(df_cargas)
    total_paradas = df_cargas["NUMPARADAS"].sum() if "NUMPARADAS" in df_cargas.columns else 0
    media_paradas = df_cargas["NUMPARADAS"].mean() if "NUMPARADAS" in df_cargas.columns and total_rotas else 0
    total_ordens = df_cargas["NUMORDENS"].sum() if "NUMORDENS" in df_cargas.columns else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card_premium("🚛", "Total de Rotas", fmt_int(total_rotas), "No periodo filtrado", []), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card_premium("🛑", "Media de Paradas por Rota", f"{media_paradas:.1f}", f"{fmt_int(int(total_paradas))} paradas no total", []), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card_premium("📦", "Total de Ordens nas Rotas", fmt_int(int(total_ordens)), "No periodo filtrado", []), unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">🚚</span>Tipo de Equipamentos</p>', unsafe_allow_html=True)
        if "TIPOEQUIPAMENTO" in df_cargas.columns:
            tipo_df = df_cargas.groupby("TIPOEQUIPAMENTO").agg(Rotas=("IDROTA", "count")).reset_index().sort_values("Rotas", ascending=False)
            fig_tipo = px.pie(tipo_df, names="TIPOEQUIPAMENTO", values="Rotas", hole=0.45,
                               color_discrete_sequence=GRADIENTE_LARANJA)
            fig_tipo.update_traces(textposition="inside", textinfo="percent+label",
                                    hovertemplate="<b>%{label}</b><br>Rotas: %{value}<extra></extra>")
            aplicar_tema_grafico(fig_tipo)
            st.plotly_chart(fig_tipo, use_container_width=True)
        else:
            st.info("Sem dados de tipo de equipamento.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        rotulo_geo = "Estado" if mostrar_estado else "Tipo de Equipamento"
        st.markdown(f'<p class="painel-titulo"><span class="ic">📊</span>Quantidade de Rotas {titulo_geo}</p>', unsafe_allow_html=True)
        if mostrar_estado and "ESTADO" in df_cargas.columns:
            qtd_df = df_cargas.groupby("ESTADO").agg(Rotas=("IDROTA", "count")).reset_index().sort_values("Rotas")
            fig_qtd = px.bar(qtd_df, x="Rotas", y="ESTADO", orientation="h", color="Rotas",
                              color_continuous_scale=GRADIENTE_LARANJA)
        elif "TIPOEQUIPAMENTO" in df_cargas.columns:
            qtd_df = df_cargas.groupby("TIPOEQUIPAMENTO").agg(Rotas=("IDROTA", "count")).reset_index().sort_values("Rotas")
            fig_qtd = px.bar(qtd_df, x="Rotas", y="TIPOEQUIPAMENTO", orientation="h", color="Rotas",
                              color_continuous_scale=GRADIENTE_LARANJA)
        else:
            fig_qtd = None
        if fig_qtd is not None:
            fig_qtd.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Rotas: %{x}<extra></extra>")
            fig_qtd.update_layout(yaxis=dict(autorange="reversed", title=""), xaxis=dict(title=""), coloraxis_showscale=False)
            aplicar_tema_grafico(fig_qtd)
            st.plotly_chart(fig_qtd, use_container_width=True)
        else:
            st.info("Sem dados suficientes.")
        st.markdown('</div>', unsafe_allow_html=True)

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">📈</span>Rotas por Tipo de Equipamento</p>', unsafe_allow_html=True)
        if "TIPOEQUIPAMENTO" in df_cargas.columns and "ESTADO" in df_cargas.columns:
            cruzado_df = df_cargas.groupby(["TIPOEQUIPAMENTO", "ESTADO"]).agg(Rotas=("IDROTA", "count")).reset_index()
            fig_cruz = px.bar(cruzado_df, x="TIPOEQUIPAMENTO", y="Rotas", color="ESTADO", barmode="group",
                               color_discrete_sequence=GRADIENTE_LARANJA + ["#60A5FA", "#34D399", "#F472B6"])
            fig_cruz.update_traces(marker_line_width=0)
            fig_cruz.update_layout(xaxis=dict(title=""), yaxis=dict(title="Rotas"))
            aplicar_tema_grafico(fig_cruz)
            st.plotly_chart(fig_cruz, use_container_width=True)
        else:
            st.info("Sem dados suficientes.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g4:
        st.markdown('<div class="painel">', unsafe_allow_html=True)
        st.markdown('<p class="painel-titulo"><span class="ic">🛑</span>Media de Paradas por Tipo de Equipamento</p>', unsafe_allow_html=True)
        if "TIPOEQUIPAMENTO" in df_cargas.columns and "NUMPARADAS" in df_cargas.columns:
            paradas_df = df_cargas.groupby("TIPOEQUIPAMENTO").agg(MediaParadas=("NUMPARADAS", "mean"), Rotas=("IDROTA", "count")).reset_index().sort_values("MediaParadas")
            fig_paradas = px.bar(paradas_df, x="MediaParadas", y="TIPOEQUIPAMENTO", orientation="h",
                                  color="MediaParadas", color_continuous_scale=GRADIENTE_LARANJA, custom_data=["Rotas"])
            fig_paradas.update_traces(
                marker_line_width=0,
                text=paradas_df["MediaParadas"].round(1),
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Media de paradas: %{x:.1f}<br>Rotas: %{customdata[0]}<extra></extra>",
            )
            fig_paradas.update_layout(yaxis=dict(autorange="reversed", title=""), xaxis=dict(title=""), coloraxis_showscale=False)
            aplicar_tema_grafico(fig_paradas)
            st.plotly_chart(fig_paradas, use_container_width=True)
        else:
            st.info("Sem dados suficientes.")
        st.markdown('</div>', unsafe_allow_html=True)

def renderizar_mapa_interativo(chave, mostrar_titulo=True, altura=480):
    if mostrar_titulo:
        st.subheader("Mapa do Brasil - Valor por Estado")

    geo = obter_geojson_brasil()
    if geo is None:
        st.warning("Nao foi possivel carregar o mapa do Brasil no momento (sem acesso a internet ou fonte indisponivel).")
        return

    valor_por_estado_sistema = df_filtrado.groupby("ESTADO")["VLTOTAL"].sum().to_dict() if "ESTADO" in df_filtrado.columns else {}
    pedidos_por_estado_sistema = df_filtrado.groupby("ESTADO")["NUMPED"].count().to_dict() if "ESTADO" in df_filtrado.columns else {}

    # UFs do mapa cujo estado do sistema esta atualmente selecionado no filtro
    ufs_selecionadas = [
        uf for uf, siglas in MAPA_UF_PARA_ESTADO.items()
        if estados_sel and set(siglas) & set(estados_sel)
    ]

    linhas_mapa = []
    for feat in geo["features"]:
        sigla_uf = feat["properties"].get("sigla")
        siglas_sistema = MAPA_UF_PARA_ESTADO.get(sigla_uf, [])
        valor = sum(valor_por_estado_sistema.get(s, 0) for s in siglas_sistema)
        pedidos = sum(pedidos_por_estado_sistema.get(s, 0) for s in siglas_sistema)
        linhas_mapa.append({
            "UF": sigla_uf, "Valor": valor, "Pedidos": pedidos,
            "TemDados": siglas_sistema != [], "Selecionado": sigla_uf in ufs_selecionadas,
        })

    df_mapa = pd.DataFrame(linhas_mapa)
    tem_selecao = len(ufs_selecionadas) > 0

    fig_mapa = px.choropleth(
        df_mapa, geojson=geo, locations="UF", featureidkey="properties.sigla",
        color="Valor", color_continuous_scale=["#3a2410", "#8a4a00", "#F59E0B", "#FDBA74"],
        custom_data=["Pedidos", "TemDados"],
        scope="south america",
        title="",
    )
    fig_mapa.update_traces(
        marker_line_color="rgba(255,255,255,0.25)", marker_line_width=1,
        marker_opacity=0.55 if tem_selecao else 1.0,
        hovertemplate="<b>%{location}</b><br>Valor: R$ %{z:,.2f}<br>Pedidos: %{customdata[0]}<extra></extra>",
    )

    # Camada extra: ilumina em laranja os estados atualmente selecionados no filtro
    if tem_selecao:
        df_sel = df_mapa[df_mapa["Selecionado"]]
        fig_destaque = go.Choropleth(
            geojson=geo, locations=df_sel["UF"], z=[1] * len(df_sel), featureidkey="properties.sigla",
            colorscale=[[0, "#F59E0B"], [1, "#F59E0B"]], showscale=False,
            marker_line_color="#FDBA74", marker_line_width=3, marker_opacity=0.95,
            customdata=df_sel[["Pedidos"]].values,
            hovertemplate="<b>%{location}</b> (selecionado)<br>Pedidos: %{customdata[0]}<extra></extra>",
        )
        fig_mapa.add_trace(fig_destaque)

    aplicar_tema_grafico(fig_mapa)
    fig_mapa.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig_mapa.update_layout(
        title_text="",
        coloraxis_showscale=False,
        height=altura,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    try:
        evento = st.plotly_chart(fig_mapa, use_container_width=True, on_select="rerun", key=f"mapa_brasil_click_{chave}")
    except TypeError:
        # Versao do Streamlit sem suporte a selecao por clique: mostra o mapa normalmente
        st.plotly_chart(fig_mapa, use_container_width=True, key=f"mapa_brasil_static_{chave}")
        evento = None

    try:
        pontos = evento.selection.points if evento and hasattr(evento, "selection") else []
    except Exception:
        pontos = []

    if pontos:
        uf_clicada = pontos[0].get("location")
        siglas_sistema = MAPA_UF_PARA_ESTADO.get(uf_clicada, [])
        if siglas_sistema and st.session_state.get("estados_sel_mapa") != siglas_sistema:
            st.session_state["estados_sel_mapa"] = siglas_sistema
            st.rerun()

    if tem_selecao:
        col_txt, col_btn = st.columns([4, 1])
        with col_txt:
            st.caption(f"Mostrando somente: {', '.join(estados_sel)}. Clique em outro estado para trocar, ou limpe o filtro 'Estado' acima para ver todos.")
        with col_btn:
            if st.button("Ver todos os estados", use_container_width=True, key=f"btn_ver_todos_{chave}"):
                st.session_state["estados_sel_mapa"] = []
                st.rerun()
    else:
        st.caption("Clique em um estado do mapa para ver somente os dados dele. Estados sem dados aparecem escurecidos.")

def renderizar_mapa():
    renderizar_mapa_interativo(chave="pagina_mapa", mostrar_titulo=True)

def renderizar_rodape():
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    n_estados = df_filtrado["ESTADO"].nunique() if "ESTADO" in df_filtrado.columns else 0
    n_cidades = df_filtrado["CIDADE"].nunique() if "CIDADE" in df_filtrado.columns else 0

    itens_rodape = [
        ("🟢", "Monitoramento em Tempo Real", "Dados atualizados a cada importacao"),
        ("✅", "Dados Confiaveis", "Linhas de totais/resumo filtradas automaticamente"),
        ("⚡", "Performance", f"{fmt_int(len(df_filtrado))} pedidos processados"),
        ("🧭", "Visao Completa", f"{n_estados} estado(s) · {fmt_int(n_cidades)} cidade(s)"),
    ]

    colunas = st.columns(4)
    for coluna, (icone, titulo, subtitulo) in zip(colunas, itens_rodape):
        with coluna:
            st.markdown(
                f'<div class="rodape-card"><div class="rodape-ic">{icone}</div>'
                f'<div><div class="rodape-t">{titulo}</div><div class="rodape-s">{subtitulo}</div></div></div>',
                unsafe_allow_html=True
            )

# ==================================================
# PAGINA DEDICADA POR ESTADO
# ==================================================
def renderizar_pagina_estado(estado):
    """Pagina isolada de um unico estado: usa somente os dados carregados
    (liberados/montados) daquele estado especifico, com seus proprios filtros
    de cidade/posicao/tipo de venda - independente da selecao global."""
    dados_estado = st.session_state["dados_por_estado"].get(estado, {})
    df_lib_estado = dados_estado.get("liberados", pd.DataFrame())
    df_mont_estado = dados_estado.get("montados", pd.DataFrame())
    df_cargas_estado = dados_estado.get("cargas", pd.DataFrame())

    label_estado = ESTADOS_LABELS.get(estado, estado)
    st.markdown(f"""
    <div class="topo-header">
        <div>
            <h2>🟠 {label_estado}</h2>
            <div class="sub">Dados individuais deste estado</div>
        </div>
        <div class="topo-meta">
            <div class="lbl">Ultima atualizacao</div>
            <div class="val">{time.strftime('%d/%m/%Y as %H:%M:%S')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_lib_estado.empty:
        st.info(f"Nenhum pedido de LIBERADOS carregado para {label_estado} ainda.")
        return

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<p class="filter-title">🔎 Filtros do estado</p>', unsafe_allow_html=True)
    col_c1, col_c2, col_c3, col_c4 = st.columns([1.6, 1.2, 1, 1])
    with col_c1:
        cidades_disp_e = sorted(df_lib_estado["CIDADE"].astype(str).unique().tolist()) if "CIDADE" in df_lib_estado.columns else []
        cidades_sel_e = st.multiselect("🏙️ Cidade", options=cidades_disp_e, placeholder="Todas as cidades", key=f"cidade_{estado}")
    with col_c2:
        if "DATA_IMPORTACAO" in df_lib_estado.columns:
            datas_disp_e = ordenar_datas_importacao_desc(df_lib_estado["DATA_IMPORTACAO"].astype(str).unique().tolist())
            datas_sel_e = st.multiselect("🗓️ Data Importacao", options=datas_disp_e, placeholder="Todo o historico", key=f"data_{estado}")
        else:
            datas_sel_e = []
    with col_c3:
        if "POSICAO" in df_lib_estado.columns:
            posicoes_disp_e = ["Todas"] + sorted(df_lib_estado["POSICAO"].astype(str).unique().tolist())
            posicao_sel_e = st.selectbox("📋 Posicao", posicoes_disp_e, key=f"posicao_{estado}")
        else:
            posicao_sel_e = "Todas"
    with col_c4:
        if "TIPOVENDA" in df_lib_estado.columns:
            tipos_disp_e = ["Todos"] + sorted(df_lib_estado["TIPOVENDA"].astype(str).unique().tolist())
            tipo_sel_e = st.selectbox("🏷️ Tipo Venda", tipos_disp_e, key=f"tipovenda_{estado}")
        else:
            tipo_sel_e = "Todos"
    st.markdown('</div>', unsafe_allow_html=True)

    df_lib_f = df_lib_estado.copy()
    if cidades_sel_e:
        df_lib_f = df_lib_f[df_lib_f["CIDADE"].isin(cidades_sel_e)]
    if datas_sel_e and "DATA_IMPORTACAO" in df_lib_f.columns:
        df_lib_f = df_lib_f[df_lib_f["DATA_IMPORTACAO"].astype(str).isin(datas_sel_e)]
    if posicao_sel_e != "Todas" and "POSICAO" in df_lib_f.columns:
        df_lib_f = df_lib_f[df_lib_f["POSICAO"].astype(str) == posicao_sel_e]
    if tipo_sel_e != "Todos" and "TIPOVENDA" in df_lib_f.columns:
        df_lib_f = df_lib_f[df_lib_f["TIPOVENDA"].astype(str) == tipo_sel_e]

    df_mont_f = df_mont_estado.copy()
    if not df_mont_f.empty and cidades_sel_e and "CIDADE" in df_mont_f.columns:
        df_mont_f = df_mont_f[df_mont_f["CIDADE"].isin(cidades_sel_e)]
    if not df_mont_f.empty and datas_sel_e and "DATA_IMPORTACAO" in df_mont_f.columns:
        df_mont_f = df_mont_f[df_mont_f["DATA_IMPORTACAO"].astype(str).isin(datas_sel_e)]

    df_cargas_f = df_cargas_estado.copy()
    if not df_cargas_f.empty and datas_sel_e and "DATA_IMPORTACAO" in df_cargas_f.columns:
        df_cargas_f = df_cargas_f[df_cargas_f["DATA_IMPORTACAO"].astype(str).isin(datas_sel_e)]

    total_pedidos_e = len(df_lib_f)
    total_valor_e   = df_lib_f["VLTOTAL"].sum()      if "VLTOTAL" in df_lib_f.columns else 0
    total_peso_e    = df_lib_f["PESOBRUTOTOT"].sum() if "PESOBRUTOTOT" in df_lib_f.columns else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card_premium("📦", "Pedidos Liberados", fmt_int(total_pedidos_e), label_estado, serie_diaria(df_lib_f, "NUMPED", "count")), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card_premium("💰", "Valor Total", fmt_brl(total_valor_e), label_estado, serie_diaria(df_lib_f, "VLTOTAL", "sum")), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card_premium("⚖️", "Peso Total", fmt_kg(total_peso_e), label_estado, serie_diaria(df_lib_f, "PESOBRUTOTOT", "sum")), unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    tabs_estado = st.tabs(["Por Municipio", "Por Praca", "Detalhes dos Pedidos", "Montados x Liberados", "Cargas"])

    with tabs_estado[0]:
        if df_lib_f.empty:
            st.info("Nenhum dado disponivel.")
        else:
            col_tab, col_graf = st.columns([1.2, 1])
            with col_tab:
                st.markdown(montar_tabela_com_total(resumo_por_cidade(df_lib_f), "Cidade"), unsafe_allow_html=True)
            with col_graf:
                dados_grafico_e = df_lib_f.groupby("CIDADE")["VLTOTAL"].sum().sort_values(ascending=False).head(10).reset_index()
                fig_e = px.bar(dados_grafico_e, x="VLTOTAL", y="CIDADE", orientation="h", title="Top 10 Cidades por Valor",
                                color="VLTOTAL", color_continuous_scale=GRADIENTE_LARANJA)
                fig_e.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Valor: R$ %{x:,.2f}<extra></extra>")
                fig_e.update_layout(yaxis=dict(autorange="reversed", title=""), xaxis=dict(title="", tickprefix="R$ ", separatethousands=True), coloraxis_showscale=False)
                aplicar_tema_grafico(fig_e)
                st.plotly_chart(fig_e, use_container_width=True)

    with tabs_estado[1]:
        if "PRACA" not in df_lib_f.columns or df_lib_f.empty:
            st.info("Nenhum dado de Praca disponivel.")
        else:
            praca_df_e = df_lib_f.groupby("PRACA").agg(
                Pedidos=("NUMPED", "count"), Valor=("VLTOTAL", "sum"), Peso=("PESOBRUTOTOT", "sum")
            ).reset_index().sort_values("Valor", ascending=False)
            fig_pr_e = px.bar(praca_df_e.sort_values("Valor"), x="Valor", y="PRACA", orientation="h", title="Valor por Praca",
                               color="Valor", color_continuous_scale=GRADIENTE_LARANJA, custom_data=["Pedidos"])
            fig_pr_e.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Valor: R$ %{x:,.2f}<br>Pedidos: %{customdata[0]}<extra></extra>")
            fig_pr_e.update_layout(yaxis=dict(autorange="reversed", title=""), xaxis=dict(title="", tickprefix="R$ ", separatethousands=True), coloraxis_showscale=False)
            aplicar_tema_grafico(fig_pr_e)
            st.plotly_chart(fig_pr_e, use_container_width=True)
            st.markdown(montar_tabela_com_total(praca_df_e, "Praca" if "Praca" in praca_df_e.columns else "PRACA"), unsafe_allow_html=True)

    with tabs_estado[2]:
        COLUNAS_EXIB_E = [c for c in [
            "NUMPED", "DATA_IMPORTACAO", "DATA", "NOMECLIENTE", "CIDADE", "PRACA",
            "NOMESUP", "NOMERCA", "POSICAO", "TIPOVENDA",
            "VLTOTAL", "PESOBRUTOTOT", "DTENTREGA",
            "NUMCARREGAMENTO", "PLACA", "DESTINO"
        ] if c in df_lib_f.columns]

        col_busca_e, col_export_e = st.columns([3, 1])
        with col_busca_e:
            busca_e = st.text_input("🔍 Busca rapida:", placeholder="Digite para filtrar...", key=f"busca_{estado}")
        df_exib_e = df_lib_f[COLUNAS_EXIB_E].copy()
        if busca_e:
            mask_e = df_exib_e.astype(str).apply(lambda row: row.str.contains(busca_e, case=False).any(), axis=1)
            df_exib_e = df_exib_e[mask_e]
        with col_export_e:
            buffer_e = io.BytesIO()
            with pd.ExcelWriter(buffer_e, engine="openpyxl") as writer:
                formatar_tabela(df_exib_e).to_excel(writer, index=False, sheet_name=estado)
            st.download_button("⬇️ Exportar Excel", data=buffer_e.getvalue(), file_name=f"pedidos_{estado}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key=f"down_{estado}")

        st.caption(f"{fmt_int(len(df_exib_e))} pedidos encontrados")
        st.markdown(tabela_premium_html(formatar_tabela(df_exib_e)), unsafe_allow_html=True)

    with tabs_estado[3]:
        if df_mont_estado.empty:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            st.write(f"Nenhum arquivo de **MONTADOS** foi importado para {label_estado} ainda. "
                     "Use a importacao individual acima e envie o arquivo de Montados deste estado.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            df_pendentes_e = calcular_pendentes_montados(df_lib_f, df_mont_f)
            total_mont_e = len(df_mont_f)
            total_lib_e = len(df_lib_f)
            total_pend_e = len(df_pendentes_e)
            pct_e = ((total_lib_e - total_pend_e) / total_lib_e * 100) if total_lib_e else 0

            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                st.markdown(kpi_card_premium("🧩", "Total Montados", fmt_int(total_mont_e), label_estado, []), unsafe_allow_html=True)
            with cc2:
                st.markdown(kpi_card_premium("⏳", "Ficaram para Tras", fmt_int(total_pend_e), "Liberados ainda nao montados", [], cor="#ef4444"), unsafe_allow_html=True)
            with cc3:
                st.markdown(kpi_card_premium("✅", "% Atendimento", f"{pct_e:.1f}%", label_estado, []), unsafe_allow_html=True)

            if total_pend_e:
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                st.markdown(f"**Pedidos liberados de {label_estado} que ainda nao foram montados:**")
                st.markdown(tabela_premium_html(formatar_tabela(df_pendentes_e[[c for c in COLUNAS_EXIB_E if c in df_pendentes_e.columns]])), unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        col_carg1_e, col_carg2_e = st.columns(2)
        with col_carg1_e:
            st.markdown('<div class="painel">', unsafe_allow_html=True)
            st.markdown('<p class="painel-titulo"><span class="ic">🚛</span>Cargas</p>', unsafe_allow_html=True)
            tabela_carg_e = tabela_cargas_resumo_estado(df_cargas_f)
            if tabela_carg_e is None:
                st.info(f"Nenhum arquivo de CARGAS foi importado para {label_estado} ainda. Envie em 'Importar dados' (ex: {estado}.xlsx).")
            else:
                st.markdown(tabela_carg_e, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_carg2_e:
            st.markdown('<div class="painel">', unsafe_allow_html=True)
            st.markdown('<p class="painel-titulo"><span class="ic">🚚</span>Rotas por Tipo de Equipamento</p>', unsafe_allow_html=True)
            tabela_tipo_e = tabela_rotas_por_tipo_equipamento(df_cargas_f)
            if tabela_tipo_e is None:
                st.info(f"Nenhum arquivo de CARGAS foi importado para {label_estado} ainda. Envie em 'Importar dados' (ex: {estado}.xlsx).")
            else:
                st.markdown(tabela_tipo_e, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs_estado[4]:
        renderizar_cargas(df_cargas_f, mostrar_estado=False)

# ==================================================
# ROTEAMENTO DE PAGINAS (SIDEBAR)
# ==================================================
if pagina_ativa.startswith("ESTADO::"):
    estado_pagina = pagina_ativa.split("::", 1)[1]
    if not is_admin and estado_pagina != usuario_logado:
        st.warning("Voce nao tem permissao para ver os dados desse estado.")
    else:
        renderizar_pagina_estado(estado_pagina)
else:
    renderizar_kpis()

    if pagina_ativa == "Dashboard":
        tabs = st.tabs(["Por Estados", "Por Municipio", "Detalhes dos Pedidos", "Montados"])
        with tabs[0]: renderizar_por_estados()
        with tabs[1]: renderizar_por_municipio()
        with tabs[2]: renderizar_detalhes()
        with tabs[3]: renderizar_montados()

    elif pagina_ativa == "Pedidos":
        renderizar_detalhes()

    elif pagina_ativa == "Estados":
        renderizar_por_estados()

    elif pagina_ativa == "Cargas":
        renderizar_cargas(df_cargas_filtrado, titulo_geo="por Estado", mostrar_estado=is_admin)

    elif pagina_ativa == "Mapas":
        renderizar_mapa()

    elif pagina_ativa == "Relatorios":
        renderizar_por_municipio()
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        renderizar_por_praca()

    elif pagina_ativa == "Alertas":
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.write("Nenhum alerta configurado no momento. Esta area fica pronta para receber regras de alerta (ex: pedidos parados, quedas de valor) em uma proxima etapa.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pagina_ativa == "Configuracoes":
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.write(f"**Estados carregados:** {', '.join(estados_carregados)}")
        st.write(f"**Total de pedidos na base:** {fmt_int(len(df))}")
        st.write(f"**Ultima atualizacao:** {time.strftime('%d/%m/%Y as %H:%M:%S')}")
        st.markdown('</div>', unsafe_allow_html=True)

    renderizar_rodape()
