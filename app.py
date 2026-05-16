import streamlit as st
import datetime as dt
import requests

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Universal Multi-Fund Terminal", page_icon="🛡️", layout="wide")

# Institutional Cyberpunk Dark Interface Configuration
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div.stNumberInput > div > div > input { background-color: #161b22; color: #58a6ff; font-weight: bold; border: 1px solid #30363d; }
    div.stSelectbox > div { background-color: #161b22; }
    div.stSlider > div { background-color: #161b22; }
    .fund-card { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .metric-title { color: #8b949e; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #ffffff; font-size: 1.6rem; font-weight: bold; margin-top: 2px; }
    .status-hold { background-color: #1f293d; border-left: 6px solid #58a6ff; padding: 15px; border-radius: 6px; color: #58a6ff; font-weight: bold; margin-top: 10px; }
    .status-harvest { background-color: #3c1e1e; border-left: 6px solid #f85149; padding: 15px; border-radius: 6px; color: #f85149; font-weight: bold; margin-top: 10px; }
    .status-accumulate { background-color: #1e3c28; border-left: 6px solid #39d353; padding: 15px; border-radius: 6px; color: #39d353; font-weight: bold; margin-top: 10px; }
    .badge-quality { background-color: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: normal; }
    </style>
    """, unsafe_allow_html=True)

# Title Header Matrix
st.title("🛡️ P.A.S.E. Universal Workspace")
st.caption("Psychological Assistant for Stock Exchange • Automated Capital Matrix v9.0")
st.markdown("---")

# --- AMFI LIVE TRACKER CENTRAL INTERNET REGISTRY ---
@st.cache_data(ttl=1800)
def get_live_nav(amfi_code):
    if not amfi_code:
        return None
    try:
        url = f"https://api.mfapi.in/mf/{amfi_code}"
        response = requests.get(url, timeout=5).json()
        return float(response["data"][0]["nav"])
    except:
        return None

# Hardcoded Official Tracking DB (With Custom Override Added)
FUND_DATABASE = {
    "UTI Nifty 50 Index Fund": {"code": "120716", "fallback": 165.50},
    "HDFC Nifty 50 Index Fund": {"code": "119063", "fallback": 210.20},
    "SBI Nifty 50 Index Fund": {"code": "119551", "fallback": 230.10},
    "ICICI Pru Nifty 50 Index Fund": {"code": "120645", "fallback": 225.40},
    "Groww Nifty 50 Index Fund": {"code": "149262", "fallback": 15.30},
    "Parag Parikh Flexi Cap Fund": {"code": "122639", "fallback": 85.40},
    "Quant Small Cap Fund": {"code": "120847", "fallback": 240.60},
    "⚠️ Custom / Other Fund (Manual Input)": {"code": None, "fallback": 0.0}
}

# --- SIDEBAR CONTROL CONTROL PANEL ---
with st.sidebar:
    st.header("⚙️ SYSTEM CONTROL CENTER")
    
    # 1. Budget Planner
    st.subheader("💰 1. Allocation Planner")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=15, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=25000.0, step=1000.0)
    
    st.markdown("---")
    
    # 2. Smart-Text Clipboard Module
    st.subheader("💾 2. Smart-Text Setup Sync")
    st.caption("Paste a backup string to load a profile, or copy the generated code below to save it.")
    restore_string = st.text_input("Paste Smart-Text Code here:")
    
    st.markdown("---")
    st.subheader("🗂️ 3. Select Active Assets")
    tracked_assets = st.multiselect(
        "Choose funds to deploy in your workspace:",
        list(FUND_DATABASE.keys()),
        default=["UTI Nifty 50 Index Fund"]
    )

# --- AUTOMATED SMART-TEXT BACKUP GENERATOR SETUP ---
parsed_backup_data = {}
if restore_string:
    try:
        blocks = restore_string.split("|")
        for b in blocks:
            parts = b.split(":")
            found_match = False
            for full_name in FUND_DATABASE.keys():
                if parts[0].strip().lower() in full_name.lower():
                    parsed_backup_data[full_name] = {
                        "capital": float(parts[1]),
                        "avg_nav": float(parts[2]),
                        "target": float(parts[3]),
                        "custom_name": parts[4] if len(parts) > 4 else "",
                        "custom_nav": float(parts[5]) if len(parts) > 5 else 0.0
                    }
                    found_match = True
            if not found_match: # Fallback to custom holder row
                parsed_backup_data["⚠️ Custom / Other Fund (Manual Input)"] = {
                    "capital": float(parts[1]),
                    "avg_nav": float(parts[2]),
                    "target": float(parts[3]),
                    "custom_name": parts[0],
                    "custom_nav": float(parts[4]) if len(parts) > 4 else 0.0
                }
    except:
        st.sidebar.error("Invalid Smart-Text configuration string format.")

# --- MAIN DASHBOARD CALCULATIONS ENGINE TRACKER ---
global_invested = 0.0
global_current_value = 0.0
backup_string_list = []

if tracked_assets:
    recommended_sip = (income * sip_pct) / 100
    st.info(f"💡 **Target Strategy Vector:** Budget allocations tracking a total pace of **₹{round(recommended_sip, 2)} / month** across your active asset containers.")
    
    for fund in tracked_assets:
        # Load preset configuration parameters from user input or backup string
        default_capital = 0.0
        default_avg = 0.0
        default_tgt = 12.0
        default_custom_name = "My Custom Asset"
        default_custom_nav = 0.0
        
        if fund in parsed_backup_data:
            default_capital = parsed_backup_data[fund]["capital"]
            default_avg = parsed_backup_data[fund]["avg_nav"]
            default_tgt = parsed_backup_data[fund]["target"]
            if "custom_name" in parsed_backup_data[fund]:
                default_custom_name = parsed_backup_data[fund]["custom_name"]
            if "custom_nav" in parsed_backup_data[fund]:
                default_custom_nav = parsed_backup_data[fund]["custom_nav"]
            
        # Isolate if this asset card is a custom entry or live API tracked
        is_custom = FUND_DATABASE[fund]["code"] is None
        
        st.markdown(f"""
        <div class="fund-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
                <span style="font-weight: bold; color: {'#ff9100' if is_custom else '#58a6ff'}; font-size: 1.1rem;">📈 {fund}</span>
                <span class="badge-quality">{'⚙️ Manual Price Override' if is_custom else '🏆 tracking quality: high (AMFI Active)'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Deploy individual user parameter input fields inside layout blocks
        if is_custom:
            col_cust1, col_cust2 = st.columns([1, 2])
            with col_cust1:
                display_name = st.text_input("Asset Label / Stock Code", value=default_custom_name, key=f"name_{fund}")
            with col_cust2:
                manual_live_nav = st.number_input("Current Live Price / Live NAV (₹)", min_value=0.0, value=default_custom_nav, step=1.0, key=f"curr_nav_{fund}")
                
            col_in1, col_in2, col_in3 = st.columns(3)
            with col_in1:
                inv_cap = st.number_input(f"Money Invested (₹)", min_value=0.0, value=default_capital, step=500.0, key=f"cap_{fund}")
            with col_in2:
                buy_nav = st.number_input(f"Your Average Purchase Price (₹)", min_value=0.0, value=default_avg, step=1.0, key=f"nav_{fund}")
            with col_in3:
                tgt_yield = st.slider(f"Target Profit Exit (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"tgt_{fund}")
                
            live_nav_price = manual_live_nav
            backup_string_list.append(f"{display_name}:{inv_cap}:{buy_nav}:{tgt_yield}:{live_nav_price}")
        else:
            display_name = fund
            col_in1, col_in2, col_in3 = st.columns(3)
            with col_in1:
                inv_cap = st.number_input(f"Money Invested (₹)", min_value=0.0, value=default_capital, step=500.0, key=f"cap_{fund}")
            with col_in2:
                buy_nav = st.number_input(f"Your Average Purchase NAV (₹)", min_value=0.0, value=default_avg, step=1.0, key=f"nav_{fund}")
            with col_in3:
                tgt_yield = st.slider(f"Target Profit Exit (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"tgt_{fund}")
                
            amfi_id = FUND_DATABASE[fund]["code"]
            live_nav_price = get_live_nav(amfi_id)
            if live_nav_price is None:
                live_nav_price = FUND_DATABASE[fund]["fallback"]
                
            short_name = fund.split(" ")[0]
            backup_string_list.append(f"{short_name}:{inv_cap}:{buy_nav}:{tgt_yield}")

        # Compute performance layers if values exist
        if inv_cap > 0 and buy_nav > 0 and live_nav_price > 0:
            total_units_owned = inv_cap / buy_nav
            current_market_val = total_units_owned * live_nav_price
            net_profit_loss = current_market_val - inv_cap
            current_yield_pct = (net_profit_loss / inv_cap) * 100
            
            global_invested += inv_cap
            global_current_value += current_market_val
            
            # Sub-Card Data Metrics Render Grid Layout
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                st.markdown(f"<span class='metric-title'>Current Value</span><div class='metric-value' style='color:#00e5ff;'>₹{round(current_market_val,2)}</div><caption style='font-size:0.75rem; color:#8b949e;'>Live Asset Price: ₹{live_nav_price}</caption>", unsafe_allow_html=True)
            with c_m2:
                sign_str = "+" if net_profit_loss >= 0 else ""
                color_str = "#39d353" if net_profit_loss >= 0 else "#f85149"
                st.markdown(f"<span class='metric-title'>Net Returns</span><div class='metric-value' style='color:{color_str};'>{sign_str}₹{round(net_profit_loss,2)}</div>", unsafe_allow_html=True)
            with c_m3:
                color_str = "#39d353" if net_profit_loss >= 0 else "#f85149"
                st.markdown(f"<span class='metric-title'>Absolute Yield</span><div class='metric-value' style='color:{color_str};'>{sign_str}{round(current_yield_pct,2)}%</div>", unsafe_allow_html=True)

            # --- SYSTEM INTELLIGENT LOGIC GATE DEPLOYMENT LOOP ---
            if current_yield_pct <= -5.0:
                avg_down_lumpsum = inv_cap * 0.20
                st.markdown(f"""
                <div class='status-accumulate'>
                    🛒 🚨 AUTOMATED CRASH RESERVE PROTOCOL TRIGGERED<br>
                    <span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>
                        Market Correction Analysis: <b>{display_name}</b> is down <b>{round(current_yield_pct, 2)}%</b> below your entry cost. Deploy a tactical lump-sum allocation of <b>₹{round(avg_down_lumpsum, 2)}</b> right now into this fund to average down your portfolio baseline and maximize recovery velocity.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            elif current_yield_pct >= tgt_yield:
                target_value_boundary = inv_cap * (1 + (tgt_yield / 100))
                surplus = current_market_val - target_value_boundary
                tranche_cash_take = surplus * 0.50
                units_to_liquidate = tranche_cash_take / live_nav_price
                
                st.markdown(f"""
                <div class='status-harvest'>
                    🚨 STRATEGIC TRANCHE HARVEST CEILING BREACHED<br>
                    <span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>
                        Execution Order: Yield ({round(current_yield_pct, 2)}%) has cleared your target window (+{tgt_yield}%). Execute a <b>Tranche 1 Partial Redemption</b> of exactly <b>{round(units_to_liquidate, 3)} units</b> (~₹{round(tranche_cash_take, 2)}) to lock in half your surplus profit into safe bank deposits while letting the rest ride momentum.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class='status-hold'>
                    🔵 CORE ACCUMULATION BUFFER STATUS SECURE<br>
                    <span style='font-size:0.85rem; font-weight:normal; color:#c9d1d9;'>
                        Current tracking yield is standing steady at {round(current_yield_pct, 2)}%. Capital profile rests safely within your specified +{tgt_yield}% target barrier logic fields. No tactical adjustments necessary.
                    </span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br><hr style='border: 1px solid #21262d;'><br>", unsafe_allow_html=True)

    # --- COMPUTE CONSOLIDATED MASTER OVERVIEW PROFILE ---
    if global_invested > 0:
        st.markdown("### 📊 Master Consolidated Ledger")
        g_profit = global_current_value - global_invested
        g_yield = (g_profit / global_invested) * 100
        
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"<div class='card-container'><span class='section-header'>Aggregate Staked Capital</span><h2 style='color:#ffffff; margin-top:5px;'>₹{round(global_invested, 2)}</h2></div>", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"<div class='card-container'><span class='section-header'>Combined Market Valuation</span><h2 style='color:#00e5ff; margin-top:5px;'>₹{round(global_current_value, 2)}</h2></div>", unsafe_allow_html=True)
            
        g_class = "profit-positive" if g_profit >= 0 else "profit-negative"
        g_sign = "+" if g_profit >= 0 else ""
        
        with mc3:
            st.markdown(f"<div class='card-container'><span class='section-header'>Consolidated Net Returns</span><h2 class='{g_class}'>{g_sign}₹{round(g_profit, 2)}</h2></div>", unsafe_allow_html=True)
        with mc4:
            st.markdown(f"<div class='card-container'><span class='section-header'>Aggregate Portfolio Yield</span><h2 class='{g_class}'>{g_sign}{round(g_yield, 2)}%</h2></div>", unsafe_allow_html=True)

        # Strategic Risk Allocation Bar Display
        st.markdown("### 🛡️ Defensive Core Shield Master Balance Bar")
        net_worth_pool = global_current_value + fd_reserves
        mkt_exposure = (global_current_value / net_worth_pool) * 100
        cash_exposure = (fd_reserves / net_worth_pool) * 100
        
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px;'>
                <span style='color: #58a6ff;'>📈 Combined Market Risk Vector ({round(mkt_exposure, 1)}%)</span>
                <span style='color: #39d353;'>🛡️ Core Shield Cash Security Layer ({round(cash_exposure, 1)}%)</span>
            </div>
            <div style='display: flex; height: 24px; border-radius: 4px; overflow: hidden;'>
                <div style='width: {mkt_exposure}%; background-color: #58a6ff;'></div>
                <div style='width: {cash_exposure}%; background-color: #39d353;'></div>
            </div>
            <div style='text-align: center; color: #ffffff; font-weight: bold; font-size: 0.95rem; margin-top: 10px;'>
                TOTAL INTEGRATED NET WORTH POOL: ₹{round(net_worth_pool, 2)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Render Active Smart-Text Backup Output Card
        st.markdown("---")
        st.markdown("### 💾 Master Fast Transfer Backup Node")
        master_string_code = "|".join(backup_string_list)
        st.code(master_string_code, language="text")
        st.caption("Copy this entire line of code and save it in your phone notes. Next time, just paste it into the left sidebar to load your full configuration profile instantly!")

else:
    st.info("### 📊 Workspace Idle Standby Grid\n\nOpen up the left control menu (`»`) and choose your target assets under **Select Active Assets** to spin up your dashboard terminals.")

# --- PERSISTENT CALCULATOR BASE ---
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
st.caption(f"P.A.S.E Universal Terminal Active | Terminal Node Sync: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
