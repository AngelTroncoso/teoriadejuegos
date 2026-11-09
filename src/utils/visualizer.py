"""
Utilidades para visualización de juegos y resultados
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
import networkx as nx


class Visualizer:
    """Clase para crear visualizaciones de teoría de juegos"""
    
    @staticmethod
    def create_payoff_matrix_heatmap(payoff_matrix: np.ndarray, 
                                     row_strategies: List[str],
                                     col_strategies: List[str],
                                     player_name: str = "Jugador 1") -> go.Figure:
        """
        Crea un mapa de calor de la matriz de pagos
        
        Args:
            payoff_matrix: Matriz de pagos (2D para un jugador)
            row_strategies: Nombres de las estrategias de las filas
            col_strategies: Nombres de las estrategias de las columnas
            player_name: Nombre del jugador
            
        Returns:
            Figura de Plotly
        """
        fig = go.Figure(data=go.Heatmap(
            z=payoff_matrix,
            x=col_strategies,
            y=row_strategies,
            colorscale='RdYlGn',
            text=payoff_matrix,
            texttemplate='%{text:.2f}',
            textfont={"size": 14},
            colorbar=dict(title="Pago")
        ))
        
        fig.update_layout(
            title=f"Matriz de Pagos - {player_name}",
            xaxis_title="Estrategias Jugador 2",
            yaxis_title="Estrategias Jugador 1",
            height=500,
            template='plotly_dark'
        )
        
        return fig
    
    @staticmethod
    def create_bimatrix_visualization(payoff_matrix: np.ndarray,
                                     row_strategies: List[str],
                                     col_strategies: List[str]) -> go.Figure:
        """
        Crea una visualización de bimatriz para juegos de 2 jugadores
        
        Args:
            payoff_matrix: Matriz de pagos (shape: n x m x 2)
            row_strategies: Estrategias del jugador 1
            col_strategies: Estrategias del jugador 2
            
        Returns:
            Figura de Plotly
        """
        # Preparar datos para la tabla
        cell_text = []
        for i in range(len(row_strategies)):
            row = []
            for j in range(len(col_strategies)):
                p1_payoff = payoff_matrix[i, j, 0]
                p2_payoff = payoff_matrix[i, j, 1]
                row.append(f"({p1_payoff:.1f}, {p2_payoff:.1f})")
            cell_text.append(row)
        
        # Crear tabla
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=[''] + col_strategies,
                fill_color='#262730',
                align='center',
                font=dict(size=14, color='white')
            ),
            cells=dict(
                values=[row_strategies] + [[cell_text[i][j] for i in range(len(row_strategies))] 
                                           for j in range(len(col_strategies))],
                fill_color='#1E1E1E',
                align='center',
                font=dict(size=13, color='white'),
                height=40
            )
        )])
        
        fig.update_layout(
            title="Matriz de Pagos Bimatriz (Jugador 1, Jugador 2)",
            height=400,
            template='plotly_dark'
        )
        
        return fig
    
    @staticmethod
    def plot_evolutionary_trajectory(trajectory: Dict[str, List[float]],
                                    title: str = "Evolución de Estrategias") -> go.Figure:
        """
        Grafica la evolución de frecuencias de estrategias
        
        Args:
            trajectory: Diccionario de estrategia -> lista de frecuencias
            title: Título del gráfico
            
        Returns:
            Figura de Plotly
        """
        fig = go.Figure()
        
        generations = list(range(len(next(iter(trajectory.values())))))
        
        for strategy, frequencies in trajectory.items():
            fig.add_trace(go.Scatter(
                x=generations,
                y=frequencies,
                mode='lines',
                name=strategy,
                line=dict(width=3)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Generación",
            yaxis_title="Frecuencia de Estrategia",
            yaxis=dict(range=[0, 1]),
            hovermode='x unified',
            template='plotly_dark',
            height=500
        )
        
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray", 
                     annotation_text="Equilibrio 50/50")
        
        return fig
    
    @staticmethod
    def plot_phase_portrait_2d(vector_field: List[Dict],
                              strategy_names: List[str]) -> go.Figure:
        """
        Crea un retrato de fase para sistemas de 2 estrategias
        
        Args:
            vector_field: Datos del campo vectorial
            strategy_names: Nombres de las dos estrategias
            
        Returns:
            Figura de Plotly
        """
        freqs = [point['freq_s1'] for point in vector_field]
        dx = [point['dx'] for point in vector_field]
        
        fig = go.Figure()
        
        # Línea de flujo
        fig.add_trace(go.Scatter(
            x=freqs,
            y=dx,
            mode='lines+markers',
            name='Dinámica de Replicadores',
            line=dict(width=3, color='#FF4B4B')
        ))
        
        # Línea de equilibrio
        fig.add_hline(y=0, line_dash="dash", line_color="green",
                     annotation_text="Equilibrio (dx/dt = 0)")
        
        fig.update_layout(
            title=f"Retrato de Fase: {strategy_names[0]} vs {strategy_names[1]}",
            xaxis_title=f"Frecuencia de {strategy_names[0]}",
            yaxis_title="Tasa de Cambio (dx/dt)",
            template='plotly_dark',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_payoff_comparison(strategies: List[str], 
                              payoffs: List[float],
                              title: str = "Comparación de Pagos") -> go.Figure:
        """
        Crea un gráfico de barras comparando pagos
        
        Args:
            strategies: Lista de estrategias
            payoffs: Lista de pagos correspondientes
            title: Título del gráfico
            
        Returns:
            Figura de Plotly
        """
        fig = go.Figure(data=[
            go.Bar(
                x=strategies,
                y=payoffs,
                marker_color=['#FF4B4B', '#4B8BFF', '#4BFF4B', '#FFB84B'][:len(strategies)],
                text=[f'{p:.2f}' for p in payoffs],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Estrategia",
            yaxis_title="Pago",
            template='plotly_dark',
            height=400
        )
        
        return fig
    
    @staticmethod
    def plot_game_tree(tree_dict: Dict, title: str = "Árbol de Decisión") -> go.Figure:
        """
        Visualiza un árbol de juego secuencial
        
        Args:
            tree_dict: Diccionario representando el árbol
            title: Título del gráfico
            
        Returns:
            Figura de Plotly
        """
        # Construir grafo con NetworkX
        G = nx.DiGraph()
        
        def add_nodes_edges(node_dict, parent_id=None, edge_label=""):
            node_id = node_dict['id']
            
            # Etiqueta del nodo
            if node_dict['is_terminal']:
                payoffs = node_dict.get('payoffs', {})
                label = f"Terminal\\n{payoffs}"
            else:
                label = f"Jugador {node_dict['player']}"
            
            G.add_node(node_id, label=label)
            
            if parent_id is not None:
                G.add_edge(parent_id, node_id, label=edge_label)
            
            # Añadir hijos
            if 'actions' in node_dict:
                for action, child in node_dict['actions'].items():
                    add_nodes_edges(child, node_id, action)
        
        add_nodes_edges(tree_dict)
        
        # Calcular posiciones con layout jerárquico
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Crear trazas para edges
        edge_x = []
        edge_y = []
        edge_labels = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Crear trazas para nodes
        node_x = []
        node_y = []
        node_text = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(G.nodes[node]['label'])
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                size=30,
                color='#4B8BFF',
                line_width=2
            )
        )
        
        # Crear figura
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=title,
                           showlegend=False,
                           hovermode='closest',
                           template='plotly_dark',
                           height=600,
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    @staticmethod
    def plot_nash_equilibria_comparison(equilibria_data: List[Dict],
                                       title: str = "Comparación de Equilibrios") -> go.Figure:
        """
        Compara múltiples equilibrios de Nash
        
        Args:
            equilibria_data: Lista de datos de equilibrios
            title: Título del gráfico
            
        Returns:
            Figura de Plotly
        """
        df_data = []
        
        for idx, eq in enumerate(equilibria_data):
            eq_name = f"Equilibrio {idx + 1}"
            for player_id, payoff in eq['payoffs'].items():
                df_data.append({
                    'Equilibrio': eq_name,
                    'Jugador': f"Jugador {player_id + 1}",
                    'Pago': payoff
                })
        
        df = pd.DataFrame(df_data)
        
        fig = px.bar(df, x='Equilibrio', y='Pago', color='Jugador',
                    barmode='group',
                    title=title,
                    template='plotly_dark')
        
        fig.update_layout(height=500)
        
        return fig
    
    @staticmethod
    def create_strategy_simplex_2d(frequencies: List[Tuple[float, float]],
                                  labels: Optional[List[str]] = None) -> go.Figure:
        """
        Crea un simplex de estrategias para 3 estrategias (visualización 2D)
        
        Args:
            frequencies: Lista de tuplas (freq1, freq2) donde freq3 = 1 - freq1 - freq2
            labels: Etiquetas opcionales para los puntos
            
        Returns:
            Figura de Plotly
        """
        x = [f[0] for f in frequencies]
        y = [f[1] for f in frequencies]
        
        fig = go.Figure()
        
        # Triángulo del simplex
        fig.add_trace(go.Scatter(
            x=[0, 1, 0, 0],
            y=[0, 0, 1, 0],
            mode='lines',
            line=dict(color='gray', dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Puntos de frecuencias
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers+text',
            marker=dict(size=12, color='#FF4B4B'),
            text=labels if labels else [f"P{i+1}" for i in range(len(frequencies))],
            textposition="top center",
            name='Poblaciones'
        ))
        
        fig.update_layout(
            title="Simplex de Estrategias",
            xaxis=dict(range=[-0.1, 1.1], title="Frecuencia Estrategia 1"),
            yaxis=dict(range=[-0.1, 1.1], title="Frecuencia Estrategia 2"),
            template='plotly_dark',
            height=600,
            width=600
        )
        
        return fig
