import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

FILE_CSV = "nhnl_history.csv"
FILE_PNG = "nhnl_chart.png"
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

def collect_and_plot():
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"📅 采集日期：{today}")

    # 1. 获取数据
    nh = ak.stock_rank_cxg_ths(symbol="一年新高")
    nl = ak.stock_rank_cxd_ths(symbol="一年新低")

    nh_cnt = len(nh)
    nl_cnt = len(nl)

    df = pd.DataFrame([{"date": today, "NH": nh_cnt, "NL": nl_cnt}])

    # 2. 保存/更新 CSV
    try:
        old = pd.read_csv(FILE_CSV)
        old["date"] = pd.to_datetime(old["date"])
        df["date"] = pd.to_datetime(df["date"])
        df = pd.concat([old, df]).drop_duplicates(subset="date")
    except FileNotFoundError:
        pass

    df.sort_values("date", inplace=True)
    df.to_csv(FILE_CSV, index=False)
    print(f"✅ 数据已保存：NH={nh_cnt}, NL={nl_cnt}")

    # 3. 绘制图表
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(df["date"], df["NH"], color="red", label="一年新高", alpha=0.7)
    ax.bar(df["date"], -df["NL"], color="green", label="一年新低", alpha=0.7)

    ax.axhline(0, color="black", linewidth=0.8)

    # 格式化日期
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    ax.set_title("A股 市场广度 (NH-NL)")
    ax.set_ylabel("股票数量")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FILE_PNG, dpi=150)
    plt.close()
    print("✅ 图表已生成")

if __name__ == "__main__":
    collect_and_plot()
