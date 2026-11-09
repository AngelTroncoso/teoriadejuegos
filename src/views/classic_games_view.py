"""
Vista de juegos clásicos de teoría de juegos
"""

import streamlit as st
import numpy as np
import pandas as pd
from src.models.matrix_game import (
    create_prisoners_dilemma,
    create_battle_of_sexes,
    create_matching_pennies,
    create_chicken_game,
    create_stag_hunt
)
from src.models.sequential_game import (
    create_ultimatum_game,
    create_trust_game,
    create_entry_game
)
from src.controllers import GameController, NashSolver
from src.utils import Visualizer, DataLoader, ux_helpers


def render():
    """Renderiza la página de juegos clásicos"""
    
    st.markdown('<h1 class="section-header">🎲 Juegos Clásicos</h1>', unsafe_allow_html=True)
    st.markdown("Explora los juegos fundamentales de la teoría de juegos y analiza sus equilibrios.")
    
    st.markdown("---")
    
    # Selector de juego
    game_type = st.selectbox(
        "Selecciona un juego:",
        [
            "Dilema del Prisionero",
            "Batalla de los Sexos",
            "Matching Pennies",
            "Juego del Gallina",
            "Caza del Ciervo",
            "Juego del Ultimátum",
            "Juego de la Confianza",
            "Entrada al Mercado"
        ]
    )
    
    # Renderizar el juego seleccionado
    if game_type == "Dilema del Prisionero":
        render_prisoners_dilemma()
    elif game_type == "Batalla de los Sexos":
        render_battle_of_sexes()
    elif game_type == "Matching Pennies":
        render_matching_pennies()
    elif game_type == "Juego del Gallina":
        render_chicken_game()
    elif game_type == "Caza del Ciervo":
        render_stag_hunt()
    elif game_type == "Juego del Ultimátum":
        render_ultimatum_game()
    elif game_type == "Juego de la Confianza":
        render_trust_game()
    elif game_type == "Entrada al Mercado":
        render_entry_game()


def render_prisoners_dilemma():
    """Renderiza el dilema del prisionero"""
    
    game = create_prisoners_dilemma()
    
    st.markdown("## 🚔 Dilema del Prisionero")
    
    # Hint tutorial
    ux_helpers.show_tutorial_hint(
        "Este es uno de los juegos más importantes. Observa cómo la racionalidad individual lleva a un resultado subóptimo.",
        "pd_hint"
    )
    
    st.markdown("""
    **Contexto**: Dos criminales son arrestados y interrogados por separado. 
    Cada uno puede cooperar con el otro (permanecer en silencio) o traicionarlo (confesar).
    
    - Si ambos **cooperan**: 3 años de cárcel cada uno
    - Si uno **traiciona** y el otro **coopera**: 0 años el traidor, 5 años el cooperador
    - Si ambos **traicionan**: 1 año de cárcel cada uno
    """)
    
    # Visualizar matriz
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Matriz de Pagos")
        visualizer = Visualizer()
        fig = visualizer.create_bimatrix_visualization(
            game.payoff_matrix,
            game.player_strategies[0],
            game.player_strategies[1]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Análisis")
        
        # Calcular equilibrios con spinner
        with ux_helpers.show_calculation_spinner("Analizando equilibrios..."):
            solver = NashSolver(game)
            equilibria = solver.find_pure_nash_equilibria()
        
        # Métricas mejoradas
        st.metric("Equilibrios de Nash", len(equilibria), help="Número de equilibrios puros encontrados")
        
        for i, eq in enumerate(equilibria):
            st.success(f"**Equilibrio {i+1}**: {eq.strategies}")
            
            # Usar métricas comparativas
            ux_helpers.create_comparison_metrics(
                "Jugador 1",
                eq.payoffs[0],
                "Jugador 2",
                eq.payoffs[1]
            )
        
        dominant = game.find_dominant_strategies()
        st.write("**Estrategias Dominantes**:")
        for player_id, strategy in dominant.items():
            if strategy:
                st.write(f"- Jugador {player_id + 1}: {strategy}")
    
    st.markdown("---")
    
    # Jugar interactivamente
    st.markdown("### 🎮 Juega Interactivamente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        p1_strategy = st.radio(
            "Estrategia Jugador 1:", 
            game.player_strategies[0], 
            key="pd_p1",
            help="Elige la estrategia para el Jugador 1"
        )
    
    with col2:
        p2_strategy = st.radio(
            "Estrategia Jugador 2:", 
            game.player_strategies[1], 
            key="pd_p2",
            help="Elige la estrategia para el Jugador 2"
        )
    
    if st.button("▶️ Jugar Ronda", key="pd_play", type="primary", use_container_width=True):
        from src.models.player import StrategyProfile
        
        with ux_helpers.show_calculation_spinner("Calculando resultados..."):
            profile = StrategyProfile(strategies={0: p1_strategy, 1: p2_strategy})
            payoffs = game.calculate_payoffs(profile)
            is_nash = game.is_nash_equilibrium(profile)
            is_pareto = game.is_pareto_optimal(profile)
        
        st.markdown("#### Resultados:")
        
        # Usar métricas con delta
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Pago Jugador 1", f"{payoffs[0]:.1f}", 
                     delta=f"{payoffs[0] - 2:.1f}" if payoffs[0] != 2 else None,
                     help="Pago obtenido por el Jugador 1")
        with col2:
            st.metric("Pago Jugador 2", f"{payoffs[1]:.1f}",
                     delta=f"{payoffs[1] - 2:.1f}" if payoffs[1] != 2 else None,
                     help="Pago obtenido por el Jugador 2")
        with col3:
            total = sum(payoffs.values())
            st.metric("Bienestar Total", f"{total:.1f}",
                     delta=f"{total - 6:.1f}" if total != 6 else None,
                     help="Suma de pagos de ambos jugadores")
        
        if is_nash:
            st.success("✅ Este resultado es un **Equilibrio de Nash**")
            ux_helpers.show_success_toast("¡Equilibrio de Nash encontrado!")
        else:
            st.warning("❌ Este resultado NO es un equilibrio de Nash")
        
        if is_pareto:
            st.success("✅ Este resultado es **Pareto Óptimo**")
        else:
            st.info("ℹ️ Este resultado NO es Pareto óptimo (existe una mejora posible)")
        
        # Guardar en historial
        if 'game_history' not in st.session_state:
            st.session_state.game_history = []
        
        st.session_state.game_history.append({
            'game': 'Dilema del Prisionero',
            'strategies': f"{p1_strategy} vs {p2_strategy}",
            'payoffs': f"({payoffs[0]}, {payoffs[1]})",
            'is_nash': is_nash
        })
        
        # Actualizar progreso
        st.session_state.classic_progress = min(st.session_state.get('classic_progress', 0) + 10, 100)
    
    # Mostrar historial si existe
    if 'game_history' in st.session_state and len(st.session_state.game_history) > 0:
        with st.expander("📜 Historial de Jugadas", expanded=False):
            history_df = pd.DataFrame(st.session_state.game_history[-5:])
            st.dataframe(history_df, use_container_width=True, hide_index=True)
            
            # Botón para exportar
            if len(st.session_state.game_history) > 0:
                full_df = pd.DataFrame(st.session_state.game_history)
                ux_helpers.export_results_button(full_df, "historial_juegos.csv")
    
    # Insights
    with st.expander("💡 Insights y Lecciones"):
        st.markdown("""
        **El Dilema**:
        - La estrategia racional individual (traicionar) lleva a un resultado subóptimo para ambos
        - Si ambos cooperaran, ambos estarían mejor
        - Ilustra el conflicto entre racionalidad individual y colectiva
        
        **Aplicaciones**:
        - Carreras armamentistas
        - Tragedia de los comunes
        - Competencia empresarial en precios
        - Doping en deportes
        """)


def render_battle_of_sexes():
    """Renderiza la batalla de los sexos"""
    
    game = create_battle_of_sexes()
    
    st.markdown("## 💑 Batalla de los Sexos")
    st.markdown("""
    Una pareja debe decidir a dónde ir esta noche. Ambos prefieren estar juntos,
    pero tienen preferencias diferentes sobre la actividad.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        visualizer = Visualizer()
        fig = visualizer.create_bimatrix_visualization(
            game.payoff_matrix,
            game.player_strategies[0],
            game.player_strategies[1]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        solver = NashSolver(game)
        equilibria = solver.find_pure_nash_equilibria()
        
        st.write(f"**Equilibrios puros**: {len(equilibria)}")
        for i, eq in enumerate(equilibria):
            st.success(f"Equilibrio {i+1}: {eq.strategies}")
        
        # Equilibrio mixto
        mixed_eq = solver.find_mixed_nash_equilibria_2x2()
        if mixed_eq:
            st.write(f"**Equilibrios mixtos**: {len(mixed_eq)}")
            for i, eq in enumerate(mixed_eq):
                st.info(f"Mixto {i+1}: P1={eq[0]}, P2={eq[1]}")
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Características**:
        - Múltiples equilibrios de Nash
        - Problema de coordinación
        - Asimetría en las preferencias
        
        **Lecciones**:
        - La comunicación previa puede ayudar a coordinar
        - Las convenciones sociales resuelven estos juegos
        - Relevante en estandarización tecnológica
        """)


def render_matching_pennies():
    """Renderiza matching pennies"""
    
    game = create_matching_pennies()
    
    st.markdown("## 🪙 Matching Pennies")
    st.markdown("Juego de suma cero: lo que uno gana, el otro pierde.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        visualizer = Visualizer()
        fig = visualizer.create_bimatrix_visualization(
            game.payoff_matrix,
            game.player_strategies[0],
            game.player_strategies[1]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        solver = NashSolver(game)
        equilibria = solver.find_pure_nash_equilibria()
        
        if len(equilibria) == 0:
            st.warning("**No hay equilibrios puros**")
        
        mixed_eq = solver.find_mixed_nash_equilibria_2x2()
        if mixed_eq:
            st.success("**Equilibrio mixto encontrado**")
            for eq in mixed_eq:
                st.write(f"P1: {eq[0]}")
                st.write(f"P2: {eq[1]}")
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Características**:
        - Juego de suma cero
        - No tiene equilibrio en estrategias puras
        - El equilibrio mixto es jugar cada estrategia con probabilidad 0.5
        
        **Aplicaciones**:
        - Penales en fútbol
        - Rock-Paper-Scissors
        - Estrategias militares de ocultamiento
        """)


def render_chicken_game():
    """Renderiza el juego del gallina"""
    
    game = create_chicken_game()
    
    st.markdown("## 🚗 Juego del Gallina")
    st.markdown("Dos conductores van uno hacia el otro. ¿Quién se desviará primero?")
    
    visualizer = Visualizer()
    fig = visualizer.create_bimatrix_visualization(
        game.payoff_matrix,
        game.player_strategies[0],
        game.player_strategies[1]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    solver = NashSolver(game)
    equilibria = solver.find_pure_nash_equilibria()
    
    st.write(f"**Equilibrios encontrados**: {len(equilibria)}")
    for eq in equilibria:
        st.success(f"Estrategias: {eq.strategies}, Pagos: {eq.payoffs}")
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **El Dilema**:
        - Es mejor desviarse que chocar
        - Pero es mejor que el otro se desvíe
        - El peor resultado es que nadie se desvíe
        
        **Aplicaciones**:
        - Escalada de conflictos internacionales
        - Huelgas laborales
        - Estrategias de entrada agresiva al mercado
        """)


def render_stag_hunt():
    """Renderiza la caza del ciervo"""
    
    game = create_stag_hunt()
    
    st.markdown("## 🦌 Caza del Ciervo")
    st.markdown("Los cazadores deben decidir si cooperan para cazar un ciervo o cazan liebres individualmente.")
    
    visualizer = Visualizer()
    fig = visualizer.create_bimatrix_visualization(
        game.payoff_matrix,
        game.player_strategies[0],
        game.player_strategies[1]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    solver = NashSolver(game)
    equilibria = solver.find_pure_nash_equilibria()
    
    for i, eq in enumerate(equilibria):
        st.success(f"**Equilibrio {i+1}**: {eq.strategies} → Pagos: {eq.payoffs}")
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Características**:
        - Dos equilibrios de Nash
        - Uno es mejor para ambos (Ciervo-Ciervo)
        - Uno es más seguro (Liebre-Liebre)
        - Ilustra el problema de coordinación y confianza
        
        **Aplicaciones**:
        - Inversión en tecnologías emergentes
        - Cooperación en investigación
        - Desarrollo de estándares industriales
        """)


def render_ultimatum_game():
    """Renderiza el juego del ultimátum"""
    
    game = create_ultimatum_game(total_amount=10.0)
    
    st.markdown("## 💰 Juego del Ultimátum")
    st.markdown("""
    El Jugador 1 propone cómo dividir $10. El Jugador 2 puede aceptar o rechazar.
    Si rechaza, nadie recibe nada.
    """)
    
    st.markdown("### Árbol de Decisión")
    visualizer = Visualizer()
    tree_dict = game.get_game_tree_dict()
    fig = visualizer.plot_game_tree(tree_dict)
    st.plotly_chart(fig, use_container_width=True)
    
    # Equilibrio perfecto en subjuegos
    equilibria = game.find_nash_equilibria()
    
    st.markdown("### Equilibrios Perfectos en Subjuegos")
    if equilibria:
        for eq in equilibria:
            st.success(f"Estrategias: {eq.strategies}")
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Predicción Teórica**:
        - El Jugador 1 debería ofrecer la cantidad mínima
        - El Jugador 2 debería aceptar cualquier oferta positiva
        
        **Realidad Experimental**:
        - Las personas suelen ofrecer 40-50% de la cantidad
        - Ofertas menores al 30% suelen ser rechazadas
        - Ilustra el papel de la equidad y las emociones
        
        **Aplicaciones**:
        - Negociaciones salariales
        - Acuerdos comerciales
        - Reparto de herencias
        """)


def render_trust_game():
    """Renderiza el juego de la confianza"""
    
    game = create_trust_game(initial_amount=10.0, multiplier=3.0)
    
    st.markdown("## 🤝 Juego de la Confianza")
    st.markdown("""
    El Jugador 1 tiene $10 y decide cuánto enviar. El monto se triplica.
    El Jugador 2 decide cuánto devolver.
    """)
    
    tree_dict = game.get_game_tree_dict()
    visualizer = Visualizer()
    fig = visualizer.plot_game_tree(tree_dict)
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Dilema**:
        - La confianza mutua maximiza las ganancias totales
        - Pero el Jugador 2 tiene incentivo a no devolver nada
        - El Jugador 1, anticipando esto, podría no enviar nada
        
        **En la Práctica**:
        - La confianza y reciprocidad son comunes
        - La reputación importa en interacciones repetidas
        - Fundamento de la cooperación económica
        
        **Aplicaciones**:
        - Contratos sin enforcement perfecto
        - Inversión extranjera
        - Crowdfunding
        """)


def render_entry_game():
    """Renderiza el juego de entrada al mercado"""
    
    game = create_entry_game()
    
    st.markdown("## 🏢 Entrada al Mercado")
    st.markdown("""
    Una empresa decide si entrar a un mercado.
    La empresa establecida decide si luchar contra el entrante o acomodarse.
    """)
    
    tree_dict = game.get_game_tree_dict()
    visualizer = Visualizer()
    fig = visualizer.plot_game_tree(tree_dict)
    st.plotly_chart(fig, use_container_width=True)
    
    equilibria = game.find_nash_equilibria()
    
    if equilibria:
        st.success(f"**Equilibrio perfecto**: {equilibria[0].strategies}")
    
    with st.expander("💡 Insights"):
        st.markdown("""
        **Análisis**:
        - La amenaza de luchar no es creíble
        - Una vez que el entrante entra, es mejor acomodar
        - El entrante, sabiendo esto, debería entrar
        
        **Lecciones**:
        - Las amenazas deben ser creíbles (subgame perfect)
        - La estructura secuencial importa
        - Relevante en antimonopolio y regulación
        
        **Aplicaciones**:
        - Entrada de nuevas empresas tecnológicas
        - Estrategias de precios predatorios
        - Barreras de entrada al mercado
        """)
