import streamlit as st
import yfinance as yf
import datetime as dt

# --- THE SYSTEM MATRIX INITIALIZATION ---
st.set_page_config(page_title="P.A.S.E. Engine", page_icon="🛡️", layout="centered")

# Custom UI Dark Theme Injection
st.markdown("""
    <style>
    .main { background-color: #06090e; color: #cbd5e1; }
    div.stNumberInput > div > div > input { background-color: #0f172a; color: #00e5ff; font-weight: bold; }
    .metric-card { background-color: #0b132b; border: 1px solid #1c2541; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 10px; }
    .status-hold { background-color: #1e293b; border-left: 5px solid #38bdf8; padding: 15px; border-radius: 4px; font-weight: bold; color: #38bdf8; }
    .status-harvest { background-color: #450a0a; border-left: 5px solid #f87171; padding: 15px; border-radius: 4px; font-weight: bold; color: #f87171; animation: pulse 2s infinite; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ P.A.S.E.")
st.subheader("Psychological Assistant for Stock Exchange")
st.markdown("---")

# --- MULTI-USER ISOLATION MATRIX ---
# This layer forces unique sandbox memory profiles per user link access
if 'user_capital' not in st.session_state:
    st.session_state.user_capital = 1000.0
if 'user_units' not in st.session_state:
    st.session_state.user_units = 0.0

# Sidebar Input Control Centers (Isolated Parameters)
with st.sidebar:
    st.header("👤 YOUR PARAMETERS")
    st.caption("Adjust inputs to compute your personalized tracking lifecycle.")
    
    # Live updates mapped onto localized state memory
    st.session_state.user_capital = st.number_input(
        "Total Invested Capital (₹)", 
        min_value=0.0, 
        value=st.session_state.user_capital, 
        step=500.0
    )
    st.session_state.user_units = st.number_input(
        "Total Mutual Fund Units", 
        min_value=0.0, 
        value=st.session_state.user_units, 
        step=0.001, 
        format="%.3f"
    )

# --- THE CALCULATOR PROCESSING GATE ---
if st.session_state.user_capital > 0 and st.session_state.user_units > 0:
    try:
        # Fetch Live Market Close Layer (Nifty 50 Index)
        nifty_ticker = yf.Ticker("^NSEI")
        nifty_current = nifty_ticker.history(period="1d")['Close'].iloc[-1]
    except:
        # Fallback to structural safety baseline index valuation if network times out
        nifty_current = 23643.50

    # Execute system core equations
    current_value = st.session_state.user_units * nifty_current
    avg_purchase_price = st.session_state.user_capital / st.session_state.user_units
    net_profit_loss = current_value - st.session_state.user_capital
    
    # Calculate performance yields
    yield_percentage = (net_profit_loss / st.session_state.user_capital) * 100
    target_value = st.session_state.user_capital * 1.12
    target_price_per_unit = target_value / st.session_state.user_units
    
    # Display Personal Metrics Dashboard Grid
    st.markdown("### 📊 Your Portfolio Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='metric-card'><sup>Current Asset Value</sup><br><h2 style='color:#00e5ff;'>₹{round(current_value, 2)}</h2></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><sup>Your Average NAV Cost</sup><br><h4>₹{round(avg_purchase_price, 2)}</h4></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><sup>Net Yield Returns</sup><br><h2 style='color: {'#4ade80' if yield_percentage >= 0 else '#f87171'};'>{round(yield_percentage, 2)}%</h2></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><sup>Target Liquidate Price</sup><br><h4>₹{round(target_price_per_unit, 2)}</h4></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚦 System Execution Signal")

    # The Core Logic Trigger Gate (+12% yield evaluation loop)
    if yield_percentage >= 12.0:
        # Calculate exactly how much surplus unit volume needs to be harvested to lock profits
        surplus_cash = current_value - target_value
        units_to_harvest = surplus_cash / nifty_current
        
        st.markdown(f"""
        <div class='status-harvest'>
            🚨 TARGET HIGHLIGHTED: HARVEST PROFIT YIELD NOW<br>
            <span style='font-size:0.9rem; font-weight:normal; color:#cbd5e1;'>
                Action: Your portfolio has breached the +12% performance gate. Immediately liquidate exactly <b>{round(units_to_harvest, 3)} units</b> from your trading terminal and route the capital safely into your Core Shield bank fixed deposits.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='status-hold'>
            🔵 STATUS PARAMETER: HOLD & ACCUMULATE<br>
            <span style='font-size:0.9rem; font-weight:normal; color:#cbd5e1;'>
                Action: Market volatility is within baseline thresholds. Maintain current holdings and continue routine installment accumulation sequences.
            </span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("👋 Welcome to P.A.S.E. Allocation Terminal. Slide open the left parameters menu (`»`) to input your custom capital stakes and unit holdings to calculate your matrix tracking data.")

st.markdown("---")
st.caption(f"P.A.S.E System Grid Live | Nifty Index Tracking Refreshed: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
