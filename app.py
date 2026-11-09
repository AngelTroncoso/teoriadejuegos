"""
Aplicación Principal: Teoría de Juegos Aplicada
Punto de entrada de la aplicación Streamlit
"""

import streamlit as st
from src.views import (
    home_view,
    classic_games_view,
    advanced_games_view,
    applications_view,
    learning_view
)

# Configuración de la página
st.set_page_config(
    page_title="Teoría de Juegos Aplicada",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #4B8BFF;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF4B4B;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Inicializar estado de sesión
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Inicio"
    
    # Sidebar - Navegación
    with st.sidebar:
        st.markdown("# 🎮 Navegación")
        st.markdown("---")
        
        page = st.radio(
            "Selecciona una sección:",
            [
                "🏠 Inicio",
                "🎲 Juegos Clásicos",
                "🧠 Análisis Avanzado",
                "🌍 Aplicaciones Reales",
                "📚 Centro de Aprendizaje"
            ],
            key="navigation"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Tu Progreso")
        
        # Barra de progreso simulada
        if 'progress' not in st.session_state:
            st.session_state.progress = 0
        
        st.progress(st.session_state.progress / 100)
        st.caption(f"Completado: {st.session_state.progress}%")
        
        st.markdown("---")
        st.markdown("### ℹ️ Acerca de")
        st.caption("""
        Aplicación educativa interactiva para aprender Teoría de Juegos
        desde conceptos básicos hasta aplicaciones avanzadas.
        """)
        
        st.markdown("---")
        st.caption("© 2026 Teoría de Juegos Aplicada")
    
    # Routing de páginas
    if page == "🏠 Inicio":
        home_view.render()
    elif page == "🎲 Juegos Clásicos":
        classic_games_view.render()
    elif page == "🧠 Análisis Avanzado":
        advanced_games_view.render()
    elif page == "🌍 Aplicaciones Reales":
        applications_view.render()
    elif page == "📚 Centro de Aprendizaje":
        learning_view.render()

if __name__ == "__main__":
    main()
