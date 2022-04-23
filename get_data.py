import numpy as np
import pandas as pd
import FinanceDataReader as fdr
import get_data_from_korea_bank as kbank

# fetch BNK by day
data = fdr.DataReader("138930", "2020-01-01")
with open("BNK_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)

# fetch S&P500 by day
data = fdr.DataReader("US500", "2020-01-01")
with open("SP500_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)

# fetch USD-KRW by day
data = fdr.DataReader("USD/KRW", "2020-01-01")
with open("USD-KRW_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)

# fetch VIX by day
data = fdr.DataReader("VIXCLS", "2020-01-01")
with open("VIX_by_day.csv", 'w', encoding="UTF8") as f:
    data.to_csv(f)

# fetch data from kbank by day
# data = kbank.fetch_data()
# with open("kbank_by_day.csv", 'w', encoding="UTF8") as f:
#     to_csv(f)
