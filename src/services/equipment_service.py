from src.models.equipment import Equipment
from src.repositories.equipment_repository import EquipmentRepository


class EquipmentValidationError(ValueError):
    pass


class EquipmentService:
    REQUIRED_TEXT_FIELDS = {
        "tag": "TAG de identificação",
        "modelo": "Modelo",
        "fabricante": "Fabricante",
        "local_instalacao": "Local de instalação",
        "status_operacional": "Status operacional",
    }

    def __init__(self, repository: EquipmentRepository | None = None) -> None:
        self.repository = repository or EquipmentRepository()

    def list_equipments(self) -> list[Equipment]:
        return self.repository.get_all()

    def get_by_tag(self, tag: str) -> Equipment | None:
        if not tag:
            return None
        return self.repository.find_by_tag(tag)

    def create_equipment(self, payload: dict, confirm_save: bool = False) -> Equipment:
        if not confirm_save:
            raise EquipmentValidationError("Confirme a gravação antes de salvar o cadastro.")

        normalized_payload = self._normalize_payload(payload)
        self._validate_required_fields(normalized_payload)
        self._validate_numeric_fields(normalized_payload)
        self._validate_unique_tag(normalized_payload["tag"])

        equipment = Equipment(**normalized_payload)
        self.repository.add(equipment)
        return equipment

    def _normalize_payload(self, payload: dict) -> dict:
        return {
            "tag": str(payload.get("tag", "")).strip().upper(),
            "modelo": str(payload.get("modelo", "")).strip(),
            "fabricante": str(payload.get("fabricante", "")).strip(),
            "potencia": float(payload.get("potencia") or 0),
            "unidade_potencia": str(payload.get("unidade_potencia", "kW")).strip(),
            "tensao": float(payload.get("tensao") or 0),
            "corrente_nominal": float(payload.get("corrente_nominal") or 0),
            "rotacao_nominal": float(payload.get("rotacao_nominal") or 0),
            "local_instalacao": str(payload.get("local_instalacao", "")).strip(),
            "status_operacional": str(payload.get("status_operacional", "")).strip(),
            "observacoes": str(payload.get("observacoes", "")).strip(),
        }

    def _validate_required_fields(self, payload: dict) -> None:
        missing_fields = [
            label for field, label in self.REQUIRED_TEXT_FIELDS.items() if not payload.get(field)
        ]
        if not payload.get("observacoes"):
            missing_fields.append("Observações")
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise EquipmentValidationError(f"Preencha os campos obrigatórios: {fields}.")

    @staticmethod
    def _validate_numeric_fields(payload: dict) -> None:
        numeric_labels = {
            "potencia": "Potência",
            "tensao": "Tensão",
            "corrente_nominal": "Corrente nominal",
            "rotacao_nominal": "Rotação nominal",
        }
        invalid = [label for field, label in numeric_labels.items() if payload.get(field, 0) <= 0]
        if invalid:
            raise EquipmentValidationError(
                f"Informe valores maiores que zero para: {', '.join(invalid)}."
            )

    def _validate_unique_tag(self, tag: str) -> None:
        if self.repository.find_by_tag(tag):
            raise EquipmentValidationError(f"A TAG {tag} já está cadastrada.")
