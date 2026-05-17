import streamlit as st
import datetime as dt
import requests
import urllib.parse
import pandas as pd
import yfinance as yf

# --- SYSTEM INITIALIZATION & THEME CORES ---
st.set_page_config(page_title="P.A.S.E. Ultimate Command Center", page_icon="🛡️", layout="wide")

# Main Title Stack Header
st.title("🛡️ P.A.S.E. Ultimate Terminal")
st.caption("Psychological Assistant for Stock Exchange • Cross-Asset Multi-Engine v15.3")
st.markdown("---")

# --- PATH A: AUTOMATED INDIAN CURRENCY FORMATTER MATRIX ---
def fmt_inr(val):
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
    if is_stock:
        try:
            ticker = yf.Ticker(code_or_ticker)
            todays_data = ticker.history(period="1d")
            if not todays_data.empty:
                return float(todays_data["Close"].iloc[-1])
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
            recovered_assets.append({
                "type": p[0], "code": p[1], "capital": float(p[2]), "buy_nav": float(p[3]), "target": float(p[4]), "vol": float(p[5])
            })
    except:
        pass

# --- SIDEBAR COMMAND MODULE CONTROL STATION ---
with st.sidebar:
    st.header("⚙️ TERMINAL COMMAND DECK")
    st.caption("Adjustments sync dynamically into your browser address bar.")
    
    income = st.number_input("Monthly Income (₹)", min_value=0, value=init_income, step=5000)
    sip_pct = st.slider("Target Allocation Pace (%)", min_value=5, max_value=50, value=init_sip_pct, step=5)
    fd_reserves = st.number_input("Core Shield Cash (FD/Savings) (₹)", min_value=0.0, value=init_shield, step=1000.0)
    
    st.markdown("---")
    asset_class_choice = st.radio("Choose Asset Class to Add:", ["Indian Mutual Funds", "NSE / BSE Live Stocks & ETFs"])
    
    selected_search_assets = []
    stock_tickers_list = []
    
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
        
        all_mf_options = list(set(filtered_options + saved_mf_names))
        selected_search_assets = st.multiselect("Deploy Funds into workspace:", options=all_mf_options, default=saved_mf_names)
        stock_tickers_list = saved_stock_tickers
    else:
        st.caption("💡 Enter Yahoo Finance tickers (e.g., RELIANCE.NS, INFY.NS)")
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
                
        st.markdown("---")
        st.subheader(f"📈 [MUTUAL FUND] {fund_name}")
        st.caption(f"AMFI ID: {scheme_code} | Target Recommended SIP: {fmt_inr(per_asset_sip_budget)}/mo")
        
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

        if inv_cap > 0 and buy_nav > 0:
            live_nav_tick = get_live_asset_price(scheme_code, is_stock=False)
            if live_nav_tick is None:
                live_nav_tick = buy_nav
                st.caption("⚠️ AMFI Database Latency Secure. Processing fallback metrics.")
                
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
                st.metric("Current Valuation", fmt_inr(current_valuation), f"Live NAV: ₹{live_nav_tick}", delta_color="off")
            with cm2:
                st.metric("Net Gains", fmt_inr(net_p_l))
            with cm3:
                st.metric("Absolute Yield", f"{round(current_yield_rate, 2)}%")

            # System Execution Alerts
            if current_yield_rate <= -15.0:
                h_lumpsum = inv_cap * 0.50
                st.error(f"🚨 MAXIMUM CRASH ACCUMULATION PROMPT • Asset down {round(current_yield_rate, 2)}%. Deploy 50% cash buffer (~{fmt_inr(h_lumpsum)}) immediately.")
            elif -15.0 < current_yield_rate <= -10.0:
                m_lumpsum = inv_cap * 0.30
                st.warning(f"🛒 DEFENSIVE LADDER • TRANCHE B • Asset down {round(current_yield_rate, 2)}%. Deploy 30% cash cushion (~{fmt_inr(m_lumpsum)}).")
            elif -10.0 < current_yield_rate <= -5.0:
                mi_lumpsum = inv_cap * 0.15
                st.info(f"🛒 DEFENSIVE LADDER • TRANCHE A • Asset down {round(current_yield_rate, 2)}%. Commit 15% entry slice (~{fmt_inr(mi_lumpsum)}) to cost-average down.")
            elif current_yield_rate >= tgt_yield:
                t_value_base = inv_cap * (1 + (tgt_yield / 100))
                trim_cash = (current_valuation - t_value_base) * (tranche_vol / 100)
                u_liquidate = trim_cash / live_nav_tick
                total_harvested_surplus_pool += trim_cash
                st.success(f"🚨 STRATEGIC EXIT CEILING BREACHED • Redeem exactly {round(u_liquidate, 3)} units (~{fmt_inr(trim_cash)}) to lock in {tranche_vol}% of surplus profit.")
            else:
                st.info(f"🔵 CORE ACCUMULATION STATUS SECURE • Tracking steady at {round(current_yield_rate, 2)}%. No tactical adjustments necessary.")

    # -------------------------------------------------------------
    # PATH B PROCESSING PIPELINE: LIVE NSE/BSE STOCKS & ETFS GRID
    # -------------------------------------------------------------
    for ticker_sym in stock_tickers_list:
        clean_ticker = ticker_sym.strip().upper()
        short_label = clean_ticker.split(".")[0]
        
        default_cap, default_buy, default_tgt, default_vol = 0.0, 0.0, 12.0, 50.0
        for ra in recovered_assets:
            if ra["type"] == "STK" and ra["code"] == clean_ticker:
                default_cap, default_buy, default_tgt, default_vol = ra["capital"], ra["buy_nav"], ra["target"], ra["vol"]
                
        st.markdown("---")
        st.subheader(f"⚡ [STOCK] {clean_ticker}")
        st.caption(f"Real-Time Exchange Stream | Target Recommended SIP: {fmt_inr(per_asset_sip_budget)}/mo")
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            inv_cap = st.number_input("Money Invested (₹)", min_value=0.0, value=default_cap, step=500.0, key=f"cap_stk_{clean_ticker}")
        with col_s2:
            buy_nav = st.number_input("Your Average Purchase Price (₹)", min_value=0.0, value=default_buy, step=1.0, key=f"nav_stk_{clean_ticker}")
        with col_s3:
            tgt_yield = st.slider("Target Exit Ceiling (%)", min_value=5.0, max_value=30.0, value=default_tgt, step=0.5, key=f"tgt_stk_{clean_ticker}")
        with col_s4:
            tranche_vol = st.slider("Harvest Volume Size (%)", min_value=10, max_value=100, value=int(default_vol), step=5, key=f"vol_stk_{clean_ticker}")
            
        url_state_builder.append(f"STK:{clean_ticker}:{inv_cap}:{buy_nav}:{tgt_yield}:{tranche_vol}")

        if inv_cap > 0 and buy_nav > 0:
            live_stock_tick = get_live_asset_price(clean_ticker, is_stock=True)
            if live_stock_tick is None:
                live_stock_tick = buy_nav
                st.caption("⚠️ Checking local asset exchange pipelines.")
                
            total_shares_held = inv_cap / buy_nav
            current_valuation = total_shares_held * live_stock_tick
            net_p_l = current_valuation - inv_cap
            current_yield_rate = (net_p_l / inv_cap) * 100
            
            global_staked_capital += inv_cap
            global_current_market_value += current_valuation
            yield_chart_data[short_label] = round(current_yield_rate, 2)
            composition_chart_data[short_label] = round(current_valuation, 2)
            
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.metric("Current Valuation", fmt_inr(current_valuation), f"Live Market Price: ₹{live_stock_tick}", delta_color="off")
            with cm2:
                st.metric("Net Gains", fmt_inr(net_p_l))
            with cm3:
                st.metric("Absolute Yield", f"{round(current_yield_rate, 2)}%")

            # Stock Tactical Alerts Loop
            if current_yield_rate <= -15.0:
                h_lumpsum = inv_cap * 0.50
                st.error(f"🚨 STOCK EXCHANGE CRASH DISCOUNT ALERT • {clean_ticker} down {round(current_yield_rate, 2)}%. Deploy 50% strategic cash buffer (~{fmt_inr(h_lumpsum)}).")
            elif -15.0 < current_yield_rate <= -10.0:
                m_lumpsum = inv_cap * 0.30
                st.warning(f"🛒 ACCUMULATION MODE LADDER B • Deploy 30% liquid cash reserves (~{fmt_inr(m_lumpsum)}) to compound long-term equity units.")
            elif -10.0 < current_yield_rate <= -5.0:
                mi_lumpsum = inv_cap * 0.15
                st.info(f"🛒 POSITION STAGING LADDER A • Commit a 15% entry slice (~{fmt_inr(mi_lumpsum)}) to capture discounted value waves.")
            elif current_yield_rate >= tgt_yield:
                t_value_base = inv_cap * (1 + (tgt_yield / 100))
                trim_cash = (current_valuation - t_value_base) * (tranche_vol / 100)
                shares_to_liquidate = trim_cash / live_stock_tick
                total_harvested_surplus_pool += trim_cash
                st.success(f"🚨 HIGH-VELOCITY HARVEST TARGET ACCESSED • Sell exactly {round(shares_to_liquidate, 3)} shares (~{fmt_inr(trim_cash)}) to lock in {tranche_vol}% of surplus gains.")
            else:
                st.info(f"🔵 STOCK MATRIX HOLD STEADY • Ticker performance stands steady at {round(current_yield_rate, 2)}%. Maintain long positions.")

    # -------------------------------------------------------------
    # DISPLAY VISUAL CHARTS DECK
    # -------------------------------------------------------------
    if yield_chart_data or composition_chart_data:
        st.markdown("---")
        st.subheader("📊 Live Analytics Performance Dashboard")
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            st.markdown("**📈 Cross-Asset Absolute Yield Radar (%)**")
            df_yields = pd.DataFrame(list(yield_chart_data.items()), columns=["Asset Label", "Yield (%)"]).set_index("Asset Label")
            st.bar_chart(df_yields, height=220)
        with col_ch2:
            st.markdown("**💎 Integrated Capital Scale Distribution (₹)**")
            df_comp = pd.DataFrame(list(composition_chart_data.items()), columns=["Asset Label", "Current Valuation (₹)"]).set_index("Asset Label")
            st.bar_chart(df_comp, height=220)

    # --- COMPUTE COMPREHENSIVE OVERVIEW PROFILE DASHBOARDS ---
    if global_staked_capital > 0:
        st.markdown("---")
        st.subheader("📊 Consolidated Master Overview")
        master_profit = global_current_market_value - global_staked_capital
        master_yield = (master_profit / global_staked_capital) * 100
        
        g1, g2, g3, g4 = st.columns(4)
        with g1:
            st.metric("Aggregate Staked Capital", fmt_inr(global_staked_capital))
        with g2:
            st.metric("Combined Market Valuation", fmt_inr(global_current_market_value))
        with g3:
            st.metric("Consolidated Net Returns", fmt_inr(master_profit))
        with g4:
            st.metric("Aggregate Portfolio Yield", f"{round(master_yield, 2)}%", "🕒 Real-time Cross-Asset Feed Active")

        # Strategic Risk Shield Balance Indicator Bar Chart
        st.markdown("---")
        st.subheader("🛡️ Defensive Core Shield Master Balance Bar")
        total_integrated_wealth = global_current_market_value + fd_reserves
        mkt_exposure_pct = float(global_current_market_value / total_integrated_wealth) if total_integrated_wealth > 0 else 0.0
        mkt_exposure_pct = max(0.0, min(1.0, mkt_exposure_pct))
        
        st.caption(f"📈 Combined Market Risk Exposure: {round(mkt_exposure_pct * 100, 1)}% | 🛡️ Cash Security Layer: {round((1 - mkt_exposure_pct) * 100, 1)}% (Includes {fmt_inr(total_harvested_surplus_pool)} harvested gains)")
        st.progress(mkt_exposure_pct)
        st.info(f"TOTAL INTEGRATED WEALTH POOL VALUE: {fmt_inr(total_integrated_wealth)}")

        # --- BACKGROUND AUTOMATED STATE SYNC ENGINE ---
        raw_state_string = "|".join(url_state_builder)
        st.query_params.update(inc=income, sip=sip_pct, shd=fd_reserves, state=raw_state_string)

else:
    st.markdown("---")
    st.info("### 📊 Terminal Workspace Active Idle Matrix\n\nOpen up the left control menu (`»`). Choose an asset class and deploy tracking containers to start your dashboard pipelines.")

# --- PERSISTENT PREDICTIVE FORWARD PLANNER ---
st.markdown("---")
st.subheader("🎯 Predictive Compound Horizon Playground")
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

st.success(f"REQUIRED SIP INSTALLMENT RADAR TO HIT TARGET: {fmt_inr(required_monthly_sip)} / month (Compounding over {horizon_years} years at a baseline of {expected_return}%)")
st.markdown("---")
st.caption(f"P.A.S.E Pro Terminal Network Active | Universal Engine Sync: {dt.datetime.now().strftime('%Y-%m-%d')} IST")
            
