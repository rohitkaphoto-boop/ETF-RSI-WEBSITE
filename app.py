import streamlit as st
import pandas as pd
import numpy as np
import investpy
from datetime import datetime

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="NSE ETF LIVE RSI Dashboard",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
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
    border-radius: 15px;
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

table {
    width: 100%;
    border-collapse: collapse;
}

thead tr {
    background-color: #1F2937;
    color: white;
}

tbody tr {
    background-color: #111827;
    color: white;
}

td, th {
    padding: 12px;
    border: 1px solid #374151;
    text-align: center;
}

a {
    color: #60A5FA;
    text-decoration: none;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("📈 NSE ETF LIVE RSI Dashboard")

st.markdown(
    "Professional Live ETF RSI Scanner"
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
    "MON100",
    "MAFANG"

]

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("Dashboard Settings")

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

if st.button("🔄 Refresh Live Data"):

    st.success("Live Data Updated")

# ------------------------------------------------
# MAIN DATA
# ------------------------------------------------

results = []

progress = st.progress(0)

for i, etf in enumerate(etfs):

    try:

        # GET HISTORICAL DATA

        df = investpy.get_etf_historical_data(

            etf=etf,
            country='india',
            from_date='01/01/2024',
            to_date=datetime.now().strftime('%d/%m/%Y')

        )

        if df.empty:
            continue

        close = df["Close"]

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

        tv_link = (
            f"https://www.tradingview.com/symbols/NSE-{etf}/"
        )

        etf_link = (
            f'<a href="{tv_link}" target="_blank">{etf}</a>'
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
# SEARCH
# ------------------------------------------------

if search_etf:

    df_results = df_results[
        df_results["ETF_NAME"]
        .str.contains(search_etf.upper())
    ]

# ------------------------------------------------
# FILTERS
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
# KPI CARDS
# ------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total ETFs", len(df_results))

with col2:
    st.metric(
        "Strong Buy",
        len(df_results[df_results["RSI"] < 30])
    )

with col3:
    st.metric(
        "Buy Zone",
        len(
            df_results[
                (df_results["RSI"] >= 30)
                &
                (df_results["RSI"] < 35)
            ]
        )
    )

with col4:
    st.metric(
        "Overbought",
        len(df_results[df_results["RSI"] > 70])
    )

# ------------------------------------------------
# MAIN TABLE
# ------------------------------------------------

st.subheader("📊 Live ETF RSI Dashboard")

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
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.caption(
    f"Last Updated: "
    f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
)
