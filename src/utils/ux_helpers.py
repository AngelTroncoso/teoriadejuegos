"""
Utilidades para mejorar la experiencia de usuario
"""
import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd


def show_calculation_spinner(message: str = "Calculando..."):
    """Context manager para mostrar spinner durante cálculos"""
    return st.spinner(f'⚙️ {message}')


def show_success_toast(message: str):
    """Muestra notificación de éxito"""
    st.toast(f'✅ {message}', icon='🎉')


def show_error_toast(message: str):
    """Muestra notificación de error"""
    st.toast(f'❌ {message}', icon='⚠️')


def show_info_toast(message: str):
    """Muestra notificación informativa"""
    st.toast(f'ℹ️ {message}', icon='💡')


def create_comparison_metrics(label1: str, value1: float, 
                              label2: str, value2: float):
    """Crea métricas comparativas lado a lado"""
    col1, col2 = st.columns(2)
    with col1:
        delta1 = value1 - value2
        st.metric(label1, f"{value1:.2f}", delta=f"{delta1:+.2f}")
    with col2:
        delta2 = value2 - value1
        st.metric(label2, f"{value2:.2f}", delta=f"{delta2:+.2f}")


def create_triple_metrics(label1: str, value1: float,
                         label2: str, value2: float,
                         label3: str, value3: float):
    """Crea tres métricas comparativas"""
    col1, col2, col3 = st.columns(3)
    
    avg = (value1 + value2 + value3) / 3
    
    with col1:
        st.metric(label1, f"{value1:.2f}", delta=f"{(value1 - avg):+.2f}")
    with col2:
        st.metric(label2, f"{value2:.2f}", delta=f"{(value2 - avg):+.2f}")
    with col3:
        st.metric(label3, f"{value3:.2f}", delta=f"{(value3 - avg):+.2f}")


def add_help_tooltip(text: str, icon: str = "💡"):
    """Añade tooltip de ayuda"""
    st.caption(f"{icon} {text}")


def empty_state(icon: str, title: str, message: str, action_label: Optional[str] = None):
    """Muestra estado vacío informativo"""
    st.markdown(f"""
    <div style='text-align: center; padding: 3rem; background-color: #262730; border-radius: 10px;'>
        <h1 style='font-size: 4rem; margin: 0;'>{icon}</h1>
        <h3 style='margin-top: 1rem;'>{title}</h3>
        <p style='color: #888; margin-bottom: 2rem;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_label:
        if st.button(action_label, use_container_width=True):
            return True
    return False


def create_progress_card(title: str, current: int, total: int, icon: str = "📊"):
    """Crea una tarjeta de progreso visual"""
    percentage = (current / total * 100) if total > 0 else 0
    
    st.markdown(f"""
    <div style='background-color: #1E1E1E; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0;'>
        <h4 style='margin: 0 0 1rem 0;'>{icon} {title}</h4>
        <div style='background-color: #262730; border-radius: 5px; height: 8px; overflow: hidden;'>
            <div style='background: linear-gradient(90deg, #FF4B4B, #FF8C8C); height: 100%; width: {percentage}%;'></div>
        </div>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #888;'>{current} de {total} completado ({percentage:.0f}%)</p>
    </div>
    """, unsafe_allow_html=True)


def show_action_buttons(primary_label: str, secondary_label: Optional[str] = None):
    """Muestra botones de acción principales"""
    if secondary_label:
        col1, col2 = st.columns(2)
        with col1:
            primary = st.button(primary_label, type="primary", use_container_width=True)
        with col2:
            secondary = st.button(secondary_label, use_container_width=True)
        return primary, secondary
    else:
        return st.button(primary_label, type="primary", use_container_width=True), False


def create_tabbed_content(tabs_dict: Dict[str, Any]):
    """Crea contenido organizado en tabs con iconos"""
    tab_names = list(tabs_dict.keys())
    tabs = st.tabs(tab_names)
    
    for tab, (name, content_func) in zip(tabs, tabs_dict.items()):
        with tab:
            content_func()


def show_tutorial_hint(message: str, key: str):
    """Muestra un hint tutorial que se puede cerrar"""
    if f'hide_hint_{key}' not in st.session_state:
        st.session_state[f'hide_hint_{key}'] = False
    
    if not st.session_state[f'hide_hint_{key}']:
        col1, col2 = st.columns([0.95, 0.05])
        with col1:
            st.info(f"💡 **Tip**: {message}")
        with col2:
            if st.button("✕", key=f"close_{key}"):
                st.session_state[f'hide_hint_{key}'] = True
                st.rerun()


def export_results_button(data: pd.DataFrame, filename: str = "resultados.csv"):
    """Botón para exportar resultados a CSV"""
    csv = data.to_csv(index=False)
    st.download_button(
        label="📥 Descargar Resultados CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )
