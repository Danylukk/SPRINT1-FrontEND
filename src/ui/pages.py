import time

import pandas as pd
import streamlit as st

from src.models.equipment import Equipment
from src.services.equipment_service import EquipmentService, EquipmentValidationError
from src.services.sensor_service import (
    build_sensor_table,
    convert_raw_sensor_data,
    simulate_raw_sensor_data,
)
from src.ui.components import (
    equipment_to_dataframe,
    inject_global_styles,
    render_empty_state,
    render_equipment_card,
    status_badge,
    status_badge_html,
)


MENU_OPTIONS = [
    "Dashboard",
    "Cadastro Técnico",
    "Consulta de Equipamentos",
    "Dados Brutos",
    "Sobre o Projeto",
]


def render_app() -> None:
    inject_global_styles()
    service = EquipmentService()

    with st.sidebar:
        st.title("Motor Digital Twin")
        st.caption("Sprint 1 | Cadastro e leitura simulada")
        selected_page = st.radio("Menu principal", MENU_OPTIONS)
        st.divider()
        st.caption("Persistência local em JSON")

    if selected_page == "Dashboard":
        render_dashboard(service)
    elif selected_page == "Cadastro Técnico":
        render_registration_page(service)
    elif selected_page == "Consulta de Equipamentos":
        render_equipment_query_page(service)
    elif selected_page == "Dados Brutos":
        render_raw_data_page(service)
    else:
        render_about_page()


def render_dashboard(service: EquipmentService) -> None:
    st.title("Dashboard")
    st.write("Visão geral dos ativos cadastrados para a Sprint 1.")

    with st.spinner("Carregando indicadores dos equipamentos..."):
        time.sleep(0.3)
        equipments = service.list_equipments()

    total = len(equipments)
    operational = sum(1 for item in equipments if item.status_operacional == "Operacional")
    attention = sum(1 for item in equipments if item.status_operacional == "Atenção")
    critical = sum(1 for item in equipments if item.status_operacional in {"Crítico", "Inativo"})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ativos cadastrados", total)
    col2.metric("Operacionais", operational)
    col3.metric("Em atenção", attention)
    col4.metric("Críticos/Inativos", critical)

    st.divider()
    st.subheader("Equipamentos recentes")
    if equipments:
        st.dataframe(equipment_to_dataframe(equipments), use_container_width=True, hide_index=True)
    else:
        render_empty_state("Nenhum equipamento cadastrado.")


def render_registration_page(service: EquipmentService) -> None:
    st.title("Cadastro Técnico")
    st.write("Cadastre motores e equipamentos com os dados necessários para consulta técnica.")
    st.caption("Os campos com * são obrigatórios. A gravação exige confirmação humana antes do salvamento.")

    if "equipment_form_version" not in st.session_state:
        st.session_state.equipment_form_version = 0

    def form_key(field_name: str) -> str:
        return f"equipment_{field_name}_{st.session_state.equipment_form_version}"

    with st.form("equipment_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            tag = st.text_input("TAG de identificação *", placeholder="Ex.: MTR-001", key=form_key("tag"))
            modelo = st.text_input("Modelo *", placeholder="Ex.: W22 IR3", key=form_key("modelo"))
            fabricante = st.text_input("Fabricante *", placeholder="Ex.: WEG", key=form_key("fabricante"))
            potencia = st.number_input(
                "Potência *", min_value=0.0, step=0.5, format="%.2f", key=form_key("potencia")
            )
            unidade_potencia = st.selectbox(
                "Unidade da potência *", ["kW", "CV"], key=form_key("unidade_potencia")
            )
        with col2:
            tensao = st.number_input(
                "Tensão em V *", min_value=0.0, step=10.0, format="%.2f", key=form_key("tensao")
            )
            corrente = st.number_input(
                "Corrente nominal em A *",
                min_value=0.0,
                step=0.5,
                format="%.2f",
                key=form_key("corrente"),
            )
            rotacao = st.number_input(
                "Rotação nominal em RPM *",
                min_value=0.0,
                step=50.0,
                format="%.2f",
                key=form_key("rotacao"),
            )
            local = st.text_input(
                "Local de instalação *", placeholder="Ex.: Linha de Produção A", key=form_key("local")
            )
            status = st.selectbox(
                "Status operacional *",
                ["Operacional", "Atenção", "Crítico", "Inativo"],
                key=form_key("status"),
            )

        observacoes = st.text_area(
            "Observações *",
            placeholder="Registre detalhes técnicos relevantes.",
            key=form_key("observacoes"),
        )
        confirm_save = st.checkbox(
            "Confirmo que revisei os dados e desejo salvar este cadastro.",
            key=form_key("confirm_save"),
        )

        submitted = st.form_submit_button("Salvar equipamento", type="primary", use_container_width=True)

    if submitted:
        payload = {
            "tag": tag,
            "modelo": modelo,
            "fabricante": fabricante,
            "potencia": potencia,
            "unidade_potencia": unidade_potencia,
            "tensao": tensao,
            "corrente_nominal": corrente,
            "rotacao_nominal": rotacao,
            "local_instalacao": local,
            "status_operacional": status,
            "observacoes": observacoes,
        }
        with st.spinner("Validando e salvando equipamento..."):
            time.sleep(0.3)
            try:
                equipment = service.create_equipment(payload, confirm_save=confirm_save)
            except EquipmentValidationError as error:
                st.error(str(error))
            else:
                st.success(f"Equipamento {equipment.tag} cadastrado com sucesso.")
                st.info("O cadastro já está disponível na consulta e nos dados brutos simulados.")

    with st.expander("Limpeza do formulário"):
        st.warning("Para evitar perda acidental de informações digitadas, confirme antes de limpar.")
        confirm_clear = st.checkbox("Confirmo que desejo limpar os dados preenchidos.", key="confirm_clear")
        if st.button("Limpar tela de cadastro", disabled=not confirm_clear):
            st.session_state.equipment_form_version += 1
            st.rerun()


def render_equipment_query_page(service: EquipmentService) -> None:
    st.title("Consulta de Equipamentos")
    st.write("Consulte os ativos cadastrados e abra a ficha técnica individual.")

    with st.spinner("Consultando arquivo local de equipamentos..."):
        time.sleep(0.3)
        equipments = service.list_equipments()

    if not equipments:
        render_empty_state("Nenhum equipamento cadastrado.")
        return

    df = equipment_to_dataframe(equipments)
    st.dataframe(df, use_container_width=True, hide_index=True)

    selected_tag = st.selectbox("Selecione um equipamento para abrir a ficha técnica", df["TAG"].tolist())
    selected_equipment = service.get_by_tag(selected_tag)

    if selected_equipment:
        st.divider()
        render_technical_sheet(selected_equipment)


def render_technical_sheet(equipment: Equipment) -> None:
    st.subheader("Ficha técnica")
    render_equipment_card(equipment)

    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="info-section">
                <h4>Identificação</h4>
                <p><strong>TAG:</strong> {equipment.tag}</p>
                <p><strong>Modelo:</strong> {equipment.modelo}</p>
                <p><strong>Fabricante:</strong> {equipment.fabricante}</p>
                <p><strong>Cadastro:</strong> {equipment.data_cadastro}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-section">
                <h4>Especificações</h4>
                <p><strong>Potência:</strong> {equipment.potencia:g} {equipment.unidade_potencia}</p>
                <p><strong>Tensão:</strong> {equipment.tensao:g} V</p>
                <p><strong>Corrente nominal:</strong> {equipment.corrente_nominal:g} A</p>
                <p><strong>Rotação nominal:</strong> {equipment.rotacao_nominal:g} RPM</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="info-section">
                <h4>Instalação e condição</h4>
                <p><strong>Local:</strong> {equipment.local_instalacao}</p>
                <div class="status-row">
                    <strong>Status operacional:</strong>
                    {status_badge_html(equipment.status_operacional)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Observações técnicas")
    st.info(equipment.observacoes)


def render_raw_data_page(service: EquipmentService) -> None:
    st.title("Dados Brutos")
    st.write("Visualização de leituras simuladas de sensores com conversão para unidades compreensíveis.")
    st.info(
        "Nesta Sprint, os dados são simulados para validar a interface. Nas próximas fases, "
        "essa camada poderá receber dados reais via ESP32 e MQTT."
    )

    equipments = service.list_equipments()
    if not equipments:
        render_empty_state("Cadastre um equipamento para visualizar dados simulados.")
        return

    tag_options = [equipment.tag for equipment in equipments]
    selected_tag = st.selectbox("Selecione o ativo monitorado", tag_options)
    selected_equipment = service.get_by_tag(selected_tag)
    if not selected_equipment:
        st.error("Equipamento não encontrado.")
        return

    st.warning("Leituras exibidas somente para demonstração acadêmica. Não representam sensores reais conectados.")

    with st.spinner("Simulando leitura bruta e convertendo valores..."):
        time.sleep(0.4)
        raw_data = simulate_raw_sensor_data(selected_equipment)
        converted_data = convert_raw_sensor_data(raw_data, selected_equipment)
        table_data = build_sensor_table(raw_data, converted_data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperatura", f"{converted_data['temperatura_c']} °C")
    col2.metric("Corrente", f"{converted_data['corrente_a']} A")
    col3.metric("Rotação", f"{converted_data['rotacao_rpm']:.0f} RPM")

    st.subheader("Tabela de conversão simulada")
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    with st.expander("Contexto da simulação"):
        st.write(
            "Os campos `temperatura_raw`, `corrente_raw` e `rotacao_raw` representam leituras "
            "numéricas simuladas, semelhantes ao que poderia chegar de um microcontrolador. "
            "Em sprint futura, esta camada pode receber mensagens MQTT de dispositivos como ESP32."
        )


def render_about_page() -> None:
    st.title("Sobre o Projeto")
    st.write(
        "Projeto acadêmico da Sprint 1 focado nos fundamentos do ativo, cadastro técnico, "
        "consulta de equipamentos e visualização inicial de dados simulados."
    )

    st.subheader("Objetivo")
    st.write(
        "Criar uma base organizada para evoluir um Digital Twin de motores e equipamentos, "
        "mantendo a interface separada das regras de negócio."
    )

    st.subheader("Tecnologias")
    st.write("Python, Streamlit, Pandas e persistência local em JSON.")

    st.subheader("Requisitos atendidos na Sprint 1")
    st.markdown(
        """
        - Cadastro técnico de ativos
        - Consulta de equipamentos
        - Ficha técnica organizada
        - Visualização de dados brutos simulados
        - Conversão para unidades compreensíveis
        - Estrutura preparada para integração futura com IoT/MQTT
        """
    )

    st.subheader("Próximas Sprints")
    st.markdown(
        """
        - Integração com ESP32
        - Comunicação via MQTT
        - Histórico de sensores
        - Alertas de anomalia
        - Digital Twin com dados reais
        """
    )
