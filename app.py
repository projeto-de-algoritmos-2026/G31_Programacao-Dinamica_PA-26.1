import streamlit as st
import pandas as pd
from knapsack import knapsack_iterativo, knapsack_recursivo

st.set_page_config(page_title="Planejador de Mala", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
# Paleta: rose #c96080 · lavender #9d7fc0 · plum #3d2233 · blush #fdf6f9
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&family=Lato:wght@400;600&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');
.material-symbols-rounded { font-family: 'Material Symbols Rounded'; font-style: normal;
    font-weight: normal; font-size: inherit; line-height: 1; vertical-align: -0.15em; }

/* Fundo com gradiente suave */
.stApp {
    background: linear-gradient(150deg, #fdf6f9 0%, #f4edf8 55%, #fdf6f9 100%);
    font-family: 'Lato', sans-serif;
}

/* Headings — Playfair + rose */
h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #c96080 !important;
    font-weight: 500 !important;
}

/* Divider */
hr { border-color: #edd6e4 !important; }

/* ── Botões ── */
button {
    border-radius: 30px !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
    transition: box-shadow 0.2s, transform 0.2s !important;
}
/* Primário */
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"],
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #c96080, #9d7fc0) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(180, 100, 140, 0.35) !important;
}
[data-testid="stBaseButton-primary"]:hover {
    box-shadow: 0 6px 22px rgba(180, 100, 140, 0.5) !important;
    transform: translateY(-1px) !important;
}
/* Secundário */
[data-testid="stBaseButton-secondary"] {
    background: #fff !important;
    border: 1.5px solid #c96080 !important;
    color: #c96080 !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    background: #fdf0f4 !important;
}

/* ── Métricas ── */
[data-testid="metric-container"] {
    background: #fff !important;
    border-radius: 20px !important;
    padding: 16px 20px !important;
    border: 1px solid #edd6e4 !important;
    box-shadow: 0 3px 16px rgba(160, 100, 130, 0.08) !important;
}
[data-testid="stMetricLabel"] p {
    color: #9d7fc0 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stMetricValue"] { color: #c96080 !important; font-weight: 700 !important; }

/* ── Barra de progresso ── */
[data-testid="stProgressBar"] > div {
    background: linear-gradient(90deg, #c96080, #9d7fc0) !important;
    border-radius: 10px !important;
}

/* ── Inputs e selectbox ── */
input, [data-testid="stSelectbox"] > div > div {
    border-radius: 12px !important;
    border-color: #ddc4d4 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid #edd6e4 !important;
    border-radius: 16px !important;
    background: #fff !important;
    box-shadow: 0 2px 10px rgba(160, 100, 130, 0.06) !important;
}

/* ── Dataframe wrapper ── */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid #edd6e4 !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 16px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #fdf6f9; }
::-webkit-scrollbar-thumb { background: #c9a0b8; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Dados padrão ───────────────────────────────────────────────────────────────
ITENS_PADRAO = [
    {"nome": "Carregador",       "peso": 0.2, "importancia": 10},
    {"nome": "Remédios",         "peso": 0.2, "importancia": 10},
    {"nome": "Adaptador tomada", "peso": 0.1, "importancia": 9},
    {"nome": "Câmera",           "peso": 0.8, "importancia": 9},
    {"nome": "Protetor solar",   "peso": 0.3, "importancia": 8},
    {"nome": "Tênis",            "peso": 1.0, "importancia": 8},
    {"nome": "Calça jeans",      "peso": 1.5, "importancia": 7},
    {"nome": "Camisetas (3×)",   "peso": 0.9, "importancia": 6},
    {"nome": "Guarda-chuva",     "peso": 0.5, "importancia": 5},
    {"nome": "Livro",            "peso": 0.5, "importancia": 4},
]

if "itens" not in st.session_state:
    st.session_state.itens = ITENS_PADRAO.copy()

# ── Cabeçalho ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1.8rem 0 0.6rem;">
    <p style="font-family:'Playfair Display',Georgia,serif; font-size:2.6rem;
              color:#c96080; margin:0; font-weight:500; letter-spacing:1px;">
        <span class="material-symbols-rounded" style="font-size:2.4rem;">luggage</span>
        Planejador de Mala de Viagem
    </p>
    <p style="font-family:'Lato',sans-serif; font-size:1rem; color:#9d7fc0;
              margin-top:0.4rem; font-style:italic; letter-spacing:0.5px;">
        organize · simplifique · viaje leve
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

esq, dir = st.columns([1, 2], gap="large")

# ── Painel esquerdo ────────────────────────────────────────────────────────────
with esq:
    st.subheader(":material/tune: Configuração")
    capacidade = st.slider("Limite de peso da mala (kg)", 1.0, 30.0, 8.0, 0.5)

    algoritmo = st.radio(
        "Versão do algoritmo",
        ["Iterativo (Tabulation)", "Recursivo (Memoization)"],
        help="Ambas produzem o mesmo resultado ótimo. A versão iterativa constrói a tabela DP de baixo para cima; a recursiva resolve de cima para baixo com cache."
    )

    st.subheader(":material/add_circle: Adicionar item")
    with st.form("form_item", clear_on_submit=True):
        nome = st.text_input("Nome do item")
        c1, c2 = st.columns(2)
        peso = c1.number_input("Peso (kg)", min_value=0.1, max_value=30.0,
                                value=0.5, step=0.1, format="%.1f")
        importancia = c2.slider("Importância", 1, 10, 5)
        adicionado = st.form_submit_button("Adicionar", icon=":material/add:", use_container_width=True)
        if adicionado and nome.strip():
            st.session_state.itens.append({
                "nome": nome.strip(),
                "peso": peso,
                "importancia": importancia
            })
            st.rerun()

    if st.session_state.itens:
        opcoes = [f"{i+1}. {it['nome']}" for i, it in enumerate(st.session_state.itens)]
        escolha = st.selectbox("Remover item", opcoes, label_visibility="collapsed")
        idx_remover = opcoes.index(escolha)
        col_rem, col_rst = st.columns(2)
        if col_rem.button("Remover", icon=":material/delete:", use_container_width=True):
            st.session_state.itens.pop(idx_remover)
            st.rerun()
        if col_rst.button("Restaurar", icon=":material/restart_alt:", use_container_width=True):
            st.session_state.itens = ITENS_PADRAO.copy()
            st.rerun()

# ── Painel direito ─────────────────────────────────────────────────────────────
with dir:
    if not st.session_state.itens:
        st.info("Adicione ao menos um item para continuar.")
    else:
        st.subheader(":material/inventory_2: Itens disponíveis")
        df_itens = pd.DataFrame(st.session_state.itens)
        df_itens.index = range(1, len(df_itens) + 1)
        df_itens.columns = ["Nome", "Peso (kg)", "Importância"]
        st.dataframe(df_itens, use_container_width=True, height=250)

        st.subheader(":material/auto_awesome: Resultado")
        if st.button("Resolver", icon=":material/play_arrow:", type="primary", use_container_width=True):
            itens = st.session_state.itens
            cap_int = round(capacidade * 10)
            pesos_int = [round(it["peso"] * 10) for it in itens]
            valores = [it["importancia"] for it in itens]

            if algoritmo.startswith("Iterativo"):
                valor_max, idx_sel, tabela_dp = knapsack_iterativo(cap_int, pesos_int, valores)
            else:
                valor_max, idx_sel = knapsack_recursivo(cap_int, pesos_int, valores)
                tabela_dp = None

            itens_sel = [itens[i] for i in idx_sel]
            peso_total = sum(it["peso"] for it in itens_sel)

            m1, m2, m3 = st.columns(3)
            m1.metric("Itens selecionados", f"{len(itens_sel)} de {len(itens)}")
            m2.metric("Peso utilizado", f"{peso_total:.1f} / {capacidade:.1f} kg")
            m3.metric("Importância total", str(valor_max))

            ocupacao = peso_total / capacidade
            st.progress(min(ocupacao, 1.0), text=f"Ocupação da mala: {ocupacao:.0%}")

            if itens_sel:
                st.success("**Itens recomendados para levar**")
                df_sel = pd.DataFrame(itens_sel)
                df_sel.index = range(1, len(df_sel) + 1)
                df_sel.columns = ["Nome", "Peso (kg)", "Importância"]
                st.dataframe(df_sel, use_container_width=True)
            else:
                st.warning("Nenhum item cabe no limite de peso definido.")

            if tabela_dp is not None:
                with st.expander("Ver tabela DP (Iterativo)", icon=":material/table_chart:"):
                    st.caption(
                        "Cada célula dp[i][j] representa a importância máxima "
                        "considerando os primeiros i itens com capacidade j × 0,1 kg. "
                        "A resposta final está na célula inferior direita."
                    )
                    nomes = [it["nome"] for it in itens]
                    rotulos = [f"{j/10:.1f}" for j in range(cap_int + 1)]
                    df_dp = pd.DataFrame(tabela_dp[1:], index=nomes, columns=rotulos)
                    st.dataframe(df_dp, use_container_width=True)
