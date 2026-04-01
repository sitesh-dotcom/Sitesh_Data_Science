import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. INITIALIZE SETTINGS
st.set_page_config(page_title="Sitesh's Market Dashboard", layout="wide")

# 2. SIDEBAR SETUP
st.sidebar.header("Settings")
market_display = st.sidebar.selectbox(
    "Select Index", 
    ["Dow Jones (^DJI)", "Nifty 50 (^NSEI)", "Bitcoin (BTC-USD)"],
    key="main_market_select"
)

time_range = st.sidebar.selectbox(
    "Select Period", 
    ["1d", "5d", "1mo", "6mo"],
    key="main_period_select"
)

ticker_map = {
    "Dow Jones (^DJI)": "^DJI", 
    "Nifty 50 (^NSEI)": "^NSEI", 
    "Bitcoin (BTC-USD)": "BTC-USD"
}
selected_ticker = ticker_map[market_display]

# 3. MAIN DASHBOARD UI
st.title("📈 Sitesh's Global Market Dashboard")

if st.button("Update Market Data", key="final_update_btn"):
    with st.spinner('Analyzing market trends...'):
        interval = "15m" if time_range == "1d" else "1h"
        data = yf.download(selected_ticker, period=time_range, interval=interval)

    if not data.empty:
        # --- STEP 1: CALCULATIONS ---
        # Moving Averages
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()

        # RSI Calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1+rs))

        # Prediction Logic
        # --- NEW DATA LOGIC ---
# Fetch data
        data = yf.download(ticker, selected_period, interval='5m' if period == '1d' else '1d')

if not data.empty:
    # Only runs if the market returned actual prices
    current_val = float(data['Close'].iloc[-1])
    prev_val = float(data['Close'].iloc[0])
    
    # Calculate changes for your metrics
    change = current_val - prev_val
    percent_change = (change / prev_val) * 100

    # Display the metric at the top
    col1.metric(ticker, f"{current_val:,.2f}", f"{percent_change:+.2f}%")
    
    # Prediction logic (existing code moves inside this block)
    data_for_model = data.dropna().copy()
    # ... rest of your model code ...
else:
    st.warning(f"No data available for {ticker} right now. The market might be closed.")
        if len(data_for_model) > 1:
            data_for_model['Seconds'] = np.arange(len(data_for_model))
            X = data_for_model[['Seconds']]
            y = data_for_model['Close']
            model = LinearRegression()
            model.fit(X, y)
            next_index = np.array([[len(data_for_model) + 1]])
            pred_val = float(prediction.item())
            prediction = model.predict(next_index)
            

        # --- STEP 2: CREATE THE UI CONTAINERS (Fixes NameError) ---
        col1, col2, col3 = st.columns(3)
        
        # --- STEP 3: FILL THE METRICS ---
        change = current_val - float(data['Open'].iloc[0])
        col1.metric("Current Price", f"{float(current_val):,.2f}", f"{float(change):,.2f}")
        rsi_val = data['RSI'].iloc[-1]
        col2.metric("RSI (14)", f"{rsi_val:,.2f}")
        
        if pred_val is not None:
            if pred_val > current_val:
                col3.success(f"Prediction: 📈 {pred_val:,.2f}")
            else:
                col3.warning(f"Prediction: 📉 {pred_val:,.2f}")
        else:
            col3.info("Awaiting data...")

        # --- STEP 4: CREATE AND SHOW CHART ---
        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'], name="Price"
        )])
        
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='20 SMA', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='50 SMA', line=dict(color='blue')))
        
        fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("No data found. Check your selection.")
        # This moves the file "up" one level to the main project folder
        