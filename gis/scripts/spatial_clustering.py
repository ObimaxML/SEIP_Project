from pathlib import Path
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "gis" / "sample_data" / "job_seeker_points_sample.csv"
OUTPUT_PATH = PROJECT_ROOT / "gis" / "outputs" / "data" / "spatial_clusters.csv"

def main():
    df = pd.read_csv(INPUT_PATH)

    # Focus on unemployed job seekers for hotspot detection
    df["currently_employed_bool"] = df["currently_employed"].astype(str).str.lower().isin(["true", "1", "yes"])
    unemployed = df[df["currently_employed_bool"] == False].copy()

    coords = unemployed[["latitude", "longitude"]].values
    scaled = StandardScaler().fit_transform(coords)

    # DBSCAN finds dense clusters without requiring a fixed number of clusters.
    dbscan = DBSCAN(eps=0.75, min_samples=2)
    unemployed["dbscan_cluster"] = dbscan.fit_predict(scaled)

    # KMeans provides planned intervention zones.
    n_clusters = min(3, len(unemployed))
    if n_clusters >= 2:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        unemployed["intervention_zone"] = kmeans.fit_predict(scaled)
    else:
        unemployed["intervention_zone"] = 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    unemployed.to_csv(OUTPUT_PATH, index=False)

    print(f"Spatial clusters written to: {OUTPUT_PATH}")
    print(unemployed[["person_key", "township_code", "dbscan_cluster", "intervention_zone"]])

if __name__ == "__main__":
    main()
