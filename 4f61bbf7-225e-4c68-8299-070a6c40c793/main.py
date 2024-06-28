from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Define the asset(s) this strategy will apply to
        self.tickers = ["AAPL"]
        self.rsi_period = 14  # Typical period for RSI
        self.ema_period = 26  # A common period for EMA
    
    @property
    def assets(self):
        # List of assets the strategy uses
        return self.tickers
    
    @property
    def interval(self):
        # The time frame for data - using '1day' for daily analysis
        return "1day"
    
    def run(self, data):
        """
        This method implements the trading logic, returning a TargetAllocation 
        based on the current data for each ticker defined in self.tickers.
        """
        
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Ensure we have enough data points for calculating RSI and EMA
            if len(data["ohlcv"]) < max(self.rsi_period, self.ema_period):
                log("Not enough data to perform analysis.")
                return TargetAllocation({})
            
            rsi_values = RSI(ticker, data["ohlcv"], self.rsi_period)
            ema_values = EMA(ticker, data["ohlcv"], self.ema_period)
            
            # Check if the last RSI and EMA values satisfy our buy/sell conditions
            if rsi_values[-1] < 30 and data["ohlcv"][-1][ticker]["close"] > ema_values[-1]:
                # Buy condition: RSI below 30 and price above EMA indicates potential uptrend
                allocation_dict[ticker] = 1.0  # Assign full allocation to this asset
            elif rsi_values[-1] > 70 or data["ohlcv"][-1][ticker]["close"] < ema_values[-1]:
                # Sell condition: RSI above 70 or price below EMA indicates potential downtrend or overbought condition
                allocation_dict[ticker] = 0  # Do not allocate to this asset
            else:
                # Hold if conditions are not met
                allocation_dict[ticker] = 0  # Keep current allocation (could be adjusted for a more dynamic strategy)
        
        # Log for debugging or information purposes
        log(f"Allocations: {allocation_location_dict}")
        
        return TargetAllocation(allocation_dict)