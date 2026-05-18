import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="NSE ETF RSI Dashboard",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM STYLE
# ------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.metric-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #374151;
}

.metric-title {
    color: #9CA3AF;
    font-size: 16px;
}

.metric-value {
    color: white;
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("📈 NSE ETF RSI Dashboard")

st.markdown(
    "Professional Low RSI ETF Buying Zone Scanner"
)

# ------------------------------------------------
# ETF LIST
# ------------------------------------------------

etfs = [

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
    "MON100",
    "MAFANG",
    "MAHKTECH",
    "HNGSNGBEES",
    "MOM50",
    "SETFNIF50",
    "UTINEXT50",
    "AXISTECETF",
    "DSPITETF",
    "KOTAKBKETF",
    "ICICINIFTY"

]

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("Dashboard Filters")

search_etf = st.sidebar.text_input(
    "Search ETF"
)

filter_option = st.sidebar.selectbox(
    "Select Filter",
    [
        "All ETFs",
        "Strong Buy",
        "Buy Zone",
        "Overbought"
    ]
)

# ------------------------------------------------
# RSI FUNCTION
# ------------------------------------------------

def calculate_rsi(data, period=14):

    delta = data.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# ------------------------------------------------
# REFRESH BUTTON
# ------------------------------------------------

if st.button("🔄 Refresh ETF Data"):

    st.success("ETF Data Updated")

# ------------------------------------------------
# DATA COLLECTION
# ------------------------------------------------

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

        if df.empty:
            continue

        close = df["Close"].squeeze()

        latest_price = round(
            float(close.iloc[-1]),
            2
        )

        rsi = calculate_rsi(close)

        latest_rsi = round(
            float(rsi.iloc[-1]),
            2
        )

        # SIGNAL

        if latest_rsi < 30:

            signal = "🟢 Strong Buy"

        elif latest_rsi < 35:

            signal = "🟡 Buy Zone"

        elif latest_rsi > 70:

            signal = "🔴 Overbought"

        else:

            signal = "⚪ Neutral"

        # TRADINGVIEW LINK

        link = (
            f"https://www.tradingview.com/symbols/NSE-{etf}/"
        )

        etf_link = (
            f'<a href="{link}" target="_blank">{etf}</a>'
        )

        results.append([
            etf,
            etf_link,
            latest_price,
            latest_rsi,
            signal
        ])

    except:
        pass

    progress.progress((i + 1) / len(etfs))

# ------------------------------------------------
# DATAFRAME
# ------------------------------------------------

columns = [
    "ETF_NAME",
    "ETF",
    "PRICE",
    "RSI",
    "SIGNAL"
]

df_results = pd.DataFrame(
    results,
    columns=columns
)

# ------------------------------------------------
# SEARCH FILTER
# ------------------------------------------------

if search_etf:

    df_results = df_results[
        df_results["ETF_NAME"]
        .str.contains(search_etf.upper())
    ]

# ------------------------------------------------
# FILTER SYSTEM
# ------------------------------------------------

if filter_option == "Strong Buy":

    df_results = df_results[
        df_results["RSI"] < 30
    ]

elif filter_option == "Buy Zone":

    df_results = df_results[
        (df_results["RSI"] >= 30)
        &
        (df_results["RSI"] < 35)
    ]

elif filter_option == "Overbought":

    df_results = df_results[
        df_results["RSI"] > 70
    ]

# ------------------------------------------------
# SORT
# ------------------------------------------------

if not df_results.empty:

    df_results = df_results.sort_values(
        by="RSI"
    )

# ------------------------------------------------
# METRIC CARDS
# ------------------------------------------------

total_etfs = len(df_results)

strong_buy = len(
    df_results[df_results["RSI"] < 30]
)

buy_zone = len(
    df_results[
        (df_results["RSI"] >= 30)
        &
        (df_results["RSI"] < 35)
    ]
)

overbought = len(
    df_results[df_results["RSI"] > 70]
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">
            Total ETFs
        </div>
        <div class="metric-value">
            {total_etfs}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">
            Strong Buy
        </div>
        <div class="metric-value">
            {strong_buy}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">
            Buy Zone
        </div>
        <div class="metric-value">
            {buy_zone}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">
            Overbought
        </div>
        <div class="metric-value">
            {overbought}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# ETF TABLE
# ------------------------------------------------

st.subheader("📊 ETF RSI Dashboard")

if not df_results.empty:

    show_df = df_results[
        [
            "ETF",
            "PRICE",
            "RSI",
            "SIGNAL"
        ]
    ]

    st.write(
        show_df.to_html(
            escape=False,
            index=False
        ),
        unsafe_allow_html=True
    )

else:

    st.warning("No ETF Data Available")

# ------------------------------------------------
# BUY ZONE TABLE
# ------------------------------------------------

buy_df = df_results[
    df_results["RSI"] < 35
]

st.subheader("🟡 Buy Zone ETFs")

if not buy_df.empty:

    buy_show = buy_df[
        [
            "ETF",
            "PRICE",
            "RSI",
            "SIGNAL"
        ]
    ]

    st.write(
        buy_show.to_html(
            escape=False,
            index=False
        ),
        unsafe_allow_html=True
    )

else:

    st.info("No ETF In Buy Zone")

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.caption(
    f"Last Updated: "
    f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
)

st.caption(
    "Powered by Streamlit + Yahoo Finance"
)
