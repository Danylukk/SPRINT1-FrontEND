import pandas as pd
import streamlit as st

from src.models.equipment import Equipment


STATUS_COLORS = {
    "Operacional": "#1f9d55",
    "Atenção": "#d99a00",
    "Crítico": "#c92a2a",
    "Inativo": "#c92a2a",
}


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .status-pill {
                display: inline-block;
                padding: 0.25rem 0.7rem;
                border-radius: 999px;
                color: white;
                font-weight: 700;
                font-size: 0.85rem;
            }
            .info-section {
                border: 1px solid rgba(148, 163, 184, 0.28);
                border-radius: 8px;
                padding: 1rem;
                background: rgba(15, 23, 42, 0.72);
                min-height: 120px;
                color: #e5e7eb;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.16);
            }
            .info-section h4 {
                color: #f8fafc;
                margin: 0 0 0.75rem 0;
                font-size: 1rem;
                font-weight: 700;
            }
            .info-section p {
                color: #d1d5db;
                margin: 0.35rem 0;
                line-height: 1.45;
            }
            .info-section strong {
                color: #f8fafc;
            }
            .info-section .status-row {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-top: 0.35rem;
                flex-wrap: wrap;
            }
            .info-section .status-row strong {
                margin: 0;
            }
            .info-section .status-pill {
                margin: 0;
            }
            .muted-text {
                color: #667085;
                font-size: 0.95rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> None:
    st.markdown(status_badge_html(status), unsafe_allow_html=True)


def status_badge_html(status: str) -> str:
    color = STATUS_COLORS.get(status, "#667085")
    return f"<span class='status-pill' style='background:{color}'>{status}</span>"


def equipment_to_dataframe(equipments: list[Equipment]) -> pd.DataFrame:
    rows = [
        {
            "TAG": item.tag,
            "Modelo": item.modelo,
            "Fabricante": item.fabricante,
            "Potência": f"{item.potencia:g} {item.unidade_potencia}",
            "Tensão": f"{item.tensao:g} V",
            "Status": item.status_operacional,
            "Data de cadastro": item.data_cadastro,
        }
        for item in equipments
    ]
    return pd.DataFrame(rows)


def render_equipment_card(equipment: Equipment) -> None:
    left, middle, right = st.columns([1.2, 1, 1])

    with left:
        st.subheader(equipment.tag)
        st.caption(f"{equipment.fabricante} | {equipment.modelo}")
        status_badge(equipment.status_operacional)

    with middle:
        st.metric("Potência", f"{equipment.potencia:g} {equipment.unidade_potencia}")
        st.metric("Tensão", f"{equipment.tensao:g} V")

    with right:
        st.metric("Corrente nominal", f"{equipment.corrente_nominal:g} A")
        st.metric("Rotação nominal", f"{equipment.rotacao_nominal:g} RPM")


def render_empty_state(message: str) -> None:
    st.info(message)
