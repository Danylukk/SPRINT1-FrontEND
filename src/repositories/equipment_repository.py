import json
from pathlib import Path

from src.models.equipment import Equipment


class EquipmentRepository:
    def __init__(self, file_path: str | Path = "data/equipments.json") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def get_all(self) -> list[Equipment]:
        data = self._read_json()
        if not data:
            examples = self._default_examples()
            self.save_all(examples)
            return examples
        return [Equipment.from_dict(item) for item in data]

    def save_all(self, equipments: list[Equipment]) -> None:
        payload = [equipment.to_dict() for equipment in equipments]
        self.file_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add(self, equipment: Equipment) -> None:
        equipments = self.get_all()
        equipments.append(equipment)
        self.save_all(equipments)

    def find_by_tag(self, tag: str) -> Equipment | None:
        normalized_tag = tag.strip().upper()
        return next((item for item in self.get_all() if item.tag == normalized_tag), None)

    def _read_json(self) -> list[dict]:
        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def _default_examples() -> list[Equipment]:
        return [
            Equipment(
                tag="MTR-001",
                modelo="WEG W22 IR3",
                fabricante="WEG",
                potencia=15.0,
                unidade_potencia="CV",
                tensao=380.0,
                corrente_nominal=28.5,
                rotacao_nominal=1750.0,
                local_instalacao="Linha de Produção A",
                status_operacional="Operacional",
                observacoes="Motor principal da esteira de alimentação.",
            ),
            Equipment(
                tag="BMB-014",
                modelo="KSB MegaBloc",
                fabricante="KSB",
                potencia=7.5,
                unidade_potencia="kW",
                tensao=220.0,
                corrente_nominal=24.0,
                rotacao_nominal=3500.0,
                local_instalacao="Casa de Bombas",
                status_operacional="Atenção",
                observacoes="Monitorar temperatura em regime contínuo.",
            ),
            Equipment(
                tag="EXA-003",
                modelo="Siroco Industrial",
                fabricante="Ventisol",
                potencia=5.0,
                unidade_potencia="CV",
                tensao=380.0,
                corrente_nominal=9.7,
                rotacao_nominal=1720.0,
                local_instalacao="Exaustão Setor B",
                status_operacional="Inativo",
                observacoes="Aguardando inspeção de rolamentos.",
            ),
        ]
