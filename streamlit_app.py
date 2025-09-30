import streamlit as st
import httpx
import json
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import date, timedelta

# Set up Streamlit page config
st.set_page_config(
    page_title="TradingAgents - AI Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

# Inject custom CSS for better visual appeal
st.markdown(
    '''
    <style>
      /* Main styling */
      .main, .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }

      /* Headers with gradient */
      h1 {
        background: linear-gradient(90deg, #1E90FF 0%, #00CED1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
      }
      h2, h3 { color: #1E90FF !important; font-weight: 600 !important; }

      /* Card-like containers */
      .stExpander {
        background: #1A1D29 !important;
        border-radius: 12px !important;
        border: 1px solid #2D3748 !important;
        margin: 10px 0 !important;
      }

      /* Metrics styling */
      .stMetric {
        background: linear-gradient(135deg, #1A1D29 0%, #252A3A 100%) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 2px solid #1E90FF !important;
      }
      .stMetricLabel {
        color: #00CED1 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
      }
      .stMetricValue {
        color: #FAFAFA !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
      }

      /* Buttons */
      .stButton>button {
        background: linear-gradient(90deg, #1E90FF 0%, #00CED1 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        border: none !important;
      }

      /* Form inputs */
      .stTextInput>div>div>input, .stDateInput>div>div>input {
        background-color: #1A1D29 !important;
        color: #FAFAFA !important;
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
      }

      /* Sidebar */
      .css-1d391kg { background-color: #0E1117 !important; }

      /* Make markdown text readable */
      .stMarkdown { color: #FAFAFA !important; }

      /* Tables */
      table { background-color: #1A1D29 !important; }
      th { background-color: #252A3A !important; color: #00CED1 !important; }
      td { color: #FAFAFA !important; }
    </style>
    ''',
    unsafe_allow_html=True
)

@st.cache_data
def fetch_trade(ticker, trade_date, deep_think_model=None, debate_rounds=None, timeout=600):
    """Fetch trading analysis from the API."""
    with st.spinner("⏳ Running multi-agent analysis (typically 3-5 minutes)... Please wait, agents are debating!"):
        params = {"ticker": ticker, "date": trade_date}
        if deep_think_model:
            params["deep_think_model"] = deep_think_model
        if debate_rounds:
            params["debate_rounds"] = debate_rounds

        # Backend URL configuration - defaults to localhost for local development
        backend_url = os.getenv("STREAMLIT_BACKEND_URL", "http://localhost:8000")

        resp = httpx.get(
            f"{backend_url}/trade",
            params=params,
            timeout=timeout
        )
    resp.raise_for_status()
    return resp.json()

@st.cache_data(show_spinner=False)
def fetch_price_data(ticker, trade_date):
    start = (trade_date - timedelta(days=30)).strftime("%Y-%m-%d")
    end = (trade_date + timedelta(days=30)).strftime("%Y-%m-%d")
    df = yf.download(ticker, start=start, end=end, progress=False)
    return df

def get_recommendation_color(rec):
    """Get color based on recommendation."""
    rec_upper = rec.upper()
    if "BUY" in rec_upper:
        return "🟢", "#00FF00"
    elif "SELL" in rec_upper:
        return "🔴", "#FF0000"
    else:
        return "🟡", "#FFD700"

# Main title with emoji
st.markdown("# 📈 TradingAgents AI")
st.markdown("### *Multi-Agent Stock Analysis for Retail Investors*")
st.markdown("---")

# Sidebar controls
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("*Advanced configuration*")

deep_think_model = st.sidebar.selectbox(
    "🤖 AI Model",
    ["gpt-4o-mini", "gpt-4o", "o4-mini"],
    index=0,
    help="Model for analysis (gpt-4o-mini is fastest)"
)

debate_rounds = st.sidebar.slider(
    "💬 Debate Rounds",
    min_value=1,
    max_value=3,
    value=1,
    help="More rounds = deeper analysis but slower"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**⏱️ Expected Time:** 3-5 minutes")
st.sidebar.markdown("**💰 Cost per analysis:** ~$0.01-0.05")

# Main form
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    ticker = st.text_input("🎯 Stock Ticker", value="AAPL", placeholder="e.g., AAPL, NVDA, TSLA")

with col2:
    trade_date = st.date_input("📅 Analysis Date", value=date.today())

with col3:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    submitted = st.button("🚀 Analyze Stock", use_container_width=True)

if submitted:
    if not ticker:
        st.error("⚠️ Please enter a stock ticker symbol.")
    else:
        try:
            date_str = trade_date.strftime("%Y-%m-%d")

            # Fetch data
            data = fetch_trade(ticker, date_str, deep_think_model, debate_rounds)

            # Success message
            st.success(f"✅ Analysis complete for **{ticker}** on {date_str}")
            st.markdown("---")

            # Top-line metrics in columns
            rec = data.get("recommendation", "N/A")
            conf = data.get("confidence", "Medium")
            processed_signal = data.get("processed_signal", "HOLD")

            emoji, color = get_recommendation_color(processed_signal)

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric("📊 Final Decision", f"{emoji} {processed_signal}")

            with metric_col2:
                st.metric("🎯 Confidence Level", conf)

            with metric_col3:
                st.metric("📈 Signal", processed_signal)

            st.markdown("---")

            # Create two columns for layout
            left_col, right_col = st.columns([1, 1])

            with left_col:
                # Analyst Reports
                st.markdown("## 📊 Market Analysis")
                analyst_reports = data.get("analyst_reports", {})

                if analyst_reports.get("market_report"):
                    with st.expander("📈 **Market Analyst Report** (Quick Read)", expanded=True):
                        st.markdown(analyst_reports["market_report"])

                if analyst_reports.get("news_report"):
                    with st.expander("📰 **News Analysis**"):
                        st.markdown(analyst_reports["news_report"])

                if analyst_reports.get("sentiment_report"):
                    with st.expander("💬 **Social Sentiment**"):
                        st.markdown(analyst_reports["sentiment_report"])

                if analyst_reports.get("technical_report"):
                    with st.expander("🔧 **Technical Analysis**"):
                        st.markdown(analyst_reports["technical_report"])

            with right_col:
                # Bull vs Bear Debate
                st.markdown("## 🐂 vs 🐻 Debate")

                # Show reasoning/investment plan
                reasoning = data.get("reasoning", "")
                if reasoning:
                    with st.expander("💼 **Investment Recommendation**", expanded=True):
                        st.markdown(reasoning)

                # Risk Management
                st.markdown("## ⚖️ Risk Assessment")
                risk_mgmt = data.get("risk_management", {})

                if risk_mgmt.get("judge_decision"):
                    with st.expander("🛡️ **Risk Manager Decision**", expanded=True):
                        st.markdown(risk_mgmt["judge_decision"])

                # Show individual risk perspectives in compact format
                risk_summaries = []
                if risk_mgmt.get("risky_summary"):
                    risk_summaries.append(("🔴 Aggressive", risk_mgmt["risky_summary"]))
                if risk_mgmt.get("neutral_summary"):
                    risk_summaries.append(("🟡 Neutral", risk_mgmt["neutral_summary"]))
                if risk_mgmt.get("safe_summary"):
                    risk_summaries.append(("🟢 Conservative", risk_mgmt["safe_summary"]))

                if risk_summaries:
                    with st.expander("📊 **Risk Perspectives**"):
                        for title, summary in risk_summaries:
                            st.markdown(f"**{title}**")
                            st.markdown(summary)
                            st.markdown("---")

            # Price chart at the bottom (full width)
            st.markdown("---")
            st.markdown(f"## 📉 {ticker} Price History (±30 days)")

            price_df = fetch_price_data(ticker, trade_date)
            if not price_df.empty:
                # Create better looking chart
                plt.style.use('dark_background')
                fig, ax = plt.subplots(figsize=(12, 4))

                # Plot with gradient-like effect
                ax.plot(price_df.index, price_df["Close"], color="#00CED1", linewidth=2.5, label="Close Price")
                ax.fill_between(price_df.index, price_df["Close"], alpha=0.3, color="#1E90FF")

                # Add trade date line
                ax.axvline(trade_date, color="#FFD700", linestyle="--", linewidth=2, label="Analysis Date")

                # Styling
                ax.set_ylabel("Price ($)", color="#FAFAFA", fontsize=12, fontweight="bold")
                ax.set_xlabel("Date", color="#FAFAFA", fontsize=12, fontweight="bold")
                ax.tick_params(colors="#FAFAFA")
                ax.grid(True, color="#2D3748", linestyle="--", alpha=0.3)
                ax.legend(facecolor="#1A1D29", edgecolor="#2D3748", labelcolor="#FAFAFA", fontsize=10)
                ax.set_facecolor("#0E1117")
                fig.patch.set_facecolor("#0E1117")

                st.pyplot(fig)
            else:
                st.info("📊 No price data available for this ticker/date range.")

            # Debug info in expander
            with st.expander("🔍 **Debug Info** (Advanced Users)"):
                st.json(data)

        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
            st.info("💡 **Tip:** Try a different date or ticker, or check if the backend is running.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.9rem;'>
    <p>⚠️ <b>Disclaimer:</b> This is a research tool, not financial advice. Always do your own research before investing.</p>
    <p>Powered by Multi-Agent AI 🤖 | Built with ❤️ for retail investors</p>
</div>
""", unsafe_allow_html=True)