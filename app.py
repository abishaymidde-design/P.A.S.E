import streamlit as st
import datetime as dt
import requests

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Custom Strategy Terminal", page_icon="🛡️", layout="wide")

# Institutional Trading Interface Style Configuration
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div.stNumberInput > div > div > input { background-color: #161b22; color: #58a6ff; font-weight: bold; border: 1px solid #30363d; }
    div.stSelectbox > div { background-color: #161b22; }
    div.stSlider > div { background-color: #161b22; }
    .card-container { background-color: #161b22; border: 1px solid #30363d; padding: 22px; border-radius: 8px; text-align: center; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
    .profit-positive { color: #39d353; font-weight: bold; font-size: 2rem; margin: 5px 0; }
    .profit-negative { color: #f85149; font-weight: bold; font-size: 2rem; margin: 5px 0; }
    .status-hold { background-color: #1f293d; border-left: 6px solid #58a6ff; padding: 20px; border-radius: 6px; color: #58a6ff; font-weight: bold; }
    .status-harvest { background-color: #3c1e1e; border-left: 6px solid #f85149; padding: 20px; border-radius: 6px; color: #f85149; font-weight: bold; }
    .section-header { color: #8b949e; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# Title Header Matrix
st.title("🛡️ P.A.S.E. Strategy Terminal")
st.caption("Psychological Assistant for Stock Exchange • Custom Yield Harvesting v6.0")
st.markdown("---")

# --- AMFI LIVE TRACKER FUNCTION ---
@st.cache_data(ttl=3600)  # Caches the data for 1 hour to stay safe and blazing fast
def get_live_nav(amfi_code):
    try:
        url = f"https://api.mfapi.in/mf/{amfi_code}"
        response = requests.get(url, timeout=10).json()
        live_nav = float(response["data"][0]["nav"])
        return live_nav
    except:
        return None

# Mapping scheme for the top Nifty 50 Direct Growth funds via official AMFI Codes
FUND_DICTIONARY = {
    "UTI Nifty 50 Index Fund (Direct Growth)": {"code": "120716", "fallback": 165.50},
    "HDFC Nifty 50 Index Fund (Direct Growth)": {"code": "119063", "fallback": 210.20},
    "SBI Nifty 50 Index Fund (Direct Growth)": {"code": "119551", "fallback": 230.10},
    "ICICI Prudential Nifty 50 Index Fund (Direct Growth)": {"code": "120645", "fallback": 225.40},
    "Groww Nifty 50 Index Fund (Direct Growth)": {"code": "149262", "fallback": 15.30}
}

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.header("⚙️ SYSTEM CONFIGURATOR")
    st.caption("Adjust control vectors to evaluate real-time deployment profiles.")
    
    # 1. Financial Planner Module
    st.subheader("💰 1. Capital Allocation Planner")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=15, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=25000.0, step=1000.0)
    
    st.markdown("---")
    
    # 2. Automated Selection Hub
    st.subheader("🗂️ 2. Select & Configure Fund")
    selected_fund = st.selectbox("Choose your Nifty 50 Fund House:", list(FUND_DICTIONARY.keys()))
    
    # Automatically fetch live price based on selection
    target_code = FUND_DICTIONARY[selected_fund]["code"]
    fetched_nav = get_live_nav(target_code)
    
    if fetched_nav is None:
        fetched_nav = FUND_DICTIONARY[selected_fund]["fallback"]
        st.sidebar.warning("Using cached baseline price layer.")
    else:
        st.sidebar.success(f"Live NAV Connected: ₹{fetched_nav}")
    
    invested_capital = st.number_input("Total Money Invested (₹)", min_value=0.0, value=0.0, step=500.0)
    average_nav = st.number_input("Your Average Purchase NAV (₹)", min_value=0.0, value=0.0, step=1.0)
    current_nav = fetched_nav
    
    st.markdown("---")
    
    # 3. Custom Target Strategy Module
    st.subheader("🎯 3. Profit Harvest Target")
    user_target_yield = st.slider("Trigger Harvest Signal At (%)", min_value=5.0, max_value=30.0, value=12.0, step=0.5)
    st.caption(f"System logic locked to fire alert at exactly **+{user_target_yield}%** returns.")

# --- COMPUTE MATRIX EQUATIONS ---
if invested_capital > 0 and current_nav > 0 and average_nav > 0:
    
    # Calculate exact mutual fund metrics dynamically based on inputs
    total_units = invested_capital / average_nav
    total_current_value = total_units * current_nav
    net_profit = total_current_value - invested_capital
    total_yield = (net_profit / invested_capital) * 100
    
    # Harvest target parameter logic ceiling (Dynamic based on user input)
    target_multiplier = 1 + (user_target_yield / 100)
    target_portfolio_value = invested_capital * target_multiplier
    recommended_sip = (income * sip_pct) / 100
    
    # 1. Operational Insights Card
    st.info(f"💡 **Target Strategy Vector:** Budgeting tracks an investment pace of **₹{round(recommended_sip, 2)} / month** into **{selected_fund}**. Engine will trigger capital liquidation sequences once absolute yield hits **+{user_target_yield}%**.")

    st.markdown("### 📊 Consolidated Investment Ledger")
    
    # Master Institutional Metric Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card-container'><span class='section-header'>Total Capital Staked</span><h2 style='color:#ffffff; margin-top:5px;'>₹{round(invested_capital, 2)}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card-container'><span class='section-header'>Current Market Value</span><h2 style='color:#00e5ff; margin-top:5px;'>₹{round(total_current_value, 2)}</h2></div>", unsafe_allow_html=True)
    
    p_class = "profit-positive" if net_profit >= 0 else "profit-negative"
    sign = "+" if net_profit >= 0 else ""
    
    with c3:
        st.markdown(f"<div class='card-container'><span class='section-header'>Net Returns Ledger</span><h2 class='{p_class}'>{sign}₹{round(net_profit, 2)}</h2></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card-container'><span class='section-header'>Absolute Portfolio Yield</span><h2 class='{p_class}'>{sign}{round(total_yield, 2)}%</h2></div>", unsafe_allow_html=True)

    st.caption(f"🤖 **Automated Pipeline Data Matrix:** Current asset price for **{selected_fund}** is pulled live at **₹{current_nav}** per unit.")

    # 2. Strategic Risk Allocation Distribution Layout
    st.markdown("### 🛡️ Defensive Core Shield Distribution Balance")
    total_wealth = total_current_value + fd_reserves
    market_exposure_pct = (total_current_value / total_wealth) * 100
    shield_pct = (fd_reserves / total_wealth) * 100
    
    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px;'>
                <span style='color: #58a6ff;'>📈 {selected_fund} Exposure ({round(market_exposure_pct, 1)}%)</span>
                <span style='color: #39d353;'>🛡️ Core Shield Cash ({round(shield_pct, 1)}%)</span>
            </div>
            <div style='display: flex; height: 24px; border-radius: 4px; overflow: hidden;'>
                <div style='width: {market_exposure_pct}%; background-color: #58a6ff;'></div>
                <div style='width: {shield_pct}%; background-color: #39d353;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_chart2:
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 10px; border-radius: 6px; border: 1px solid #30363d; text-align: center; height: 56px;'>
            <span style='font-size: 0.75rem; color: #8b949e;'>TOTAL COMBINED WEALTH</span><br>
            <h4 style='color: #ffffff; margin: 0;'>₹{round(total_wealth, 2)}</h4>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚦 Execution Matrix Signals")

    # 3. Execution Signal Assessment Matrix Loop (Evaluated against User-Selected Target)
    if total_yield >= user_target_yield:
        surplus_cash = total_current_value - target_portfolio_value
        units_to_harvest = surplus_cash / current_nav
        st.markdown(f"""
        <div class='status-harvest'>
            🚨 LIQUIDATION PROTOCOL ENGAGED • {selected_fund.upper()}<br>
            <span style='font-size:0.9rem; font-weight:normal; color:#c9d1d9;'>
                Action: Asset has breached your personalized performance ceiling of <b>{user_target_yield}%</b> (Current: {round(total_yield, 2)}%). Redeem exactly <b>{round(units_to_harvest, 3)} units</b> via your trading terminal and route the capital safely into your Core Shield bank fixed deposits.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='status-hold'>
            🔵 SYSTEM STATUS: ACCUMULATING HOLD PROFILE<br>
            <span style='font-size:0.9rem; font-weight:normal; color:#c9d1d9;'>
                {selected_fund} performance is tracking at {round(total_yield, 2)}%. Capital is steady below your targeted {user_target_yield}% harvest gateway threshold. Maintain current asset accumulation sequences.
            </span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("### 📊 System Standby Matrix\n\nSlide open the left control configurations panel (`»`). Choose your Nifty 50 Fund House from the menu dropdown list, calibrate your custom target harvest percentage, and input your ledger parameters to arm your main dashboard pipeline.")

# 4. Long-Term Compound Velocity Forecaster Panel
st.markdown("---")
st.markdown("### 🎯 Predictive Compound Horizon Playground")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    target_goal = st.number_input("Target Corpus Goal (₹)", min_value=10000, value=500000, step=50000)
with col_s2:
    horizon_years = st.slider("Time Horizon Grid (Years)", min_value=1, max_value=30, value=5, step=1)
with col_s3:
    expected_return = st.slider("Expected Compounding Rate (CAGR %)", min_value=8, max_value=25, value=12, step=1)

# Back-compute required systematic investment amounts using financial compound matrix math
r = (expected_return / 12) / 100
n = horizon_years * 12
required_monthly_sip = target_goal / (((1 + r)**n - 1) / r * (1 + r))

st.markdown(f"""
<div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; text-align: center;'>
    <span style='font-size: 0.85rem; color: #8b949e;'>REQUIRED SIP INSTALLMENT RADAR TO HIT TARGET</span><br>
    <h2 style='color: #39d353; margin-top: 5px;'>₹{round(required_monthly_sip, 2)} / month</h2>
    <span style='font-size: 0.75rem; color: #8b949e;'>Compounding over {horizon_years} years at an evaluation metric of {expected_return}% annualized growth velocity.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"P.A.S.E Custom Terminal Node Active | Global Grid Sync: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
