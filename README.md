# Sprint 1 - Motor Digital Twin

Projeto acadêmico desenvolvido em Streamlit para a Sprint 1: **Fundamentos do Ativo e Interface de Cadastro**.

A aplicação organiza o cadastro técnico de motores/equipamentos, permite a consulta dos ativos registrados e apresenta uma visualização inicial de dados brutos simulados com conversão para unidades compreensíveis. A proposta é criar uma base simples, funcional e bem separada em camadas para evolução futura rumo a um Digital Twin com dados reais.

## Objetivo da Sprint

Desenvolver uma interface funcional para:

- Cadastrar tecnicamente motores e equipamentos.
- Consultar ativos cadastrados.
- Abrir uma ficha técnica organizada por equipamento.
- Simular dados brutos de sensores.
- Converter os dados simulados para temperatura, corrente e rotação em unidades compreensíveis.
- Preparar a estrutura para integração futura com IoT/MQTT, sem implementar MQTT real nesta Sprint.

## Tecnologias usadas

- Python
- Streamlit
- Pandas
- JSON para persistência local

## Requisitos atendidos

- Sidebar com menu principal.
- Dashboard com indicadores dos equipamentos cadastrados.
- Cadastro técnico de ativos.
- Validação de campos obrigatórios.
- Confirmação humana antes de salvar o cadastro.
- Bloqueio de TAG duplicada.
- Consulta de equipamentos em tabela.
- Ficha técnica organizada em blocos.
- Status com cor semântica.
- Visualização de dados brutos simulados.
- Tabela com valor bruto, fórmula/conversão aplicada e valor convertido.
- Métricas em cards para temperatura, corrente e rotação.
- Persistência local em `data/equipments.json`.
- Criação automática de dados iniciais de exemplo quando o JSON está vazio.
- Estrutura separada entre interface, serviços, repositório e modelo.

## Estrutura do projeto

```text
sprint1_motor_digital_twin/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── equipments.json
├── src/
│   ├── __init__.py
│   ├── models/
│   │   └── equipment.py
│   ├── services/
│   │   ├── equipment_service.py
│   │   └── sensor_service.py
│   ├── repositories/
│   │   └── equipment_repository.py
│   └── ui/
│       ├── components.py
│       └── pages.py
```

## Como instalar

```bash
cd sprint1_motor_digital_twin
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

No Linux/macOS, ative o ambiente com:

```bash
source .venv/bin/activate
```

## Como executar

```bash
streamlit run app.py
```

Depois de executar, acesse o endereço exibido pelo Streamlit no terminal, normalmente:

```text
http://localhost:8501
```

## Roteiro curto para vídeo de demonstração

1. Abrir o Dashboard.
2. Mostrar os equipamentos cadastrados.
3. Cadastrar um novo motor.
4. Consultar o motor na tabela.
5. Abrir a ficha técnica.
6. Acessar Dados Brutos e mostrar a conversão simulada.

## Próximos passos

- Integrar sensores com ESP32.
- Receber dados reais via MQTT.
- Criar histórico de sensores.
- Implementar alertas de anomalia.
- Evoluir para um Digital Twin com dados reais.
