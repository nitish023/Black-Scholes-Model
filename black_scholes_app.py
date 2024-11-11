"""
Streamlit App for Black-Scholes Option Pricing Model

Author: Nitish Chawla

"""

import streamlit as st
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
    st.header("Input Parameters")
    current_price = st.number_input("Current Price", min_value=0.0, step=1.0, value=100.0)
    strike = st.number_input("Strike Price", min_value=0.0, step=1.0, value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", min_value=0.0, step=0.01, value=1.0)
    volatility - st.number_input("Volatility (σ)", min_value=0.0, max_value=1.0, step=0.01, value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.05)
