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
    .sip-badge { background-color: #1f242c; border: 1px solid #388bfd; color: #58a6ff; padding: 4px 12px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; display: inline-block; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Main Title Stack Header
st.title("🛡️ P.A.S.E. Pro Workspace")
st.caption("Psychological Assistant for Stock Exchange • Universal Search Suite v14.1")
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
    st.caption("Adjustments sync dynamically into your browser address bar for simple bookmark saving.")
    
    income = st.number_input("Monthly Income (₹)", min_value=0, value=init_income, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=init_sip_pct, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=init_shield, step=1000.0)
    
    st.markdown("---")
    
    st.subheader("🔍 Universal Asset Search")
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

# --- MASTER COMPILATION Pools ---
global_staked_capital = 0.0
global_current_market_value = 0.0
total_harvested_surplus_pool = 0.0
url_state_builder = []

yield_chart_data = {}
composition_chart_data = {}

active_fund_count = len([f for f in selected_search_assets if f in GLOBAL_AMFI_DB])
recommended_sip = (income * sip_pct) / 100
per_fund_sip_budget = recommended_sip / max(active_fund_count, 1)

if selected_search_assets and selected_search_assets != ["Search for an asset above..."]:
    st.info(f"💡 **Target Strategy Vector:** Active setup tracking a baseline investment target pace of **₹{round(recommended_sip, 2)} / month**.")
    
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
                
        st.markdown(f'<div class="fund-card"><div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;"><span style="font-weight: bold; color: #58a6ff; font-size: 1.1rem;">📈 {fund_name}</span><span class="badge-quality">CODE ID: {scheme_code}</span></div></div>', unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            inv_cap = st.number_input("Money Invested (₹)", min_value=0.0, value=default_cap, step=500.0, key=f"cap_id_{scheme_code}")
        with col_f2:
            buy_nav = st.number_input("Your Average Purchase NAV (₹)", min_value=0.0, value=default_buy, step=1.0, key=f"nav_id_{scheme_code}")
        with col_f3:
            tgt_yield = st.slider("Target Exit Ceiling (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"tgt_id_{scheme_code}")
        with col_f4:
            tranche_vol = st.slider("Harvest Volume Size (%)", min_value=10, max_value=100, value=int(default_vol), step=5, key=f"vol_id_{scheme_code}")
            
        url_state_builder.append(f"{scheme_code}:{inv_cap}:{buy_nav}:{tgt_yield}:{tranche_vol}")
        st.markdown(f"<div class='sip-badge'>🎯 Recommended Monthly Entry: ₹{round(per_fund_sip_budget, 2)} / month</div>", unsafe_allow_html=True)

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
            
            yield_chart_data[short_label] = round(current_yield_rate, 2)
            composition_chart_data[short_label] = round(current_valuation, 2)
            
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(f"<span class='metric-title'>Current Valuation</span><div class='metric-value' style='color:#00e5ff;'>₹{round(current_valuation, 2)}</div><caption style='font-size:0.75rem; color:#8b949e;'>Live NAV: ₹{live_nav_tick}</caption>", unsafe_allow_html=True)
            with cm2:
                s_char = "+" if net_p_l >= 0 else ""
                s_color = "#39d353" if net_p_l >= 0 else "#f85149"
                st.markdown(f"<span class='metric-title'>Net Gains</span><div class='metric-value' style='color:{s_color};'>{s_char}₹{round(net_p_l, 2)}</div>", unsafe_allow_html=True)
            with cm3:
                st.markdown(f"<span class='metric-title'>Absolute Yield</span><div class='metric-value' style='color:{s_color};'>{s_char}{round(current_yield_rate, 2)}%</div>", unsafe_allow_html=True)

            # --- SYSTEM SIGNALS LOOP (CLEAN REWRITE NO TRIPLE QUOTES) ---
            if current_yield_rate <= -15.0:
                h_lumpsum = inv_cap * 0.50
                msg = f"🚨 MAXIMUM CRASH ACCUMULATION PROMPT • Asset down {round(current_yield_rate, 2)}%. Deploy 50% cash buffer (~₹{round(h_lumpsum, 2)}) to average down baseline parameters immediately."
                st.markdown(f"<div class='status-accumulate' style='border-left: 6px solid #ff1111; background-color: #4a1515; color: #ff5555; padding:15px; border-radius:6px; font-weight:bold; margin-top:10px;'>{msg}</div>", unsafe_allow_html=True)
                
            elif -15.0 < current_yield_rate <= -10.0:
                m_lumpsum = inv_cap * 0.30
                msg = f"🛒 DEFENSIVE LADDER • TRANCHE B • Asset down {round(current_yield_rate, 2)}%. Deploy 30% cash cushion (~₹{round(m_lumpsum, 2)}) to accumulate premium units at a heavy discount."
                st.markdown(f"<div class='status-accumulate' style='border-left: 6px solid #ff9100; background-color: #3d2314; color: #ff9100; padding:15px; border-radius:6px; font-weight:bold; margin-top:10px;'>{msg}</div>", unsafe_allow_html=True)
                
            elif -10.0 < current_yield_rate <= -5.0:
                mi_lumpsum = inv_cap * 0.15
                msg = f"🛒 DEFENSIVE LADDER • TRANCHE A • Asset down {round(current_yield_rate, 2)}%. Commit a target 15% entry slice (~₹{round(mi_lumpsum, 2)}) to smooth out acquisition averages."
                st.markdown(f"<div class='status-accumulate' style='padding:15px; border-radius:6px; font-weight:bold; margin-top:10px;'>{msg}</div>", unsafe_allow_html=True)
                
            elif current_yield_rate >= tgt_yield:
                t_value_base = inv_cap * (1 + (tgt_yield / 100))
                surplus = current_valuation - t_value_base
                trim_cash = surplus * (tranche_vol / 100)
                u_liquidate = trim_cash / live_nav_tick
                total_harvested_surplus_pool += trim_cash
                msg = f"🚨 STRATEGIC EXIT CEILING BREACHED • Yield has cleared threshold (+{tgt_yield}%). Redeem exactly {round(u_liquidate, 3)} units (~₹{round(trim_cash, 2)}) to lock in {tranche_vol}% of surplus profit."
                st.markdown(f"<div class='status-harvest' style='padding:15px; border-radius:6px; font-weight:bold; margin-top:10px;'>{msg}</div>", unsafe_allow_html=True)
                
            else:
                msg = f"🔵 CORE ACCUMULATION STATUS SECURE • Tracking steady at {round(current_yield_rate, 2)}%. Values oscillate safely below your designated +{tgt_yield}% harvest gate ceiling."
                st.markdown(f"<div class='status-hold' style='padding:15px; border-radius:6px; font-weight:bold; margin-top:10px;'>{msg}</div>", unsafe_allow_html=True)

        st.markdown("<br><hr style='border: 1px solid #21262d;'><br>", unsafe_allow_html=True)

    # --- DISPLAY VISUAL CHARTS DECK ---
    if yield_chart_data and composition_chart_data:
        st.markdown("### 📊 Live Analytics Performance Dashboard")
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            st.markdown("<div class='chart-box'><span class='section-header'>📈 Multi-Fund Absolute Yield Radar (%)</span></div>", unsafe_allow_html=True)
            df_yields = pd.DataFrame(list(yield_chart_data.items()), columns=['Asset Name', 'Yield (%)']).set_index('Asset Name')
            st.bar_chart(df_yields, height=220)
        with col_ch2:
            st.markdown("<div class='chart-box'><span class='section-header'>💎 Market Capital Concentration Allocation (₹)</span></div>", unsafe_allow_html=True)
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
        mkt_exposure_pct = float(global_current_market_value / total_integrated_wealth) if total_integrated_wealth > 0 else 0.0
        mkt_exposure_pct = max(0.0, min(1.0, mkt_exposure_pct))
        
        st.markdown(f"<div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; margin-bottom: 8px;'><div style='display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 8px;'><span style='color: #58a6ff;'>📈 Combined Market Risk Allocation ({round(mkt_exposure_pct * 100, 1)}%)</span><span style='color: #39d353;'>🛡️ Core Shield Cash Security Layer ({round((1 - mkt_exposure_pct) * 100, 1)}%) <i style='color:#8b949e; font-size:0.75rem;'>(Includes ₹{round(total_harvested_surplus_pool,2)} locked returns)</i></span></div></div>", unsafe_allow_html=True)
        st.progress(mkt_exposure_pct)
        st.markdown(f"<div style='text-align: center; color: #ffffff; font-weight: bold; font-size: 0.95rem; margin-top: -5px; margin-bottom:25px;'>TOTAL INTEGRATED WEALTH POOL VALUE: ₹{round(total_integrated_wealth, 2)}</div>", unsafe_allow_html=True)

        # --- BACKGROUND AUTOMATED STATE SYNC ENGINE ---
        raw_state_string = "|".join(url_state_builder)
        st.query_params.update(inc=income, sip=sip_pct, shd=fd_reserves, state=raw_state_string)

else:
    st.info("### 📊 Terminal Workspace Active Idle Matrix\n\nOpen up the left control menu (`»`). Enter keywords into the Search Engine to deploy workspace containers.")

# --- PERSISTENT PREDICTIVE FORWARD PLANNER ---
st.markdown("---")
st.markdown("### 🎯 Predictive Compound Horizon Playground")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    target_goal = st.number_input("Target Corpus Goal (₹)", min_value=10000, value=500000, step=50000)
with col_s2:
    horizon_years = st.slider("Time Horizon Grid (Years)", min_value=1, max_value=30, value=5, step=1)
with col_s3:
    expected_return = st.slider("Expected Compounding Rate (CAGR %)", min_value=8, max_value=25, value=12, step=1)

r = (expected_return / 12) / 100
n = horizon_years * 12
required_monthly_sip = target_goal / (((1 + r)**n - 1) / r * (1 + r))

st.markdown(f"<div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; text-align: center;'><span style='font-size: 0.85rem; color: #8b949e;'>REQUIRED SIP INSTALLMENT RADAR TO HIT TARGET</span><br><h2 style='color: #39d353; margin-top: 5px;'>₹{round(required_monthly_sip, 2)} / month</h2><span style='font-size: 0.75rem; color: #8b949e;'>Compounding over {horizon_years} years at an annualized growth rate baseline of {expected_return}%.</span></div>", unsafe_allow_html=True)
st.markdown("---")
st.caption(f"P.A.S.E Pro Terminal Network Active | System Node Sync: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
