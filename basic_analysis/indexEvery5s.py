import requests
import datetime
import pandas as pd
import io

date = datetime.date(2024,6,26)
datestr = date.strftime("%Y%m%d")

# receieve data
res = requests.get("https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_INDEX?date=20240626&response=csv&date="+datestr+"&_=1719389447327")
#res.text[:1000]

# Organize data into dataframe using pandas, and delete unecessary row, column
df = pd.read_csv(io.StringIO(res.text.replace("=", "")), header=1, index_col='時間')
df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

# Change the original time(string) to a time that the computer can understand
df.index = pd.to_datetime(datestr + ' ' + df.index)

# all data types transfrom to FLOAT
df = df.applymap(lambda s: float(str(s).replace("," , "")))
