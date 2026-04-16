import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime
import plotly.graph_objects as go
import plotly.express as px

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RubiniCoins – Farm Manager",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── TIBIA-STYLE CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=IM+Fell+English:ital@0;1&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* ── ROOT VARS ─────────────────────────────── */
:root {
    --bg-void:        #080400;
    --bg-panel:       #150c00;
    --bg-card:        #1e1200;
    --bg-inner:       #2a1800;
    --gold-bright:    #d4a843;
    --gold-dim:       #9a7530;
    --gold-glow:      #f0c060;
    --parchment:      #e8d5a3;
    --parchment-dim:  #c4a870;
    --blood-red:      #8b1a1a;
    --blood-glow:     #cc2222;
    --border-gold:    #6b4c2a;
    --border-bright:  #a07840;
    --success-green:  #4a8a3a;
    --success-glow:   #72c256;
    --shadow-gold:    rgba(212, 168, 67, 0.25);
    --shadow-dark:    rgba(0, 0, 0, 0.8);
}

/* ── GLOBAL ────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-void) !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(100, 60, 0, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(80, 40, 0, 0.06) 0%, transparent 60%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Crect width='60' height='60' fill='none'/%3E%3Cpath d='M0 0h60v60H0z' fill='none' stroke='%23ffffff04' stroke-width='0.5'/%3E%3Cpath d='M30 0v60M0 30h60' stroke='%23ffffff02' stroke-width='0.3'/%3E%3C/svg%3E");
    font-family: 'Crimson Text', Georgia, serif !important;
    color: var(--parchment) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0800 0%, #150c00 40%, #0e0800 100%) !important;
    border-right: 2px solid var(--border-gold) !important;
    box-shadow: 4px 0 20px rgba(0,0,0,0.8) !important;
}

[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 40px,
        rgba(212,168,67,0.02) 40px,
        rgba(212,168,67,0.02) 41px
    );
    pointer-events: none;
}

/* ── TYPOGRAPHY ────────────────────────────── */
h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold-bright) !important;
    text-shadow: 0 0 20px var(--shadow-gold), 0 2px 4px var(--shadow-dark) !important;
    letter-spacing: 0.04em !important;
}

.stMarkdown p { color: var(--parchment) !important; }

/* ── INPUTS ────────────────────────────────── */
input[type="number"], input[type="text"], textarea,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background: var(--bg-inner) !important;
    border: 1px solid var(--border-gold) !important;
    border-radius: 3px !important;
    color: var(--parchment) !important;
    font-family: 'Crimson Text', serif !important;
    font-size: 1.05rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

input[type="number"]:focus, input[type="text"]:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold-bright) !important;
    box-shadow: 0 0 12px var(--shadow-gold) !important;
    outline: none !important;
}

/* ── BUTTONS ───────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #3d2200 0%, #5a3300 50%, #3d2200 100%) !important;
    border: 1px solid var(--gold-dim) !important;
    border-top-color: var(--gold-bright) !important;
    border-radius: 3px !important;
    color: var(--gold-bright) !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    padding: 0.5rem 1.2rem !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.6), inset 0 1px 0 rgba(212,168,67,0.2) !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5a3300 0%, #7a4800 50%, #5a3300 100%) !important;
    border-color: var(--gold-bright) !important;
    box-shadow: 0 0 18px var(--shadow-gold), 0 4px 10px rgba(0,0,0,0.8) !important;
    color: var(--gold-glow) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── SELECT / DATE ─────────────────────────── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stDateInput"] > div > div {
    background: var(--bg-inner) !important;
    border-color: var(--border-gold) !important;
    color: var(--parchment) !important;
}

/* ── METRIC CARDS ──────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--bg-card), var(--bg-inner)) !important;
    border: 1px solid var(--border-gold) !important;
    border-radius: 4px !important;
    padding: 1rem !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.7), inset 0 1px 0 rgba(212,168,67,0.1) !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold-bright), transparent);
}

[data-testid="stMetricLabel"] {
    color: var(--parchment-dim) !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: var(--gold-bright) !important;
    font-family: 'Cinzel', serif !important;
    font-size: 1.4rem !important;
    text-shadow: 0 0 15px var(--shadow-gold) !important;
}

[data-testid="stMetricDelta"] { font-family: 'Crimson Text', serif !important; }

/* ── TABS ──────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--bg-panel) !important;
    border-bottom: 2px solid var(--border-gold) !important;
    gap: 0 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--parchment-dim) !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
    border-bottom: 3px solid transparent !important;
    transition: all 0.2s !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--gold-bright) !important;
    background: rgba(212,168,67,0.06) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--gold-bright) !important;
    background: rgba(212,168,67,0.08) !important;
    border-bottom: 3px solid var(--gold-bright) !important;
    text-shadow: 0 0 12px var(--shadow-gold) !important;
}

/* ── DATAFRAME ─────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-gold) !important;
    border-radius: 4px !important;
    overflow: hidden !important;
}

/* ── DIVIDER ───────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border-gold) !important;
    margin: 1.5rem 0 !important;
    opacity: 0.5 !important;
}

/* ── SUCCESS / INFO / WARNING ALERTS ───────── */
[data-testid="stAlert"] {
    border-radius: 3px !important;
    border-left-width: 4px !important;
}

/* ── SCROLLBAR ─────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb { background: var(--border-gold); border-radius: 3px; }

/* ── SECTION BOX HELPER ─────────────────────── */
.tibia-box {
    background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-inner) 100%);
    border: 1px solid var(--border-gold);
    border-radius: 4px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.7), inset 0 1px 0 rgba(212,168,67,0.1);
    position: relative;
}

.tibia-box::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold-bright), transparent);
    border-radius: 4px 4px 0 0;
}

.tibia-title {
    font-family: 'Cinzel', serif;
    color: var(--gold-bright);
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(107,76,42,0.5);
    text-shadow: 0 0 12px rgba(212,168,67,0.4);
}

.tibia-value {
    font-family: 'Cinzel', serif;
    color: var(--gold-glow);
    font-size: 1.8rem;
    text-shadow: 0 0 20px rgba(212,168,67,0.5);
}

.big-result {
    font-family: 'Cinzel', serif;
    color: var(--success-glow);
    font-size: 2.4rem;
    font-weight: 700;
    text-shadow: 0 0 25px rgba(114,194,86,0.5);
    text-align: center;
    padding: 0.5rem 0;
}

.ornament {
    color: var(--gold-dim);
    font-size: 1.2rem;
    text-align: center;
    letter-spacing: 0.3em;
    padding: 0.3rem 0;
}

.sidebar-hero {
    text-align: center;
    padding: 1.2rem 0.5rem;
    border-bottom: 1px solid var(--border-gold);
    margin-bottom: 1rem;
}

.sidebar-hero h2 {
    font-family: 'Cinzel', serif !important;
    font-size: 1.1rem !important;
    font-weight: 900 !important;
    color: var(--gold-bright) !important;
    text-shadow: 0 0 20px var(--shadow-gold) !important;
    margin: 0.3rem 0 !important;
}

.sidebar-hero p {
    color: var(--parchment-dim) !important;
    font-style: italic !important;
    font-size: 0.8rem !important;
}

.badge {
    display: inline-block;
    background: var(--blood-red);
    border: 1px solid #c0392b;
    border-radius: 3px;
    padding: 0.15rem 0.5rem;
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    color: #ffaaaa;
    text-transform: uppercase;
    vertical-align: middle;
    margin-left: 0.4rem;
}

.profit-pos { color: var(--success-glow) !important; }
.profit-neg { color: #ff6b6b !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATA PERSISTENCE ────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hunt_log.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(records):
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

def records_to_df(records):
    if not records:
        return pd.DataFrame(columns=["data", "char", "mapa", "gold_bruto", "balanco", "horas", "notas"])
    df = pd.DataFrame(records)
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data", ascending=False).reset_index(drop=True)
    return df

if "hunt_records" not in st.session_state:
    st.session_state.hunt_records = load_data()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-hero">
        <div style="font-size:2.5rem">⚔️</div>
        <h2>RubiniCoins</h2>
        <p><em>Farm Manager & Gold Tracker</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tibia-title">⚙️ Configurações de Mercado</div>', unsafe_allow_html=True)

    gold_por_hora = st.number_input(
        "Gold farmado por hora",
        value=1_000_000, step=50_000, format="%d",
        help="Gold bruto coletado por hora de hunt"
    )
    preco_coin_gold = st.number_input(
        "1 RubiniCoin em gold",
        value=55_000, step=500, format="%d",
        help="Quanto gold vale 1 RubiniCoin no market"
    )
    valor_1000_coins = st.number_input(
        "1000 Coins em R$",
        value=85.0, step=1.0, format="%.2f",
        help="Preço pago na loja por 1000 coins"
    )

    st.markdown("---")
    st.markdown('<div class="tibia-title">📊 Resultado da Calc</div>', unsafe_allow_html=True)

    coins_por_hora  = gold_por_hora / preco_coin_gold
    reais_por_coin  = valor_1000_coins / 1000
    reais_por_hora  = coins_por_hora * reais_por_coin
    reais_por_dia_8 = reais_por_hora * 8

    st.markdown(f"""
    <div class="tibia-box" style="padding:1rem">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem">
            <span style="color:var(--parchment-dim);font-size:0.85rem">Coins/hora</span>
            <span style="color:var(--gold-bright);font-weight:600">{coins_por_hora:.1f}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem">
            <span style="color:var(--parchment-dim);font-size:0.85rem">R$/coin</span>
            <span style="color:var(--gold-bright);font-weight:600">R$ {reais_por_coin:.4f}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem">
            <span style="color:var(--parchment-dim);font-size:0.85rem">R$/hora</span>
            <span style="color:var(--gold-bright);font-weight:600">R$ {reais_por_hora:.2f}</span>
        </div>
        <hr style="margin:0.5rem 0;opacity:0.3">
        <div style="display:flex;justify-content:space-between">
            <span style="color:var(--parchment-dim);font-size:0.85rem">R$/dia (8h)</span>
            <span style="color:var(--success-glow);font-weight:700;font-size:1.1rem">R$ {reais_por_dia_8:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem">
    <h1 style="font-size:2.2rem;margin-bottom:0.2rem">⚔️ RubiniCoins Farm Manager ⚔️</h1>
    <p style="color:var(--parchment-dim);font-style:italic;font-size:1rem;margin:0">
        Gerencie seus hunts, acompanhe seu ouro e domine o mercado
    </p>
    <div class="ornament">✦ ─────────────── ✦ ─────────────── ✦</div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "⚔️  Registrar Hunt",
    "📜  Histórico",
    "📊  Análise Mensal",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – REGISTRAR HUNT
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)

    col_form, col_preview = st.columns([1.2, 1], gap="large")

    with col_form:
        st.markdown('<div class="tibia-box">', unsafe_allow_html=True)
        st.markdown('<div class="tibia-title">📋 Novo Registro de Hunt</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            hunt_date = st.date_input("📅 Data", value=date.today())
        with c2:
            char_name = st.text_input("🗡️ Personagem", placeholder="ex: KnightXaolin")

        hunt_map = st.text_input("🗺️ Mapa / Spawn", placeholder="ex: Demon Oak, Roshamuul...")

        c3, c4 = st.columns(2)
        with c3:
            gold_bruto = st.number_input("💰 Gold Bruto", value=0, step=10_000, format="%d",
                                          help="Total de gold coletado na hunt")
        with c4:
            balanco = st.number_input("⚖️ Balanço Líquido", value=0, step=10_000, format="%d",
                                       help="Gold bruto - suprimentos gastados")

        c5, c6 = st.columns(2)
        with c5:
            horas = st.number_input("⏱️ Horas Huntadas", value=2.0, step=0.5, format="%.1f")
        with c6:
            xp_ganho = st.number_input("✨ XP Ganho (M)", value=0.0, step=0.5, format="%.1f",
                                        help="XP em milhões")

        notas = st.text_area("📝 Notas", placeholder="Loot especial, condições da hunt...", height=80)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("⚔️  REGISTRAR HUNT", use_container_width=True):
            if gold_bruto == 0:
                st.warning("⚠️ Insira ao menos o gold bruto para registrar.")
            else:
                record = {
                    "data":       str(hunt_date),
                    "char":       char_name or "—",
                    "mapa":       hunt_map or "—",
                    "gold_bruto": gold_bruto,
                    "balanco":    balanco,
                    "horas":      horas,
                    "xp_ganho":   xp_ganho,
                    "notas":      notas,
                    "timestamp":  datetime.now().isoformat(),
                }
                st.session_state.hunt_records.append(record)
                save_data(st.session_state.hunt_records)
                st.success("✅ Hunt registrado com sucesso!")
                st.balloons()

    with col_preview:
        # ── Live calc for this session ──────────────────────────────────────
        st.markdown('<div class="tibia-box">', unsafe_allow_html=True)
        st.markdown('<div class="tibia-title">🧮 Prévia do Hunt Atual</div>', unsafe_allow_html=True)

        gasto = max(0, gold_bruto - balanco)
        gold_liq_hora = balanco / horas if horas > 0 else 0
        coins_hunt = balanco / preco_coin_gold if preco_coin_gold > 0 else 0
        reais_hunt = coins_hunt * reais_por_coin
        lucro_cor = "profit-pos" if balanco >= 0 else "profit-neg"
        lucro_sinal = "+" if balanco >= 0 else ""

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:0.8rem">
            <div style="background:var(--bg-panel);border:1px solid var(--border-gold);border-radius:3px;padding:0.8rem;text-align:center">
                <div style="color:var(--parchment-dim);font-size:0.72rem;letter-spacing:0.08em;font-family:'Cinzel',serif;text-transform:uppercase">Gold Bruto</div>
                <div style="color:var(--gold-bright);font-family:'Cinzel',serif;font-size:1.1rem;font-weight:600">{gold_bruto:,.0f}</div>
            </div>
            <div style="background:var(--bg-panel);border:1px solid var(--border-gold);border-radius:3px;padding:0.8rem;text-align:center">
                <div style="color:var(--parchment-dim);font-size:0.72rem;letter-spacing:0.08em;font-family:'Cinzel',serif;text-transform:uppercase">Gastos</div>
                <div style="color:#ff9a6c;font-family:'Cinzel',serif;font-size:1.1rem;font-weight:600">{gasto:,.0f}</div>
            </div>
            <div style="background:var(--bg-panel);border:1px solid var(--border-gold);border-radius:3px;padding:0.8rem;text-align:center">
                <div style="color:var(--parchment-dim);font-size:0.72rem;letter-spacing:0.08em;font-family:'Cinzel',serif;text-transform:uppercase">Gold/hora</div>
                <div style="color:var(--gold-bright);font-family:'Cinzel',serif;font-size:1.1rem;font-weight:600">{gold_liq_hora:,.0f}</div>
            </div>
            <div style="background:var(--bg-panel);border:1px solid var(--border-gold);border-radius:3px;padding:0.8rem;text-align:center">
                <div style="color:var(--parchment-dim);font-size:0.72rem;letter-spacing:0.08em;font-family:'Cinzel',serif;text-transform:uppercase">Coins</div>
                <div style="color:var(--gold-bright);font-family:'Cinzel',serif;font-size:1.1rem;font-weight:600">{coins_hunt:.1f}</div>
            </div>
        </div>
        <div style="background:var(--bg-panel);border:1px solid var(--border-gold);border-radius:3px;padding:1rem;text-align:center">
            <div style="color:var(--parchment-dim);font-size:0.72rem;letter-spacing:0.1em;font-family:'Cinzel',serif;text-transform:uppercase;margin-bottom:0.3rem">💰 Lucro do Hunt em R$</div>
            <div class="{lucro_cor}" style="font-family:'Cinzel',serif;font-size:2rem;font-weight:700">
                {lucro_sinal}R$ {reais_hunt:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Taxa efetiva vs estimada ────────────────────────────────────────
        if horas > 0 and gold_bruto > 0:
            taxa_efetiva = (balanco / horas) / gold_por_hora * 100 if gold_por_hora > 0 else 0
            st.markdown(f"""
            <div class="tibia-box" style="padding:1rem">
                <div class="tibia-title">📈 Eficiência</div>
                <div style="display:flex;align-items:center;gap:0.8rem">
                    <div style="flex:1;background:var(--bg-panel);border-radius:3px;height:14px;overflow:hidden">
                        <div style="height:100%;width:{min(taxa_efetiva,100):.0f}%;background:linear-gradient(90deg,#8b1a1a,#d4a843,#72c256);border-radius:3px;transition:width 0.5s"></div>
                    </div>
                    <div style="color:var(--gold-bright);font-family:'Cinzel',serif;font-size:0.9rem;min-width:48px">{taxa_efetiva:.0f}%</div>
                </div>
                <div style="color:var(--parchment-dim);font-size:0.78rem;margin-top:0.4rem;font-style:italic">
                    Eficiência em relação à meta de {gold_por_hora:,.0f} gold/h
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – HISTÓRICO
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
    records = st.session_state.hunt_records

    if not records:
        st.markdown("""
        <div class="tibia-box" style="text-align:center;padding:3rem">
            <div style="font-size:3rem;margin-bottom:1rem">🏜️</div>
            <div style="font-family:'Cinzel',serif;color:var(--parchment-dim);font-size:1.1rem">
                Nenhum hunt registrado ainda
            </div>
            <div style="color:var(--gold-dim);font-style:italic;margin-top:0.5rem;font-size:0.9rem">
                Vá para a aba "Registrar Hunt" para começar!
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = records_to_df(records)

        # KPIs totais
        total_gold   = df["gold_bruto"].sum()
        total_balanco = df["balanco"].sum()
        total_horas  = df["horas"].sum()
        total_hunts  = len(df)
        total_coins  = total_balanco / preco_coin_gold if preco_coin_gold > 0 else 0
        total_reais  = total_coins * reais_por_coin

        st.markdown('<div class="tibia-title">🏆 Totais Acumulados</div>', unsafe_allow_html=True)
        km1, km2, km3, km4, km5 = st.columns(5)
        with km1: st.metric("Total de Hunts",   f"{total_hunts}")
        with km2: st.metric("Horas Huntadas",   f"{total_horas:.1f}h")
        with km3: st.metric("Gold Bruto Total",  f"{total_gold/1e6:.2f}M")
        with km4: st.metric("Balanço Total",     f"{total_balanco/1e6:.2f}M")
        with km5: st.metric("💰 Total em R$",   f"R$ {total_reais:.2f}")

        st.markdown("---")

        # Tabela formatada
        st.markdown('<div class="tibia-title">📋 Registros</div>', unsafe_allow_html=True)
        df_display = df.copy()
        df_display["data"] = df_display["data"].dt.strftime("%d/%m/%Y")
        df_display["gold_bruto"] = df_display["gold_bruto"].apply(lambda x: f"{x:,.0f}")
        df_display["balanco"]    = df_display["balanco"].apply(lambda x: f"{x:,.0f}")
        df_display["horas"]      = df_display["horas"].apply(lambda x: f"{x:.1f}h")

        df_display = df_display.rename(columns={
            "data": "Data", "char": "Personagem", "mapa": "Mapa",
            "gold_bruto": "Gold Bruto", "balanco": "Balanço",
            "horas": "Horas", "notas": "Notas"
        })
        cols_show = ["Data", "Personagem", "Mapa", "Gold Bruto", "Balanço", "Horas", "Notas"]
        st.dataframe(df_display[cols_show], use_container_width=True, hide_index=True)

        # Delete last
        if st.button("🗑️  Remover Último Registro"):
            if st.session_state.hunt_records:
                st.session_state.hunt_records.pop()
                save_data(st.session_state.hunt_records)
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – ANÁLISE MENSAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
    records = st.session_state.hunt_records

    if len(records) < 2:
        st.markdown("""
        <div class="tibia-box" style="text-align:center;padding:3rem">
            <div style="font-size:3rem;margin-bottom:1rem">📊</div>
            <div style="font-family:'Cinzel',serif;color:var(--parchment-dim);font-size:1.1rem">
                Registre pelo menos 2 hunts para ver a análise
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = records_to_df(records)
        df["mes_ano"]  = df["data"].dt.to_period("M")
        df["reais"]    = (df["balanco"] / preco_coin_gold) * reais_por_coin
        df["gold_hora"]= df.apply(lambda r: r["balanco"] / r["horas"] if r["horas"] > 0 else 0, axis=1)

        # Seletor de mês
        meses = sorted(df["mes_ano"].unique(), reverse=True)
        mes_str = [str(m) for m in meses]
        sel_mes = st.selectbox("📅 Selecionar Mês", mes_str)

        df_mes = df[df["mes_ano"] == sel_mes].copy()
        df_mes = df_mes.sort_values("data")

        # Métricas do mês
        n_dias       = df_mes["data"].nunique()
        n_hunts      = len(df_mes)
        gold_total   = df_mes["gold_bruto"].sum()
        balanco_total= df_mes["balanco"].sum()
        horas_total  = df_mes["horas"].sum()
        reais_total  = df_mes["reais"].sum()
        media_dia_gold  = balanco_total / n_dias if n_dias > 0 else 0
        media_dia_reais = reais_total / n_dias if n_dias > 0 else 0
        media_hora_gold = balanco_total / horas_total if horas_total > 0 else 0

        st.markdown(f'<div class="tibia-title">📅 Resumo de {sel_mes}</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Dias com Hunt",     f"{n_dias} dias")
        with c2: st.metric("Total de Hunts",    f"{n_hunts}")
        with c3: st.metric("Horas Totais",      f"{horas_total:.1f}h")
        with c4: st.metric("💰 Renda Total R$", f"R$ {reais_total:.2f}")

        c5, c6, c7 = st.columns(3)
        with c5: st.metric("Média Gold/Dia",    f"{media_dia_gold/1e6:.2f}M")
        with c6: st.metric("Média R$/Dia",      f"R$ {media_dia_reais:.2f}")
        with c7: st.metric("Média Gold/Hora",   f"{media_hora_gold/1e6:.2f}M")

        st.markdown("---")

        # Gráfico: Balanço por dia
        df_daily = df_mes.groupby("data").agg(
            gold_bruto=("gold_bruto", "sum"),
            balanco=("balanco", "sum"),
            horas=("horas", "sum"),
            reais=("reais", "sum"),
        ).reset_index()
        df_daily["reais_pos"] = df_daily["reais"].clip(lower=0)
        df_daily["reais_neg"] = df_daily["reais"].clip(upper=0)

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown('<div class="tibia-title">📈 Balanço em R$ por Dia</div>', unsafe_allow_html=True)
            fig1 = go.Figure()
            colors = ["#72c256" if v >= 0 else "#ff6b6b" for v in df_daily["reais"]]
            fig1.add_trace(go.Bar(
                x=df_daily["data"].dt.strftime("%d/%m"),
                y=df_daily["reais"],
                marker_color=colors,
                marker_line_color="#d4a843",
                marker_line_width=0.5,
                name="R$ por dia",
                hovertemplate="<b>%{x}</b><br>R$ %{y:.2f}<extra></extra>",
            ))
            fig1.add_hline(y=df_daily["reais"].mean(), line_dash="dash",
                           line_color="#d4a843", line_width=1.5,
                           annotation_text=f"Média: R$ {df_daily['reais'].mean():.2f}",
                           annotation_font_color="#d4a843")
            fig1.update_layout(
                plot_bgcolor="#150c00",
                paper_bgcolor="#150c00",
                font=dict(color="#e8d5a3", family="Crimson Text"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870")),
                yaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870"),
                           tickprefix="R$ "),
                showlegend=False,
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col_g2:
            st.markdown('<div class="tibia-title">⏱️ Horas Huntadas por Dia</div>', unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_daily["data"].dt.strftime("%d/%m"),
                y=df_daily["horas"],
                mode="lines+markers",
                line=dict(color="#d4a843", width=2),
                marker=dict(color="#f0c060", size=8, line=dict(color="#d4a843", width=1)),
                fill="tozeroy",
                fillcolor="rgba(212,168,67,0.07)",
                name="Horas",
                hovertemplate="<b>%{x}</b><br>%{y:.1f}h<extra></extra>",
            ))
            fig2.add_hline(y=df_daily["horas"].mean(), line_dash="dash",
                           line_color="#9a7530", line_width=1.5,
                           annotation_text=f"Média: {df_daily['horas'].mean():.1f}h",
                           annotation_font_color="#9a7530")
            fig2.update_layout(
                plot_bgcolor="#150c00",
                paper_bgcolor="#150c00",
                font=dict(color="#e8d5a3", family="Crimson Text"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870")),
                yaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870"),
                           ticksuffix="h"),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Gráfico acumulado
        st.markdown('<div class="tibia-title">📈 Renda Acumulada no Mês (R$)</div>', unsafe_allow_html=True)
        df_daily["reais_acum"] = df_daily["reais"].cumsum()
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df_daily["data"].dt.strftime("%d/%m"),
            y=df_daily["reais_acum"],
            mode="lines+markers",
            line=dict(color="#72c256", width=2.5),
            marker=dict(color="#72c256", size=7, line=dict(color="#4a8a3a", width=1)),
            fill="tozeroy",
            fillcolor="rgba(114,194,86,0.08)",
            hovertemplate="<b>%{x}</b><br>Acumulado: R$ %{y:.2f}<extra></extra>",
        ))
        fig3.update_layout(
            plot_bgcolor="#150c00",
            paper_bgcolor="#150c00",
            font=dict(color="#e8d5a3", family="Crimson Text"),
            margin=dict(l=10, r=10, t=20, b=10),
            height=280,
            xaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870")),
            yaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870"),
                       tickprefix="R$ "),
            showlegend=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Comparativo entre meses (se houver mais de 1 mês)
        if len(meses) > 1:
            st.markdown("---")
            st.markdown('<div class="tibia-title">📊 Comparativo Entre Meses</div>', unsafe_allow_html=True)
            df_comp = df.copy()
            df_comp["mes_str"] = df_comp["mes_ano"].astype(str)
            df_mensal = df_comp.groupby("mes_str").agg(
                reais=("reais", "sum"),
                dias=("data", "nunique"),
                horas=("horas", "sum"),
            ).reset_index()
            df_mensal["reais_por_dia"] = df_mensal["reais"] / df_mensal["dias"]
            df_mensal = df_mensal.sort_values("mes_str")

            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                name="Total R$",
                x=df_mensal["mes_str"],
                y=df_mensal["reais"],
                marker_color="#d4a843",
                marker_line_color="#9a7530",
                marker_line_width=0.8,
                hovertemplate="<b>%{x}</b><br>Total: R$ %{y:.2f}<extra></extra>",
            ))
            fig4.add_trace(go.Scatter(
                name="Média/Dia R$",
                x=df_mensal["mes_str"],
                y=df_mensal["reais_por_dia"],
                mode="lines+markers",
                line=dict(color="#72c256", width=2, dash="dot"),
                marker=dict(color="#72c256", size=8),
                yaxis="y2",
                hovertemplate="<b>%{x}</b><br>Média/dia: R$ %{y:.2f}<extra></extra>",
            ))
            fig4.update_layout(
                plot_bgcolor="#150c00",
                paper_bgcolor="#150c00",
                font=dict(color="#e8d5a3", family="Crimson Text"),
                margin=dict(l=10, r=10, t=20, b=10),
                height=300,
                barmode="group",
                xaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870")),
                yaxis=dict(gridcolor="#2a1800", tickfont=dict(color="#c4a870"),
                           tickprefix="R$ ", title="Total R$"),
                yaxis2=dict(overlaying="y", side="right",
                            tickfont=dict(color="#72c256"),
                            tickprefix="R$ ", title="Média/Dia",
                            gridcolor="transparent"),
                legend=dict(
                    bgcolor="rgba(21,12,0,0.8)",
                    bordercolor="#6b4c2a",
                    borderwidth=1,
                    font=dict(color="#e8d5a3"),
                ),
            )
            st.plotly_chart(fig4, use_container_width=True)
