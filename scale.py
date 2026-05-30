import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 起始日期
start_date = datetime(2026, 5, 18)
end_date   = datetime(2026, 5, 28)

funds_data = {'510050': [], '510300': [], '510500': [], '512100': [], '588000': [], '159915': []}
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    for fund, data in funds_data.items():
        try:
            df = ak.fund_etf_scale_sse(date=date_str)
            df =df[df['基金代码']==fund]  # 过滤出指定基金的行
            if not df.empty:
                df["统计日期"] = date_str  # 防止源数据没日期
                data.append(df)
                print(f"✅ 成功获取 {date_str}")
            else:
                df = ak.fund_etf_scale_szse(date=date_str)
                df =df[df['基金代码']==fund]  # 过滤出指定基金的行
        except Exception as e:
            print(f"❌ {date_str} 请求失败：{e}")

    current_date += timedelta(days=1)
# 合并所有日期的数据
for fund, data in funds_data.items():
    fund_etf_scale_sse_df = pd.concat(data, ignore_index=True)
    fund_etf_scale_sse_df.to_csv(f"D:\Python Project\stock\ETF scale\\funds_data\\fund_etf_scale_{fund}.csv", index=False)