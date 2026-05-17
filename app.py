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
st.caption("Psychological Assistant for Stock Exchange • Live Analytics Visualization Engine v13.0")
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
    # PASS 1: Calculate metrics and collect data vectors for graphs
    # -------------------------------------------------------------
    for fund_name in selected_search_assets:
        if fund_name not in GLOBAL_AMFI_DB:
            continue
        scheme_code = GLOBAL_AMFI_DB[fund_name]
        
        default_cap, default_buy, default_tgt, default_vol = 0.0, 0.0, 12.0, 50.0
        for ra in recovered_assets:
            if ra["code"] == scheme_code:
                default_cap, default_buy, default_tgt, default_vol = ra["capital"], ra["buy_nav"], ra["target"], ra["vol"]
        
        # Create unique keys for session states to avoid widget redraw glitches
        inv_cap = st.sidebar.hidden = query_params.get(f"c_{scheme_code}", default_cap)
        buy_nav = st.sidebar.hidden = query_params.get(f"n_{scheme_code}", default_buy)
        
        # Short clean token for graph legends (e.g., "UTI Nifty 50" instead of full 80-char string)
        short_label = fund_name.replace(" (Direct Growth)", "").replace(" Fund", "")
        short_label = (short_label[:22] + '..') if len(short_label) > 24 else short_label

        # Read actual runtime inputs later down the layout thread, but prepare mathematical buffers
        url_state_builder.append(f"{scheme_code}")

    # -------------------------------------------------------------
    # PASS 2: Live UI Card Rendering and Algorithmic Parsing
    # -------------------------------------------------------------
    compiled_cards_data = []
    
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
        </div>
        """, unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            inv_cap = st.number_input("Money Invested (₹)", min_value=0.0, value=default_cap, step=500.0, key=f"c_{scheme_code}")
        with col_f2:
            buy_nav = st.number_input("Your Average Purchase NAV (₹)", min_value=0.0, value=default_buy, step=1.0, key=f"n_{scheme_code}")
        with col_f3:
            tgt_yield = st.slider("Target Exit Ceiling (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"t_{scheme_code}")
        with col_f4:
            tranche_vol = st.slider("Harvest Volume Size (%)", min_value=10, max_value=100, value=int(default_vol), step=5, key=f"v_{scheme_code}")
            
        # Re-verify and rebuild exact active string structures
        url_state_builder[-1] = f"{scheme_code}:{inv_cap}:{buy_nav}:{tgt_yield}:{tranche_vol}"

        if inv_cap > 0 and buy_nav > 0:
            live_nav_tick = get_live_nav_price(scheme_code)
            if live_nav_tick is None:
                live_nav_tick = buy_nav
                
            total_units_held = inv_cap / buy_nav
            current_valuation = total_units_held * live_nav_tick
            net_p_l = current_valuation - inv_cap
            current_yield_rate = (net_p_l / inv_cap) * 100
            
            global_staked_capital += inv_cap
            global_current_market_value += current_valuation
            
            # Map values out to charts registries
            yield_chart_data[short_label] = round(current_yield_rate, 2)
            composition_chart_data[short_label] = round(current_valuation, 2)
            
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(f"<span class='metric-title'>Current Valuation</span><div class='metric-value' style='color:#00e5ff;'>₹{round(current_valuation, 2)}</div><caption style='font-size:0.75rem; color:#8b949e;'>Live NAV Price: ₹{live_nav_tick}</caption>", unsafe_allow_html=True)
            with cm2:
                s_char = "+" if net_p_l >= 0 else ""
                s_color = "#39d353" if net_p_l >= 0 else "#f85149"
                st.markdown(f"<span class='metric-title'>Net Gains</span><div class='metric-value' style='color:{s_color};'>{s_char}₹{round(net_p_l, 2)}</div>", unsafe_allow_html=True)
            with cm3:
                st.markdown(f"<span class='metric-title'>Current Absolute Yield</span><div class='metric-value' style='color:{s_color};'>{s_char}{round(current_yield_rate, 2)}%</div>", unsafe_allow_html=True)

            # Execution alerts loop
            if current_yield_rate <= -15.0:
                heavy_crash_lumpsum = inv_cap * 0.50
                st.markdown(f"<div class='status-accumulate' style='border-left: 6px solid #ff1111; background-color: #4a1515; color: #ff5555;'>🚨 MAXIMUM CRASH ACCUMULATION PROMPT engaged<br><span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>Action: Asset down <b>{round(current_yield_rate, 2)}%</b>. Deploy <b>50% cash buffer</b> (~₹{round(heavy_crash_lumpsum, 2)}) to exploit major institutional cycle recovery vectors.</span></div>", unsafe_allow_html=True)
            elif -15.0 < current_yield_rate <= -10.0:
                major_correction_lumpsum = inv_cap * 0.30
                st.markdown(f"<div class='status-accumulate' style='border-left: 6px solid #ff9100; background-color: #3d2314; color: #ff9100;'>🛒 DEFENSIVE LADDER • TRANCHE B PROMPT engaged<br><span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>Action: Asset down <b>{round(current_yield_rate, 2)}%</b>. Deploy <b>30% cash cushion</b> (~₹{round(major_correction_lumpsum, 2)}) to accumulate heavy premium units at a discount.</span></div>", unsafe_allow_html=True)
            elif -10.0 < current_yield_rate <= -5.0:
                minor_dip_lumpsum = inv_cap * 0.15
                st.markdown(f"<div class='status-accumulate'>🛒 DEFENSIVE LADDER • TRANCHE A PROMPT engaged<br><span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>Action: Asset down <b>{round(current_yield_rate, 2)}%</b>. Deploy a cautious <b>15% entry slice</b> (~₹{round(minor_dip_lumpsum, 2)}) to begin cost-averaging down safely.</span></div>", unsafe_allow_html=True)
            elif current_yield_rate >= tgt_yield:
                target_value_baseline = inv_cap * (1 + (tgt_yield / 100))
                raw_surplus_cash = current_valuation - target_value_baseline
                custom_tranche_cash_trim = raw_surplus_cash * (tranche_vol / 100)
                units_to_liquidate = custom_tranche_cash_trim / live_nav_tick
                st.markdown(f"<div class='status-harvest'>🚨 STRATEGIC EXIT BREED • TRANCHEA EXECUTION ENGAGED<br><span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>Action: Yield has cleared target threshold (+{tgt_yield}%). Redeem exactly <b>{round(units_to_liquidate, 3)} units</b> (~₹{round(custom_tranche_cash_trim, 2)}) on your broker dashboard to secure {tranche_vol}% of surplus profit.</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='status-hold'>🔵 CORE ACCUMULATION STATUS SECURE<br><span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>Current yield at {round(current_yield_rate, 2)}%. Asset runs smoothly below your designated +{tgt_yield}% harvest target gate. Maintain systematic deployment positions.</span></div>", unsafe_allow_html=True)
        st.markdown("<br><hr style='border: 1px solid #21262d;'><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # PASS 3: Display Live Interactive Visual Charts Deck Top Tier
    # -------------------------------------------------------------
    if yield_chart_data or composition_chart_data:
        st.markdown("### 📊 Live Analytics Performance Dashboard")
        col_ch1, col_ch2 = st.columns(2)
        
        with col_ch1:
            st.markdown("<div class='chart-box'><span class='section-header'>📈 Multi-Fund Absolute Yield Radar (%)</span><br><br></div>", unsafe_allow_html=True)
            # Render a native interactive vertical bar chart showing performance velocities side by side
            df_yields = pd.DataFrame(list(yield_chart_data.items()), columns=['Asset Name', 'Yield (%)']).set_index('Asset Name')
            st.bar_chart(df_yields, height=220)
            
        with col_ch2:
            st.markdown("<div class='chart-box'><span class='section-header'>💎 Market Capital Concentration Allocation (₹)</span><br><br></div>", unsafe_allow_html=True)
            # Render a structural bar chart showing exactly where their capital scale blocks are concentrated
            df_comp = pd.DataFrame(list(composition_chart_data.items()), columns=['Asset Name', 'Current Value (₹)']).set_index('Asset Name')
            st.bar_chart(df_comp, height=220)

    # --- COMPUTE COMPREHENSIVE OVERVIEW PROFILE DASHBOARDS ---
    if global_staked_capital > 0:
        st.markdown("### 📊 Consolidated Master Overview")
        master_profit = global_current_market_value - global_staked_capital
        master_yield = (master_profit / global_staked_capital) * 100
        
        g1, g2, g3, g4 = st.columns(4)
        with g1:
            st.markdown(f"<div class='card-container'><span class='section-header'>Aggregate Staked Capital</span><h2 style='color:#ffffff; margin-top:5px;'>₹{round(global_staked_capital, 2)}</h2></div>", unsafe_allow_html=True)
        with g2:
            st.markdown(f"<div class='card-container'><span class='section-header'>Combined Market Valuation</span><h2 style='color:#00e5ff; margin-top:5px;'>₹{round(global_current_market_value, 2)}</h2></div>", unsafe_allow_html=True)
            
        m_class = "profit-positive" if master_profit >= 0 else "profit-negative"
        m_sign = "+" if master_profit >= 0 else ""
        
        with g3:
            st.markdown(f"<div class='card-container'><span class='section-header'>Consolidated Net Returns</span><h2 class='{m_class}'>{m_sign}₹{round(master_profit, 2)}</h2></div>", unsafe_allow_html=True)
        with g4:
            st.markdown(f"<div class='card-container'><span class='section-header'>Aggregate Portfolio Yield</span><h2 class='{m_class}'>{m_sign}{round(master_yield, 2)}%</h2><div class='badge-settlement'>🕒 NAV settles daily after market close</div></div>", unsafe_allow_html=True)

        # Strategic Risk Shield Balance Indicator Bar Chart
        st.markdown("### 🛡️ Defensive Core Shield Master Balance Bar")
        total_integrated_wealth = global_current_market_value + fd_reserves
        mkt_exposure_pct = (global_current_market_value / total_integrated_wealth)
        shield_reserve_pct = (fd_reserves / total_integrated_wealth)
        
        # Deploy native high-performance structural progress containers to avoid canvas loading delays
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 8px;'>
                <span style='color: #58a6ff;'>📈 Combined Market Risk Allocation ({round(mkt_exposure_pct * 100, 1)}%)</span>
                <span style='color: #39d353;'>🛡️ Core Shield Cash Security Layer ({round(shield_reserve_pct * 100, 1)}%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(mkt_exposure_pct)
        st.markdown(f"<div style='text-align: center; color: #ffffff; font-weight: bold; font-size: 0.95rem; margin-top: -5px; margin-bottom:25px;'>TOTAL INTEGRATED WEALTH POOL VALUE: ₹{round(total_integrated_wealth, 2)}</div>", unsafe_allow_html=True)

        # --- BACKGROUND AUTOMATED STATE SYNC ENGINE ---
        raw_state_string = "|".join(url_state_builder)
        st.query_params.update(inc=income, sip=sip_pct, shd=fd_reserves, state=raw_state_string)

else:
    st.info("### 📊 Terminal Workspace Active Idle Matrix\n\nOpen up the left control menu (`»`). Enter keywords into the **Universal Asset Registry Search Engine** and select your fund houses to activate your tracking command dashboard panels.")

# --- PERSISTENT PREDICTIVE FORWARD PLANNER ---
st.markdown("---")
st.markdown("### 🎯 Predictive Compound Horizon Playground")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    target_goal = st.number_input("Target Corpus Goal (₹)", min_value=10000, value=500000, step=50000)
with col_s2:
    horizon_years = st.slider("Time Horizon Grid (Years)", min_value=1, max_value=30, value=5, step=1)
with col_s3:
    expected_retu
