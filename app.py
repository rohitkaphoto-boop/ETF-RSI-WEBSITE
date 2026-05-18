import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="NSE ETF RSI Scanner",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: white;
}

table {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📈 NSE ETF RSI Scanner")

st.markdown(
    "### Professional Low RSI ETF Buying Zone Scanner"
)

# ---------------------------------------------------
# ETF LIST
# ---------------------------------------------------

etfs = [

    # MAIN ETFs

    "NIFTYBEES",
    "BANKBEES",
    "JUNIORBEES",
    "ITBEES",
    "AUTOBEES",
    "PSUBNKIETF",
    "CPSEETF",
    "ICICIB22",
    "MID150BEES",
    "NEXT50",
    "PHARMABEES",
    "ENERGYETF",
    "INFRABEES",
    "CONSUMBEES",
    "DIVOPPBEES",
    "NV20BEES",
    "QUAL30IETF",
    "ALPHAETF",
    "LOWVOLIETF",

    # FOREIGN ETFs

    "MON100",
    "MAFANG",
    "MAHKTECH",
    "HNGSNGBEES",

    # EXTRA ETFs

    "MOM50",
    "NIFITETF",
    "SETFNIF50",
    "AXISTECETF",
    "DSPITETF",
    "UTINEXT50",
    "KOTAKBKETF",
    "ICICINIFTY",
    "ABSLNN50ET"
]

# REMOVE DUPLICATES

etfs = list(set(etfs))

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

if st.button("🔄 Refresh ETF Data"):

    st.success("ETF Data Updated Successfully")

# ---------------------------------------------------
# MAIN DATA
# ---------------------------------------------------

results = []

progress = st.progress(0)

for i, etf in enumerate(etfs):

    try:

        symbol = etf + ".NS"

        df = yf.download(
            symbol,
            period="3mo",
            interval="1d",
            progress=False
        )

        # SKIP EMPTY

        if df.empty:
            continue

        # FIX CLOSE COLUMN

        close = df['Close'].squeeze()

        # LATEST PRICE

        latest_price = float(
            round(close.iloc[-1], 2)
        )

        # RSI

        rsi = calculate_rsi(close)

        latest_rsi = float(
            round(rsi.iloc[-1], 2)
        )

        # SIGNAL

        if latest_rsi < 30:

            signal = "🟢 STRONG BUY"

        elif latest_rsi < 35:

            signal = "🟡 BUY ZONE"

        elif latest_rsi > 70:

            signal = "🔴 OVERBOUGHT"

        else:

            signal = "⚪ NEUTRAL"

        # TRADINGVIEW LINK

        tradingview_link = (
            f"https://www.tradingview.com/symbols/NSE-{etf}/"
        )

        etf_link = (
            f'<a href="{tradingview_link}" '
            f'target="_blank">{etf}</a>'
        )

        # APPEND DATA

        results.append([

            etf_link,
            latest_price,
            latest_rsi,
            signal

        ])

    except:

        pass

    progress.progress((i + 1) / len(etfs))

# ---------------------------------------------------
# DATAFRAME
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
# SORT BY RSI
# ---------------------------------------------------

df_results = df_results.sort_values(
    by="RSI"
)

# ---------------------------------------------------
# ETF DATA TABLE
# ---------------------------------------------------

st.subheader("📊 ETF RSI Data")

if not df_results.empty:

    st.write(

        df_results.to_html(
            escape=False,
            index=False
        ),

        unsafe_allow_html=True

    )

else:

    st.warning("No ETF Data Available")

# ---------------------------------------------------
# BUY ZONE
# ---------------------------------------------------

buy_df = df_results[
    df_results["RSI"] < 35
]

st.subheader("🟡 Buy Zone ETFs")

if not buy_df.empty:

    st.write(

        buy_df.to_html(
            escape=False,
            index=False
        ),

        unsafe_allow_html=True

    )

else:

    st.info("No ETF In Buy Zone")

# ---------------------------------------------------
# STRONG BUY ZONE
# ---------------------------------------------------

strong_buy_df = df_results[
    df_results["RSI"] < 30
]

st.subheader("🟢 Strong Buy ETFs")

if not strong_buy_df.empty:

    st.write(

        strong_buy_df.to_html(
            escape=False,
            index=False
        ),

        unsafe_allow_html=True

    )

else:

    st.info("No Strong Buy ETF Found")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📌 RSI RULES")

st.sidebar.success("RSI Below 30 = Strong Buy")

st.sidebar.warning("RSI Below 35 = Buy Zone")

st.sidebar.error("RSI Above 70 = Overbought")

# ---------------------------------------------------
# LAST UPDATED
# ---------------------------------------------------

st.caption(

    f"Last Updated: "
    f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"

)
