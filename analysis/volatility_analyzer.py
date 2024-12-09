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
        """计算日内波动"""
        df['date'] = df['timestamp'].dt.date
        df['price_change'] = df['close'].astype(float).diff()
        df['price_change_pct'] = df['price_change'] / df['close'].shift(1) * 100
        
        def analyze_price_movements(group):
            # 计算价格变动
            changes = group['price_change_pct']
            
            # 统计上涨和下跌次数
            up_moves = changes[changes > 0]
            down_moves = changes[changes < 0]
            
            return pd.Series({
                'positive_moves': up_moves.sum(),  # 上涨累计幅度
                'negative_moves': abs(down_moves.sum()),  # 下跌累计幅度
                'total_volatility': up_moves.sum() + abs(down_moves.sum()),  # 总波动
                'up_count': len(up_moves),  # 上涨次数
                'down_count': len(down_moves),  # 下跌次数
                'max_up': up_moves.max() if len(up_moves) > 0 else 0,  # 最大单次上涨
                'max_down': abs(down_moves.min()) if len(down_moves) > 0 else 0,  # 最大单次下跌
                'avg_up': up_moves.mean() if len(up_moves) > 0 else 0,  # 平均上涨幅度
                'avg_down': abs(down_moves.mean()) if len(down_moves) > 0 else 0  # 平均下跌幅度
            })
        
        # 创建一个新的DataFrame来存储统计结果
        stats_df = df.groupby('date').apply(analyze_price_movements)
        
        # 将统计结果合并回原始数据框
        df = df.join(stats_df, on='date')
        
        return df  # 返回包含原始数据和统计结果的完整数据框

    def analyze_volatility_distribution(self, df):
        """分析日内波动分布"""
        results = []
        total_days = len(df['date'].unique())  # 修改为使用唯一日期计数
        
        for low, high in VOLATILITY_RANGES:
            mask = (df['total_volatility'] >= low) & \
                   (df['total_volatility'] < high if high != float('inf') else True)
            
            period_stats = df[mask]
            count = len(period_stats['date'].unique())  # 修改为使用唯一日期计数
            
            if high == float('inf'):
                range_str = f"{low}%+"
            else:
                range_str = f"{low}%-{high}%"
            
            results.append({
                'range': range_str,
                'count': count,
                'percentage': round((count / total_days) * 100, 2),
                'avg_total_volatility': round(period_stats['total_volatility'].mean(), 2),
                'avg_up_moves': round(period_stats['up_count'].mean(), 1),  # 平均上涨次数
                'avg_down_moves': round(period_stats['down_count'].mean(), 1),  # 平均下跌次数
                'avg_up_pct': round(period_stats['avg_up'].mean(), 2),  # 平均单次上涨幅度
                'avg_down_pct': round(period_stats['avg_down'].mean(), 2),  # 平均单次下跌幅度
                'max_single_up': round(period_stats['max_up'].max(), 2),  # 最大单次上涨
                'max_single_down': round(period_stats['max_down'].max(), 2)  # 最大单次下跌
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
