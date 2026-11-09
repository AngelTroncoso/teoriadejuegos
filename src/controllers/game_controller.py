"""
Controlador principal para la gestión de juegos
"""

from typing import Dict, List, Optional, Any
import numpy as np
from src.models import Game, MatrixGame, SequentialGame, EvolutionaryGame, Player
from src.models.player import StrategyProfile


class GameController:
    """Controlador para gestionar juegos y sus interacciones"""
    
    def __init__(self):
        """Inicializa el controlador de juegos"""
        self.current_game: Optional[Game] = None
        self.game_history: List[Dict] = []
    
    def set_game(self, game: Game) -> None:
        """
        Establece el juego actual
        
        Args:
            game: Instancia del juego a establecer
        """
        self.current_game = game
    
    def initialize_players(self, player_names: List[str]) -> None:
        """
        Inicializa jugadores para el juego actual
        
        Args:
            player_names: Lista de nombres de jugadores
        """
        if not self.current_game:
            raise ValueError("No hay un juego establecido")
        
        if len(player_names) != self.current_game.num_players:
            raise ValueError(f"Se requieren {self.current_game.num_players} jugadores")
        
        for idx, name in enumerate(player_names):
            player = Player(name=name, player_id=idx)
            
            # Añadir estrategias según el tipo de juego
            if isinstance(self.current_game, MatrixGame):
                for strategy in self.current_game.player_strategies[idx]:
                    player.add_strategy(strategy)
            elif isinstance(self.current_game, EvolutionaryGame):
                for strategy in self.current_game.strategies:
                    player.add_strategy(strategy)
            
            self.current_game.add_player(player)
    
    def play_round(self, strategies: Dict[int, str]) -> Dict[str, Any]:
        """
        Juega una ronda del juego actual
        
        Args:
            strategies: Diccionario de player_id -> estrategia elegida
            
        Returns:
            Resultado de la ronda incluyendo pagos y análisis
        """
        if not self.current_game:
            raise ValueError("No hay un juego establecido")
        
        payoffs = self.current_game.play_round(strategies)
        
        # Analizar el resultado
        strategy_profile = StrategyProfile(strategies=strategies, payoffs=payoffs)
        is_nash = self.current_game.is_nash_equilibrium(strategy_profile)
        
        result = {
            'strategies': strategies,
            'payoffs': payoffs,
            'is_nash_equilibrium': is_nash,
            'round_number': len(self.current_game.history)
        }
        
        # Añadir análisis adicional para juegos de matriz
        if isinstance(self.current_game, MatrixGame):
            is_pareto = self.current_game.is_pareto_optimal(strategy_profile)
            result['is_pareto_optimal'] = is_pareto
        
        self.game_history.append(result)
        return result
    
    def get_game_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen completo del juego actual
        
        Returns:
            Diccionario con información resumida del juego
        """
        if not self.current_game:
            return {}
        
        summary = self.current_game.get_game_summary()
        summary['history'] = self.game_history
        
        # Añadir estadísticas
        if self.game_history:
            total_payoffs = {pid: 0.0 for pid in range(self.current_game.num_players)}
            for round_data in self.game_history:
                for pid, payoff in round_data['payoffs'].items():
                    total_payoffs[pid] += payoff
            
            summary['total_payoffs'] = total_payoffs
            summary['average_payoffs'] = {
                pid: total / len(self.game_history)
                for pid, total in total_payoffs.items()
            }
        
        return summary
    
    def reset_current_game(self) -> None:
        """Reinicia el juego actual"""
        if self.current_game:
            self.current_game.reset_game()
        self.game_history.clear()
    
    def get_best_responses(self) -> Dict[int, Dict[str, str]]:
        """
        Calcula las mejores respuestas para cada jugador contra cada combinación
        de estrategias de los oponentes
        
        Returns:
            Diccionario anidado de mejores respuestas
        """
        if not self.current_game:
            return {}
        
        if not isinstance(self.current_game, MatrixGame):
            return {}
        
        best_responses = {}
        
        for player_id in range(self.current_game.num_players):
            best_responses[player_id] = {}
            
            # Para simplificar, solo manejamos juegos de 2 jugadores
            if self.current_game.num_players == 2:
                opponent_id = 1 - player_id
                for opponent_strategy in self.current_game.player_strategies[opponent_id]:
                    others = {opponent_id: opponent_strategy}
                    best = self.current_game.get_best_response(player_id, others)
                    best_responses[player_id][opponent_strategy] = best
        
        return best_responses
    
    def analyze_dominant_strategies(self) -> Dict[int, Optional[str]]:
        """
        Analiza estrategias dominantes en el juego actual
        
        Returns:
            Diccionario de player_id -> estrategia dominante (o None)
        """
        if not isinstance(self.current_game, MatrixGame):
            return {}
        
        return self.current_game.find_dominant_strategies()
    
    def compare_outcomes(self, profile1: Dict[int, str], 
                        profile2: Dict[int, str]) -> Dict[str, Any]:
        """
        Compara dos perfiles de estrategia
        
        Args:
            profile1: Primer perfil de estrategias
            profile2: Segundo perfil de estrategias
            
        Returns:
            Comparación detallada
        """
        if not self.current_game:
            return {}
        
        sp1 = StrategyProfile(strategies=profile1)
        sp2 = StrategyProfile(strategies=profile2)
        
        payoffs1 = self.current_game.calculate_payoffs(sp1)
        payoffs2 = self.current_game.calculate_payoffs(sp2)
        
        comparison = {
            'profile1': {
                'strategies': profile1,
                'payoffs': payoffs1,
                'is_nash': self.current_game.is_nash_equilibrium(sp1),
                'total': sum(payoffs1.values())
            },
            'profile2': {
                'strategies': profile2,
                'payoffs': payoffs2,
                'is_nash': self.current_game.is_nash_equilibrium(sp2),
                'total': sum(payoffs2.values())
            }
        }
        
        # Determinar si uno domina al otro en Pareto
        better_for_some = False
        worse_for_any = False
        
        for pid in range(self.current_game.num_players):
            if payoffs1[pid] > payoffs2[pid]:
                better_for_some = True
            if payoffs1[pid] < payoffs2[pid]:
                worse_for_any = True
        
        comparison['profile1_pareto_dominates_profile2'] = better_for_some and not worse_for_any
        comparison['profile2_pareto_dominates_profile1'] = (
            not better_for_some and worse_for_any
        )
        
        return comparison
    
    def get_payoff_matrix_formatted(self) -> Optional[np.ndarray]:
        """
        Obtiene la matriz de pagos del juego actual si es un MatrixGame
        
        Returns:
            Matriz de pagos o None
        """
        if isinstance(self.current_game, MatrixGame):
            return self.current_game.payoff_matrix
        return None
