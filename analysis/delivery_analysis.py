from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

Path("output").mkdir(exist_ok=True)
df = pd.read_csv("data/delivery_orders.csv", parse_dates=["order_date"])

df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["on_time_flag"] = (df["delivery_status"] == "On Time").astype(int)

overall = {
    "orders": len(df),
    "on_time_rate": round(df["on_time_flag"].mean() * 100, 1),
    "average_delivery_days": round(df["actual_delivery_days"].mean(), 2),
    "average_delivery_cost_eur": round(df["delivery_cost_eur"].mean(), 2)
}
print("Overall KPIs:", overall)

carrier_kpis = df.groupby("carrier").agg(
    orders=("order_id", "count"),
    on_time_rate=("on_time_flag", "mean"),
    average_delivery_days=("actual_delivery_days", "mean"),
    average_cost=("delivery_cost_eur", "mean")
).reset_index()
carrier_kpis["on_time_rate"] = (carrier_kpis["on_time_rate"] * 100).round(1)
carrier_kpis = carrier_kpis.round({"average_delivery_days": 2, "average_cost": 2})
carrier_kpis.to_csv("output/carrier_kpis.csv", index=False)
print(carrier_kpis)

region_kpis = df.groupby("delivery_type").agg(
    orders=("order_id", "count"),
    on_time_rate=("on_time_flag", "mean"),
    average_delivery_days=("actual_delivery_days", "mean")
).reset_index()
region_kpis["on_time_rate"] = (region_kpis["on_time_rate"] * 100).round(1)
region_kpis = region_kpis.round({"average_delivery_days": 2})
region_kpis.to_csv("output/delivery_type_kpis.csv", index=False)
print(region_kpis)

monthly = df.groupby("month").agg(
    orders=("order_id", "count"),
    on_time_rate=("on_time_flag", "mean")
).reset_index()
monthly["on_time_rate"] = (monthly["on_time_rate"] * 100).round(1)
monthly.to_csv("output/monthly_kpis.csv", index=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
axes[0].bar(carrier_kpis["carrier"], carrier_kpis["on_time_rate"], color="#4C72B0")
axes[0].set_title("On-Time Delivery Rate by Carrier")
axes[0].set_ylabel("On-time rate (%)")
axes[0].tick_params(axis="x", rotation=30)

axes[1].bar(region_kpis["delivery_type"], region_kpis["on_time_rate"], color="#55A868")
axes[1].set_title("On-Time Delivery Rate: Urban vs Rural")
axes[1].set_ylabel("On-time rate (%)")

axes[2].plot(monthly["month"], monthly["on_time_rate"], marker="o", color="#C44E52")
axes[2].set_title("Monthly On-Time Delivery Rate")
axes[2].set_ylabel("On-time rate (%)")
axes[2].tick_params(axis="x", rotation=60)

plt.tight_layout()
plt.savefig("output/delivery_performance_dashboard.png", dpi=150)
print("Saved charts and KPI tables to output/.")
