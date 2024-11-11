"""
Streamlit App for Black-Scholes Option Pricing Model

Author: Nitish Chawla

"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from black_scholes import BlackScholes


#Page Configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


