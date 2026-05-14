from pathlib import Path

import pandas as pd


class TelemetryRepository:
    COLUMNS = [
        "timestamp",
        "tag",
        "temperatura_c",
        "vibracao_mm_s",
        "corrente_a",
        "rotacao_rpm",
    ]

    def __init__(self, file_path: str | Path = "data/telemetry_history.csv") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.save_history(pd.DataFrame(columns=self.COLUMNS))

    def read_history(self) -> pd.DataFrame:
        try:
            history = pd.read_csv(self.file_path)
        except (pd.errors.EmptyDataError, OSError):
            history = pd.DataFrame(columns=self.COLUMNS)

        for column in self.COLUMNS:
            if column not in history.columns:
                history[column] = pd.NA

        history = history[self.COLUMNS].copy()
        history["timestamp"] = pd.to_datetime(history["timestamp"], errors="coerce")
        numeric_columns = ["temperatura_c", "vibracao_mm_s", "corrente_a", "rotacao_rpm"]
        for column in numeric_columns:
            history[column] = pd.to_numeric(history[column], errors="coerce")

        return history.dropna(subset=["timestamp", "tag"])

    def save_history(self, history: pd.DataFrame) -> None:
        normalized = history.reindex(columns=self.COLUMNS)
        normalized.to_csv(self.file_path, index=False)

    def append_rows(self, rows: list[dict]) -> None:
        if not rows:
            return
        history = self.read_history()
        updated = pd.concat([history, pd.DataFrame(rows)], ignore_index=True)
        self.save_history(updated)
