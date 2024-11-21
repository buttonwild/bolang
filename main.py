from analysis.volatility_analyzer import VolatilityAnalyzer
from config.config import ONE_YEAR_AGO, THREE_YEARS_AGO

def main():
    analyzer = VolatilityAnalyzer()
    
    # 分析一年数据
    print("分析过去一年的数据...")
    df_one_year = analyzer.get_historical_data(ONE_YEAR_AGO)
    df_one_year = analyzer.calculate_daily_volatility(df_one_year)
    results_one_year = analyzer.analyze_volatility_distribution(df_one_year)
    
    print("\n过去一年的波动率分布：")
    print(results_one_year.to_string(index=False))
    
    # 分析三年数据
    print("\n分析过去三年的数据...")
    df_three_years = analyzer.get_historical_data(THREE_YEARS_AGO)
    df_three_years = analyzer.calculate_daily_volatility(df_three_years)
    results_three_years = analyzer.analyze_volatility_distribution(df_three_years)
    
    print("\n过去三年的波动率分布：")
    print(results_three_years.to_string(index=False))

if __name__ == "__main__":
    main()
