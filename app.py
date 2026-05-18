# Professional NSE ETF RSI Dashboard — Full app.py Code

Replace your FULL old `app.py` code with this new professional dashboard code.

This version includes:

* Professional dark dashboard UI
* KPI cards
* ETF ranking table
* Strong Buy / Buy Zone filters
* Sidebar controls
* Search system
* Auto sorting
* TradingView clickable links
* Progress loader
* Responsive layout
* Foreign + Indian ETFs
* Colorful metrics
* Modern styling

---

```python
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Professional NSE ETF RSI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

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

.metric-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #374151;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.metric-title {
    color: #9ca3af;
    font-size: 16px;
}

.metric-value {
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.buy {
    color: #22c55e;
    font-weight: bold;
}

.warning {
    color: #facc15;
    font-weight: bold;
}

.overbought {
    color: #ef4444;
    font-weight: bold;
}

.neutral {
    color: #9ca3af;
    font-weight: bold;
}

.table-container {
    background-color: #111827;
    padding: 10px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("📈 Professional NSE ETF RSI Dashboard")

st.markdown(
    "Real-Time Low RSI ETF Buying Zone Scanner"
)

# -------------------------------------------------
# ETF LIST
# -------------------------------------------------

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

etfs = list(set(etfs))

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("⚙ Dashboard Settings")

search_etf = st.sidebar.text_input(
    "Search ETF"
)

rsi_filter = st.sidebar.selectbox(
    "Select RSI Filter",
    [
        "All ETFs",
        "Strong Buy",
        "Buy Zone",
        "Overbought"
    ]
)

# -------------------------------------------------
# RSI FUNCTION
# -------------------------------------------------


def calculate_rsi(data, period=14):

    delta = data.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# -------------------------------------------------
# REFRESH BUTTON
# -------------------------------------------------

if st.button("🔄 Refresh Live ETF Data"):

    st.success("ETF Data Refreshed Successfully")

# -------------------------------------------------
# MAIN DATA COLLECTION
# -------------------------------------------------

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

        close = df['Close'].squeeze()

        latest_price = float(
            round(close.iloc[-1], 2)
        )

        rsi = calculate_rsi(close)

        latest_rsi = float(
            round(rsi.iloc[-1], 2)
        )

        # SIGNAL

        if latest_rsi < 30:

            signal = "🟢 Strong Buy"
            signal_class = "buy"

        elif latest_rsi < 35:

            signal = "🟡 Buy Zone"
            signal_class = "warning"

        elif latest_rsi > 70:

            signal = "🔴 Overbought"
            signal_class = "overbought"

        else:

            signal = "⚪ Neutral"
            signal_class = "neutral"

        # TRADINGVIEW LINK

        tradingview_link = (
            f"https://www.tradingview.com/symbols/NSE-{etf}/"
        )

        etf_link = (
            f'<a href="{tradingview_link}" '
            f'target="_blank">{etf}</a>'
        )

        results.append([
            etf,
            etf_link,
            latest_price,
            latest_rsi,
            signal,
            signal_class
        ])

    except:
        pass

    progress.progress((i + 1) / len(etfs))

# -------------------------------------------------
# DATAFRAME
# -------------------------------------------------

columns = [
    "ETF_NAME",
    "ETF",
    "PRICE",
    "RSI",
    "SIGNAL",
    "SIGNAL_CLASS"
]

df_results = pd.DataFrame(
    results,
    columns=columns
)

# -------------------------------------------------
# SEARCH FILTER
# -------------------------------------------------

if search_etf:

    df_results = df_results[
        df_results['ETF_NAME']
        .str.contains(search_etf.upper())
    ]

# -------------------------------------------------
# RSI FILTER
# -------------------------------------------------

if rsi_filter == "Strong Buy":

    df_results = df_results[
        df_results['RSI'] < 30
    ]

elif rsi_filter == "Buy Zone":

    df_results = df_results[
        (df_results['RSI'] >= 30) &
        (df_results['RSI'] < 35)
    ]

elif rsi_filter == "Overbought":

    df_results = df_results[
        df_results['RSI'] > 70
    ]

# -------------------------------------------------
# SORT
# -------------------------------------------------

if not df_results.empty:

    df_results = df_results.sort_values(
        by="RSI"
    )

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

if not df_results.empty:

    total_etfs = len(df_results)

    strong_buy_count = len(
        df_results[df_results['RSI'] < 30]
    )

    buy_zone_count = len(
        df_results[
            (df_results['RSI'] >= 30) &
            (df_results['RSI'] < 35)
        ]
    )

    overbought_count = len(
        df_results[df_results['RSI'] > 70]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total ETFs</div>
            <div class="metric-value">{total_etfs}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Strong Buy</div>
            <div class="metric-value">{strong_buy_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Buy Zone</div>
            <div class="metric-value">{buy_zone_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Overbought</div>
            <div class="metric-value">{overbought_count}</div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# MAIN TABLE
# -------------------------------------------------

st.subheader("📊 ETF RSI Dashboard")

if not df_results.empty:

    display_df = df_results[[
        'ETF',
        'PRICE',
        'RSI',
        'SIGNAL'
    ]]

    st.write(
        display_df.to_html(
            escape=False,
            index=False
        ),
        unsafe_allow_html=True
    )

else:

    st.warning("No ETF Data Available")

# -------------------------------------------------
# BUY ZONE TABLE
# -------------------------------------------------

buy_df = df_results[
    df_results['RSI'] < 35
]

st.subheader("🟡 Buy Zone ETFs")

if not buy_df.empty:

    buy_display = buy_df[[
        'ETF',
        'PRICE',
        'RSI',
        'SIGNAL'
    ]]

    st.write(
        buy_display.to_html(
            escape=False,
            index=False
        ),
        unsafe_allow_html=True
    )

else:

    st.info("No ETF Currently In Buy Zone")

# -------------------------------------------------
# STRONG BUY TABLE
# -------------------------------------------------

strong_buy_df = df_results[
    df_results['RSI'] < 30
]

st.subheader("🟢 Strong Buy ETFs")

if not strong_buy_df.empty:

    strong_display = strong_buy_df[[
        'ETF',
        'PRICE',
        'RSI',
        'SIGNAL'
    ]]

    st.write(
        strong_display.to_html(
            escape=False,
            index=False
        ),
        unsafe_allow_html=True
    )

else:

    st.info("No Strong Buy ETF Found")

# -------------------------------------------------
# SIDEBAR RULES
# -------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.title("📌 RSI Rules")

st.sidebar.success("RSI < 30 = Strong Buy")

st.sidebar.warning("RSI < 35 = Buy Zone")

st.sidebar.error("RSI > 70 = Overbought")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")

st.caption(
    f"Last Updated: "
    f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
)

st.caption(
    "Powered by Streamlit + Yahoo Finance"
)
```

---

# HOW TO UPDATE YOUR WEBSITE

## STEP 1

Open your GitHub repository.

---

## STEP 2

Open:

```text
app.py
```

---

## STEP 3

Click:

```text
✏ Edit
```

---

## STEP 4

Delete ALL old code.

---

## STEP 5

Paste this FULL new professional code.

Keyboard:

```text
CTRL + V
```

---

## STEP 6

Scroll down.

Click:

```text
Commit changes
```

---

# FINAL RESULT

Your website will now look like a professional trading dashboard with:

* Dark theme
* Dashboard cards
* ETF search
* RSI filters
* TradingView links
* Buy Zone tables
* Strong Buy tables
* Sidebar controls
* Live ETF scanner
* Mobile friendly UI
* Modern professional design
