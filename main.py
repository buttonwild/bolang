from analysis.volatility_analyzer import VolatilityAnalyzer
from config.config import ONE_YEAR_AGO, THREE_YEARS_AGO, TRADING_PAIRS

def main():
    analyzer = VolatilityAnalyzer()
    
    for symbol in TRADING_PAIRS:
        print(f"\n分析 {symbol} 的数据...")
        
        # 分析一年数据
        print("\n过去一年的数据...")
        df_one_year = analyzer.get_historical_data(ONE_YEAR_AGO, symbol)
        df_one_year = analyzer.calculate_daily_volatility(df_one_year)
        results_one_year = analyzer.analyze_volatility_distribution(df_one_year)
        
        print(f"\n{symbol} 过去一年的波动率分布：")
        print(results_one_year.to_string(index=False))
        
        # 分析三年数据
        print("\n过去三年的数据...")
        df_three_years = analyzer.get_historical_data(THREE_YEARS_AGO, symbol)
        df_three_years = analyzer.calculate_daily_volatility(df_three_years)
        results_three_years = analyzer.analyze_volatility_distribution(df_three_years)
        
        print(f"\n{symbol} 过去三年的波动率分布：")
        print(results_three_years.to_string(index=False))
        
        print("\n" + "="*50)  # 分隔线

if __name__ == "__main__":
    main()
