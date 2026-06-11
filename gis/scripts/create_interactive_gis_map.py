from pathlib import Path
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster

PROJECT_ROOT = Path(__file__).resolve().parents[2]
POINTS_PATH = PROJECT_ROOT / "gis" / "sample_data" / "job_seeker_points_sample.csv"
CLUSTERS_PATH = PROJECT_ROOT / "gis" / "outputs" / "data" / "spatial_clusters.csv"
CENTRES_PATH = PROJECT_ROOT / "gis" / "outputs" / "data" / "recommended_training_centres.csv"
OUTPUT_PATH = PROJECT_ROOT / "gis" / "outputs" / "maps" / "seip_interactive_spatial_intelligence_map.html"

def main():
    df = pd.read_csv(POINTS_PATH)
    m = folium.Map(location=[-26.20, 28.03], zoom_start=10, tiles="OpenStreetMap")

    unemployed = df[df["currently_employed"].astype(str).str.lower().isin(["false", "0", "no"])]
    heat_data = unemployed[["latitude", "longitude"]].dropna().values.tolist()
    HeatMap(heat_data, name="Unemployment Heatmap", radius=22, blur=14).add_to(m)

    marker_cluster = MarkerCluster(name="Job Seeker Points").add_to(m)
    for _, row in df.iterrows():
        employed = str(row["currently_employed"]).lower() in ["true", "1", "yes"]
        colour = "green" if employed else "red"
        popup = f"""
        <b>Township:</b> {row['township_code']}<br>
        <b>Ward:</b> {row['ward_number']}<br>
        <b>Age:</b> {row['age']}<br>
        <b>Employed:</b> {row['currently_employed']}<br>
        <b>Training Interest:</b> {row['training_interest']}<br>
        <b>Preferred Training:</b> {row['preferred_training_area']}
        """
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            popup=folium.Popup(popup, max_width=300),
            color=colour,
            fill=True,
            fill_opacity=0.75
        ).add_to(marker_cluster)

    if CENTRES_PATH.exists():
        centres = pd.read_csv(CENTRES_PATH)
        for _, c in centres.iterrows():
            popup = f"""
            <b>Recommended Training Centre</b><br>
            <b>Centre ID:</b> {c['recommended_centre_id']}<br>
            <b>Demand Count:</b> {c['demand_count']}<br>
            <b>Top Township:</b> {c['top_township']}<br>
            <b>Top Training Area:</b> {c['top_training_area']}
            """
            folium.Marker(
                location=[c["recommended_latitude"], c["recommended_longitude"]],
                popup=folium.Popup(popup, max_width=300),
                icon=folium.Icon(color="blue", icon="education", prefix="fa")
            ).add_to(m)

    folium.LayerControl().add_to(m)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    m.save(OUTPUT_PATH)

    print(f"Interactive GIS map created: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
