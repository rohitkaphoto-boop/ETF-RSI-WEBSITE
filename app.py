import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------

st.set_page_config(
    page_title="NSE ETF RSI Scanner",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📈 NSE ETF RSI Scanner")

st.markdown(
    "Professional Low RSI ETF Buying Zone Scanner"
)

# ---------------------------------------------------
# ETF LIST
# ---------------------------------------------------

etfs = [
    "NIFTYBEES",
    "BANKBEES",
    "JUNIORBEES",
    "ITBEES",
    "PSUBNKIETF",
    "CPSEETF",
    "ICICIB22",
    "MON100",
    "MAFANG"
]

# ---------------------------------------------------
# RSI FUNCTION
# ---------------------------------------------------

def calculate_rsi(data, period=14):

    delta = data.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# ---------------------------------------------------
# REFRESH BUTTON
# ---------------------------------------------------

if st.button("🔄 Refresh Data"):

    st.info("Updating ETF Data...")

# ---------------------------------------------------
# MAIN DATA COLLECTION
# ---------------------------------------------------

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

        # CHECK EMPTY DATA

        if df.empty:
            continue

        # FIX CLOSE COLUMN

        close = df['Close'].squeeze()

        # GET PRICE

        latest_price = float(
            round(close.iloc[-1], 2)
        )

        # CALCULATE RSI

        rsi = calculate_rsi(close)

        latest_rsi = float(
            round(rsi.iloc[-1], 2)
        )

        # SIGNAL SYSTEM

        if latest_rsi < 30:

            signal = "🟢 Strong Buy"

        elif latest_rsi < 35:

            signal = "🟡 Buy Zone"

        elif latest_rsi > 70:

            signal = "🔴 Overbought"

        else:

            signal = "⚪ Neutral"

        # STORE RESULTS

        results.append([
            etf,
            latest_price,
            latest_rsi,
            signal
        ])

    except Exception as e:

        st.error(f"Error loading {etf}")

# ---------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------

df_results = pd.DataFrame(
    results,
    columns=[
        "ETF",
        "PRICE",
        "RSI",
        "SIGNAL"
    ]
)

# ---------------------------------------------------
# SHOW ETF TABLE
# ---------------------------------------------------

st.subheader("📊 ETF RSI Data")

if not df_results.empty:

    st.dataframe(
        df_results,
        use_container_width=True
    )

else:

    st.warning("No ETF Data Found")

# ---------------------------------------------------
# BUY ZONE TABLE
# ---------------------------------------------------

buy_df = df_results[
    df_results["RSI"] < 35
]

st.subheader("🟢 Low RSI Buying Zone")

if not buy_df.empty:

    st.dataframe(
        buy_df,
        use_container_width=True
    )

else:

    st.info("No ETF currently in Buy Zone")

# ---------------------------------------------------
# LAST UPDATED
# ---------------------------------------------------

st.caption(
    f"Last Updated: "
    f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
)
