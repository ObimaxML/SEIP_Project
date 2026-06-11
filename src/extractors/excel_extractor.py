from pathlib import Path
import pandas as pd

class SurveyExtractor:
    def __init__(self, supported_extensions):
        self.supported_extensions = supported_extensions

    def normalise_columns(self, df):
        df = df.copy()
        df.columns = (
            df.columns.str.strip().str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
        )
        return df

    def read_file(self, file_path: Path):
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == ".xlsx":
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        df = self.normalise_columns(df)
        df["source_file_name"] = file_path.name
        return df

    def read_directory(self, directory: Path):
        frames = [
            self.read_file(p)
            for p in directory.iterdir()
            if p.suffix.lower() in self.supported_extensions
        ]
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)
