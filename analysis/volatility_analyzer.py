from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from config.config import VOLATILITY_RANGES

class VolatilityAnalyzer:
    def __init__(self):
        self.client = Client(None, None)

    def get_historical_data(self, start_time, symbol, end_time=None):
        """获取历史K线数据"""
        klines = self.client.get_historical_klines(
            symbol,
            Client.KLINE_INTERVAL_1DAY,
            start_time,
            end_time
        )
        
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 
            'volume', 'close_time', 'quote_volume', 'trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
        
        return df

    def calculate_daily_volatility(self, df):
        """计算每日波动率"""
        df['daily_volatility'] = ((df['high'].astype(float) - df['low'].astype(float)) / 
                                 df['low'].astype(float) * 100)
        return df

    def analyze_volatility_distribution(self, df):
        """分析波动率分布"""
        results = []
        total_days = len(df)
        
        for low, high in VOLATILITY_RANGES:
            if high == float('inf'):
                count = len(df[df['daily_volatility'] >= low])
                range_str = f"{low}%+"
            else:
                count = len(df[(df['daily_volatility'] >= low) & 
                             (df['daily_volatility'] < high)])
                range_str = f"{low}%-{high}%"
                
            percentage = (count / total_days) * 100
            results.append({
                'range': range_str,
                'count': count,
                'percentage': round(percentage, 2)
            })
            
        return pd.DataFrame(results)

    def calculate_amplitude(self, df):
        """计算每日振幅
        振幅 = (最高价 - 最低价) / 开盘价 × 100%
        """
        df['amplitude'] = ((df['high'].astype(float) - df['low'].astype(float)) / 
                          df['open'].astype(float) * 100)
        return df

    def analyze_amplitude_distribution(self, df):
        """分析振幅分布"""
        results = []
        df = df.dropna(subset=['amplitude'])
        total_days = len(df)
        
        AMPLITUDE_RANGES = [
            (i, i + 1) for i in range(0, 10)
        ]
        AMPLITUDE_RANGES.append((10, float('inf')))
        
        for low, high in AMPLITUDE_RANGES:
            if high == float('inf'):
                count = len(df[df['amplitude'] >= low])
                range_str = f"{low}%+"
            else:
                count = len(df[(df['amplitude'] >= low) & 
                             (df['amplitude'] < high)])
                range_str = f"{low}%-{high}%"
                
            percentage = (count / total_days) * 100
            results.append({
                'range': range_str,
                'count': count,
                'percentage': round(percentage, 2)
            })
            
        return pd.DataFrame(results)
