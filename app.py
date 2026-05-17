import streamlit as st
import datetime as dt
import requests
import urllib.parse

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
    .badge-quality { background-color: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .card-container { background-color: #161b22; border: 1px solid #30363d; padding: 22px; border-radius: 8px; text-align: center; margin-bottom: 15px; }
    .profit-positive { color: #39d353; font-weight: bold; font-size: 2rem; margin: 5px 0; }
    .profit-negative { color: #f85149; font-weight: bold; font-size: 2rem; margin: 5px 0; }
    .section-header { color: #8b949e; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# Main Title Stack Header
st.title("🛡️ P.A.S.E. Pro Workspace")
st.caption("Psychological Assistant for Stock Exchange • Universal Search & Link Persistence Suite v10.0")
st.markdown("---")

# --- GLOBAL LIVE AMFI AUTOMATION INTERNET ENGINES ---
@st.cache_data(ttl=3600)
def load_global_amfi_directory():
    """Fetches the absolute latest complete master database records from AMFI registry"""
    try:
        url = "https://api.mfapi.in/mf"
        records = requests.get(url, timeout=10).json()
        return {item["schemeName"]: str(item["schemeCode"]) for item in records}
    except:
        return {}

@st.cache_data(ttl=1800)
def get_live_nav_price(amfi_code):
    """Pulls precise instantaneous asset pricing vectors for any selected code"""
    if not amfi_code:
        return None
    try:
        url = f"https://api.mfapi.in/mf/{amfi_code}"
        res = requests.get(url, timeout=5).json()
        return float(res["data"][0]["nav"])
    except:
        return None

# Compile Master Database Directory On Main App Boot Thread
with st.spinner("🤖 Mapping global AMFI mutual fund registries..."):
    GLOBAL_AMFI_DB = load_global_amfi_directory()

# --- RECOVER ROUTED URL STATE STATE PARAMETERS ---
# Reads parameters directly from the browser address bar for instant bookmark restoration
query_params = st.query_params

init_income = int(query_params.get("inc", [50000])[0]) if "inc" in query_params else 50000
init_sip_pct = int(query_params.get("sip", [15])[0]) if "sip" in query_params else 15
init_shield = float(query_params.get("shd", [25000.0])[0]) if "shd" in query_params else 25000.0

# Decode URL state payload string back into active memory matrices
recovered_assets = []
if "state" in query_params:
    try:
        decoded_state = urllib.parse.unquote(query_params["state"])
        # Format schema: CODE:CAP:BUY:TGT:VOL|CODE2:CAP2...
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
    st.caption("Calibrate systematic layers. Click sync to lock structures directly to your bookmark URL link.")
    
    # 1. Capital Distribution Layout
    st.subheader("💰 1. Allocation Planner")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=init_income, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=init_sip_pct, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=init_shield, step=1000.0)
    
    st.markdown("---")
    
    # 2. Intelligent AMFI Query Multi-Search Cloud Engine
    st.subheader("🔍 2. Universal Asset Registry Search")
    st.caption("Type any fund keyword to search across thousands of active Indian options simultaneously.")
    search_query = st.text_input("Enter Fund House / Asset Keyword:", value="")
    
    filtered_options = []
    if len(search_query) >= 3 and GLOBAL_AMFI_DB:
        filtered_options = [name for name in GLOBAL_AMFI_DB.keys() if search_query.lower() in name.lower()][:25]
    elif not search_query and recovered_assets:
        # Keep currently loaded recovered assets matching inside visibility windows
        for ra in recovered_assets:
            for full_n, c_code in GLOBAL_AMFI_DB.items():
                if c_code == ra["code"]:
                    filtered_options.append(full_n)
                    
    selected_search_assets = st.multiselect(
        "Deploy verified selections into workspace:",
        options=filtered_options if filtered_options else ["Search for an asset above..."],
        default=[n for n in filtered_options if any(GLOBAL_AMFI_DB.get(n) == ra["code"] for ra in recovered_assets)] if recovered_assets else []
    )

# --- EXECUTE CALCULATION MATRIX LOOPS ---
global_staked_capital = 0.0
global_current_market_value = 0.0
url_state_builder = []

if selected_search_assets and selected_search_assets != ["Search for an asset above..."]:
    recommended_sip = (income * sip_pct) / 100
    st.info(f"💡 **Target Strategy Vector:** System parameters tracking an ongoing investment pacing target of **₹{round(recommended_sip, 2)} / month** across active structures.")
    
    for fund_name in selected_search_assets:
        if fund_name not in GLOBAL_AMFI_DB:
            continue
            
        scheme_code = GLOBAL_AMFI_DB[fund_name]
        
        # Pull parameter defaults out of recovered query arrays if matching keys intersect
        default_cap, default_buy, default_tgt, default_vol = 0.0, 0.0, 12.0, 50.0
        for ra in recovered_assets:
            if ra["code"] == scheme_code:
                default_cap, default_buy, default_tgt, default_vol = ra["capital"], ra["buy_nav"], ra["target"], ra["vol"]
                
        # Render Premium Dynamic Asset Cards Layout Frame
        st.markdown(f"""
        <div class="fund-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
                <span style="font-weight: bold; color: #58a6ff; font-size: 1.1rem;">📈 {fund_name}</span>
                <span class="badge-quality">AMFI ID: {scheme_code} • Live Stream Secure</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Build clean inline input parameter fields layout rows
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            inv_cap = st.number_input("Money Invested (₹)", min_value=0.0, value=default_cap, step=500.0, key=f"c_{scheme_code}")
        with col_f2:
            buy_nav = st.number_input("Your Average Purchase NAV (₹)", min_value=0.0, value=default_buy, step=1.0, key=f"n_{scheme_code}")
        with col_f3:
            tgt_yield = st.slider("Target Exit Ceiling (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"t_{scheme_code}")
        with col_f4:
            tranche_vol = st.slider("Harvest Volume Size (%)", min_value=10, max_value=100, value=int(default_vol), step=5, key=f"v_{scheme_code}")
            
        # Append elements cleanly into raw URL state storage arrays
        url_state_builder.append(f"{scheme_code}:{inv_cap}:{buy_nav}:{tgt_yield}:{tranche_vol}")

        # Compute internal execution vector mathematics if inputs compile cleanly
        if inv_cap > 0 and buy_nav > 0:
            live_nav_tick = get_live_nav_price(scheme_code)
            if live_nav_tick is None:
                live_nav_tick = buy_nav # Safe fallback parameter default mapping
                
            total_units_held = inv_cap / buy_nav
            current_valuation = total_units_held * live_nav_tick
            net_p_l = current_valuation - inv_cap
            current_yield_rate = (net_p_l / inv_cap) * 100
            
            global_staked_capital += inv_cap
            global_current_market_value += current_valuation
            
            # Print asset structural cards metric sub-grids
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(f"<span class='metric-title'>Current Valuation</span><div class='metric-value' style='color:#00e5ff;'>₹{round(current_valuation, 2)}</div><caption style='font-size:0.75rem; color:#8b949e;'>Live NAV Asset Price: ₹{live_nav_tick}</caption>", unsafe_allow_html=True)
            with cm2:
                s_char = "+" if net_p_l >= 0 else ""
                s_color = "#39d353" if net_p_l >= 0 else "#f85149"
                st.markdown(f"<span class='metric-title'>Net Gains</span><div class='metric-value' style='color:{s_color};'>{s_char}₹{round(net_p_l, 2)}</div>", unsafe_allow_html=True)
            with cm3:
                st.markdown(f"<span class='metric-title'>Current Absolute Yield</span><div class='metric-value' style='color:{s_color};'>{s_char}{round(current_yield_rate, 2)}%</div>", unsafe_allow_html=True)

            # --- SYSTEM RULES-BASED ALGORITHMIC SIGNAL CHECK LOOPS ---
            if current_yield_rate <= -5.0:
                suggested_lumpsum_buy = inv_cap * 0.20
                st.markdown(f"""
                <div class='status-accumulate'>
                    🛒 AUTOMATED ACCUMULATION RADAR ACTIVE • RE-BALANCE BUY OPEN<br>
                    <span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>
                        Strategy Vector: <b>{fund_name}</b> is down <b>{round(current_yield_rate, 2)}%</b> below your acquisition price. Deploy a tactical lump-sum allocation order of <b>₹{round(suggested_lumpsum_buy, 2)}</b> right now into your trading app to average down your entry cost basis and maximize future upside.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            elif current_yield_rate >= tgt_yield:
                target_value_baseline = inv_cap * (1 + (tgt_yield / 100))
                raw_surplus_cash = current_valuation - target_value_baseline
                custom_tranche_cash_trim = raw_surplus_cash * (tranche_vol / 100)
                units_to_liquidate = custom_tranche_cash_trim / live_nav_tick
                
                st.markdown(f"""
                <div class='status-harvest'>
                    🚨 STRATEGIC CEILING BREACH • TRANCHE EXECUTION MANDATED<br>
                    <span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>
                        Execution Order: Yield performance ({round(current_yield_rate, 2)}%) has successfully breached your custom profit gateway (+{tgt_yield}%). Execute a targeted <b>Tranche Partial Redemption of {tranche_vol}% of surplus gains</b> by selling exactly <b>{round(units_to_liquidate, 3)} units</b> (~₹{round(custom_tranche_cash_trim, 2)}) via Groww/Zerodha, routing the proceeds straight into your secure Core Shield cash reserves.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class='status-hold'>
                    🔵 STANDARD BUFFER ACCUMULATION MODE HOLD SECURE<br>
                    <span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>
                        Current tracking metrics show a stable hold profile at {round(current_yield_rate, 2)}%. Asset values oscillate safely beneath your designated +{tgt_yield}% harvest strategy window logic loops. Maintain active routine systematic monthly deposits.
                    </span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br><hr style='border: 1px solid #21262d;'><br>", unsafe_allow_html=True)

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
            st.markdown(f"<div class='card-container'><span class='section-header'>Aggregate Portfolio Yield</span><h2 class='{m_class}'>{m_sign}{round(master_yield, 2)}%</h2></div>", unsafe_allow_html=True)

        # Strategic Risk Shield Balance Indicator Bar Chart
        st.markdown("### 🛡️ Defensive Core Shield Master Balance Bar")
        total_integrated_wealth = global_current_market_value + fd_reserves
        mkt_exposure_pct = (global_current_value / total_integrated_wealth) * 100 if 'global_current_value' in locals() else (global_current_market_value / total_integrated_wealth) * 100
        shield_reserve_pct = (fd_reserves / total_integrated_wealth) * 100
        
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px;'>
                <span style='color: #58a6ff;'>📈 Combined Market Risk Allocation ({round(mkt_exposure_pct, 1)}%)</span>
                <span style='color: #39d353;'>🛡️ Core Shield Cash Cushion reserves ({round(shield_reserve_pct, 1)}%)</span>
            </div>
            <div style='display: flex; height: 24px; border-radius: 4px; overflow: hidden;'>
                <div style='width: {mkt_exposure_pct}%; background-color: #58a6ff;'></div>
                <div style='width: {shield_reserve_pct}%; background-color: #39d353;'></div>
            </div>
            <div style='text-align: center; color: #ffffff; font-weight: bold; font-size: 0.95rem; margin-top: 10px;'>
                TOTAL INTEGRATED WEALTH POOL VALUE: ₹{round(total_integrated_wealth, 2)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- SYSTEM LINK RE-WRITING COMPILATION HUB ---
        st.markdown("---")
        st.markdown("### 🔗 Lock Strategy State to URL Bookmark")
        st.caption("Clicking this button compiles all your portfolio elements and embeds them directly inside your browser address link. Simply bookmark the updated link on your phone to instantly load your dashboard in one tap next time!")
        
        raw_state_string = "|".join(url_state_builder)
        encoded_state_url = urllib.parse.quote(raw_state_string)
        
        # Build the programmatic query link parameter structure
        sync_link = f"?inc={income}&sip={sip_pct}&shd={fd_reserves}&state={encoded_state_url}"
        
        if st.button("🔒 Synchronize State Link"):
            # Update active browser parameters via native streamlit commands
            st.query_params.update(inc=income, sip=sip_pct, shd=fd_reserves, state=raw_state_string)
            st.success("Configuration successfully locked! Copy the updated URL link from your browser header or bookmark it now.")
            st.code(sync_link, language="text")

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
    expected_return = st.slider("Expected Compounding Rate (CAGR %)", min_value=8, max_value=25, value=12, step=1)

r = (expected_return / 12) / 100
n = horizon_years * 12
required_monthly_sip = target_goal / (((1 + r)**n - 1) / r * (1 + r))

st.markdown(f"""
<div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; text-align: center;'>
    <span style='font-size: 0.85rem; color: #8b949e;'>REQUIRED SIP INSTALLMENT RADAR TO HIT TARGET</span><br>
    <h2 style='color: #39d353; margin-top: 5px;'>₹{round(required_monthly_sip, 2)} / month</h2>
    <span style='font-size: 0.75rem; color: #8b949e;'>Compounding over {horizon_years} years at an annualized growth velocity baseline of {expected_return}%.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"P.A.S.E Pro Terminal Network Active | Grid Node System Sync: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
