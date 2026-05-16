import streamlit as st
import datetime as dt
import requests
import pandas as pd

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Ultimate Multi-Fund Terminal", page_icon="🛡️", layout="wide")

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
st.title("🛡️ P.A.S.E. Multi-Fund Workspace")
st.caption("Psychological Assistant for Stock Exchange • Advanced Multi-Asset AMFI Engine v7.0")
st.markdown("---")

# --- AMFI LIVE TRACKER CORE ---
@st.cache_data(ttl=3600)
def get_live_nav(amfi_code):
    try:
        url = f"https://api.mfapi.in/mf/{amfi_code}"
        response = requests.get(url, timeout=10).json()
        return float(response["data"][0]["nav"])
    except:
        return None

# Extended Global Mapping Scheme for Index & Active Alpha Funds
FUND_DB = {
    "UTI Nifty 50 Index Fund": {"code": "120716", "fallback": 165.50},
    "HDFC Nifty 50 Index Fund": {"code": "119063", "fallback": 210.20},
    "SBI Nifty 50 Index Fund": {"code": "119551", "fallback": 230.10},
    "ICICI Pru Nifty 50 Index Fund": {"code": "120645", "fallback": 225.40},
    "Groww Nifty 50 Index Fund": {"code": "149262", "fallback": 15.30},
    "Parag Parikh Flexi Cap Fund": {"code": "122639", "fallback": 85.40},
    "Quant Small Cap Fund": {"code": "120847", "fallback": 240.60}
}

# --- INITIALIZE MULTI-ASSET SESSION MEMORY ---
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = [
        {"Fund Name": "UTI Nifty 50 Index Fund", "Invested Capital": 10000.0, "Average Buy NAV": 150.0, "My Target %": 12.0},
        {"Fund Name": "Quant Small Cap Fund", "Invested Capital": 5000.0, "Average Buy NAV": 210.0, "My Target %": 15.0}
    ]

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.header("⚙️ TERMINAL CONFIGURATOR")
    st.caption("Adjust your capital allocations and portfolio entries below.")
    
    # 1. Budget Planner
    st.subheader("💰 1. Allocation Planner")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=15, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=25000.0, step=1000.0)
    
    st.markdown("---")
    
    # 2. Dynamic Editable Portfolio Registry
    st.subheader("🗂️ 2. Active Portfolio Ledger")
    st.caption("Double-click rows to modify fund choices, purchase history, and individual profit goals.")
    
    df_template = pd.DataFrame(st.session_state.portfolio)
    edited_df = st.data_editor(
        df_template,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Fund Name": st.column_config.SelectboxColumn("Fund Name", options=list(FUND_DB.keys()), required=True),
            "Invested Capital": st.column_config.NumberColumn("Invested Capital (₹)", min_value=0.0, step=500.0, required=True),
            "Average Buy NAV": st.column_config.NumberColumn("Average Buy NAV (₹)", min_value=0.0, step=0.1, required=True),
            "My Target %": st.column_config.SliderColumn("My Target %", min_value=5.0, max_value=30.0, step=0.5, default=12.0)
        }
    )
    
    if st.button("🔒 Sync Ledger & Compute"):
        st.session_state.portfolio = edited_df.to_dict(orient="records")
        st.success("Portfolio matrix locked!")

# --- PROCESSING ENGINE CORE ---
total_invested = 0.0
total_current_value = 0.0
harvest_protocols = []
hold_protocols = []

for row in st.session_state.portfolio:
    try:
        name = row["Fund Name"]
        invested = float(row["Invested Capital"])
        avg_nav = float(row["Average Buy NAV"])
        target_yield = float(row["My Target %"])
        
        if invested > 0 and avg_nav > 0 and name in FUND_DB:
            # Fetch live asset valuation dynamically
            amfi_code = FUND_DB[name]["code"]
            live_nav = get_live_nav(amfi_code)
            if live_nav is None:
                live_nav = FUND_DB[name]["fallback"]
                
            # Run core trading formulas
            units = invested / avg_nav
            current_value = units * live_nav
            net_return = current_value - invested
            individual_yield = (net_return / invested) * 100
            
            total_invested += invested
            total_current_value += current_value
            
            # Sort into active execution vectors
            asset_data = {
                "name": name, "yield": individual_yield, "invested": invested, 
                "current": current_value, "units": units, "live_nav": live_nav,
                "target": target_yield
            }
            
            if individual_yield >= target_yield:
                # Calculate required fractional units to trim back to the target ceiling
                target_value = invested * (1 + (target_yield / 100))
                surplus_cash = current_value - target_value
                units_to_sell = surplus_cash / live_nav
                asset_data["units_to_sell"] = units_to_sell
                harvest_protocols.append(asset_data)
            else:
                hold_protocols.append(asset_data)
    except:
        pass

# --- RENDER MAIN INTERFACE TERMINAL ---
if total_invested > 0:
    net_profit = total_current_value - total_invested
    total_yield = (net_profit / total_invested) * 100
    recommended_sip = (income * sip_pct) / 100
    
    st.info(f"💡 **Target Strategy Vector:** Budgeting tracks an investment pace of **₹{round(recommended_sip, 2)} / month** ({sip_pct}% allocation) across your active assets. Maintain systematic reserves.")

    st.markdown("### 📊 Consolidated Portfolio Ledger")
    
    # Master Institutional Metric Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card-container'><span class='section-header'>Total Capital Staked</span><h2 style='color:#ffffff; margin-top:5px;'>₹{round(total_invested,
