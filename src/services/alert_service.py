from dataclasses import dataclass


STATUS_HEALTHY = "Saudável"
STATUS_WARNING = "Atenção"
STATUS_CRITICAL = "Crítico"


@dataclass(frozen=True)
class AlertResult:
    status: str
    message: str


class AlertService:
    STATUS_ORDER = {
        STATUS_HEALTHY: 0,
        STATUS_WARNING: 1,
        STATUS_CRITICAL: 2,
    }

    def evaluate_temperature(self, temperatura_c: float) -> AlertResult:
        if temperatura_c <= 70:
            return AlertResult(STATUS_HEALTHY, "Temperatura dentro da faixa saudável.")
        if temperatura_c <= 85:
            return AlertResult(STATUS_WARNING, "Temperatura em atenção. Acompanhar tendência.")
        return AlertResult(STATUS_CRITICAL, "Temperatura crítica. Recomenda-se inspeção.")

    def evaluate_vibration(self, vibracao_mm_s: float) -> AlertResult:
        if vibracao_mm_s <= 4.5:
            return AlertResult(STATUS_HEALTHY, "Vibração dentro da faixa saudável.")
        if vibracao_mm_s <= 7.0:
            return AlertResult(STATUS_WARNING, "Vibração em atenção. Verificar rolamentos e fixação.")
        return AlertResult(STATUS_CRITICAL, "Vibração crítica. Priorizar análise mecânica.")

    def evaluate_current(self, corrente_a: float, corrente_nominal: float) -> AlertResult:
        if corrente_nominal <= 0:
            return AlertResult(STATUS_WARNING, "Corrente nominal não cadastrada para comparação.")

        percentual = (corrente_a / corrente_nominal) * 100
        if percentual <= 100:
            return AlertResult(STATUS_HEALTHY, "Corrente dentro da faixa nominal.")
        if percentual <= 115:
            return AlertResult(STATUS_WARNING, "Corrente acima do nominal. Acompanhar carga.")
        return AlertResult(STATUS_CRITICAL, "Corrente crítica. Verificar sobrecarga.")

    def evaluate_all(self, reading: dict, corrente_nominal: float) -> dict[str, AlertResult | str]:
        temperature = self.evaluate_temperature(float(reading["temperatura_c"]))
        vibration = self.evaluate_vibration(float(reading["vibracao_mm_s"]))
        current = self.evaluate_current(float(reading["corrente_a"]), corrente_nominal)
        overall = max(
            [temperature.status, vibration.status, current.status],
            key=lambda status: self.STATUS_ORDER[status],
        )

        return {
            "temperatura": temperature,
            "vibracao": vibration,
            "corrente": current,
            "geral": overall,
        }
