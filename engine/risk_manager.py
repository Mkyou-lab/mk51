import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd

class RiskManager:
    def __init__(self):
        self.daily_loss = 0
        self.max_daily_loss = 3.0      # %
        self.max_drawdown = 6.0        # %
        self.max_open_trades = 3
        self.max_trades_per_day = 10
        self.max_consecutive_losses = 3
        self.max_spread = 30
        self.trades_today = 0
        self.consecutive_losses = 0
        self.start_balance = 0
        self.last_equity = 0

    def update_account_info(self):
        info = mt5.account_info()
        self.last_equity = info.equity
        if self.start_balance == 0:
            self.start_balance = info.balance

    def can_trade(self) -> bool:
        self.update_account_info()
        drawdown = (self.start_balance - self.last_equity) / self.start_balance * 100
        if drawdown > self.max_drawdown:
            print("🚨 MAX DRAWDOWN REACHED - ENGINE STOPPED")
            return False
        if self.daily_loss > self.max_daily_loss:
            print("🚨 DAILY LOSS LIMIT REACHED")
            return False
        if self.trades_today >= self.max_trades_per_day:
            return False
        if self.consecutive_losses >= self.max_consecutive_losses:
            return False
        return True

    def calculate_lot_size(self, signal, risk_percent: float = 1.0) -> float:
        account = mt5.account_info()
        sl_distance = abs(signal.entry - signal.sl) / mt5.symbol_info(signal.symbol).point
        if sl_distance == 0: return 0.01

        risk_amount = account.balance * (risk_percent / 100)
        tick_value = mt5.symbol_info(signal.symbol).trade_tick_value
        lot = risk_amount / (sl_distance * tick_value)
        
        # Broker limits
        symbol_info = mt5.symbol_info(signal.symbol)
        lot = max(symbol_info.volume_min, min(symbol_info.volume_max, round(lot / symbol_info.volume_step) * symbol_info.volume_step))
        return lot