import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Load forecasts
cluster_0_forecast = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\cluster0_forecast.csv", index_col=0, parse_dates=True)
cluster_1_forecast = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\cluster1_forecast.csv", index_col=0, parse_dates=True)

# Ensure column names
cluster_0_forecast = cluster_0_forecast.iloc[:, 0]
cluster_1_forecast = cluster_1_forecast.iloc[:, 0]

cluster_0_forecast.name = "Cluster 0 (RSP + ISP)"
cluster_1_forecast.name = "Cluster 1 (BSP + DSP + BSL + SAIL)"

# Plot
plt.figure(figsize=(14, 5))
plt.plot(cluster_0_forecast.index, cluster_0_forecast.values, label=cluster_0_forecast.name, marker='o', linewidth=2)
plt.plot(cluster_1_forecast.index, cluster_1_forecast.values, label=cluster_1_forecast.name, marker='s', linestyle='--', linewidth=2)
plt.title("Forecast Comparison: Cluster 0 vs Cluster 1 (2025–2030)")
plt.xlabel("Year")
plt.ylabel("Energy Consumption (Gcal/tcs)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\comparison_plot.png")
plt.show()


print("""
🔍 Cluster Comparison: Cluster 0 vs Cluster 1

🏗️ Structural Overview:
- Cluster 0 comprises RSP and ISP — both modernized legacy plants with advanced technologies and relatively lower production volumes.
- Cluster 1 includes BSP, DSP, BSL, and the SAIL average — a more diverse and larger group of high-capacity, specialized production units.

🌱 Sustainability Performance:
- Cluster 0 (RSP + ISP):
  • RSP is a national leader in green innovations — pioneering biochar injection, zero liquid discharge systems, and large-scale afforestation.
  • ISP has achieved full slag reuse, dry gas cleaning, and modernization of emission controls.

- Cluster 1 (BSP + DSP + BSL):
  • BSP leads in circular economy with green tiles and floating solar.
  • DSP shows focused mill upgrades and pollution control.
  • BSL excels in energy reuse and slag-to-paver conversion.
  • However, sustainability efforts are more fragmented and less centralized across Cluster 1.

📊 Energy Consumption & Forecast:
- Cluster 0:
  • Shows a steeper and more consistent decline in energy consumption (Gcal/tcs).
  • Forecast suggests further gains due to strong sustainability momentum and fewer legacy bottlenecks.

- Cluster 1:
  • Decline in energy usage is more gradual.
  • Hybrid forecast projects modest improvement, but overall performance is stabilized by SAIL-wide efforts.

📈 Strategic Recommendations:
- Cluster 0:
  • Should scale its innovations (biochar, ZLD) to industrial scale.
  • Consider joint hydrogen-based pilot programs and shared renewable power infrastructure.

- Cluster 1:
  • Needs stronger cluster-level integration of sustainability data and planning.
  • Should prioritize centralized AI energy dashboards, bulk floating solar deployments, and internal carbon pricing trials.

🔚 Summary:
Cluster 0 is currently ahead in innovation and energy performance, while Cluster 1 holds higher production capacity and untapped sustainability potential. Strategic alignment could yield transformative results across SAIL.
""")
