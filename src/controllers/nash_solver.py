"""
Solucionador de equilibrios de Nash
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from scipy.optimize import linprog
from itertools import product
from src.models import MatrixGame
from src.models.player import StrategyProfile


class NashSolver:
    """Solucionador para encontrar equilibrios de Nash puros y mixtos"""
    
    def __init__(self, game: MatrixGame):
        """
        Inicializa el solucionador
        
        Args:
            game: Juego de matriz a resolver
        """
        if not isinstance(game, MatrixGame):
            raise ValueError("NashSolver solo funciona con MatrixGame")
        
        self.game = game
        self.pure_equilibria: List[StrategyProfile] = []
        self.mixed_equilibria: List[Dict[int, np.ndarray]] = []
    
    def find_pure_nash_equilibria(self) -> List[StrategyProfile]:
        """
        Encuentra todos los equilibrios de Nash puros
        
        Returns:
            Lista de equilibrios puros
        """
        self.pure_equilibria = self.game.find_nash_equilibria()
        return self.pure_equilibria
    
    def find_mixed_nash_equilibria_2x2(self) -> List[Dict[int, np.ndarray]]:
        """
        Encuentra equilibrios mixtos para juegos 2x2
        
        Returns:
            Lista de equilibrios mixtos (distribuciones de probabilidad)
        """
        if self.game.num_players != 2:
            return []
        
        if len(self.game.player_strategies[0]) != 2 or len(self.game.player_strategies[1]) != 2:
            return []
        
        # Extraer matriz de pagos
        # payoff_matrix[i, j] = [payoff_player1, payoff_player2]
        matrix = self.game.payoff_matrix
        
        # Pagos para jugador 1
        a11, a12 = matrix[0, 0, 0], matrix[0, 1, 0]
        a21, a22 = matrix[1, 0, 0], matrix[1, 1, 0]
        
        # Pagos para jugador 2
        b11, b12 = matrix[0, 0, 1], matrix[0, 1, 1]
        b21, b22 = matrix[1, 0, 1], matrix[1, 1, 1]
        
        mixed_equilibria = []
        
        # Calcular equilibrio mixto si existe
        # Para jugador 2: debe ser indiferente entre sus estrategias
        # p * b11 + (1-p) * b21 = p * b12 + (1-p) * b22
        # p * (b11 - b21 - b12 + b22) = b22 - b21
        
        denom_p = (b11 - b21 - b12 + b22)
        if abs(denom_p) > 1e-10:
            p = (b22 - b21) / denom_p
            
            if 0 < p < 1:
                # Calcular q para jugador 1
                denom_q = (a11 - a12 - a21 + a22)
                if abs(denom_q) > 1e-10:
                    q = (a22 - a12) / denom_q
                    
                    if 0 < q < 1:
                        # Tenemos un equilibrio mixto
                        mixed_equilibria.append({
                            0: np.array([p, 1 - p]),
                            1: np.array([q, 1 - q])
                        })
        
        self.mixed_equilibria = mixed_equilibria
        return mixed_equilibria
    
    def calculate_expected_payoff_mixed(self, player_id: int, 
                                       mixed_profile: Dict[int, np.ndarray]) -> float:
        """
        Calcula el pago esperado para un jugador bajo un perfil mixto
        
        Args:
            player_id: ID del jugador
            mixed_profile: Perfil de estrategias mixtas
            
        Returns:
            Pago esperado
        """
        if self.game.num_players != 2:
            raise ValueError("Solo implementado para juegos de 2 jugadores")
        
        expected_payoff = 0.0
        matrix = self.game.payoff_matrix
        
        # Iterar sobre todas las combinaciones de estrategias puras
        for i, prob_i in enumerate(mixed_profile[0]):
            for j, prob_j in enumerate(mixed_profile[1]):
                payoff = matrix[i, j, player_id]
                probability = prob_i * prob_j
                expected_payoff += probability * payoff
        
        return expected_payoff
    
    def verify_nash_equilibrium_mixed(self, mixed_profile: Dict[int, np.ndarray], 
                                     epsilon: float = 1e-6) -> bool:
        """
        Verifica si un perfil mixto es un equilibrio de Nash
        
        Args:
            mixed_profile: Perfil de estrategias mixtas
            epsilon: Tolerancia numérica
            
        Returns:
            True si es equilibrio de Nash
        """
        for player_id in range(self.game.num_players):
            current_payoff = self.calculate_expected_payoff_mixed(player_id, mixed_profile)
            
            # Probar desviaciones puras
            for strategy_idx in range(len(self.game.player_strategies[player_id])):
                # Crear perfil desviado
                deviation_profile = mixed_profile.copy()
                pure_strategy = np.zeros(len(self.game.player_strategies[player_id]))
                pure_strategy[strategy_idx] = 1.0
                deviation_profile[player_id] = pure_strategy
                
                deviation_payoff = self.calculate_expected_payoff_mixed(
                    player_id, deviation_profile
                )
                
                # Si la desviación es mejor, no es equilibrio
                if deviation_payoff > current_payoff + epsilon:
                    return False
        
        return True
    
    def get_all_equilibria(self) -> Dict[str, List]:
        """
        Encuentra todos los equilibrios (puros y mixtos)
        
        Returns:
            Diccionario con equilibrios puros y mixtos
        """
        pure = self.find_pure_nash_equilibria()
        
        mixed = []
        if self.game.num_players == 2 and all(
            len(strategies) == 2 for strategies in self.game.player_strategies
        ):
            mixed = self.find_mixed_nash_equilibria_2x2()
        
        return {
            'pure': pure,
            'mixed': mixed
        }
    
    def analyze_equilibrium_payoffs(self) -> Dict[str, Any]:
        """
        Analiza los pagos de todos los equilibrios encontrados
        
        Returns:
            Análisis detallado de pagos
        """
        all_eq = self.get_all_equilibria()
        
        analysis = {
            'pure_equilibria': [],
            'mixed_equilibria': [],
            'summary': {}
        }
        
        # Analizar equilibrios puros
        for profile in all_eq['pure']:
            payoffs = self.game.calculate_payoffs(profile)
            analysis['pure_equilibria'].append({
                'strategies': profile.strategies,
                'payoffs': payoffs,
                'total_welfare': sum(payoffs.values())
            })
        
        # Analizar equilibrios mixtos
        for mixed_profile in all_eq['mixed']:
            payoffs = {
                pid: self.calculate_expected_payoff_mixed(pid, mixed_profile)
                for pid in range(self.game.num_players)
            }
            analysis['mixed_equilibria'].append({
                'probabilities': {
                    pid: mixed_profile[pid].tolist()
                    for pid in mixed_profile
                },
                'expected_payoffs': payoffs,
                'total_welfare': sum(payoffs.values())
            })
        
        # Resumen
        analysis['summary'] = {
            'num_pure_equilibria': len(all_eq['pure']),
            'num_mixed_equilibria': len(all_eq['mixed']),
            'total_equilibria': len(all_eq['pure']) + len(all_eq['mixed'])
        }
        
        return analysis
    
    def get_support_enumeration_method(self) -> List[Dict[int, np.ndarray]]:
        """
        Método de enumeración de soportes para encontrar equilibrios mixtos
        (Implementación simplificada para juegos pequeños)
        
        Returns:
            Lista de equilibrios mixtos
        """
        # Implementación simplificada - solo para juegos 2x2
        if self.game.num_players == 2 and all(
            len(strategies) == 2 for strategies in self.game.player_strategies
        ):
            return self.find_mixed_nash_equilibria_2x2()
        
        return []
