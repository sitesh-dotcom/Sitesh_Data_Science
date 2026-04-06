import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Global Market Dashboard", layout="wide")

st.title("📈 Sitesh's Global Market Dashboard")

# -------------------------------
# SIDEBAR SETTINGS
# -------------------------------
st.sidebar.header("Settings")

index_options = {
    "Dow Jones (^DJI)": "^DJI",
    "S&P 500 (^GSPC)": "^GSPC",
    "NASDAQ (^IXIC)": "^IXIC",
    "NIFTY 50 (^NSEI)": "^NSEI",
    "BANK NIFTY (^NSEBANK)": "^NSEBANK"
}

selected_index = st.sidebar.selectbox("Select Index", list(index_options.keys()))
symbol = index_options[selected_index]

period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo"])

auto_refresh = st.sidebar.checkbox("Enable Auto Refresh (10 sec)", value=False)

# -------------------------------
# AUTO REFRESH LOGIC
# -------------------------------
if auto_refresh:
    time.sleep(10)
    st.rerun()

# -------------------------------
# FETCH DATA FUNCTION
# -------------------------------
@st.cache_data(ttl=60)
def fetch_data(symbol, period):
    data = yf.download(symbol, period=period, interval="1m")
    return data

# -------------------------------
# LOAD DATA
# -------------------------------
with st.spinner("Fetching market data..."):
    data = fetch_data(symbol, period)

# -------------------------------
# ERROR HANDLING
# -------------------------------
if data.empty:
    st.error("❌ No data fetched. Market may be closed.")
    st.stop()

if 'Close' not in data.columns:
    st.error("❌ 'Close' column missing.")
    st.stop()

# -------------------------------
# FIX SERIES ISSUE (IMPORTANT)
# -------------------------------
close_data = data['Close']

if isinstance(close_data, pd.DataFrame):
    close_data = close_data.iloc[:, 0]

close_data = close_data.dropna()

if close_data.empty:
    st.error("❌ No valid Close data available.")
    st.stop()

# -------------------------------
# CALCULATIONS
# -------------------------------
current_val = float(close_data.iloc[-1])
prev_val = float(close_data.iloc[-2]) if len(close_data) > 1 else current_val

change = current_val - prev_val
percent_change = (change / prev_val) * 100 if prev_val != 0 else 0

# -------------------------------
# METRICS DISPLAY
# -------------------------------
st.subheader(selected_index)

col1, col2, col3 = st.columns(3)

col1.metric("Current Value", f"{current_val:.2f}")
col2.metric("Change", f"{change:.2f}")
col3.metric("Change %", f"{percent_change:.2f}%")

# -------------------------------
# CANDLESTICK CHART
# -------------------------------
st.subheader("📊 Candlestick Chart")

fig = go.Figure(data=[go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
)])

fig.update_layout(
    xaxis_rangeslider_visible=False,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# LINE CHART (OPTIONAL)
# -------------------------------
st.subheader("📈 Close Price Trend")
st.line_chart(close_data)

# -------------------------------
# RAW DATA
# -------------------------------
with st.expander("🔍 Show Raw Data"):
    st.write(data.tail())