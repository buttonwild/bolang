from analysis.volatility_analyzer import VolatilityAnalyzer
from config.config import ONE_YEAR_AGO, THREE_YEARS_AGO, TRADING_PAIRS, START_DATE, END_DATE, SAVE_TO_EXCEL
import pandas as pd
from datetime import datetime

def main():
    analyzer = VolatilityAnalyzer()
    
    for symbol in TRADING_PAIRS:
        print(f"\n分析 {symbol} 的数据...")
        
        if START_DATE and END_DATE:
            print(f"\n{START_DATE} 到 {END_DATE} 的数据...")
            df = analyzer.get_historical_data(START_DATE, symbol, END_DATE)
            df = analyzer.calculate_daily_volatility(df)
            df = analyzer.calculate_amplitude(df)
            
            results_volatility = analyzer.analyze_volatility_distribution(df)
            results_amplitude = analyzer.analyze_amplitude_distribution(df)
            
            # 打印结果
            print("\n波动率分布:")
            print(results_volatility)
            print("\n振幅分布:")
            print(results_amplitude)
            
            if SAVE_TO_EXCEL:
                # 保存数据到Excel
                with pd.ExcelWriter(f'{symbol}_{START_DATE}_to_{END_DATE}.xlsx') as writer:
                    df.to_excel(writer, sheet_name='原始数据', index=False)
                    results_volatility.to_excel(writer, sheet_name='波动率分布', index=False)
                    results_amplitude.to_excel(writer, sheet_name='振幅分布', index=False)
                print(f"\n数据已保存到 {symbol}_{START_DATE}_to_{END_DATE}.xlsx")
        
        else:
            print("\n获取过去三年的数据...")
            df_three_years = analyzer.get_historical_data(THREE_YEARS_AGO, symbol)
            df_three_years = analyzer.calculate_daily_volatility(df_three_years)
            df_three_years = analyzer.calculate_amplitude(df_three_years)
            
            results_volatility_three_years = analyzer.analyze_volatility_distribution(df_three_years)
            results_amplitude_three_years = analyzer.analyze_amplitude_distribution(df_three_years)
            
            # 打印结果
            print("\n波动率分布:")
            print(results_volatility_three_years)
            print("\n振幅分布:")
            print(results_amplitude_three_years)
            
            if SAVE_TO_EXCEL:
                # 保存数据到Excel
                current_date = datetime.now().strftime('%Y-%m-%d')
                with pd.ExcelWriter(f'{symbol}_three_years_to_{current_date}.xlsx') as writer:
                    df_three_years.to_excel(writer, sheet_name='原始数据', index=False)
                    results_volatility_three_years.to_excel(writer, sheet_name='波动率分布', index=False)
                    results_amplitude_three_years.to_excel(writer, sheet_name='振幅分布', index=False)
                print(f"\n数据已保存到 {symbol}_three_years_to_{current_date}.xlsx")
        
        print("\n" + "="*50)  # 分隔线

if __name__ == "__main__":
    main()
