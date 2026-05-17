import streamlit as st
import datetime as dt
import requests
import urllib.parse
import pandas as pd
import yfinance as yf

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Ultimate Command Center", page_icon="🛡️", layout="wide")

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
    .profit-positive { color: #39d353; font-weight: bold; font-size: 1.8rem; margin: 5px 0; }
    .profit-negative { color: #f85149; font-weight: bold; font-size: 1.8rem; margin: 5px 0; }
    .section-header { color: #8b949e; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .badge-quality { background-color: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .badge-settlement { background-color: #1b1f24; border: 1px solid #21262d; color: #8b949e; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; display: inline-block; margin-top: 5px; }
    .chart-box { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    .sip-badge { background-color: #1f242c; border: 1px solid #388bfd; color: #58a6ff; padding: 4px 12px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; display: inline-block; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Main Title Stack Header
st.title("🛡️ P.A.S.E. Ultimate Terminal")
st.caption("Psychological Assistant for Stock Exchange • Cross-Asset Multi-Engine v15.0")
st.markdown("---")

# --- PATH A: AUTOMATED INDIAN CURRENCY FORMATTER MATRIX ---
def fmt_inr(val):
    """Formats raw floats into clean Indian style numbering layout with proper comma sets"""
    try:
        sign = "-" if val < 0 else ""
        val = abs(val)
        s = f"{val:.2f}"
        parts = s.split(".")
        num = parts[0]
        dec = parts[1]
        if len(num) > 3:
            last_three = num[-3:]
            remaining = num[:-3]
            out = ""
            while len(remaining) > 2:
                out = "," + remaining[-2:] + out
                remaining = remaining[:-2]
            if remaining:
                out = remaining + out
            return f"₹{sign}{out},{last_three}.{dec}"
        else:
            return f"₹{sign}{num}.{dec}"
    except:
        return f"₹{val}"

# --- GLOBAL LIVE AMFI AUTOMATION INTERNET ENGINES ---
@st.cache_data(ttl=86400)
def load_global_amfi_directory():
    try:
        url = "https://api.mfapi.in/mf"
        records = requests.get(url, timeout=5).json()
        return {item["schemeName"]: str(item["schemeCode"]) for item in records}
    except:
        return {}

def get_live_asset_price(code_or_ticker, is_stock=False):
    """PATH A & B Fail-Safe Live Price Engine for Mutual Funds & Real-Time Stocks"""
    if is_stock:
        try:
            ticker = yf.Ticker(code_or_ticker)
            todays_data = ticker.history(period='1d')
            if not todays_data.empty:
                return float(todays_data['Close'].iloc[-1])
        except:
            pass
        return None
    else:
        try:
            url = f"https://api.mfapi.in/mf/{code_or_ticker}"
            res = requests.get(url, timeout=3).json()
            return float(res["data"][0]["nav"])
        except:
            return None

with st.spinner("🤖 Booting Cross-Asset Databases..."):
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
            # Schema: TYPE(MF/STK):CODE_OR_TICKER:CAP:BUY:TGT:VOL
            recovered_assets.append({
                "type": p[0], "code": p[1], "capital": float(p[2]), "buy_nav": float(p[3]), "target": float(p[4]), "vol": float(p[5])
            })
    except:
        pass

# --- SIDEBAR COMMAND MODULE CONTROL STATION ---
with st.sidebar:
    st.header("⚙️ TERMINAL COMMAND DECK")
    st.caption("Adjustments seamlessly rewrite into your active browser address bar for simple bookmark saving.")
    
    income = st.number_input("Monthly Income (₹)", min_value=0, value=init_income, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=init_sip_pct, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=init_shield, step=1000.0)
    
    st.markdown("---")
    
    # PATH B: Dual Selector Thread for Stocks & Funds
    asset_class_choice = st.radio("Choose Asset Class to Add:", ["Indian Mutual Funds", "NSE / BSE Live Stocks & ETFs"])
    
    selected_search_assets = []
    stock_tickers_list = []
    
    # Load previously saved states back into active multiselects to avoid wipeouts
    saved_mf_names = []
    saved_stock_tickers = [ra["code"] for ra in recovered_assets if ra["type"] == "STK"]
    
    if recovered_assets and GLOBAL_AMFI_DB:
        for ra in recovered_assets:
            if ra["type"] == "MF":
                for name, code in GLOBAL_AMFI_DB.items():
                    if code == ra["code"]:
                        saved_mf_names.append(name)

    if asset_class_choice == "Indian Mutual Funds":
        search_query = st.text_input("Search Mutual Fund Houses:", value="")
        filtered_options = []
        if len(search_query) >= 3 and GLOBAL_AMFI_DB:
            filtered_options = [name for name in GLOBAL_AMFI_DB.keys() if search_query.lower() in name.lower()][:20]
        
        # Merge currently queried funds with previously saved fund options
        all_mf_options = list(set(filtered_options + saved_mf_names))
        selected_search_assets = st.multiselect("Deploy Funds into workspace:", options=all_mf_options, default=saved_mf_names)
        stock_tickers_list = saved_stock_tickers
    else:
        st.caption("💡 Enter tickers matching Yahoo Finance codes (e.g., RELIANCE.NS, INFY.NS, NIFTYBEES.NS)")
        stock_input = st.text_input("Enter Ticker Code + Press Enter:", value="")
        if stock_input and stock_input.upper() not in saved_stock_tickers:
            saved_stock_tickers.append(stock_input.upper())
        stock_tickers_list = st.multiselect("Active Stocks Terminal Matrix:", options=saved_stock_tickers, default=saved_stock_tickers)
        selected_search_assets = saved_mf_names

# --- CONSOLIDATION UTILITIES POOL ---
global_staked_capital = 0.0
global_current_market_value = 0.0
total_harvested_surplus_pool = 0.0
url_state_builder = []

yield_chart_data = {}
composition_chart_data = {}

total_active_assets_count = len([f for f in selected_search_assets if f in GLOBAL_AMFI_DB]) + len(stock_tickers_list)
recommended_sip = (income * sip_pct) / 100
per_asset_sip_budget = recommended_sip / max(total_active_assets_count, 1)

# -------------------------------------------------------------
# CORE PROCESSING PIPELINE: MUTUAL FUNDS GRID
# -------------------------------------------------------------
if total_active_assets_count > 0:
    st.info(f"💡 **Target Strategy Vector:** Active setup tracking a total investment target pace of **{fmt_inr(recommended_sip)} / month**.")
    
    # Process Mutual Funds Block
    for fund_name in selected_search_assets:
        if fund_name not in GLOBAL_AMFI_DB:
            continue
        scheme_code = GLOBAL_AMFI_DB[fund_name]
        short_label = fund_name.replace(" (Direct Growth)", "").replace(" Fund", "")
        short_label = (short_label[:20] + '..') if len(short_label) > 22 else short_label
        
        default_cap, default_buy, default_tgt, default_vol = 0.0, 0.0, 12.0, 50.0
        for ra in recovered_assets:
            if ra["type"] == "MF" and ra["code"] == scheme_code:
                default_cap, default_buy, default_tgt, default_vol = ra["capital"], ra["buy_nav"], ra["target"], ra["vol"]
                
        st.markdown(f'<div class="fund-card"><div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;"><span style="font-weight: bold; color: #58a6ff; font-size: 1.1rem;">📈 [MUTUAL FUND] {fund_name}</span><span class="badge-quality">AMFI ID: {scheme_code}</span></div></div>', unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            inv_cap = st.number_input("Money Invested (₹)", min_value=0.0, value=default_cap, step=500.0, key=f"cap_mf_{scheme_code}")
        with col_f2:
            buy_nav = st.number_input("Your Average Purchase NAV (₹)", min_value=0.0, value=default_buy, step=1.0, key=f"nav_mf_{scheme_code}")
        with col_f3:
            tgt_yield = st.slider("Target Exit Ceiling (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"tgt_mf_{scheme_code}")
        with col_f4:
            tranche_vol = st.slider("Harvest Volume Size (%)", min_value=10, max_value=100, value=int(default_vol), step=5, key=f"vol_mf_{scheme_code}")
            
        url_state_builder.append(f"MF:{scheme_code}:{inv_cap}:{buy_nav}:{tgt_yield}:{tranche_vol}")
        st.markdown(f"<div class='sip-badge'>🎯 Recommended Monthly Entry: {fmt_inr(per_asset_sip_budget)} / month</div>", unsafe_allow_html=True)

        if inv_cap > 0 and buy_nav > 0:
            live_nav_tick = get_live_asset_price(scheme_code, is_stock=False)
            if live_nav_tick is None:
                live_nav_tick = buy_nav
                st.caption("⚠️ AMFI Latency Registry Secure. Processing Fallback matrix indexes.")
                
            total_units_held = inv_cap / buy_nav
            current_valuation = total_units_held * live_nav_tick
            net_p_l = current_valuation - inv_cap
            current_yield_rate = (net_p_l / inv_cap) * 100
            
            global_staked_capital += inv_cap
            global_current_market_value += current_valuation
            yield_chart_data[short_label] = round(current_yield_rate, 2)
            composition_chart_data[short_label] = round(current_valuation, 2)
            
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(f"<span class='metric-title'>Current Valuation</span><div class='metric-value' style='color:#00e5ff;'>{fmt_inr(current_valuation)}</div><caption style='font-size:0.75rem; color:#8b949e;'>Live NAV: ₹{live_nav_tick}</caption>", unsafe_allow_html=True)
            with cm2:
                s_color = "#39d353" if net_p_l >= 0 else "#f85149"
                st.markdown(f"<span class='metric-title'>Net Gains</span><div class='metric-value' style='color:{s_color};'>{'+' if net_p_l >= 0 else ''}{fmt_inr(net_p_l)}</div>", unsafe_allow_html=True)
            with cm3:
                st.markdown(f"<span class='metric-title'>Absolute Yield</span><div class='metric-value' style='color:{s_color};'>{'+' if net_p_l >= 0 else ''}{round(current_yield_rate, 2)}%</div>", unsafe_allow_html=True)

            # Execution Logic Alerts Layer
            if current_yield_rate <= -15.0:
                h_lumpsum = inv_cap * 0.50
                st.markdown(f"<div class='status-accumulate' style='border-left: 6px solid #ff1111; background-color: #
                
