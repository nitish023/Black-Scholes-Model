"""
Black-Scholes Option Pricing Model

Author: Nitish Chawla

Description: This script contains a class that implements the Black-Scholes option pricing model
to calculate the European call and put option prices and their Greeks (Delta and Gamma).

"""

from numpy import exp, sqrt, log
from scipy.stats import norm

class BlackScholes:
    def __init__(self, time_to_maturity: float, strike: float, current_price: float, volatility: float, interest_rate: float):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_d1_d2(self):
        """Calculates d1 and d2 for the Black-Scholes formula"""
        d1 = (log(self.current_price / self.strike) + (self.interest_rate + (self.volatility ** 2) / 2) * self.time_to_maturity) / (self.volatility * sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * sqrt(self.time_to_maturity)
        return d1, d2
    
    def call_price(self):
        """Calculates the price of a call option"""
        d1, d2 = self.calculate_d1_d2()
        call_price = self.current_price * norm.cdf(d1) - self.strike * exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)
        return call_price
    
    def put_price(self):
        """Calculates the price of a put option"""
        d1, d2 = self.calculate_d1_d2()
        put_price = self.strike * exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - self.current_price * norm.cdf(-d1)
        return put_price
    
    def call_delta(self):
        """Calculates the delta of a call option"""
        d1, _ = self.calculate_d1_d2()
        call_delta = norm.cdf(d1)
        return call_delta
    
    def put_delta(self):
        """Calculates the delta of a put option"""
        d1, _ = self.calculate_d1_d2()
        put_delta = norm.cdf(d1) - 1
        return put_delta
    
    def call_put_gamma(self):
        """Calculates the gamma of a call or put option"""
        d1, _ = self.calculate_d1_d2()
        gamma = norm.pdf(d1) / (self.current_price * self.volatility * sqrt(self.time_to_maturity))
        return gamma
    
if __name__ == "__main__":
    time_to_maturity = 1
    strike = 100
    current_price = 100
    volatility = 0.2
    interest_rate = 0.05

    BS = BlackScholes(time_to_maturity = time_to_maturity, strike = strike, current_price = current_price, volatility = volatility, interest_rate = interest_rate)

