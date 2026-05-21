import akshare as ak
import pandas as pd
from datetime import datetime

FILE = "nhnl_history.csv"

def main():
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"📅 采集日期：{today}")

    nh = ak.stock_rank_cxg_ths(symbol="一年新高")
    nl = ak.stock_rank_cxd_ths(symbol="一年新低")

    nh_cnt = len(nh)
    nl_cnt = len(nl)

    # ✅ 只关心我们要的两列，不管 AKShare 返回多少列
    df = pd.DataFrame([{
        "date": today,
        "NH": nh_cnt,
        "NL": nl_cnt
    }])

    try:
        old = pd.read_csv(FILE)
        # ✅ 强制只保留我们需要的列
        old = old[["date", "NH", "NL"]]
        df = pd.concat([old, df]).drop_duplicates(subset="date")
    except FileNotFoundError:
        pass

    df.to_csv(FILE, index=False, encoding="utf-8-sig")
    print(f"✅ 已保存：NH={nh_cnt}, NL={nl_cnt}")

if __name__ == "__main__":
    main()
