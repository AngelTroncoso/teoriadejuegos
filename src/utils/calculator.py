"""
Utilidades para cálculos de teoría de juegos
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy.optimize import linprog


class GameCalculator:
    """Clase con métodos estáticos para cálculos de teoría de juegos"""
    
    @staticmethod
    def calculate_social_welfare(payoffs: Dict[int, float]) -> float:
        """
        Calcula el bienestar social total
        
        Args:
            payoffs: Diccionario de pagos por jugador
            
        Returns:
            Suma total de pagos
        """
        return sum(payoffs.values())
    
    @staticmethod
    def calculate_gini_coefficient(payoffs: List[float]) -> float:
        """
        Calcula el coeficiente de Gini para medir desigualdad
        
        Args:
            payoffs: Lista de pagos
            
        Returns:
            Coeficiente de Gini (0 = perfecta igualdad, 1 = perfecta desigualdad)
        """
        if len(payoffs) == 0:
            return 0.0
        
        sorted_payoffs = np.sort(payoffs)
        n = len(sorted_payoffs)
        index = np.arange(1, n + 1)
        
        gini = (2 * np.sum(index * sorted_payoffs)) / (n * np.sum(sorted_payoffs)) - (n + 1) / n
        
        return gini
    
    @staticmethod
    def calculate_shapley_value(characteristic_function: Dict[frozenset, float],
                                num_players: int) -> Dict[int, float]:
        """
        Calcula el valor de Shapley para juegos cooperativos
        
        Args:
            characteristic_function: Función característica v(S) para coaliciones S
            num_players: Número de jugadores
            
        Returns:
            Valor de Shapley para cada jugador
        """
        from itertools import combinations, permutations
        from math import factorial
        
        shapley_values = {i: 0.0 for i in range(num_players)}
        
        # Para cada jugador
        for player in range(num_players):
            value = 0.0
            
            # Para cada tamaño de coalición
            for size in range(num_players):
                # Obtener todas las coaliciones de ese tamaño que no incluyen al jugador
                other_players = [p for p in range(num_players) if p != player]
                
                for coalition in combinations(other_players, size):
                    coalition_set = frozenset(coalition)
                    coalition_with_player = frozenset(list(coalition) + [player])
                    
                    # Contribución marginal
                    v_with = characteristic_function.get(coalition_with_player, 0.0)
                    v_without = characteristic_function.get(coalition_set, 0.0)
                    marginal_contribution = v_with - v_without
                    
                    # Peso
                    weight = (factorial(size) * factorial(num_players - size - 1)) / factorial(num_players)
                    
                    value += weight * marginal_contribution
            
            shapley_values[player] = value
        
        return shapley_values
    
    @staticmethod
    def calculate_core(characteristic_function: Dict[frozenset, float],
                      num_players: int) -> Optional[List[np.ndarray]]:
        """
        Calcula el núcleo (core) de un juego cooperativo
        
        Args:
            characteristic_function: Función característica
            num_players: Número de jugadores
            
        Returns:
            Puntos en el núcleo o None si está vacío
        """
        # El núcleo es el conjunto de asignaciones que no pueden ser mejoradas
        # por ninguna coalición
        # Implementación simplificada para juegos pequeños
        
        grand_coalition = frozenset(range(num_players))
        total_value = characteristic_function.get(grand_coalition, 0.0)
        
        # Punto equitativo como estimación inicial
        equal_split = np.array([total_value / num_players] * num_players)
        
        # Verificar si el split equitativo está en el núcleo
        in_core = True
        for size in range(1, num_players):
            from itertools import combinations
            for coalition in combinations(range(num_players), size):
                coalition_value = characteristic_function.get(frozenset(coalition), 0.0)
                allocation_to_coalition = sum(equal_split[i] for i in coalition)
                
                if allocation_to_coalition < coalition_value:
                    in_core = False
                    break
            if not in_core:
                break
        
        if in_core:
            return [equal_split]
        else:
            return None
    
    @staticmethod
    def calculate_banzhaf_power_index(weights: List[int], quota: int) -> Dict[int, float]:
        """
        Calcula el índice de poder de Banzhaf para juegos de votación
        
        Args:
            weights: Pesos de voto de cada jugador
            quota: Cuota mínima para ganar
            
        Returns:
            Índice de poder para cada jugador
        """
        from itertools import combinations
        
        num_players = len(weights)
        swing_counts = {i: 0 for i in range(num_players)}
        
        # Para cada coalición posible
        for size in range(num_players + 1):
            for coalition in combinations(range(num_players), size):
                coalition_weight = sum(weights[i] for i in coalition)
                
                # Para cada jugador no en la coalición
                for player in range(num_players):
                    if player not in coalition:
                        # Verificar si el jugador es pivote
                        with_player = coalition_weight + weights[player]
                        
                        if coalition_weight < quota <= with_player:
                            swing_counts[player] += 1
        
        # Normalizar
        total_swings = sum(swing_counts.values())
        
        if total_swings == 0:
            return {i: 1.0 / num_players for i in range(num_players)}
        
        power_index = {i: count / total_swings for i, count in swing_counts.items()}
        
        return power_index
    
    @staticmethod
    def calculate_expected_utility(probabilities: np.ndarray, 
                                  utilities: np.ndarray) -> float:
        """
        Calcula la utilidad esperada dada una distribución de probabilidad
        
        Args:
            probabilities: Vector de probabilidades
            utilities: Vector de utilidades
            
        Returns:
            Utilidad esperada
        """
        return np.dot(probabilities, utilities)
    
    @staticmethod
    def find_maximin_strategy(payoff_matrix: np.ndarray) -> Tuple[int, float]:
        """
        Encuentra la estrategia maximin (maximizar el mínimo pago)
        
        Args:
            payoff_matrix: Matriz de pagos del jugador
            
        Returns:
            Tupla (índice de estrategia, valor maximin)
        """
        min_payoffs = np.min(payoff_matrix, axis=1)
        maximin_idx = np.argmax(min_payoffs)
        maximin_value = min_payoffs[maximin_idx]
        
        return maximin_idx, maximin_value
    
    @staticmethod
    def find_minimax_strategy(payoff_matrix: np.ndarray) -> Tuple[int, float]:
        """
        Encuentra la estrategia minimax (minimizar el máximo pago del oponente)
        
        Args:
            payoff_matrix: Matriz de pagos del oponente
            
        Returns:
            Tupla (índice de estrategia, valor minimax)
        """
        max_payoffs = np.max(payoff_matrix, axis=0)
        minimax_idx = np.argmin(max_payoffs)
        minimax_value = max_payoffs[minimax_idx]
        
        return minimax_idx, minimax_value
    
    @staticmethod
    def calculate_risk_dominance(payoffs_eq1: Tuple[float, float],
                                 payoffs_eq2: Tuple[float, float],
                                 outside_payoffs: Tuple[float, float]) -> str:
        """
        Determina qué equilibrio tiene dominancia de riesgo
        
        Args:
            payoffs_eq1: Pagos en equilibrio 1 (jugador1, jugador2)
            payoffs_eq2: Pagos en equilibrio 2 (jugador1, jugador2)
            outside_payoffs: Pagos fuera de equilibrio
            
        Returns:
            "eq1" o "eq2" dependiendo de qué equilibrio domina
        """
        # Producto de Nash
        nash_product_1 = ((payoffs_eq1[0] - outside_payoffs[0]) * 
                         (payoffs_eq1[1] - outside_payoffs[1]))
        nash_product_2 = ((payoffs_eq2[0] - outside_payoffs[0]) * 
                         (payoffs_eq2[1] - outside_payoffs[1]))
        
        return "eq1" if nash_product_1 > nash_product_2 else "eq2"
    
    @staticmethod
    def calculate_regret(payoff_matrix: np.ndarray, 
                        strategy_chosen: int,
                        opponent_strategy: int) -> float:
        """
        Calcula el arrepentimiento (regret) de una decisión
        
        Args:
            payoff_matrix: Matriz de pagos
            strategy_chosen: Estrategia elegida
            opponent_strategy: Estrategia del oponente
            
        Returns:
            Valor del arrepentimiento
        """
        actual_payoff = payoff_matrix[strategy_chosen, opponent_strategy]
        best_payoff = np.max(payoff_matrix[:, opponent_strategy])
        
        return best_payoff - actual_payoff
    
    @staticmethod
    def calculate_price_of_anarchy(social_optimum: float,
                                  nash_equilibrium_welfare: float) -> float:
        """
        Calcula el precio de la anarquía
        
        Args:
            social_optimum: Bienestar social óptimo
            nash_equilibrium_welfare: Bienestar en equilibrio de Nash
            
        Returns:
            Precio de la anarquía
        """
        if nash_equilibrium_welfare == 0:
            return float('inf')
        
        return social_optimum / nash_equilibrium_welfare
