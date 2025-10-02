# Black-Scholes Option Pricing Model  

This project implements the **Black-Scholes Option Pricing Model** using **Streamlit**, providing an interactive interface to calculate and visualize option prices for European-style options. The application allows users to explore option pricing under different market conditions and integrates a **machine learning module** to forecast volatility from historical data.  

## Features  
- **User-Friendly Interface**  
  - Sidebar inputs for parameters such as current price, strike price, time to maturity, volatility (σ), and risk-free interest rate.  
  - Option to choose between manual volatility input or ML-predicted volatility.  

- **Machine Learning Volatility Forecasting**  
  - Ridge Regression and Random Forest models trained on historical stock returns and technical indicators (rolling volatility, EWMA, RSI, momentum).  
  - Predicts forward-looking volatility to address the constant-σ limitation of the Black-Scholes model.  

- **Live Market Data via API**  
  - Fetches current stock prices directly from the **Yahoo Finance API**.  
  - Supports real-time pricing and scenario testing with dynamic parameter updates.  

- **Interactive Visualizations**  
  - Heatmaps display call and put option prices across ranges of spot prices and volatilities.  
  - Helps users understand price sensitivity to different inputs.  

## Tech Stack  
- **Python**: Core Black-Scholes implementation and ML models.  
- **Streamlit**: Interactive web interface.  
- **Scikit-learn**: Ridge Regression & Random Forest models for volatility prediction.  
- **NumPy / Pandas**: Numerical computation and data handling.  
- **Matplotlib / Seaborn / Plotly**: Heatmap and chart visualizations.  
- **Yahoo Finance API**: Live financial data integration.

## Author  
[Nitish Chawla](https://www.linkedin.com/in/nitishchawla-/)  
