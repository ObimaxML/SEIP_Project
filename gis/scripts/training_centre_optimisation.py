from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "gis" / "sample_data" / "job_seeker_points_sample.csv"
OUTPUT_PATH = PROJECT_ROOT / "gis" / "outputs" / "data" / "recommended_training_centres.csv"

def main():
    df = pd.read_csv(INPUT_PATH)
    df["currently_employed_bool"] = df["currently_employed"].astype(str).str.lower().isin(["true", "1", "yes"])
    df["training_interest_bool"] = df["training_interest"].astype(str).str.lower().isin(["true", "1", "yes"])

    demand = df[
        (df["currently_employed_bool"] == False)
        & (df["training_interest_bool"] == True)
    ].copy()

    if len(demand) < 2:
        raise ValueError("Not enough demand points to recommend centres.")

    n_centres = min(3, len(demand))
    kmeans = KMeans(n_clusters=n_centres, random_state=42, n_init=10)
    demand["recommended_centre_id"] = kmeans.fit_predict(demand[["latitude", "longitude"]])

    centres = pd.DataFrame(kmeans.cluster_centers_, columns=["recommended_latitude", "recommended_longitude"])
    centres["recommended_centre_id"] = centres.index

    demand_summary = (
        demand.groupby("recommended_centre_id")
        .agg(
            demand_count=("person_key", "count"),
            top_township=("township_code", lambda x: x.mode().iloc[0]),
            top_training_area=("preferred_training_area", lambda x: x.mode().iloc[0])
        )
        .reset_index()
    )

    output = centres.merge(demand_summary, on="recommended_centre_id")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_PATH, index=False)

    print(f"Recommended training centres written to: {OUTPUT_PATH}")
    print(output)

if __name__ == "__main__":
    main()
