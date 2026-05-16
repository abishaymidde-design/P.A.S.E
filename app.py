import streamlit as st
import datetime as dt
import pandas as pd

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Ultimate Terminal", page_icon="🛡️", layout="wide")

# Institutional Trading Interface Style Configuration
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div.stNumberInput > div > div > input { background-color: #161b22; color: #58a6ff; font-weight: bold; border: 1px solid #30363d; }
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
st.title("🛡️ P.A.S.E. Ultimate Terminal")
st.caption("Psychological Assistant for Stock Exchange • Enterprise Sandbox Portfolio Suite v3.0")
st.markdown("---")

# --- MULTI-USER ISOLATION ENGINE ---
if 'assets' not in st.session_state:
    st.session_state.assets = [
        {"Asset Name": "Nifty 50 Index Fund", "Invested Capital": 10000.0, "Avg Purchase NAV": 42.50, "Current NAV": 45.10},
        {"Asset Name": "Active Small Cap Fund", "Invested Capital": 5000.0, "Avg Purchase NAV": 112.00, "Current NAV": 131.50}
    ]

# --- SIDEBAR CONTROL CONTROL CORE ---
with st.sidebar:
    st.header("⚙️ SYSTEM CONFIGURATOR")
    st.caption("Adjust control vectors to evaluate real-time deployment profiles.")
    
    # 1. Financial Planner Module
    st.subheader("💰 1. Capital Allocation Planner")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=15, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=25000.0, step=1000.0)
    
    st.markdown("---")
    
    # 2. Portfolio Configuration Registry
    st.subheader("🗂️ 2. Live Asset Ledger")
    st.caption("Modify or append elements into your individual isolated session container.")
    
    # Simple data frame editor to mirror live broker tables
    df_editor = st.data_editable = pd.DataFrame(st.session_state.assets)
    updated_df = st.data_editor(df_editor, num_rows="dynamic", hide_index=True)
    
    # Save the input state changes
    if st.button("🔒 Save Parameters & Run"):
        st.session_state.assets = updated_df.to_dict(orient="records")
        st.success("Allocation parameters locked.")

# --- COMPUTE MATRIX EQUATIONS ---
assets_list = st.session_state.assets
total_invested = 0.0
total_current_value = 0.0
harvest_triggers = []

for asset in assets_list:
    try:
        inv = float(asset.get("Invested Capital", 0))
        avg_nav = float(asset.get("Avg Purchase NAV", 0))
        cur_nav = float(asset.get("Current NAV", 0))
        name = asset.get("Asset Name", "Unknown Asset")
        
        if inv > 0 and avg_nav > 0 and cur_nav > 0:
            units = inv / avg_nav
            c_val = units * cur_nav
            yield_p = ((c_val - inv) / inv) * 100
            
            total_invested += inv
            total_current_value += c_val
            
            # Identify individual asset trigger gates (+12%)
            if yield_p >= 12.0:
                t_val = inv * 1.12
                surplus = c_val - t_val
                units_to_sell = surplus / cur_nav
                harvest_triggers.append({"name": name, "units": round(units_to_sell, 3), "yield": round(yield_p, 2)})
    except:
        pass

# --- RENDER TRADING STATION UI ---
if total_invested > 0:
    net_profit = total_current_value - total_invested
    total_yield = (net_profit / total_invested) * 100
    recommended_sip = (income * sip_pct) / 100
    
    # 1. Operational Insights Card
    st.info(f"💡 **Target Strategy Vector:** Based on your earnings configuration, target a recurring installment pace of **₹{round(recommended_sip, 2)} / month** ({sip_pct}% allocation). Maintain systematic deployment.")

    st.markdown("### 📊 Consolidated Investment Ledger")
    
    # Master Institutional Metric Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card-container'><span class='section-header'>Total Capital Staked</span><h2 style='color:#ffffff; margin-top:5px;'>₹{round(total_invested, 2)}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card-container'><span class='section-header'>Current Market Value</span><h2 style='color:#00e5ff; margin-top:5px;'>₹{round(total_current_value, 2)}</h2></div>", unsafe_allow_html=True)
    
    p_class = "profit-positive" if net_profit >= 0 else "profit-negative"
    sign = "+" if net_profit >= 0 else ""
    
    with c3:
        st.markdown(f"<div class='card-container'><span class='section-header'>Net Returns Ledger</span><h2 class='{p_class}'>{sign}₹{round(net_profit, 2)}</h2></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card-container'><span class='section-header'>Absolute Performance Portfolio Yield</span><h2 class='{p_class}'>{sign}{round(total_yield, 2)}%</h2></div>", unsafe_allow_html=True)

    # 2. Strategic Risk Allocation Distribution Layout
    st.markdown("### 🛡️ Defensive Core Shield Distribution Balance")
    total_wealth = total_current_value + fd_reserves
    market_exposure_pct = (total_current_value / total_wealth) * 100
    shield_pct = (fd_reserves / total_wealth) * 100
    
    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        # Render a sleek text-based horizontal distribution visualization bar
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px;'>
                <span style='color: #58a6ff;'>📈 Market Risk Allocation ({round(market_exposure_pct, 1)}%)</span>
                <span style='color: #39d353;'>🛡️ Core Shield Reserves ({round(shield_pct, 1)}%)</span>
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
            <span style='font-size: 0.75rem; color: #8b949e;'>NET NET ASSETS</span><br>
            <h4 style='color: #ffffff; margin: 0;'>₹{round(total_wealth, 2)}</h4>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚦 Execution Matrix Signals")

    # 3. Execution Signal Assessment Matrix Loop
    if len(harvest_triggers) > 0:
        for alert in harvest_triggers:
            st.markdown(f"""
            <div class='status-harvest' style='margin-bottom: 10px;'>
                🚨 LIQUIDATION PROTOCOL ENGAGED • {alert['name'].upper()}<br>
                <span style='font-size:0.9rem; font-weight:normal; color:#c9d1d9;'>
                    Action: Asset has reached a performance yield of <b>{alert['yield']}%</b>. Redeem exactly <b>{alert['units']} units</b> via your trading terminal (Groww/Zerodha) and move the realized profit safely into your Core Shield reserves.
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='status-hold'>
            🔵 SYSTEM STATUS: ACCUMULATING HOLD PROFILE<br>
            <span style='font-size:0.9rem; font-weight:normal; color:#c9d1d9;'>
                All active portfolios are currently clearing performance boundaries safely within parameters. Maintain target accumulation protocols.
            </span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("### 📊 System Standby Matrix\n\nSlide open the left control configurations panel (`»`). Add your assets directly into the tracking grid to arm your dashboard pipeline.")

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

# 5. Fast Transfer Protocol Storage Data Bank
st.markdown("---")
st.markdown("### 💾 Fast Transfer Backup Registry")
st.caption("Since this terminal acts as an isolated private sandbox container, copy this data text record to save or load your layouts inside your private notes application.")
backup_string = str(st.session_state.assets)
st.text_area("Your Copyable Matrix String Data Pool", value=backup_string, help="Copy everything inside this element to back up your asset positions.")

st.markdown("---")
st.caption(f"P.A.S.E Pro Terminal Network Node Live | Global Grid Sync: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
st.markdown("---")
st.caption(f"P.A.S.E System Grid Live | Nifty Index Tracking Refreshed: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
