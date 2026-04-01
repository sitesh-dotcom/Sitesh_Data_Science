import streamlit as st
import yfinance as yf
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Global Market Dashboard", layout="wide")

st.title("📈 Sitesh's Global Market Dashboard")

# -------------------------------
# Sidebar Settings
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
selected_symbol = index_options[selected_index]

period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])

# -------------------------------
# Fetch Data Button
# -------------------------------
if st.button("Update Market Data"):

    with st.spinner("Fetching data..."):

        try:
            # Fetch data
            data = yf.download(selected_symbol, period=period, interval="1m")

            # -------------------------------
            # ERROR HANDLING
            # -------------------------------
            if data.empty:
                st.error("❌ No data fetched. Market might be closed or symbol issue.")
                st.stop()

            if 'Close' not in data.columns:
                st.error("❌ 'Close' column not found in data.")
                st.stop()

            # Clean data
            data = data.dropna()

            if data.empty:
                st.error("❌ Data contains only NaN values.")
                st.stop()

            # -------------------------------
            # SAFE VALUE EXTRACTION
            # -------------------------------
            current_val = float(data['Close'].iloc[-1])
            prev_val = float(data['Close'].iloc[-2]) if len(data) > 1 else current_val

            change = current_val - prev_val
            percent_change = (change / prev_val) * 100 if prev_val != 0 else 0

            # -------------------------------
            # DISPLAY METRICS
            # -------------------------------
            st.subheader(f"{selected_index}")

            col1, col2, col3 = st.columns(3)

            col1.metric("Current Value", f"{current_val:.2f}")
            col2.metric("Change", f"{change:.2f}")
            col3.metric("Change %", f"{percent_change:.2f}%")

            # -------------------------------
            # CHART
            # -------------------------------
            st.line_chart(data['Close'])

            # -------------------------------
            # DEBUG (Optional)
            # -------------------------------
            with st.expander("Show Raw Data"):
                st.write(data.tail())

        except Exception as e:
            st.error(f"⚠️ Error occurred: {e}")
            st.stop()