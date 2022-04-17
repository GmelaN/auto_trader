import numpy as np
import pandas as pd
import FinanceDataReader as fdr

# fetch BNK by day
data = fdr.DataReader("138930", "2020-01-01")
with open("BNK_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)

# fetch S&P500 by day
data = fdr.DataReader("US500", "2020-01-01")
with open("SP500_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)

# fetvh USD-KRW by day
data = fdr.DataReader("USD/KRW", "2020-01-01")
with open("USD-KRW_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)


