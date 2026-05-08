from random import randint

from src.models.equipment import Equipment


def simulate_raw_sensor_data(equipment: Equipment) -> dict[str, int]:
    load_factor = 1.0
    if equipment.status_operacional == "Atenção":
        load_factor = 1.12
    elif equipment.status_operacional in {"Crítico", "Inativo"}:
        load_factor = 1.25

    return {
        "temperatura_raw": randint(420, 780),
        "corrente_raw": int(randint(300, 900) * load_factor),
        "rotacao_raw": int(randint(600, 970) * load_factor),
    }


def convert_raw_sensor_data(raw_data: dict[str, int], equipment: Equipment) -> dict[str, float]:
    temperatura_c = (raw_data["temperatura_raw"] / 1023) * 120
    corrente_a = (raw_data["corrente_raw"] / 1023) * (equipment.corrente_nominal * 1.5)
    rotacao_rpm = (raw_data["rotacao_raw"] / 1023) * (equipment.rotacao_nominal * 1.15)

    return {
        "temperatura_c": round(temperatura_c, 1),
        "corrente_a": round(corrente_a, 2),
        "rotacao_rpm": round(rotacao_rpm, 0),
    }


def build_sensor_table(raw_data: dict[str, int], converted_data: dict[str, float]) -> list[dict[str, str]]:
    return [
        {
            "Nome do sensor": "Temperatura",
            "Valor bruto": str(raw_data["temperatura_raw"]),
            "Fórmula/conversão aplicada": "raw / 1023 * 120",
            "Valor convertido": f"{converted_data['temperatura_c']} °C",
        },
        {
            "Nome do sensor": "Corrente",
            "Valor bruto": str(raw_data["corrente_raw"]),
            "Fórmula/conversão aplicada": "raw / 1023 * corrente nominal * 1,5",
            "Valor convertido": f"{converted_data['corrente_a']} A",
        },
        {
            "Nome do sensor": "Rotação",
            "Valor bruto": str(raw_data["rotacao_raw"]),
            "Fórmula/conversão aplicada": "raw / 1023 * rotação nominal * 1,15",
            "Valor convertido": f"{converted_data['rotacao_rpm']:.0f} RPM",
        },
    ]
