"""
Implementación de juegos de matriz (forma normal)
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from itertools import product
from .game import Game
from .player import StrategyProfile


class MatrixGame(Game):
    """Juego en forma de matriz (forma normal)"""
    
    def __init__(self, name: str, description: str, payoff_matrix: np.ndarray, 
                 player_strategies: List[List[str]]):
        """
        Inicializa un juego de matriz
        
        Args:
            name: Nombre del juego
            description: Descripción del juego
            payoff_matrix: Matriz de pagos (dimensiones: estrategias_p1 x estrategias_p2 x num_players)
            player_strategies: Lista de estrategias para cada jugador
        """
        num_players = len(player_strategies)
        super().__init__(name, description, num_players)
        
        self.payoff_matrix = np.array(payoff_matrix)
        self.player_strategies = player_strategies
        
        # Validar dimensiones
        expected_shape = tuple([len(s) for s in player_strategies] + [num_players])
        if self.payoff_matrix.shape != expected_shape:
            raise ValueError(f"La matriz de pagos debe tener forma {expected_shape}, tiene {self.payoff_matrix.shape}")
    
    def calculate_payoffs(self, strategy_profile: StrategyProfile) -> Dict[int, float]:
        """
        Calcula los pagos para un perfil de estrategias
        
        Args:
            strategy_profile: Perfil de estrategias
            
        Returns:
            Diccionario de pagos por jugador
        """
        # Obtener índices de estrategias
        indices = []
        for player_id in range(self.num_players):
            strategy = strategy_profile.get_strategy(player_id)
            strategy_index = self.player_strategies[player_id].index(strategy)
            indices.append(strategy_index)
        
        # Obtener pagos de la matriz
        indices_tuple = tuple(indices)
        payoffs = self.payoff_matrix[indices_tuple]
        
        return {player_id: float(payoffs[player_id]) for player_id in range(self.num_players)}
    
    def get_best_response(self, player_id: int, others_strategies: Dict[int, str]) -> str:
        """
        Calcula la mejor respuesta para un jugador
        
        Args:
            player_id: ID del jugador
            others_strategies: Estrategias de los otros jugadores
            
        Returns:
            Mejor estrategia para el jugador
        """
        best_payoff = float('-inf')
        best_strategy = None
        
        for strategy in self.player_strategies[player_id]:
            # Crear perfil de estrategias completo
            strategies = others_strategies.copy()
            strategies[player_id] = strategy
            profile = StrategyProfile(strategies=strategies)
            
            # Calcular pago
            payoffs = self.calculate_payoffs(profile)
            payoff = payoffs[player_id]
            
            if payoff > best_payoff:
                best_payoff = payoff
                best_strategy = strategy
        
        return best_strategy
    
    def find_nash_equilibria(self) -> List[StrategyProfile]:
        """
        Encuentra todos los equilibrios de Nash puros
        
        Returns:
            Lista de equilibrios de Nash
        """
        equilibria = []
        
        # Generar todos los perfiles de estrategia posibles
        all_strategies = list(product(*self.player_strategies))
        
        for strategy_tuple in all_strategies:
            strategies = {i: strategy_tuple[i] for i in range(self.num_players)}
            profile = StrategyProfile(strategies=strategies)
            
            if self.is_nash_equilibrium(profile):
                payoffs = self.calculate_payoffs(profile)
                profile.payoffs = payoffs
                equilibria.append(profile)
        
        return equilibria
    
    def find_dominant_strategies(self) -> Dict[int, Optional[str]]:
        """
        Encuentra estrategias estrictamente dominantes para cada jugador
        
        Returns:
            Diccionario de player_id -> estrategia dominante (o None)
        """
        dominant = {}
        
        for player_id in range(self.num_players):
            for candidate in self.player_strategies[player_id]:
                is_dominant = True
                
                # Verificar si candidate domina todas las demás estrategias
                for other_strategy in self.player_strategies[player_id]:
                    if candidate == other_strategy:
                        continue
                    
                    # Verificar para todos los perfiles de estrategia de los oponentes
                    other_players_strategies = [
                        self.player_strategies[i] for i in range(self.num_players) 
                        if i != player_id
                    ]
                    
                    for opponent_profile in product(*other_players_strategies):
                        # Construir perfil completo
                        strategies_candidate = {player_id: candidate}
                        strategies_other = {player_id: other_strategy}
                        
                        idx = 0
                        for i in range(self.num_players):
                            if i != player_id:
                                strategies_candidate[i] = opponent_profile[idx]
                                strategies_other[i] = opponent_profile[idx]
                                idx += 1
                        
                        profile_candidate = StrategyProfile(strategies=strategies_candidate)
                        profile_other = StrategyProfile(strategies=strategies_other)
                        
                        payoff_candidate = self.calculate_payoffs(profile_candidate)[player_id]
                        payoff_other = self.calculate_payoffs(profile_other)[player_id]
                        
                        if payoff_candidate <= payoff_other:
                            is_dominant = False
                            break
                    
                    if not is_dominant:
                        break
                
                if is_dominant:
                    dominant[player_id] = candidate
                    break
            
            if player_id not in dominant:
                dominant[player_id] = None
        
        return dominant
    
    def is_pareto_optimal(self, strategy_profile: StrategyProfile) -> bool:
        """
        Verifica si un perfil de estrategias es Pareto óptimo
        
        Args:
            strategy_profile: Perfil a verificar
            
        Returns:
            True si es Pareto óptimo
        """
        current_payoffs = self.calculate_payoffs(strategy_profile)
        
        # Generar todos los perfiles posibles
        all_strategies = list(product(*self.player_strategies))
        
        for strategy_tuple in all_strategies:
            strategies = {i: strategy_tuple[i] for i in range(self.num_players)}
            test_profile = StrategyProfile(strategies=strategies)
            test_payoffs = self.calculate_payoffs(test_profile)
            
            # Verificar si test_profile domina a strategy_profile en Pareto
            better_for_some = False
            worse_for_any = False
            
            for player_id in range(self.num_players):
                if test_payoffs[player_id] > current_payoffs[player_id]:
                    better_for_some = True
                if test_payoffs[player_id] < current_payoffs[player_id]:
                    worse_for_any = True
            
            # Si es mejor para alguien y no peor para nadie, no es Pareto óptimo
            if better_for_some and not worse_for_any:
                return False
        
        return True
    
    def get_payoff_matrix_as_dict(self) -> Dict:
        """
        Convierte la matriz de pagos a un formato serializable
        
        Returns:
            Diccionario con información de la matriz
        """
        return {
            'shape': self.payoff_matrix.shape,
            'strategies': self.player_strategies,
            'matrix': self.payoff_matrix.tolist()
        }


def create_prisoners_dilemma() -> MatrixGame:
    """Crea el juego del Dilema del Prisionero clásico"""
    payoff_matrix = np.array([
        [[3, 3], [0, 5]],
        [[5, 0], [1, 1]]
    ])
    strategies = [['Cooperar', 'Traicionar'], ['Cooperar', 'Traicionar']]
    
    return MatrixGame(
        name="Dilema del Prisionero",
        description="Dos criminales deben decidir si cooperan entre sí o traicionan al otro.",
        payoff_matrix=payoff_matrix,
        player_strategies=strategies
    )


def create_battle_of_sexes() -> MatrixGame:
    """Crea el juego de la Batalla de los Sexos"""
    payoff_matrix = np.array([
        [[2, 1], [0, 0]],
        [[0, 0], [1, 2]]
    ])
    strategies = [['Ópera', 'Fútbol'], ['Ópera', 'Fútbol']]
    
    return MatrixGame(
        name="Batalla de los Sexos",
        description="Una pareja debe coordinar su actividad, pero cada uno prefiere una diferente.",
        payoff_matrix=payoff_matrix,
        player_strategies=strategies
    )


def create_matching_pennies() -> MatrixGame:
    """Crea el juego de Matching Pennies"""
    payoff_matrix = np.array([
        [[1, -1], [-1, 1]],
        [[-1, 1], [1, -1]]
    ])
    strategies = [['Cara', 'Cruz'], ['Cara', 'Cruz']]
    
    return MatrixGame(
        name="Matching Pennies",
        description="Juego de suma cero donde los jugadores eligen cara o cruz.",
        payoff_matrix=payoff_matrix,
        player_strategies=strategies
    )


def create_chicken_game() -> MatrixGame:
    """Crea el juego del Gallina"""
    payoff_matrix = np.array([
        [[0, 0], [-1, 1]],
        [[1, -1], [-10, -10]]
    ])
    strategies = [['Desviarse', 'Continuar'], ['Desviarse', 'Continuar']]
    
    return MatrixGame(
        name="Juego del Gallina",
        description="Dos conductores van uno hacia el otro. ¿Quién se desviará primero?",
        payoff_matrix=payoff_matrix,
        player_strategies=strategies
    )


def create_stag_hunt() -> MatrixGame:
    """Crea el juego de la Caza del Ciervo"""
    payoff_matrix = np.array([
        [[4, 4], [0, 3]],
        [[3, 0], [2, 2]]
    ])
    strategies = [['Ciervo', 'Liebre'], ['Ciervo', 'Liebre']]
    
    return MatrixGame(
        name="Caza del Ciervo",
        description="Los cazadores deben decidir si cooperan para cazar un ciervo o cazan liebres individualmente.",
        payoff_matrix=payoff_matrix,
        player_strategies=strategies
    )
