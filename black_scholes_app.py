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

    current_price = st.number_input("Current Price", min_value=0.0, step=1.0, value=100.0)
    strike = st.number_input("Strike Price", min_value=0.0, step=1.0, value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", min_value=0.0, step=0.01, value=1.0)
    volatility = st.number_input("Volatility (σ)", min_value=0.0, max_value=1.0, step=0.01, value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.05)

    st.markdown("---")
    calculate_button = st.button("Heatmap Parameters")
    spot_min = st.number_input("Min Spot Price", min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input("Max Spot Price", min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)


def plot_heatmap(bs_model, spot_range, vol_range, strike):
    call_prices = np.zeroes((len(vol_range), len(spot_range)))
    put_prices = np.zeroes((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_inst = BlackScholes(time_to_maturity=bs_model.time_to_maturity, strike=strike, current_price=spot, volatility=vol, interest_rate=bs_model.interest_rate)
            call_prices[i, j] = bs_inst.call_price()
            put_prices[i, j] = bs_inst.put_price()

    #Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
    ax_call.set_title("Call Option Prices")
    ax_call.set_xlabel("Spot Price")
    ax_call.set_ylabel("Volatility")

    #Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
    ax_put.set_title("Put Option Prices")
    ax_put.set_xlabel("Spot Price")
    ax_put.set_ylabel("Volatility")

    return fig_call, fig_put


#Main Page
st.title("Black-Scholes Option Pricing Model")

#Inputs Table
input_data = {
    "Current Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity": [time_to_maturity],
    "Volatility": [volatility],
    "Risk-Free Interest Rate": [interest_rate]
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