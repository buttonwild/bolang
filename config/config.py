# 交易对设置
TRADING_PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "DOGEUSDT",
]

# 默认时间范围设置
ONE_YEAR_AGO = "1 year ago UTC"
THREE_YEARS_AGO = "3 years ago UTC"

# 可选的具体时间范围设置
#START_DATE = "2022-04-28"  # 例如 "2022-04-28"
#END_DATE = "2023-04-28"  # 例如 "2023-04-28"
START_DATE = ""
END_DATE = ""

# 波动率区间设置 - 每1%一个区间
VOLATILITY_RANGES = [
    (i, i + 1) for i in range(0, 10)  # 生成0-1%, 1-2%, ..., 9-10%的区间
]
VOLATILITY_RANGES.append((10, float('inf')))  # 添加10%以上的区间

# 数据保存设置
SAVE_TO_EXCEL = 0  # 设置为1时保存Excel文件，设置为0时只输出结果
