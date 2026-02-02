# PRE PROCESSING

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Compute average energy consumption per plant
plant_avg = df.groupby("Plant")["Energy_Gcal_tcs"].mean().reset_index()

# Normalize the energy values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(plant_avg[["Energy_Gcal_tcs"]])

# Elbow Method to find the optimal number of clusters (k)
inertia = []
k_range = range(1, 7)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot the elbow curve
plt.figure(figsize=(6, 4))
plt.plot(k_range, inertia, marker='o')
plt.title("Elbow Method for Optimal k")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.grid(True)
plt.tight_layout()
plt.show()

# Final clustering with chosen k
optimal_k = 2
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
plant_avg["Cluster"] = kmeans.fit_predict(X_scaled)

# Show cluster assignments
print(plant_avg.sort_values("Cluster"))
