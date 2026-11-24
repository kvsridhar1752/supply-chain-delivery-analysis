import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

regions = ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"]
carriers = ["Carrier A", "Carrier B", "Carrier C", "Carrier D"]

n = 5000
order_dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 365, n), unit="D")

region = np.random.choice(regions, n, p=[0.25, 0.20, 0.20, 0.18, 0.17])
carrier = np.random.choice(carriers, n, p=[0.30, 0.28, 0.24, 0.18])
rural = np.random.choice([0, 1], n, p=[0.70, 0.30])

base_days = np.random.randint(2, 7, n)
delay_days = np.random.choice([0, 1, 2, 3], n, p=[0.76, 0.13, 0.07, 0.04])

# Make Carrier D and rural deliveries more likely to be delayed
delay_days = np.where(carrier == "Carrier D", delay_days + np.random.choice([0, 1], n, p=[0.60, 0.40]), delay_days)
delay_days = np.where(rural == 1, delay_days + np.random.choice([0, 1], n, p=[0.65, 0.35]), delay_days)

month = order_dates.dt.month
peak_delay = np.where(np.isin(month, [11, 12]), np.random.choice([0, 1], n, p=[0.65, 0.35]), 0)
delay_days = delay_days + peak_delay

actual_days = base_days + delay_days
planned_days = base_days
status = np.where(actual_days <= planned_days, "On Time", "Late")
cost = np.round(8 + actual_days * 1.8 + rural * 3.5 + np.random.normal(0, 1.5, n), 2)

df = pd.DataFrame({
    "order_id": [f"ORD{i:05d}" for i in range(1, n + 1)],
    "order_date": order_dates.strftime("%Y-%m-%d"),
    "carrier": carrier,
    "region": region,
    "delivery_type": np.where(rural == 1, "Rural", "Urban"),
    "planned_delivery_days": planned_days,
    "actual_delivery_days": actual_days,
    "delivery_cost_eur": cost,
    "delivery_status": status
})

Path("data").mkdir(exist_ok=True)
df.to_csv("data/delivery_orders.csv", index=False)
print(f"Created data/delivery_orders.csv with {len(df)} records.")
