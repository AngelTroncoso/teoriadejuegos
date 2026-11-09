"""
Vista de juegos avanzados y análisis evolutivo
"""

import streamlit as st
import numpy as np
from src.models.evolutionary_game import (
    create_hawk_dove_game,
    create_rock_paper_scissors_game,
    create_coordination_game,
    Population
)
from src.controllers import SimulationController
from src.utils import Visualizer


def render():
    """Renderiza la página de análisis avanzado"""
    
    st.markdown('<h1 class="section-header">🧠 Análisis Avanzado</h1>', unsafe_allow_html=True)
    st.markdown("Explora dinámicas evolutivas y simulaciones de poblaciones.")
    
    st.markdown("---")
    
    # Tabs para diferentes tipos de análisis
    tab1, tab2, tab3 = st.tabs([
        "🧬 Juegos Evolutivos",
        "📊 Simulaciones",
        "🔬 Laboratorio"
    ])
    
    with tab1:
        render_evolutionary_games()
    
    with tab2:
        render_simulations()
    
    with tab3:
        render_laboratory()


def render_evolutionary_games():
    """Renderiza sección de juegos evolutivos"""
    
    st.markdown("## 🧬 Dinámicas Evolutivas")
    
    game_type = st.selectbox(
        "Selecciona un juego evolutivo:",
        ["Halcón-Paloma", "Piedra-Papel-Tijera", "Coordinación"]
    )
    
    if game_type == "Halcón-Paloma":
        render_hawk_dove()
    elif game_type == "Piedra-Papel-Tijera":
        render_rps()
    elif game_type == "Coordinación":
        render_coordination()


def render_hawk_dove():
    """Renderiza el juego Halcón-Paloma"""
    
    st.markdown("### 🦅 Halcón-Paloma")
    
    # Parámetros configurables
    col1, col2 = st.columns(2)
    
    with col1:
        value = st.slider("Valor del Recurso (V)", 1.0, 10.0, 4.0, 0.5)
    
    with col2:
        cost = st.slider("Costo de Pelear (C)", 1.0, 15.0, 6.0, 0.5)
    
    game = create_hawk_dove_game(value=value, cost=cost)
    
    st.markdown("""
    **Contexto**: Dos animales compiten por un recurso. Los halcones pelean,
    las palomas comparten. Pelear es costoso pero puede dar todo el recurso.
    """)
    
    # Mostrar matriz de pagos
    st.markdown("#### Matriz de Pagos")
    payoff_text = f"""
    | | Halcón | Paloma |
    |---|--------|--------|
    | **Halcón** | {(value-cost)/2:.2f} | {value:.2f} |
    | **Paloma** | 0 | {value/2:.2f} |
    """
    st.markdown(payoff_text)
    
    # Encontrar ESS
    ess = game.find_evolutionarily_stable_strategies()
    
    if ess:
        st.success(f"**Estrategias Evolutivamente Estables**: {', '.join(ess)}")
    else:
        st.info("**No hay ESS puras**. Existe un equilibrio mixto.")
    
    # Simulación
    st.markdown("#### 🎮 Simulación Evolutiva")
    
    col1, col2 = st.columns(2)
    
    with col1:
        initial_hawks = st.slider("% Inicial de Halcones", 0, 100, 50, 5)
    
    with col2:
        generations = st.slider("Generaciones", 10, 200, 100, 10)
    
    if st.button("▶️ Ejecutar Simulación", key="hd_sim"):
        # Crear población inicial
        freq_hawk = initial_hawks / 100.0
        initial_pop = Population(
            strategy_frequencies={"Halcón": freq_hawk, "Paloma": 1 - freq_hawk}
        )
        
        # Ejecutar simulación
        controller = SimulationController(game)
        history = controller.run_simulation(initial_pop, generations=generations)
        
        # Obtener trayectoria
        trajectory = controller.calculate_trajectory()
        
        # Visualizar
        visualizer = Visualizer()
        fig = visualizer.plot_evolutionary_trajectory(
            trajectory,
            title="Evolución de Estrategias: Halcón-Paloma"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Análisis de convergencia
        analysis = controller.analyze_convergence()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("¿Convergió?", "Sí" if analysis['converged'] else "No")
        
        with col2:
            dominant = analysis.get('dominant_strategy', 'N/A')
            st.metric("Estrategia Dominante", dominant)
        
        with col3:
            final_fitness = analysis.get('final_fitness', 0)
            st.metric("Fitness Final", f"{final_fitness:.3f}")
    
    with st.expander("💡 Insights"):
        st.markdown(f"""
        **Análisis con V={value}, C={cost}**:
        
        - Si C > V: Los halcones puros no pueden invadir una población de palomas
        - Si C < V: Los halcones tienen ventaja
        - Equilibrio mixto esperado: {value/cost:.2%} halcones
        
        **Aplicaciones**:
        - Comportamiento territorial en animales
        - Estrategias agresivas vs. pacíficas
        - Escalada de conflictos
        """)


def render_rps():
    """Renderiza Piedra-Papel-Tijera evolutivo"""
    
    st.markdown("### ✊✋✌️ Piedra-Papel-Tijera Evolutivo")
    
    game = create_rock_paper_scissors_game()
    
    st.markdown("""
    Versión evolutiva del clásico juego de manos. Cada estrategia vence a una y pierde contra otra.
    """)
    
    # Simulación
    st.markdown("#### Población Inicial")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rock_freq = st.slider("% Piedra", 0, 100, 33, 1)
    with col2:
        paper_freq = st.slider("% Papel", 0, 100, 33, 1)
    with col3:
        scissors_freq = 100 - rock_freq - paper_freq
        st.metric("% Tijera", scissors_freq)
    
    generations = st.slider("Generaciones", 50, 500, 200, 50)
    
    if st.button("▶️ Ejecutar Simulación", key="rps_sim"):
        initial_pop = Population(
            strategy_frequencies={
                "Piedra": rock_freq / 100.0,
                "Papel": paper_freq / 100.0,
                "Tijera": scissors_freq / 100.0
            }
        )
        
        controller = SimulationController(game)
        history = controller.run_simulation(initial_pop, generations=generations)
        trajectory = controller.calculate_trajectory()
        
        visualizer = Visualizer()
        fig = visualizer.plot_evolutionary_trajectory(
            trajectory,
            title="Evolución: Piedra-Papel-Tijera"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Observación**: Este sistema exhibe dinámicas cíclicas. No converge a un equilibrio
        estable, sino que las frecuencias oscilan perpetuamente.
        """)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Características**:
        - Sistema intransitivo (no hay estrategia óptima)
        - Dinámicas cíclicas perpetuas
        - Equilibrio mixto teórico: 1/3 cada estrategia
        
        **Aplicaciones**:
        - Sistemas ecológicos con depredadores múltiples
        - Competencia de especies
        - Estrategias de negocio cíclicas
        """)


def render_coordination():
    """Renderiza juego de coordinación"""
    
    st.markdown("### 🤝 Juego de Coordinación Evolutivo")
    
    high_payoff = st.slider("Pago Alto (Estrategia A)", 1.0, 10.0, 5.0, 0.5)
    low_payoff = st.slider("Pago Bajo (Estrategia B)", 1.0, 10.0, 2.0, 0.5)
    
    game = create_coordination_game(high_payoff=high_payoff, low_payoff=low_payoff)
    
    st.markdown("""
    Dos equilibrios posibles: todos juegan A o todos juegan B.
    La pregunta es: ¿hacia cuál converge la población?
    """)
    
    # Múltiples condiciones iniciales
    st.markdown("#### Comparación de Condiciones Iniciales")
    
    if st.button("▶️ Comparar Trayectorias", key="coord_compare"):
        populations = [
            Population(strategy_frequencies={"A": 0.1, "B": 0.9}),
            Population(strategy_frequencies={"A": 0.3, "B": 0.7}),
            Population(strategy_frequencies={"A": 0.5, "B": 0.5}),
            Population(strategy_frequencies={"A": 0.7, "B": 0.3}),
            Population(strategy_frequencies={"A": 0.9, "B": 0.1}),
        ]
        
        controller = SimulationController(game)
        results = controller.compare_initial_conditions(populations, generations=100)
        
        # Visualizar todas las trayectorias
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        for i, result in enumerate(results):
            fig.add_trace(go.Scatter(
                x=list(range(len(result['trajectory']['A']))),
                y=result['trajectory']['A'],
                name=f"Inicio: {result['initial_frequencies']['A']:.1%} A",
                mode='lines'
            ))
        
        fig.update_layout(
            title="Convergencia desde Diferentes Condiciones Iniciales",
            xaxis_title="Generación",
            yaxis_title="Frecuencia de Estrategia A",
            template='plotly_dark',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Observación**: Existe un punto crítico. Si la población inicial está por encima,
        converge al equilibrio alto (A). Si está por debajo, converge al equilibrio bajo (B).
        """)


def render_simulations():
    """Renderiza sección de simulaciones"""
    
    st.markdown("## 📊 Simulaciones Avanzadas")
    
    st.markdown("### 🔬 Invasión de Mutantes")
    
    st.markdown("""
    Simula la invasión de una estrategia mutante en una población residente.
    """)
    
    game = create_hawk_dove_game()
    
    col1, col2 = st.columns(2)
    
    with col1:
        resident = st.selectbox("Estrategia Residente:", game.strategies, key="resident")
    
    with col2:
        mutant = st.selectbox("Estrategia Mutante:", 
                             [s for s in game.strategies if s != resident],
                             key="mutant")
    
    mutant_fraction = st.slider("Fracción Inicial de Mutantes", 0.01, 0.20, 0.05, 0.01)
    
    if st.button("▶️ Simular Invasión"):
        controller = SimulationController(game)
        result = controller.simulate_invasion(
            resident_strategy=resident,
            mutant_strategy=mutant,
            mutant_fraction=mutant_fraction,
            generations=150
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Fracción Inicial", f"{result['initial_mutant_fraction']:.1%}")
        
        with col2:
            st.metric("Fracción Final", f"{result['final_mutant_fraction']:.1%}")
        
        with col3:
            if result['invasion_successful']:
                st.success("✅ Invasión Exitosa")
            elif result['mutant_increased']:
                st.warning("⚠️ Mutante Aumentó")
            else:
                st.error("❌ Invasión Falló")
        
        # Visualizar
        trajectory = {
            resident: [p.get_frequency(resident) for p in result['history']],
            mutant: [p.get_frequency(mutant) for p in result['history']]
        }
        
        visualizer = Visualizer()
        fig = visualizer.plot_evolutionary_trajectory(
            trajectory,
            title=f"Invasión: {mutant} → {resident}"
        )
        st.plotly_chart(fig, use_container_width=True)


def render_laboratory():
    """Renderiza laboratorio experimental"""
    
    st.markdown("## 🔬 Laboratorio de Juegos Personalizados")
    
    st.markdown("""
    Crea tu propio juego de 2 estrategias y analiza su dinámica evolutiva.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Nombres de Estrategias")
        s1_name = st.text_input("Estrategia 1:", "Estrategia A")
        s2_name = st.text_input("Estrategia 2:", "Estrategia B")
    
    with col2:
        st.markdown("### Matriz de Pagos")
        st.caption(f"{s1_name} vs {s1_name}")
        a11 = st.number_input("Pago:", -10.0, 10.0, 3.0, 0.5, key="a11")
        
        st.caption(f"{s1_name} vs {s2_name}")
        a12 = st.number_input("Pago:", -10.0, 10.0, 0.0, 0.5, key="a12")
        
        st.caption(f"{s2_name} vs {s1_name}")
        a21 = st.number_input("Pago:", -10.0, 10.0, 5.0, 0.5, key="a21")
        
        st.caption(f"{s2_name} vs {s2_name}")
        a22 = st.number_input("Pago:", -10.0, 10.0, 1.0, 0.5, key="a22")
    
    if st.button("🎮 Crear y Simular"):
        # Crear juego personalizado
        def custom_payoff(s1, s2):
            if s1 == s1_name and s2 == s1_name:
                return a11
            elif s1 == s1_name and s2 == s2_name:
                return a12
            elif s1 == s2_name and s2 == s1_name:
                return a21
            else:
                return a22
        
        from src.models.evolutionary_game import EvolutionaryGame
        
        game = EvolutionaryGame(
            name="Juego Personalizado",
            description="Juego creado en el laboratorio",
            strategies=[s1_name, s2_name],
            payoff_function=custom_payoff
        )
        
        # Encontrar ESS
        ess = game.find_evolutionarily_stable_strategies()
        
        if ess:
            st.success(f"**ESS encontradas**: {', '.join(ess)}")
        else:
            st.info("No hay ESS puras")
        
        # Simular
        initial_pop = Population(
            strategy_frequencies={s1_name: 0.5, s2_name: 0.5}
        )
        
        controller = SimulationController(game)
        history = controller.run_simulation(initial_pop, generations=100)
        trajectory = controller.calculate_trajectory()
        
        visualizer = Visualizer()
        fig = visualizer.plot_evolutionary_trajectory(
            trajectory,
            title="Evolución de tu Juego Personalizado"
        )
        st.plotly_chart(fig, use_container_width=True)
