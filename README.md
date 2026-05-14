# Sprint 2 - Motor Digital Twin

Projeto acadêmico em Streamlit para cadastro técnico e acompanhamento operacional simulado de motores. A Sprint 2 evolui a base da Sprint 1 sem refazê-la: mantém `data/equipments.json`, cadastro, consulta, ficha técnica e Dados Brutos, e adiciona um **Dashboard Operacional** com histórico local, alertas e gráficos temporais.

## Funcionalidades

- Dashboard geral dos ativos cadastrados.
- Cadastro técnico com validação de campos obrigatórios e bloqueio de TAG duplicada.
- Consulta de equipamentos e ficha técnica individual.
- Dados Brutos simulados, mantendo a camada antiga sem MQTT real.
- Dashboard Operacional por área/planta usando `local_instalacao`.
- Seleção de TAG filtrada pela área.
- Telemetria atual simulada por temperatura, vibração, corrente e rotação.
- Histórico em `data/telemetry_history.csv`.
- Gráficos interativos com Plotly.
- Alertas visuais por severidade.
- Placa simulada do motor com placeholder visual em HTML/CSS e card técnico dinâmico.

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly
- JSON para cadastro técnico local
- CSV para histórico de telemetria local

## Como executar

```bash
cd sprint1_motor_digital_twin
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

No Linux/macOS, ative o ambiente com:

```bash
source .venv/bin/activate
```

Depois de iniciar, acesse o endereço exibido pelo Streamlit, normalmente:

```text
http://localhost:8501
```

## Estrutura do projeto

```text
sprint1_motor_digital_twin/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── equipments.json
│   └── telemetry_history.csv
└── src/
    ├── models/
    │   └── equipment.py
    ├── repositories/
    │   ├── equipment_repository.py
    │   └── telemetry_repository.py
    ├── services/
    │   ├── alert_service.py
    │   ├── equipment_service.py
    │   ├── sensor_service.py
    │   └── telemetry_service.py
    └── ui/
        ├── components.py
        └── pages.py
```

## Dados simulados

Os equipamentos continuam persistidos em `data/equipments.json`. A Sprint 2 adiciona exemplos para áreas operacionais úteis:

- Linha de Produção A
- Linha de Produção B
- Utilidades
- Bombeamento

O histórico operacional é criado automaticamente em `data/telemetry_history.csv` com as colunas:

```text
timestamp, tag, temperatura_c, vibracao_mm_s, corrente_a, rotacao_rpm
```

Quando uma TAG ainda não tem histórico, o app gera pontos simulados iniciais. O botão **Gerar nova leitura simulada** acrescenta uma nova linha ao CSV para a TAG selecionada.

## Regras de alerta

- Temperatura: até 70 °C é saudável; até 85 °C é atenção; acima de 85 °C é crítico.
- Vibração: até 4,5 mm/s é saudável; até 7,0 mm/s é atenção; acima de 7,0 mm/s é crítico.
- Corrente: até 100% da corrente nominal é saudável; até 115% é atenção; acima de 115% é crítico.

A saúde geral do ativo é calculada pelo pior status entre temperatura, vibração e corrente.

## Placa simulada

A Sprint 2 exibe uma placa simulada do motor na seção **Placa do Motor** do Dashboard Operacional. Ela é um placeholder visual em HTML/CSS com aparência de placa industrial, exibindo TAG, modelo, fabricante, potência, tensão, corrente nominal e rotação nominal a partir do cadastro do ativo.

Essa placa representa visualmente a identificação do motor selecionado e reforça a rastreabilidade entre cadastro, localização e telemetria. O card técnico permanece abaixo da placa para deixar os dados legíveis e vinculados ao cadastro.

OCR e visão computacional real não foram implementados nesta Sprint. A interface apenas prepara o espaço visual para uma evolução futura com leitura real de imagens de placa.
