from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class Equipment:
    tag: str
    modelo: str
    fabricante: str
    potencia: float
    unidade_potencia: str
    tensao: float
    corrente_nominal: float
    rotacao_nominal: float
    local_instalacao: str
    status_operacional: str
    observacoes: str
    data_cadastro: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Equipment":
        return cls(
            id=data.get("id", str(uuid4())),
            tag=str(data.get("tag", "")).strip().upper(),
            modelo=str(data.get("modelo", "")).strip(),
            fabricante=str(data.get("fabricante", "")).strip(),
            potencia=float(data.get("potencia", 0)),
            unidade_potencia=str(data.get("unidade_potencia", "kW")),
            tensao=float(data.get("tensao", 0)),
            corrente_nominal=float(data.get("corrente_nominal", 0)),
            rotacao_nominal=float(data.get("rotacao_nominal", 0)),
            local_instalacao=str(data.get("local_instalacao", "")).strip(),
            status_operacional=str(data.get("status_operacional", "Operacional")),
            observacoes=str(data.get("observacoes", "")).strip(),
            data_cadastro=str(data.get("data_cadastro", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
        )
