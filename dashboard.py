# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import io
import re
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    layout="wide",
    page_title="Gestao a Vista - Delly's",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@300;400;600;700&display=swap');

@media (prefers-color-scheme: dark) {
    :root { --bg-overlay: rgba(0,0,0,0.82); --text: white; --text-muted: rgba(255,255,255,0.55); --border: rgba(255,255,255,0.15); --input-bg: rgba(30,30,30,0.95); --input-border: rgba(255,255,255,0.25); --input-text: white; --menu-bg: #1a1a1a; --kpi-bg: rgba(255,255,255,0.07); --kpi-border: rgba(255,255,255,0.15); --tab-color: rgba(255,255,255,0.6); --tab-sel: white; --df-bg: rgba(255,255,255,0.04); --df-border: rgba(255,255,255,0.12); --cell-color: rgba(255,255,255,0.88); --hr: rgba(255,255,255,0.1); --caption: rgba(255,255,255,0.5); --alert-bg: rgba(30,30,30,0.9); --header-border: rgba(255,255,255,0.15); }
}
@media (prefers-color-scheme: light) {
    :root { --bg-overlay: rgba(255,255,255,0.88); --text: #111; --text-muted: rgba(0,0,0,0.55); --border: rgba(0,0,0,0.15); --input-bg: rgba(255,255,255,0.95); --input-border: rgba(0,0,0,0.25); --input-text: #111; --menu-bg: #f5f5f5; --kpi-bg: rgba(255,255,255,0.85); --kpi-border: rgba(0,0,0,0.12); --tab-color: rgba(0,0,0,0.55); --tab-sel: #111; --df-bg: rgba(255,255,255,0.7); --df-border: rgba(0,0,0,0.12); --cell-color: #111; --hr: rgba(0,0,0,0.1); --caption: rgba(0,0,0,0.5); --alert-bg: rgba(240,240,240,0.95); --header-border: rgba(0,0,0,0.12); }
}

header {visibility: hidden;}
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container { padding-left: 1.5rem !important; padding-right: 1.5rem !important; padding-top: 1.5rem; padding-bottom: 1rem; max-width: 100% !important; }
.stApp { background-image: url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important; font-family: 'Nunito', sans-serif !important; }
[data-testid="stAppViewContainer"] { background-color: var(--bg-overlay) !important; }
[data-testid="stMain"], [data-testid="stMainBlockContainer"], .main, .main > div { background-color: transparent !important; }
h1, h2, h3, h4, h5, h6, p, label, div, span, li, a, [class*="st-"], [data-testid] { color: var(--text) !important; font-family: 'Nunito', sans-serif !important; }
[data-testid="stIconMaterial"], .material-symbols-outlined, .material-icons, span[class*="material-symbols"] { font-family: 'Material Symbols Outlined' !important; line-height: 1 !important; }
[data-testid="stExpander"] summary { display: flex !important; align-items: center !important; gap: 8px !important; }
[data-testid="stExpander"] summary span { position: static !important; }
[data-testid="stFileUploaderDropzone"] { flex-wrap: wrap !important; }
input, textarea, select { background-color: var(--input-bg) !important; border: 1px solid var(--input-border) !important; border-radius: 8px !important; color: var(--input-text) !important; -webkit-text-fill-color: var(--input-text) !important; }
[data-testid="stSelectbox"] > div > div, [data-baseweb="select"] > div { background-color: var(--input-bg) !important; border: 1px solid var(--input-border) !important; border-radius: 8px !important; color: var(--input-text) !important; }
[data-baseweb="popover"], [data-baseweb="menu"], ul[data-baseweb="menu"] { background-color: var(--menu-bg) !important; border: 1px solid var(--border) !important; }
[data-baseweb="menu"] li, [role="option"] { background-color: var(--menu-bg) !important; color: var(--text) !important; }
[data-baseweb="menu"] li:hover, [role="option"]:hover { background-color: rgba(255,180,0,0.15) !important; }
[data-testid="stMultiSelect"] > div > div { background-color: var(--input-bg) !important; border: 1px solid var(--input-border) !important; border-radius: 8px !important; }
[data-baseweb="tag"] { background-color: rgba(255,180,0,0.25) !important; border-radius: 4px !important; border: 1px solid rgba(255,180,0,0.5) !important; }
[data-testid="stMetric"] { background: var(--kpi-bg) !important; border: 1px solid var(--kpi-border) !important; border-radius: 10px !important; padding: 12px !important; }
.header-container { display: flex; align-items: center; justify-content: center; gap: 18px; padding: 10px 0 24px 0; border-bottom: 1px solid var(--header-border); margin-bottom: 28px; }
.header-container img { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; border: 3px solid rgba(255, 180, 0, 0.7); box-shadow: 0 0 20px rgba(255, 180, 0, 0.3); }
.header-container h1 { margin: 0; font-family: 'Bebas Neue', sans-serif !important; font-size: 46px !important; letter-spacing: 3px; text-shadow: 0 2px 12px rgba(255,180,0,0.4); }
.kpi-card { background: var(--kpi-bg); border: 1px solid var(--kpi-border); border-top: 3px solid rgba(255, 180, 0, 0.8); border-radius: 12px; padding: 20px 24px; text-align: center; backdrop-filter: blur(8px); transition: transform 0.2s; }
.kpi-card:hover { transform: translateY(-3px); border-top-color: rgba(255, 200, 50, 1); }
.kpi-icon { font-size: 28px; margin-bottom: 6px; }
.kpi-label { font-size: 12px !important; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted) !important; margin-bottom: 4px; }
.kpi-value { font-size: 28px !important; font-weight: 700 !important; line-height: 1.2; }
.filter-title { font-size: 13px !important; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,180,0,0.85) !important; margin-bottom: 10px; }
[data-testid="stTabs"] button { font-family: 'Nunito', sans-serif !important; font-weight: 600 !important; font-size: 13px !important; letter-spacing: 0.5px; color: var(--tab-color) !important; border-radius: 8px 8px 0 0; background: transparent !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--tab-sel) !important; border-bottom: 2px solid rgba(255, 180, 0, 0.9) !important; background: transparent !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] { background-color: transparent !important; }
[data-testid="stDataFrame"] { background: var(--df-bg) !important; border-radius: 10px !important; border: 1px solid var(--df-border) !important; overflow: hidden; }
[data-testid="stDataFrame"] [class*="header"], [data-testid="stDataFrame"] [role="columnheader"] { background: rgba(255, 180, 0, 0.12) !important; color: rgba(255, 180, 0, 1) !important; font-weight: 700 !important; font-size: 12px !important; text-transform: uppercase !important; letter-spacing: 0.8px !important; border-bottom: 1px solid rgba(255,180,0,0.25) !important; }
[data-testid="stDataFrame"] [role="gridcell"] { color: var(--cell-color) !important; font-size: 13px !important; border-bottom: 1px solid var(--border) !important; }
hr { border-color: var(--hr) !important; }
[data-testid="stDownloadButton"] button { background: rgba(255, 180, 0, 0.15) !important; border: 1px solid rgba(255, 180, 0, 0.6) !important; color: rgba(255, 180, 0, 1) !important; font-family: 'Nunito', sans-serif !important; font-weight: 700 !important; font-size: 13px !important; border-radius: 8px !important; padding: 8px 16px !important; width: 100% !important; transition: all 0.2s !important; }
[data-testid="stDownloadButton"] button:hover { background: rgba(255, 180, 0, 0.35) !important; border-color: rgba(255, 210, 80, 1) !important; transform: translateY(-1px) !important; }
[data-testid="stCaptionContainer"] p { color: var(--caption) !important; }
[data-testid="stAlert"] { background-color: var(--alert-bg) !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <img src="https://is4-ssl.mzstatic.com/image/thumb/Purple126/v4/13/93/57/139357e7-7bd2-43b9-1b59-8a6ffb9665a9/source/512x512bb.jpg">
    <h1>Gestao a Vista - Delly's</h1>
</div>
""", unsafe_allow_html=True)

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

def parse_numero_brl(valor):
    """Converte valores numericos vindos da planilha (formato BR ou US) para float."""
    if pd.isna(valor):
        return 0.0
    s = str(valor).strip()
    if s == "":
        return 0.0
    s = s.replace(" ", "").replace("R$", "")
    if "," in s and "." in s:
        # Formato 1.234,56 -> remove separador de milhar, troca virgula por ponto
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
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True).dt.strftime("%d/%m/%Y")
                df[col] = df[col].fillna("")
            except Exception:
                pass

    cols_texto = ["NOMECLIENTE", "POSICAO", "NOMERCA", "NOMESUP", "CIDADE",
                  "TIPOVENDA", "PRACA", "DESTINO", "PLACA"]
    for col in cols_texto:
        if col in df.columns:
            df[col] = df[col].replace(0, "").astype(str)

    # ------------------------------------------------
    # Remove linhas de TOTAIS/RESUMO que vem junto na planilha.
    # Pedidos reais sempre tem POSICAO = "L" (Liberado) ou "M" (Montado)
    # e um NUMPED numerico valido. Linhas de total costumam trazer
    # codigo de filial (ex: 308, 439, 801) na coluna POSICAO e/ou
    # NUMPED vazio - essas sao descartadas para nao duplicar valores.
    # ------------------------------------------------
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

# FUNCOES AUXILIARES
# ==================================================
def fmt_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_kg(valor):
    return f"{valor:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_int(valor):
    return f"{valor:,}".replace(",", ".")

def tabela_html(df, max_height=480, compact=False):
    cols = df.columns.tolist()
    header = "".join(f'<th>{c}</th>' for c in cols)
    rows = ""
    for _, row in df.iterrows():
        cells = "".join(f'<td>{row[c]}</td>' for c in cols)
        rows += f"<tr>{cells}</tr>"
    uid = f"tbl_{abs(hash(str(df.columns.tolist()) + str(len(df)) + str(compact)))}"
    altura_css = f"max-height:{max_height}px;overflow-y:auto;" if max_height else ""
    pad_th = "6px 10px" if compact else "11px 16px"
    pad_td = "5px 10px" if compact else "9px 16px"
    font_th = "10px" if compact else "11px"
    font_td = "12px" if compact else "13px"
    html = f"""
    <div id="{uid}" style="overflow-x:auto;border-radius:10px;border:1px solid rgba(255,255,255,0.12);{altura_css}">
    <table style="width:100%;border-collapse:collapse;font-family:'Nunito',sans-serif;font-size:{font_td};min-width:{'260px' if compact else '600px'};">
        <thead style="position:sticky;top:0;z-index:2;">
            <tr style="background:rgba(20,20,20,0.97);border-bottom:2px solid rgba(255,180,0,0.4);">{header}</tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>
    <style>
    #{uid} th {{ padding:{pad_th};text-align:left;color:rgba(255,210,80,1);font-weight:700;font-size:{font_th};text-transform:uppercase;letter-spacing:0.8px;white-space:nowrap; }}
    #{uid} td {{ padding:{pad_td};color:rgba(255,255,255,0.88);border-bottom:1px solid rgba(255,255,255,0.05);white-space:nowrap; }}
    #{uid} tbody tr:hover td {{ background:rgba(255,180,0,0.08); }}
    #{uid}::-webkit-scrollbar {{ height:7px;width:7px; }}
    #{uid}::-webkit-scrollbar-track {{ background:rgba(255,255,255,0.05);border-radius:10px; }}
    #{uid}::-webkit-scrollbar-thumb {{ background:rgba(255,180,0,0.6);border-radius:10px; }}
    #{uid}::-webkit-scrollbar-thumb:hover {{ background:rgba(255,180,0,0.9); }}
    </style>
    """
    return html

def formatar_tabela(df):
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
    resumo["Valor"] = resumo["Valor"].apply(fmt_brl)
    resumo["Peso"]  = resumo["Peso"].apply(fmt_kg)
    resumo.rename(columns={"CIDADE": "Cidade"}, inplace=True)
    return resumo

def resumo_por_estado(df):
    resumo = df.groupby("ESTADO").agg(
        Pedidos=("NUMPED",       "count"),
        Valor  =("VLTOTAL",      "sum"),
        Peso   =("PESOBRUTOTOT", "sum")
    ).reset_index().sort_values("Valor", ascending=False)
    resumo["Valor_FMT"] = resumo["Valor"].apply(fmt_brl)
    resumo["Peso_FMT"]  = resumo["Peso"].apply(fmt_kg)
    resumo.rename(columns={"ESTADO": "Estado"}, inplace=True)
    return resumo

# ==================================================
# STATUS DOS DADOS IMPORTADOS
# ==================================================
estados_carregados = sorted(df["ESTADO"].unique().tolist()) if "ESTADO" in df.columns else []
st.caption(f"Dados importados de {len(estados_carregados)} estado(s): {', '.join(estados_carregados)} • {fmt_int(len(df))} pedidos no total")

# ==================================================
# FILTROS GLOBAIS
# ==================================================
st.markdown('<p class="filter-title">Filtros</p>', unsafe_allow_html=True)

col_f0, col_f1, col_f2, col_f3, col_f4 = st.columns([1.3, 2, 2, 1, 1])

with col_f0:
    estados_disp = estados_carregados
    estados_sel  = st.multiselect("Filtrar por Estado", options=estados_disp, placeholder="Todos os estados")

with col_f1:
    cidades_disp = sorted(df["CIDADE"].astype(str).unique().tolist()) if "CIDADE" in df.columns else []
    cidades_sel  = st.multiselect("Filtrar por Cidade", options=cidades_disp, placeholder="Todas as cidades")

with col_f2:
    pracas_disp = sorted(df["PRACA"].astype(str).unique().tolist()) if "PRACA" in df.columns else []
    pracas_sel  = st.multiselect("Filtrar por Praca", options=pracas_disp, placeholder="Todas as pracas")

with col_f3:
    if "POSICAO" in df.columns:
        posicoes_disp = ["Todas"] + sorted(df["POSICAO"].astype(str).unique().tolist())
        posicao_sel = st.selectbox("Posicao", posicoes_disp)
    else:
        posicao_sel = "Todas"

with col_f4:
    if "TIPOVENDA" in df.columns:
        tipos_disp = ["Todos"] + sorted(df["TIPOVENDA"].astype(str).unique().tolist())
        tipo_sel = st.selectbox("Tipo Venda", tipos_disp)
    else:
        tipo_sel = "Todos"

# ==================================================
# APLICA FILTROS GLOBAIS
# ==================================================
df_filtrado = df.copy()

if estados_sel:
    df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estados_sel)]

if cidades_sel:
    df_filtrado = df_filtrado[df_filtrado["CIDADE"].isin(cidades_sel)]

if pracas_sel:
    df_filtrado = df_filtrado[df_filtrado["PRACA"].isin(pracas_sel)]

if posicao_sel != "Todas" and "POSICAO" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["POSICAO"].astype(str) == posicao_sel]

if tipo_sel != "Todos" and "TIPOVENDA" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["TIPOVENDA"].astype(str) == tipo_sel]

st.markdown("---")

# ==================================================
# ABAS
# ==================================================
tab_estados, tab1, tab2, tab3, tab4 = st.tabs([
    "Por Estados", "Por Municipio", "Por Supervisor", "Por Praca", "Detalhes dos Pedidos"
])

def mostrar_kpis_globais():
    total_pedidos = len(df_filtrado)
    total_valor   = df_filtrado["VLTOTAL"].sum()       if "VLTOTAL"      in df_filtrado.columns else 0
    total_peso    = df_filtrado["PESOBRUTOTOT"].sum()  if "PESOBRUTOTOT" in df_filtrado.columns else 0

    total_pedidos_fmt = fmt_int(total_pedidos)

    _, c1, c2, c3, _ = st.columns([0.5, 2, 2, 2, 0.5])
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Total de Pedidos</div>
            <div class="kpi-value">{total_pedidos_fmt}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Valor Total</div>
            <div class="kpi-value">{fmt_brl(total_valor)}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚖️</div>
            <div class="kpi-label">Peso Total</div>
            <div class="kpi-value">{fmt_kg(total_peso)}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ---------- ABA POR ESTADOS ----------
with tab_estados:
    mostrar_kpis_globais()
    st.subheader("Resumo por Estado")

    if "ESTADO" not in df_filtrado.columns or df_filtrado.empty:
        st.info("Nenhum dado disponivel.")
    else:
        estado_df = resumo_por_estado(df_filtrado)

        col_tabela, col_grafico = st.columns([1.2, 1])

        with col_tabela:
            tabela_est = estado_df[["Estado", "Pedidos", "Valor_FMT", "Peso_FMT"]].rename(columns={
                "Valor_FMT": "Valor",
                "Peso_FMT" : "Peso",
            })
            st.markdown(tabela_html(tabela_est, max_height=None), unsafe_allow_html=True)

        with col_grafico:
            fig_estado = px.bar(
                estado_df.sort_values("Valor"),
                x="Valor", y="Estado", orientation="h",
                title="Valor por Estado", color="Valor",
                color_continuous_scale=["#b35c00", "#ffb400", "#ffe066"],
                custom_data=["Valor_FMT", "Pedidos"],
            )
            fig_estado.update_traces(
                marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>Valor: %{customdata[0]}<br>Pedidos: %{customdata[1]}<extra></extra>"
            )
            fig_estado.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", title_font_size=15, coloraxis_showscale=False,
                margin=dict(l=0, r=10, t=40, b=10),
                yaxis=dict(autorange="reversed", title=""),
                xaxis=dict(title="", tickprefix="R$ ", separatethousands=True),
            )
            st.plotly_chart(fig_estado, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        fig_pizza_estado = px.pie(
            estado_df, names="Estado", values="Valor",
            title="Participacao por Valor (R$) - Todos os Estados",
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            custom_data=["Valor_FMT", "Pedidos"],
        )
        fig_pizza_estado.update_traces(
            textposition="inside", textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Valor: %{customdata[0]}<br>Pedidos: %{customdata[1]}<extra></extra>"
        )
        fig_pizza_estado.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="white", title_font_size=14,
            legend=dict(font=dict(color="white")),
            margin=dict(l=0, r=0, t=40, b=10),
        )
        st.plotly_chart(fig_pizza_estado, use_container_width=True)

# ---------- ABA 1: POR MUNICIPIO ----------
with tab1:
    mostrar_kpis_globais()
    st.subheader("Resumo por Municipio")
    col_tabela, col_grafico = st.columns([1.2, 1])

    with col_tabela:
        st.markdown(tabela_html(resumo_por_cidade(df_filtrado)), unsafe_allow_html=True)

    with col_grafico:
        if "CIDADE" in df_filtrado.columns and not df_filtrado.empty:
            dados_grafico = df_filtrado.groupby("CIDADE")["VLTOTAL"].sum().sort_values(ascending=False).head(10).reset_index()
            dados_grafico["VLTOTAL_FMT"] = dados_grafico["VLTOTAL"].apply(fmt_brl)
            fig = px.bar(
                dados_grafico, x="VLTOTAL", y="CIDADE", orientation="h",
                title="Top 10 Cidades por Valor", color="VLTOTAL",
                color_continuous_scale=["#b35c00", "#ffb400", "#ffe066"],
                custom_data=["VLTOTAL_FMT"],
            )
            fig.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Valor: %{customdata[0]}<extra></extra>")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", title_font_size=15, coloraxis_showscale=False,
                margin=dict(l=0, r=10, t=40, b=10),
                yaxis=dict(autorange="reversed", title=""),
                xaxis=dict(title="", tickprefix="R$ ", separatethousands=True),
            )
            st.plotly_chart(fig, use_container_width=True)

# ---------- ABA 2: POR SUPERVISOR ----------
with tab2:
    mostrar_kpis_globais()
    st.subheader("Quantitativo por Supervisor")

    if "NOMESUP" not in df_filtrado.columns:
        st.warning("Coluna NOMESUP nao encontrada na planilha.")
    elif df_filtrado.empty:
        st.info("Nenhum dado disponivel com os filtros selecionados.")
    else:
        sup_df = df_filtrado.groupby("NOMESUP").agg(
            Pedidos     =("NUMPED",       "count"),
            Valor_Total =("VLTOTAL",      "sum"),
            Peso_Total  =("PESOBRUTOTOT", "sum")
        ).reset_index().sort_values("Pedidos", ascending=False)

        sup_df["Valor_FMT"] = sup_df["Valor_Total"].apply(fmt_brl)
        sup_df["Peso_FMT"]  = sup_df["Peso_Total"].apply(fmt_kg)

        total_sups = len(sup_df)
        top_sup    = sup_df.iloc[0]["NOMESUP"]
        top_ped    = int(sup_df.iloc[0]["Pedidos"])

        k1, k2, k3 = st.columns(3)
        k1.metric("Total de Supervisores", total_sups)
        k2.metric("Supervisor Lider", top_sup)
        k3.metric("Pedidos do Lider", top_ped)

        st.markdown("<br>", unsafe_allow_html=True)
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig_ped = px.bar(
                sup_df.sort_values("Pedidos"),
                x="Pedidos", y="NOMESUP", orientation="h",
                title="Pedidos por Supervisor", color="Pedidos",
                color_continuous_scale=["#b35c00", "#ffb400", "#ffe066"],
                custom_data=["Valor_FMT"], text="Pedidos",
            )
            fig_ped.update_traces(
                marker_line_width=0, textposition="outside",
                textfont=dict(color="white", size=12),
                hovertemplate="<b>%{y}</b><br>Pedidos: %{x}<br>Valor: %{customdata[0]}<extra></extra>"
            )
            fig_ped.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", title_font_size=14, coloraxis_showscale=False,
                margin=dict(l=0, r=60, t=40, b=10),
                yaxis=dict(title=""), xaxis=dict(title=""),
            )
            st.plotly_chart(fig_ped, use_container_width=True)

        with col_g2:
            fig_pie = px.pie(
                sup_df, names="NOMESUP", values="Valor_Total",
                title="Participacao por Valor (R$)",
                color_discrete_sequence=px.colors.sequential.Oranges_r,
                custom_data=["Valor_FMT"],
            )
            fig_pie.update_traces(
                textposition="inside", textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Valor: %{customdata[0]}<br>Participacao: %{percent}<extra></extra>"
            )
            fig_pie.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", title_font_size=14,
                legend=dict(font=dict(color="white")),
                margin=dict(l=0, r=0, t=40, b=10),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Tabela Resumo por Supervisor")
        tabela_sup = sup_df[["NOMESUP", "Pedidos", "Valor_FMT", "Peso_FMT"]].rename(columns={
            "NOMESUP"   : "Supervisor",
            "Valor_FMT" : "Valor Total",
            "Peso_FMT"  : "Peso Total",
        })
        st.markdown(tabela_html(tabela_sup), unsafe_allow_html=True)

# ---------- ABA 3: POR PRACA ----------
with tab3:
    mostrar_kpis_globais()
    st.subheader("Quantitativo por Praca")

    if "PRACA" not in df_filtrado.columns or df_filtrado.empty:
        st.info("Nenhum dado disponivel.")
    else:
        praca_df = df_filtrado.groupby("PRACA").agg(
            Pedidos     =("NUMPED",       "count"),
            Valor_Total =("VLTOTAL",      "sum"),
            Peso_Total  =("PESOBRUTOTOT", "sum")
        ).reset_index().sort_values("Valor_Total", ascending=False)

        praca_df["Valor_FMT"] = praca_df["Valor_Total"].apply(fmt_brl)
        praca_df["Peso_FMT"]  = praca_df["Peso_Total"].apply(fmt_kg)

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig_pr = px.bar(
                praca_df.sort_values("Valor_Total"),
                x="Valor_Total", y="PRACA", orientation="h",
                title="Valor por Praca", color="Valor_Total",
                color_continuous_scale=["#b35c00", "#ffb400", "#ffe066"],
                custom_data=["Valor_FMT", "Pedidos"],
            )
            fig_pr.update_traces(
                marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>Valor: %{customdata[0]}<br>Pedidos: %{customdata[1]}<extra></extra>"
            )
            fig_pr.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="white", title_font_size=14, coloraxis_showscale=False,
                margin=dict(l=0, r=10, t=40, b=10),
                yaxis=dict(autorange="reversed", title=""),
                xaxis=dict(title="", tickprefix="R$ ", separatethousands=True),
            )
            st.plotly_chart(fig_pr, use_container_width=True)

        with col_g2:
            if "TIPOVENDA" in df_filtrado.columns:
                tipo_df = df_filtrado.groupby("TIPOVENDA").agg(
                    Pedidos=("NUMPED",  "count"),
                    Valor  =("VLTOTAL", "sum")
                ).reset_index()
                tipo_df["Valor_FMT"] = tipo_df["Valor"].apply(fmt_brl)
                fig_tipo = px.pie(
                    tipo_df, names="TIPOVENDA", values="Valor",
                    title="Distribuicao por Tipo de Venda",
                    color_discrete_sequence=["#ffb400", "#b35c00", "#ffe066", "#ff8800"],
                    custom_data=["Valor_FMT", "Pedidos"],
                )
                fig_tipo.update_traces(
                    textposition="inside", textinfo="percent+label",
                    hovertemplate="<b>%{label}</b><br>Valor: %{customdata[0]}<br>Pedidos: %{customdata[1]}<extra></extra>"
                )
                fig_tipo.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font_color="white", title_font_size=14,
                    legend=dict(font=dict(color="white")),
                    margin=dict(l=0, r=0, t=40, b=10),
                )
                st.plotly_chart(fig_tipo, use_container_width=True)

        st.subheader("Tabela por Praca")
        tabela_pr = praca_df[["PRACA", "Pedidos", "Valor_FMT", "Peso_FMT"]].rename(columns={
            "PRACA"     : "Praca",
            "Valor_FMT" : "Valor Total",
            "Peso_FMT"  : "Peso Total",
        })
        st.markdown(tabela_html(tabela_pr), unsafe_allow_html=True)

# ---------- ABA 4: DETALHES DOS PEDIDOS ----------
with tab4:
    mostrar_kpis_globais()
    st.subheader("Todos os Pedidos")

    # Colunas visiveis na tabela (ordem logica)
    COLUNAS_EXIB = [c for c in [
        "NUMPED", "ESTADO", "DATA", "NOMECLIENTE", "CIDADE", "PRACA",
        "NOMESUP", "NOMERCA", "POSICAO", "TIPOVENDA",
        "VLTOTAL", "PESOBRUTOTOT", "DTENTREGA",
        "NUMCARREGAMENTO", "PLACA", "DESTINO"
    ] if c in df_filtrado.columns]

    col_busca, col_ordem, col_export = st.columns([3, 1, 1])
    with col_busca:
        busca = st.text_input("Busca rapida (qualquer campo):", placeholder="Digite para filtrar...")
    with col_ordem:
        if "VLTOTAL" in df_filtrado.columns:
            ordem = st.selectbox("Ordenar por", ["Padrao", "Maior Valor", "Menor Valor"])
        else:
            ordem = "Padrao"

    df_exib = df_filtrado[COLUNAS_EXIB].copy()

    if busca:
        mask = df_exib.apply(lambda row: row.astype(str).str.contains(busca, case=False).any(), axis=1)
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
        st.download_button(
            label="Exportar Excel",
            data=buffer.getvalue(),
            file_name="pedidos_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.caption(f"{fmt_int(len(df_exib))} pedidos encontrados")
    st.markdown(tabela_html(formatar_tabela(df_exib)), unsafe_allow_html=True)
