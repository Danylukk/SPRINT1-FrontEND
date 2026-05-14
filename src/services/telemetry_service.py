from datetime import datetime, timedelta
from random import Random

import pandas as pd

from src.models.equipment import Equipment
from src.repositories.telemetry_repository import TelemetryRepository


class TelemetryService:
    def __init__(self, repository: TelemetryRepository | None = None) -> None:
        self.repository = repository or TelemetryRepository()

    def ensure_history(self, equipments: list[Equipment]) -> pd.DataFrame:
        history = self.repository.read_history()
        existing_tags = set(history["tag"].dropna().astype(str)) if not history.empty else set()
        missing_equipments = [equipment for equipment in equipments if equipment.tag not in existing_tags]

        if missing_equipments:
            rows: list[dict] = []
            for equipment in missing_equipments:
                rows.extend(self._build_initial_rows(equipment))
            self.repository.append_rows(rows)
            history = self.repository.read_history()

        return history

    def get_history_for_tag(self, equipment: Equipment) -> pd.DataFrame:
        history = self.ensure_history([equipment])
        tag_history = history[history["tag"] == equipment.tag].copy()
        return tag_history.sort_values("timestamp")

    def get_current_reading(self, equipment: Equipment) -> dict:
        history = self.get_history_for_tag(equipment)
        if history.empty:
            row = self.generate_reading(equipment)
            self.repository.append_rows([row])
            return row

        latest = history.sort_values("timestamp").iloc[-1]
        return {
            "timestamp": latest["timestamp"],
            "tag": latest["tag"],
            "temperatura_c": float(latest["temperatura_c"]),
            "vibracao_mm_s": float(latest["vibracao_mm_s"]),
            "corrente_a": float(latest["corrente_a"]),
            "rotacao_rpm": float(latest["rotacao_rpm"]),
        }

    def append_current_snapshot(self, equipment: Equipment) -> dict:
        row = self.generate_reading(equipment)
        self.repository.append_rows([row])
        return row

    def prepare_chart_data(self, equipment: Equipment) -> pd.DataFrame:
        history = self.get_history_for_tag(equipment)
        return history.tail(48).copy()

    def generate_reading(self, equipment: Equipment, timestamp: datetime | None = None, step: int = 0) -> dict:
        reading_time = timestamp or datetime.now()
        rng = Random(f"{equipment.tag}-{reading_time:%Y%m%d%H%M}-{step}")
        profile = self._profile_for_equipment(equipment)
        load_wave = ((step % 12) - 6) / 6

        temperatura = profile["temperatura"] + load_wave * 2.8 + rng.uniform(-2.2, 2.2)
        vibracao = profile["vibracao"] + load_wave * 0.35 + rng.uniform(-0.35, 0.35)
        corrente = profile["corrente_factor"] * equipment.corrente_nominal + rng.uniform(
            -0.05, 0.05
        ) * max(equipment.corrente_nominal, 1)
        rotacao = equipment.rotacao_nominal * profile["rotacao_factor"] + rng.uniform(-18, 18)

        return {
            "timestamp": reading_time.replace(microsecond=0).isoformat(sep=" "),
            "tag": equipment.tag,
            "temperatura_c": round(max(20, temperatura), 1),
            "vibracao_mm_s": round(max(0.2, vibracao), 2),
            "corrente_a": round(max(0.1, corrente), 2),
            "rotacao_rpm": round(max(0, rotacao), 0),
        }

    def _build_initial_rows(self, equipment: Equipment, total_points: int = 48) -> list[dict]:
        start_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(
            hours=total_points - 1
        )
        return [
            self.generate_reading(equipment, timestamp=start_time + timedelta(hours=index), step=index)
            for index in range(total_points)
        ]

    @staticmethod
    def _profile_for_equipment(equipment: Equipment) -> dict[str, float]:
        status = equipment.status_operacional
        if status == "Atenção":
            return {
                "temperatura": 76.0,
                "vibracao": 5.6,
                "corrente_factor": 1.08,
                "rotacao_factor": 0.98,
            }
        if status in {"Crítico", "Inativo"}:
            return {
                "temperatura": 89.0,
                "vibracao": 7.4,
                "corrente_factor": 1.19,
                "rotacao_factor": 0.95,
            }
        return {
            "temperatura": 61.0,
            "vibracao": 3.2,
            "corrente_factor": 0.86,
            "rotacao_factor": 0.99,
        }
