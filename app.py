import streamlit as st
import datetime as dt
import requests
import urllib.parse
import pandas as pd

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Pro Workspace", page_icon="🛡️", layout="wide")

# Premium Cyberpunk Institutional Trading Theme Configuration
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div.stNumberInput > div > div > input { background-color: #161b22; color: #58a6ff; font-weight: bold; border: 1px solid #30363d; }
    div.stSelectbox > div { background-color: #161b22; }
    div.stSlider > div { background-color: #161b22; }
    div.stTextInput > div > div > input { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; }
    .fund-card { background-color: #161b22; border: 1px solid #30363d; padding: 22px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); }
    .metric-title { color: #8b949e; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #ffffff; font-size: 1.8rem; font-weight: bold; margin-top: 2px; }
    .status-hold { background-color: #1f293d; border-left: 6px solid #58a6ff; padding: 18px; border-radius: 6px; color: #58a6ff; font-weight: bold; margin-top: 12px; }
    .status-harvest { background-color: #3c1e1e; border-left: 6px solid #f85149; padding: 18px; border-radius: 6px; color: #f85149; font-weight: bold; margin-top: 12px; }
    .status-accumulate { background-color: #1e3c28; border-left: 6px solid #39d353; padding: 18px; border-radius: 6px; color: #39d353; font-weight: bold; margin-top: 12px; }
    .card-container { background-color: #161b22; border: 1px solid #30363d; padding: 22px; border-radius: 8px; text-align: center; margin-bottom: 15px; }
    .profit-positive { color: #39d353; font-weight: bold; font-size: 2rem; margin: 5px 0; }
    .profit-negative { color: #f85149; font-weight: bold; font-size: 2rem; margin: 5px 0; }
    .section-header { color: #8b949e; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .badge-quality { background-color: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .badge-settlement { background-color: #1b1f24; border: 1px solid #21262d; color: #8b949e; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; display: inline-block; margin-top: 5px; }
    .chart-box { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Main Title Stack Header
st.title("🛡️ P.A.S.E. Pro Workspace")
st.caption("Psychological Assistant for Stock Exchange • Live Analytics Visualization Engine v13.1")
st.markdown("---")

# --- GLOBAL LIVE AMFI AUTOMATION INTERNET ENGINES ---
@st.cache_data(ttl=86400)
def load_global_amfi_directory():
    try:
        url = "https://api.mfapi.in/mf"
        records = requests.get(url, timeout=10).json()
        return {item["schemeName"]: str(item["schemeCode"]) for item in records}
    except:
        return {}

@st.cache_data(ttl=1800)
def get_live_nav_price(amfi_code):
    if not amfi_code:
        return None
    try:
        url = f"https://api.mfapi.in/mf/{amfi_code}"
        res = requests.get(url, timeout=5).json()
        return float(res["data"][0]["nav"])
    except:
        return None

with st.spinner("🤖 Mapping global AMFI mutual fund registries..."):
    GLOBAL_AMFI_DB = load_global_amfi_directory()

# --- RECOVER ROUTED URL STATE PARAMETERS ---
query_params = st.query_params

init_income = int(query_params.get("inc", 50000)) if "inc" in query_params else 50000
init_sip_pct = int(query_params.get("sip", 15)) if "sip" in query_params else 15
init_shield = float(query_params.get("shd", 25000.0)) if "shd" in query_params else 25000.0

recovered_assets = []
if "state" in query_params:
    try:
        decoded_state = urllib.parse.unquote(query_params["state"])
        blocks = decoded_state.split("|")
        for b in blocks:
            p = b.split(":")
            recovered_assets.append({
                "code": p[0], "capital": float(p[1]), "buy_nav": float(p[2]), "target": float(p[3]), "vol": float(p[4])
            })
    except:
        pass

# --- SIDEBAR COMMAND MODULE CONTROL STATION ---
with st.sidebar:
    st.header("⚙️ TERMINAL CORE CONFIGS")
    st.caption("All adjustments dynamically lock straight into your active browser address bar for instant bookmark saving.")
    
    # 1. Capital Distribution Layout
    st.subheader("💰 1. Allocation Planner")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=init_income, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=init_sip_pct, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=init_shield, step=1000.0)
    
    st.markdown("---")
    
    # 2. Universal Search Hub
    st.subheader("🔍 2. Universal Asset Registry Search")
    st.caption("Type any fund keyword to immediately isolate targets out of the live master registry.")
    search_query = st.text_input("Enter Fund House / Asset Keyword:", value="")
    
    filtered_options = []
    if len(search_query) >= 3 and GLOBAL_AMFI_DB:
        filtered_options = [name for name in GLOBAL_AMFI_DB.keys() if search_query.lower() in name.lower()][:25]
    elif not search_query and recovered_assets:
        for ra in recovered_assets:
            for full_n, c_code in GLOBAL_AMFI_DB.items():
                if c_code == ra["code"]:
                    filtered_options.append(full_n)
                    
    selected_search_assets = st.multiselect(
        "Deploy verified selections into workspace:",
        options=filtered_options if filtered_options else ["Search for an asset above..."],
        default=[n for n in filtered_options if any(GLOBAL_AMFI_DB.get(n) == ra["code"] for ra in recovered_assets)] if recovered_assets else []
    )

# --- MASTER COMPILATION POOLS ---
global_staked_capital = 0.0
global_current_market_value = 0.0
url_state_builder = []

# Visualization data holders
yield_chart_data = {}
composition_chart_data = {}

if selected_search_assets and selected_search_assets != ["Search for an asset above..."]:
    recommended_sip = (income * sip_pct) / 100
    st.info(f"💡 **Target Strategy Vector:** System parameters tracking an ongoing investment pacing target of **₹{round(recommended_sip, 2)} / month** across active structures.")
    
    # -------------------------------------------------------------
    # PASS 1: Render Live UI Cards and Process Metrics
    # -------------------------------------------------------------
    for fund_name in selected_search_assets:
        if fund_name not in GLOBAL_AMFI_DB:
            continue
        scheme_code = GLOBAL_AMFI_DB[fund_name]
        short_label = fund_name.replace(" (Direct Growth)", "").replace(" Fund", "")
        short_label = (short_label[:22] + '..') if len(short_label) > 24 else short_label
        
        default_cap, default_buy, default_tgt, default_vol = 0.0, 0.0, 12.0, 50.0
        for ra in recovered_assets:
            if ra["code"] == scheme_code:
                default_cap, default_buy, default_tgt, default_vol = ra["capital"], ra["buy_nav"], ra["target"], ra["vol"]
                
        st.markdown(f"""
        <div class="fund-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
                <span style="font-weight: bold; color: #58a6ff; font-size: 1.1rem;">📈 {fund_name}</span>
                <span class="badge-quality">AMFI ID: {scheme_code} • System Monitored</span>
            </div>
        
