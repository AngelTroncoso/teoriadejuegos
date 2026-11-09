"""
Vista principal / Home de la aplicación
"""

import streamlit as st


def render():
    """Renderiza la página de inicio"""
    
    # Header principal
    st.markdown('<h1 class="main-header">🎮 Teoría de Juegos Aplicada</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #888;">De los Juegos de Mesa a la Solución de Problemas Complejos</p>',
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Introducción
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🌟 ¿Qué es la Teoría de Juegos?")
        st.markdown("""
        La **Teoría de Juegos** es una rama de las matemáticas y la economía que estudia 
        situaciones de **conflicto y cooperación** entre agentes racionales. Proporciona un 
        marco matemático para analizar la toma de decisiones estratégicas.
        
        ### 🎯 ¿Por qué es importante?
        
        - **Economía**: Análisis de mercados, subastas y competencia empresarial
        - **Ciencias Políticas**: Negociaciones internacionales y sistemas electorales
        - **Biología**: Evolución de comportamientos y estrategias de supervivencia
        - **Tecnología**: Diseño de protocolos de redes y algoritmos distribuidos
        - **Ciencias Sociales**: Cooperación humana y dilemas sociales
        """)
    
    with col2:
        st.markdown("## 📊 Estadísticas")
        st.metric("Juegos Disponibles", "10+")
        st.metric("Conceptos Cubiertos", "15+")
        st.metric("Aplicaciones Reales", "8+")
        
        st.markdown("---")
        st.info("💡 **Tip**: Comienza explorando los juegos clásicos para entender los conceptos fundamentales.")
    
    st.markdown("---")
    
    # Características principales
    st.markdown("## 🚀 Características de esta Aplicación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎲 Juegos Interactivos
        
        Experimenta con juegos clásicos:
        - Dilema del Prisionero
        - Batalla de los Sexos
        - Juego del Gallina
        - Matching Pennies
        - Y más...
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 Análisis Avanzado
        
        Herramientas de análisis:
        - Equilibrios de Nash
        - Estrategias dominantes
        - Óptimo de Pareto
        - Dinámicas evolutivas
        - Simulaciones
        """)
    
    with col3:
        st.markdown("""
        ### 🌍 Aplicaciones Reales
        
        Casos de estudio en:
        - Subastas en línea
        - Criptomonedas
        - Votaciones
        - Negociaciones
        - Diseño de mercados
        """)
    
    st.markdown("---")
    
    # Conceptos clave
    st.markdown("## 📚 Conceptos Clave")
    
    with st.expander("🎯 Equilibrio de Nash"):
        st.markdown("""
        Un **Equilibrio de Nash** es una situación donde ningún jugador puede mejorar 
        su resultado cambiando unilateralmente su estrategia, asumiendo que los demás 
        jugadores mantienen sus estrategias.
        
        **Ejemplo**: En el dilema del prisionero, el equilibrio es que ambos traicionen, 
        aunque cooperar sería mejor para ambos.
        """)
    
    with st.expander("💪 Estrategia Dominante"):
        st.markdown("""
        Una **Estrategia Dominante** es aquella que proporciona el mejor resultado 
        para un jugador, independientemente de lo que hagan los demás jugadores.
        
        **Ejemplo**: En el dilema del prisionero, "traicionar" es una estrategia 
        dominante para ambos jugadores.
        """)
    
    with st.expander("🎭 Equilibrio Perfecto en Subjuegos"):
        st.markdown("""
        En juegos secuenciales, un **Equilibrio Perfecto en Subjuegos** es aquel que 
        representa un equilibrio de Nash en cada punto del juego, no solo al final.
        
        **Ejemplo**: En el juego del ultimátum, el equilibrio perfecto es ofrecer 
        la cantidad mínima posible.
        """)
    
    with st.expander("🧬 Estrategia Evolutivamente Estable (ESS)"):
        st.markdown("""
        Una **ESS** es una estrategia que, si es adoptada por la población, no puede 
        ser invadida por ninguna estrategia mutante alternativa.
        
        **Ejemplo**: En el juego Halcón-Paloma, puede existir un equilibrio mixto 
        como ESS.
        """)
    
    st.markdown("---")
    
    # Ruta de aprendizaje sugerida
    st.markdown("## 🗺️ Ruta de Aprendizaje Sugerida")
    
    st.markdown("""
    1. **🎲 Juegos Clásicos** → Comienza aquí para entender los fundamentos
    2. **🧠 Análisis Avanzado** → Profundiza en equilibrios y estrategias
    3. **🌍 Aplicaciones Reales** → Ve cómo se aplica en el mundo real
    4. **📚 Centro de Aprendizaje** → Refuerza tu conocimiento con ejercicios
    """)
    
    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background-color: #262730; border-radius: 10px;">
            <h3>🎯 ¿Listo para comenzar?</h3>
            <p>Explora los juegos clásicos y descubre los fascinantes principios de la teoría de juegos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Autores y referencias
    st.markdown("## 👨‍🔬 Pioneros de la Teoría de Juegos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **John von Neumann**
        
        Matemático húngaro, fundador de la teoría de juegos junto con Oskar Morgenstern (1944).
        """)
    
    with col2:
        st.markdown("""
        **John Nash**
        
        Premio Nobel de Economía 1994 por su concepto del equilibrio de Nash.
        """)
    
    with col3:
        st.markdown("""
        **Robert Aumann**
        
        Premio Nobel de Economía 2005 por sus contribuciones a la teoría de juegos cooperativos.
        """)
    
    # Footer
    st.markdown("---")
    st.caption("© 2026 Teoría de Juegos Aplicada - Herramienta Educativa Interactiva")
