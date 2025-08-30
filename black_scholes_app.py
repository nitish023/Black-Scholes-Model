"""
Streamlit App for Black-Scholes Option Pricing Model

Author: Nitish Chawla
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import date, timedelta
from black_scholes import BlackScholes

#Page Configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-container {
            display: flex;
            justify-content: center;
            align_items: center;
            padding: 8px;
            width: auto;
            margin: 0 auto;
    }
            
    .metric-call {
            background-color: #90ee90;
            color: black;
            margin-right: 10px;
            border-radius: 10px;
    }
            
    .metric-put {
            background-color: #ffcccb;
            color: black;
            border-radius: 10px;
    }
            
    .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            margin: 0;
    }
            
    .metric-label {
            font-size: 1rem;
            margin: 4px;
    }
    
</style>
            """, unsafe_allow_html=True)

#Sidebar
with st.sidebar:
    st.header("📊 Black-Scholes Model Inputs")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/nitishchawla-/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Nitish Chawla`</a>', unsafe_allow_html=True)

    ticker = st.text_input(
        "Ticker Symbol",
        value="AAPL",
        help="Enter the stock symbol (e.g., NVDA for NVIDIA Corp.)",
    )
    try:
        ticker_data = yf.Ticker(ticker)
        current_price = ticker_data.history(period="1d")["Close"].iloc[-1]
        st.write(f"Current Price for {ticker}: ${current_price:.2f}")
    except Exception:
        current_price = 100.0
        st.warning(
            "Unable to fetch price for the ticker. Using default price of $100.0."
        )
    strike = st.number_input(
        "Strike Price",
        min_value=0.0,
        step=1.0,
        value=100.0,
        help="The price at which the option can be exercised at maturity.",
    )
    today = date.today()
    default_exercise_date = today + timedelta(days=365)
    exercise_date = st.date_input(
        "Exercise Date",
        value=default_exercise_date,
        min_value=today,
        help="The option's expiration date.",
    )
    time_to_maturity = (exercise_date - today).days / 365
    
    volatility_pct = st.number_input(
        "Volatility (σ) (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        value=20.0,
        help="A measure of the stock's price variability. Higher values indicate more volatile stocks. 0% means no volatility (unrealistic).",
    )
    interest_rate_pct = st.number_input(
        "Risk-Free Interest Rate (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        value=5.0,
        help="The theoretical rate of return of an investment with zero-risk. Usually based on government bonds. 100% means doubling your money with no risk (again unrealistic).",
    )
    volatility = volatility_pct / 100
    interest_rate = interest_rate_pct / 100
    st.markdown("---")
    calculate_button = st.button("Heatmap Parameters")
    spot_min = st.number_input("Min Spot Price", min_value=0.01, value=current_price * 0.8, step=0.01)
    spot_max = st.number_input("Max Spot Price", min_value=0.01, value=current_price * 1.2, step=0.01)
    vol_min_pct = st.slider(
        "Min Volatility for Heatmap (%)",
        min_value=1.0,
        max_value=100.0,
        value=volatility_pct * 0.5,
        step=1.0,
    )
    vol_max_pct = st.slider(
        "Max Volatility for Heatmap (%)",
        min_value=1.0,
        max_value=100.0,
        value=volatility_pct * 1.5,
        step=1.0,
    )

    vol_min = vol_min_pct / 100
    vol_max = vol_max_pct / 100

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)


def plot_heatmap(bs_model, spot_range, vol_range, strike):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    vol_labels = np.round(np.array(vol_range) * 100, 2)

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_inst = BlackScholes(time_to_maturity=bs_model.time_to_maturity, strike=strike, current_price=spot, volatility=vol, interest_rate=bs_model.interest_rate)
            call_prices[i, j] = bs_inst.call_price()
            put_prices[i, j] = bs_inst.put_price()

    #Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=vol_labels, annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
    ax_call.set_title("Call Option Prices")
    ax_call.set_xlabel("Spot Price")
    ax_call.set_ylabel("Volatility")

    #Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=vol_labels, annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
    ax_put.set_title("Put Option Prices")
    ax_put.set_xlabel("Spot Price")
    ax_put.set_ylabel("Volatility (%)")

    return fig_call, fig_put


#Main Page
st.title("Black-Scholes Option Pricing Model")

#Inputs Table
input_data = {
    "Current Price": [current_price],
    "Strike Price": [strike],
    "Exercise Date": [exercise_date],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (%)": [volatility_pct],
    "Risk-Free Interest Rate (%)": [interest_rate_pct]
}

input_df = pd.DataFrame(input_data)
st.table(input_df)

#Black-Scholes Model
bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price = bs_model.call_price()
put_price = bs_model.put_price()

#Displaying Option Prices
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
                """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
                """, unsafe_allow_html=True)
    
st.markdown("")
st.title("Option Prices Interactive Heatmap")
st.info("The heatmap below shows the option prices for different spot prices and volatilities while keeping the strike price constant.")

col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    heatmap_fig_call, _ = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    _, heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_put)