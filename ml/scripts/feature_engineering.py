import pandas as pd

def add_employment_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["age_band"] = pd.cut(
        df["age"],
        bins=[0, 24, 34, 44, 54, 64, 120],
        labels=["15-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        include_lowest=True
    )

    df["youth_flag"] = df["age"].between(15, 34)
    df["long_term_unemployed_flag"] = df["months_unemployed"].fillna(0) >= 12
    df["very_long_term_unemployed_flag"] = df["months_unemployed"].fillna(0) >= 24
    df["matric_or_higher_flag"] = df["nqf_level"].fillna(0) >= 4
    df["post_school_flag"] = df["nqf_level"].fillna(0) >= 5

    df["digital_access_score"] = (
        df["has_smartphone"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
        + df["digital_literacy_level"].astype(str).str.lower().map({
            "none": 0,
            "basic": 1,
            "intermediate": 2,
            "advanced": 3
        }).fillna(0)
    )

    df["mobility_score"] = (
        df["willing_to_relocate"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
        + df["transport_mode"].astype(str).str.lower().isin(["taxi", "bus", "train", "car"]).astype(int)
    )

    df["work_readiness_score"] = (
        df["matric_or_higher_flag"].astype(int)
        + df["post_school_flag"].astype(int)
        + (df["digital_access_score"] >= 2).astype(int)
        + (df["mobility_score"] >= 1).astype(int)
        + df["training_interest"].astype(str).str.lower().isin(["true", "1", "yes"]).astype(int)
    )

    return df
