from analysis.volatility_analyzer import VolatilityAnalyzer
from config.config import ONE_YEAR_AGO, THREE_YEARS_AGO, TRADING_PAIRS, START_DATE, END_DATE

def main():
    analyzer = VolatilityAnalyzer()
    
    for symbol in TRADING_PAIRS:
        print(f"\n分析 {symbol} 的数据...")
        
        if START_DATE and END_DATE:
            # 使用指定的时间范围
            print(f"\n{START_DATE} 到 {END_DATE} 的数据...")
            df = analyzer.get_historical_data(START_DATE, symbol, END_DATE)
            df = analyzer.calculate_daily_volatility(df)
            df = analyzer.calculate_amplitude(df)
            
            results_volatility = analyzer.analyze_volatility_distribution(df)
            results_amplitude = analyzer.analyze_amplitude_distribution(df)
            
            print(f"\n{symbol} 的波动率分布：")
            print(results_volatility.to_string(index=False))
            
            print(f"\n{symbol} 的振幅分布：")
            print(results_amplitude.to_string(index=False))
        
        else:
            # 使用默认的过去一年和三年的时间范围
            print("\n过去一年的数据...")
            df_one_year = analyzer.get_historical_data(ONE_YEAR_AGO, symbol)
            df_one_year = analyzer.calculate_daily_volatility(df_one_year)
            df_one_year = analyzer.calculate_amplitude(df_one_year)
            
            results_volatility_one_year = analyzer.analyze_volatility_distribution(df_one_year)
            results_amplitude_one_year = analyzer.analyze_amplitude_distribution(df_one_year)
            
            print(f"\n{symbol} 过去一年的波动率分布：")
            print(results_volatility_one_year.to_string(index=False))
            
            print(f"\n{symbol} 过去一年的振幅分布：")
            print(results_amplitude_one_year.to_string(index=False))
            
            print("\n过去三年的数据...")
            df_three_years = analyzer.get_historical_data(THREE_YEARS_AGO, symbol)
            df_three_years = analyzer.calculate_daily_volatility(df_three_years)
            df_three_years = analyzer.calculate_amplitude(df_three_years)
            
            results_volatility_three_years = analyzer.analyze_volatility_distribution(df_three_years)
            results_amplitude_three_years = analyzer.analyze_amplitude_distribution(df_three_years)
            
            print(f"\n{symbol} 过去三年的波动率分布：")
            print(results_volatility_three_years.to_string(index=False))
            
            print(f"\n{symbol} 过去三年的振幅分布：")
            print(results_amplitude_three_years.to_string(index=False))
        
        print("\n" + "="*50)  # 分隔线

if __name__ == "__main__":
    main()
