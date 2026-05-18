import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# PAGE SETTINGS

st.set_page_config(
    page_title="ETF RSI Scanner",
    page_icon="📈",
    layout="wide"
)

# TITLE

st.title("📈 NSE ETF RSI Scanner")
st.markdown("Professional Low RSI ETF Buying Zone Scanner")

# ETF LIST

etfs = [
    "NIFTYBEES",
    "BANKBEES",
    "JUNIORBEES",
    "ITBEES",
    "AUTOBEES",
    "PSUBNKBEES",
    "CPSEETF",
    "ICICIB22",
    "MID150BEES",
    "NEXT50",
    "PHARMABEES",
    "ENERGYETF",
    "INFRABEES",
    "MON100",
    "MAFANG"
]

# RSI FUNCTION

def calculate_rsi(data, period=14):

    delta = data.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# BUTTON

if st.button("🔄 Refresh Data"):

    st.info("Updating ETF Data...")

# MAIN DATA

results = []

for etf in etfs:

    try:

        symbol = etf + ".NS"

        df = yf.download(
            symbol,
            period="3mo",
            interval="1d",
            progress=False
        )

        close = df['Close']

        latest_price = round(close.iloc[-1], 2)

        rsi = calculate_rsi(close)

        latest_rsi = round(rsi.iloc[-1], 2)

        # SIGNAL

        if latest_rsi < 30:
            signal = "🟢 Strong Buy"

        elif latest_rsi < 35:
            signal = "🟡 Buy Zone"

        elif latest_rsi > 70:
            signal = "🔴 Overbought"

        else:
            signal = "⚪ Neutral"

        results.append([
            etf,
            latest_price,
            latest_rsi,
            signal
        ])

    except:
        pass

# DATAFRAME

df_results = pd.DataFrame(
    results,
    columns=[
        "ETF",
        "PRICE",
        "RSI",
        "SIGNAL"
    ]
)

# DISPLAY TABLE

st.subheader("📊 ETF RSI Data")

st.dataframe(
    df_results,
    use_container_width=True
)

# BUY ZONE

buy_df = df_results[
    df_results["RSI"] < 35
]

st.subheader("🟢 Low RSI Buying Zone")

st.dataframe(
    buy_df,
    use_container_width=True
)

# LAST UPDATE

st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
)
