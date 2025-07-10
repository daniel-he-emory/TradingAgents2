import streamlit as st
import httpx
import json
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, timedelta

# Set up Streamlit page config (no theme argument)
st.set_page_config(
    page_title="TradingAgents Dashboard",
    layout="centered",
    initial_sidebar_state="auto",
)

# Inject custom dark theme and brand CSS
st.markdown(
    '''
    <style>
      /* Main background and text */
      .main, .stApp { background-color: #1e1e1e !important; color: #f0f0f0 !important; }
      /* Brand blue for headers */
      h1, h2, h3, .st-emotion-cache-10trblm, .st-emotion-cache-1v0mbdj, .stExpanderHeader { color: #1E90FF !important; }
      /* Expander header font size */
      .stExpanderHeader { font-size: 1.15rem !important; }
      /* Metric styling */
      .stMetric { background: #23272F !important; border-radius: 8px; }
      .stMetricLabel { color: #1E90FF !important; font-size: 1.1rem !important; }
      .stMetricValue { color: #F5F6FA !important; font-size: 2rem !important; }
      /* Widget backgrounds */
      .stTextInput, .stDateInput, .stButton, .stForm { background-color: #23272F !important; color: #F5F6FA !important; }
      /* Matplotlib dark style override */
      .stPlotlyChart, .stPyplot { background-color: #181A1B !important; }
    </style>
    ''',
    unsafe_allow_html=True
)

@st.cache_data
def fetch_trade(ticker, trade_date, deep_think_model=None, debate_rounds=None, timeout=60):
    """Fetch trading analysis from the API with a spinner and extended timeout."""
    with st.spinner("Fetching trading analysis…"):
        params = {"ticker": ticker, "date": trade_date}
        if deep_think_model:
            params["deep_think_model"] = deep_think_model
        if debate_rounds:
            params["debate_rounds"] = debate_rounds
        
        resp = httpx.get(
            "https://tradingagents2-1.onrender.com/trade",
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

# Sidebar controls
st.sidebar.title("Advanced Settings")
deep_think_model = st.sidebar.selectbox(
    "Deep Think Model",
    ["o4-mini", "gpt-4o-mini", "gpt-4.1-nano"],
    index=0,
    help="Select the model for deep thinking processes"
)

debate_rounds = st.sidebar.slider(
    "Debate Rounds",
    min_value=1,
    max_value=5,
    value=2,
    help="Number of debate rounds between bull and bear researchers"
)

with st.form("trading_form"):
    ticker = st.text_input("Ticker Symbol", value="AAPL", help="e.g., AAPL, GOOGL, TSLA")
    trade_date = st.date_input("Trade Date", value=date.today())
    submitted = st.form_submit_button("Get Trading Analysis")

if submitted:
    if not ticker:
        st.error("Please enter a ticker symbol.")
    else:
        try:
            date_str = trade_date.strftime("%Y-%m-%d")
            data = fetch_trade(ticker, date_str, deep_think_model, debate_rounds)
        except Exception as e:
            st.error(f"Failed to fetch analysis: {e}")
            st.stop()
        else:
            # Top-line metrics
            rec = data.get("recommendation", "N/A")
            conf = data.get("confidence", "N/A")
            st.metric("Recommendation", rec)
            st.metric("Confidence", conf)
            
            # Analyst Reports
            analyst_reports = data.get("analyst_reports", {})
            if analyst_reports.get("market_report"):
                with st.expander("Market Analyst Report"):
                    st.write(analyst_reports["market_report"])
            
            if analyst_reports.get("news_report"):
                with st.expander("News Analyst Report"):
                    st.write(analyst_reports["news_report"])
                    
            if analyst_reports.get("sentiment_report"):
                with st.expander("Social Media Analyst Report"):
                    st.write(analyst_reports["sentiment_report"])
                    
            if analyst_reports.get("technical_report"):
                with st.expander("Technical Analyst Report"):
                    st.write(analyst_reports["technical_report"])
            
            # Bull vs Bear Debate
            debate_logs = data.get("debate_logs", [])
            if debate_logs:
                with st.expander("Bull vs Bear Debate"):
                    for log in debate_logs:
                        st.write(f"**Round {log['round']} - {log['type'].title()}:**")
                        st.write(log["message"])
                        st.write("---")
            
            # Risk Management Team
            risk_mgmt = data.get("risk_management", {})
            with st.expander("Risk Management Analysis"):
                if risk_mgmt.get("risky_summary"):
                    st.write("**Aggressive Analysis:**")
                    st.write(risk_mgmt["risky_summary"])
                    st.write("")
                
                if risk_mgmt.get("safe_summary"):
                    st.write("**Conservative Analysis:**")
                    st.write(risk_mgmt["safe_summary"])
                    st.write("")
                    
                if risk_mgmt.get("neutral_summary"):
                    st.write("**Neutral Analysis:**")
                    st.write(risk_mgmt["neutral_summary"])
                    st.write("")
                
            if risk_mgmt.get("judge_decision"):
                st.write("**Risk Manager Decision:**")
                st.write(risk_mgmt["judge_decision"])
        
        # Final Rationale and Trading Plan
        rationale = data.get("reasoning", "No rationale provided.")
        plan = data.get("processed_signal", "No plan provided.")
        
        with st.expander("Final Rationale"):
            st.write(rationale)
        with st.expander("Trading Plan"):
            st.write(plan)
        # Price chart
        st.subheader(f"{ticker} Price History (±30 days)")
        price_df = fetch_price_data(ticker, trade_date)
        if not price_df.empty:
            # --- Matplotlib dark style for plot ---
            plt.style.use('dark_background')  # Dark background for plot
            fig, ax = plt.subplots(figsize=(6, 3))
            price_df["Close"].plot(ax=ax, color="#1E90FF", linewidth=2)
            ax.axvline(trade_date, color="#F5F6FA", linestyle="--", label="Trade Date")
            ax.set_ylabel("Close Price ($)", color="#F5F6FA")
            ax.set_xlabel("Date", color="#F5F6FA")
            ax.tick_params(colors="#F5F6FA")
            ax.grid(True, color="#444", linestyle="--", alpha=0.3)
            ax.legend(facecolor="#23272F", edgecolor="#23272F", labelcolor="#F5F6FA")
            st.pyplot(fig)
        else:
            st.info("No price data available for this ticker/date range.")

st.markdown("---")
st.markdown("""
### How to run:
1. Install dependencies:
   ```bash
   pip install streamlit httpx yfinance matplotlib
   ```
2. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```
3. Make sure your TradingAgents API is running on http://127.0.0.1:8000
""")