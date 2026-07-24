# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import io
import re
import json
import time
import urllib.request
import plotly.express as px
import plotly.graph_objects as go

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
[data-testid="stAppViewContainer"] { background: transparent !important; position: relative; z-index: 1; }
[data-testid="stMain"], [data-testid="stMainBlockContainer"], .main, .main > div { background-color: transparent !important; }
.block-container { padding: 1rem 1.6rem 1.4rem 1.6rem !important; max-width: 100% !important; position: relative; z-index: 1; }

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
    "MG.ES": "Minas Gerais / Espirito Santo (MG.ES)",
    "SP":    "Sao Paulo (SP)",
    "SPW":   "Sao Paulo WFS (SPW)",
}

# UF real no mapa -> sigla(s) usada(s) no nosso sistema
MAPA_UF_PARA_ESTADO = {
    "AM": ["AM"],
    "BA": ["BA"],
    "DF": ["DF"],
    "MG": ["MG.ES"],
    "SP": ["SP", "SPW"],
}

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
    if tem(r'MG[\.\-_ ]?ES') or "MINAS GERAIS" in nome:
        return "MG.ES"
    if tem(r'D[\.\-_ ]?F(?![A-Z0-9])') or "DISTRITO FEDERAL" in nome:
        return "DF"
    if tem(r'(?<![A-Z0-9])BA(?![A-Z0-9])') or "BAHIA" in nome:
        return "BA"
    if tem(r'(?<![A-Z0-9])AM(?![A-Z0-9])') or "AMAZONAS" in nome:
        return "AM"
    if tem(r'(?<![A-Z0-9])SP(?![A-Z0-9])') or "SAO PAULO" in nome:
        return "SP"
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
    ("Mapas",          "📍"),
    ("Relatorios",     "📈"),
    ("Alertas",        "🔔"),
    ("Configuracoes",  "⚙️"),
]

if "pagina_ativa" not in st.session_state:
    st.session_state["pagina_ativa"] = "Dashboard"

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

pagina_ativa = st.session_state["pagina_ativa"]

# ==================================================
# IMPORTACAO DE DADOS (upload manual, direto no site)
# ==================================================
with st.expander("📥 Importar dados", expanded=("dados_carregados" not in st.session_state)):
    arquivos = st.file_uploader(
        "Arraste os arquivos de todos os estados aqui — o estado de cada um e identificado automaticamente",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True,
    )

    mapa_estado_manual = {}

    if arquivos:
        nao_identificados = [a for a in arquivos if detectar_estado_pelo_nome(a.name) is None]

        if nao_identificados:
            st.caption("Nao identifiquei o estado destes arquivos pelo nome — selecione manualmente:")
            for arq in nao_identificados:
                col_nome, col_sel = st.columns([3, 1])
                with col_nome:
                    st.write(arq.name)
                with col_sel:
                    mapa_estado_manual[arq.name] = st.selectbox(
                        "Estado", list(ESTADOS_LABELS.keys()),
                        key=f"manual_{arq.name}", label_visibility="collapsed"
                    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        processar = st.button("Processar dados", type="primary", use_container_width=True)
    with col_btn2:
        limpar = st.button("Limpar dados carregados", use_container_width=True)

    if limpar:
        st.session_state.pop("dados_carregados", None)
        st.session_state.pop("erros_importacao", None)
        st.rerun()

    if processar:
        if not arquivos:
            st.warning("Nenhum arquivo foi enviado. Selecione ao menos um arquivo e clique em processar novamente.")
        else:
            frames = []
            erros = []
            for arquivo in arquivos:
                try:
                    estado = detectar_estado_pelo_nome(arquivo.name) or mapa_estado_manual.get(arquivo.name)
                    if estado is None:
                        erros.append(f"{arquivo.name}: nao foi possivel identificar o estado.")
                        continue
                    df_estado = ler_arquivo_upload(arquivo)
                    df_estado = tratar_dataframe(df_estado)
                    df_estado["ESTADO"] = estado
                    frames.append(df_estado)
                except Exception as e:
                    erros.append(f"{arquivo.name}: {e}")

            st.session_state["erros_importacao"] = erros

            if frames:
                estados_processados = sorted(set(f["ESTADO"].iloc[0] for f in frames))
                st.session_state["dados_carregados"] = pd.concat(frames, ignore_index=True)
                st.success(f"Dados importados com sucesso! Estados: {', '.join(estados_processados)}")
            elif not erros:
                st.warning("Nenhum arquivo valido foi processado.")

if st.session_state.get("erros_importacao"):
    with st.expander(f"⚠️ {len(st.session_state['erros_importacao'])} erro(s) na importacao"):
        for e in st.session_state["erros_importacao"]:
            st.write(e)

if "dados_carregados" not in st.session_state:
    st.info("Envie os arquivos acima e clique em 'Processar dados' para comecar.")
    st.stop()

df = st.session_state["dados_carregados"]

if df.empty:
    st.warning("Os arquivos importados nao geraram nenhum pedido valido. Confira os arquivos e tente novamente.")
    st.stop()

# ==================================================
# CABECALHO SUPERIOR
# ==================================================
st.markdown(f"""
<div class="topo-header">
    <div>
        <h2>Ola, Gestor 👋</h2>
        <div class="sub">Acompanhe os pedidos em tempo real</div>
    </div>
    <div class="topo-meta">
        <div class="lbl">Ultima atualizacao</div>
        <div class="val">{time.strftime('%d/%m/%Y as %H:%M:%S')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_espaco, col_atualiza = st.columns([5, 1.1])
with col_atualiza:
    if st.button("🔄  Atualizar Dados", use_container_width=True):
        st.rerun()

# ==================================================
# FILTROS GLOBAIS
# ==================================================
estados_carregados = sorted(df["ESTADO"].unique().tolist()) if "ESTADO" in df.columns else []

st.markdown('<div class="glass-box">', unsafe_allow_html=True)
st.markdown('<p class="filter-title">🔎 Filtros</p>', unsafe_allow_html=True)

col_f0, col_f1, col_f3, col_f4 = st.columns([1.3, 2, 1, 1])

with col_f0:
    estados_sel = st.multiselect("🌎 Estado", options=estados_carregados, placeholder="Todos os estados",
                                  default=st.session_state.get("estados_sel_mapa", []))

with col_f1:
    cidades_disp = sorted(df["CIDADE"].astype(str).unique().tolist()) if "CIDADE" in df.columns else []
    cidades_sel  = st.multiselect("🏙️ Cidade", options=cidades_disp, placeholder="Todas as cidades")

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
if posicao_sel != "Todas" and "POSICAO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["POSICAO"].astype(str) == posicao_sel]
if tipo_sel != "Todos" and "TIPOVENDA" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["TIPOVENDA"].astype(str) == tipo_sel]

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
    st.subheader("Resumo por Estado")
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
        "NUMPED", "ESTADO", "DATA", "NOMECLIENTE", "CIDADE", "PRACA",
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
# ROTEAMENTO DE PAGINAS (SIDEBAR)
# ==================================================
renderizar_kpis()

if pagina_ativa == "Dashboard":
    tabs = st.tabs(["Por Estados", "Por Municipio", "Detalhes dos Pedidos"])
    with tabs[0]: renderizar_por_estados()
    with tabs[1]: renderizar_por_municipio()
    with tabs[2]: renderizar_detalhes()

elif pagina_ativa == "Pedidos":
    renderizar_detalhes()

elif pagina_ativa == "Estados":
    renderizar_por_estados()

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
