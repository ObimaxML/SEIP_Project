from pathlib import Path
import pandas as pd
import math

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "gis" / "sample_data" / "job_seeker_points_sample.csv"
OUTPUT_PATH = PROJECT_ROOT / "gis" / "outputs" / "data" / "opportunity_access_scores.csv"

# Sample opportunity centres: replace later with real employer/training provider locations.
OPPORTUNITY_CENTRES = [
    {"centre_name": "Soweto Skills Hub", "centre_type": "Training", "latitude": -26.2360, "longitude": 27.9270},
    {"centre_name": "Alexandra Job Centre", "centre_type": "Placement", "latitude": -26.1050, "longitude": 28.1000},
    {"centre_name": "Tembisa ICT Hub", "centre_type": "Training", "latitude": -26.0070, "longitude": 28.2120},
]

def haversine_km(lat1, lon1, lat2, lon2):
    radius = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def main():
    df = pd.read_csv(INPUT_PATH)
    rows = []

    for _, seeker in df.iterrows():
        distances = []
        for centre in OPPORTUNITY_CENTRES:
            km = haversine_km(
                seeker["latitude"], seeker["longitude"],
                centre["latitude"], centre["longitude"]
            )
            distances.append({**centre, "distance_km": km})

        nearest = min(distances, key=lambda x: x["distance_km"])
        access_score = max(0, 100 - nearest["distance_km"] * 10)

        rows.append({
            "person_key": seeker["person_key"],
            "township_code": seeker["township_code"],
            "nearest_centre": nearest["centre_name"],
            "nearest_centre_type": nearest["centre_type"],
            "distance_km": round(nearest["distance_km"], 2),
            "opportunity_access_score": round(access_score, 2)
        })

    out = pd.DataFrame(rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"Opportunity access scores written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
