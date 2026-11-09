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
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/AngelTroncoso/teoriadejuegos',
        'Report a bug': 'https://github.com/AngelTroncoso/teoriadejuegos/issues',
        'About': '# Teoría de Juegos Aplicada v1.0\nAplicación educativa interactiva para aprender teoría de juegos.'
    }
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
    
    # Onboarding para primera visita
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = False
        st.balloons()
        st.success("""
        ### 👋 ¡Bienvenido a Teoría de Juegos Aplicada!
        
        **Te recomendamos empezar por:**
        1. 🏠 **Inicio** - Conoce los conceptos fundamentales
        2. 🎲 **Juegos Clásicos** - Interactúa con el Dilema del Prisionero
        3. 📚 **Centro de Aprendizaje** - Refuerza tus conocimientos
        """)
    
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
        
        # Sistema de progreso mejorado
        progress_data = {
            "Juegos Clásicos": st.session_state.get('classic_progress', 0),
            "Análisis Avanzado": st.session_state.get('advanced_progress', 0),
            "Aplicaciones": st.session_state.get('apps_progress', 0),
            "Aprendizaje": st.session_state.get('learning_progress', 0)
        }
        
        total_progress = sum(progress_data.values()) / len(progress_data)
        
        # Barra de progreso principal
        st.progress(total_progress / 100)
        st.caption(f"**Total: {total_progress:.0f}%** completado")
        
        # Desglose por módulo
        with st.expander("📈 Ver desglose", expanded=False):
            for module, progress in progress_data.items():
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.caption(module)
                with col2:
                    st.caption(f"{progress}%")
                st.progress(progress / 100)
        
        # Acceso rápido
        st.markdown("---")
        st.markdown("### ⚡ Acceso Rápido")
        if st.button("🔄 Reiniciar Progreso", use_container_width=True):
            for key in list(st.session_state.keys()):
                if '_progress' in key:
                    st.session_state[key] = 0
            st.toast("✅ Progreso reiniciado", icon="🔄")
            st.rerun()
        
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
