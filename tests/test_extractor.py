import pandas as pd
from src.extractors.excel_extractor import SurveyExtractor

def test_normalise_columns():
    extractor = SurveyExtractor([".csv"])
    df = pd.DataFrame(columns=["First Name", "Last-Name", " Township "])
    normalised = extractor.normalise_columns(df)
    assert list(normalised.columns) == ["first_name", "last_name", "township"]
