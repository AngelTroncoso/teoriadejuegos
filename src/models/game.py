"""
Clase base abstracta para todos los juegos
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
import numpy as np
from .player import Player, StrategyProfile


class Game(ABC):
    """Clase base abstracta para juegos de teoría de juegos"""
    
    def __init__(self, name: str, description: str, num_players: int):
        """
        Inicializa un juego
        
        Args:
            name: Nombre del juego
            description: Descripción del juego
            num_players: Número de jugadores
        """
        self.name = name
        self.description = description
        self.num_players = num_players
        self.players: List[Player] = []
        self.history: List[StrategyProfile] = []
        self._is_initialized = False
    
    def add_player(self, player: Player) -> None:
        """
        Añade un jugador al juego
        
        Args:
            player: Instancia de Player a añadir
        """
        if len(self.players) >= self.num_players:
            raise ValueError(f"El juego ya tiene el máximo de {self.num_players} jugadores")
        self.players.append(player)
        if len(self.players) == self.num_players:
            self._is_initialized = True
    
    def get_player(self, player_id: int) -> Optional[Player]:
        """
        Obtiene un jugador por su ID
        
        Args:
            player_id: ID del jugador
            
        Returns:
            Player o None si no existe
        """
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    @abstractmethod
    def calculate_payoffs(self, strategy_profile: StrategyProfile) -> Dict[int, float]:
        """
        Calcula los pagos para un perfil de estrategias dado
        
        Args:
            strategy_profile: Perfil de estrategias de todos los jugadores
            
        Returns:
            Diccionario con pagos para cada jugador
        """
        pass
    
    @abstractmethod
    def get_best_response(self, player_id: int, others_strategies: Dict[int, str]) -> str:
        """
        Calcula la mejor respuesta para un jugador dadas las estrategias de los demás
        
        Args:
            player_id: ID del jugador
            others_strategies: Estrategias de los otros jugadores
            
        Returns:
            Nombre de la mejor estrategia
        """
        pass
    
    @abstractmethod
    def find_nash_equilibria(self) -> List[StrategyProfile]:
        """
        Encuentra todos los equilibrios de Nash del juego
        
        Returns:
            Lista de perfiles de estrategia en equilibrio de Nash
        """
        pass
    
    def is_nash_equilibrium(self, strategy_profile: StrategyProfile) -> bool:
        """
        Verifica si un perfil de estrategias es un equilibrio de Nash
        
        Un perfil (s1, s2, ..., sn) es equilibrio de Nash puro si y solo si:
        Para cada jugador i: payoff_i(si, s-i) >= payoff_i(si', s-i) para toda estrategia alternativa si'
        
        Args:
            strategy_profile: Perfil de estrategias a verificar
            
        Returns:
            True si es equilibrio de Nash, False en caso contrario
        """
        # Iterar sobre IDs de jugadores en lugar de self.players
        for player_id in range(self.num_players):
            # Construir diccionario con estrategias de los otros jugadores
            others = {pid: strategy_profile.get_strategy(pid) 
                     for pid in range(self.num_players) if pid != player_id}
            
            # Obtener mejor respuesta del jugador dado lo que hacen los demás
            best_response = self.get_best_response(player_id, others)
            
            # Si la mejor respuesta no coincide con la estrategia actual, no es equilibrio
            if best_response != strategy_profile.get_strategy(player_id):
                return False
        
        return True
    
    def play_round(self, strategies: Dict[int, str]) -> Dict[int, float]:
        """
        Juega una ronda del juego con las estrategias especificadas
        
        Args:
            strategies: Diccionario de player_id -> estrategia
            
        Returns:
            Pagos resultantes para cada jugador
        """
        strategy_profile = StrategyProfile(strategies=strategies)
        payoffs = self.calculate_payoffs(strategy_profile)
        strategy_profile.payoffs = payoffs
        self.history.append(strategy_profile)
        
        # Actualizar pagos de jugadores
        for player_id, payoff in payoffs.items():
            player = self.get_player(player_id)
            if player:
                player.update_payoff(payoff)
        
        return payoffs
    
    def reset_game(self) -> None:
        """Reinicia el juego limpiando historial y pagos"""
        self.history.clear()
        for player in self.players:
            player.reset_payoff()
    
    def get_game_summary(self) -> Dict:
        """
        Obtiene un resumen del estado actual del juego
        
        Returns:
            Diccionario con información del juego
        """
        return {
            'name': self.name,
            'description': self.description,
            'num_players': self.num_players,
            'rounds_played': len(self.history),
            'players': [
                {
                    'name': p.name,
                    'id': p.player_id,
                    'total_payoff': p.payoff,
                    'strategies': p.strategies
                }
                for p in self.players
            ]
        }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', players={len(self.players)})"
    
    def __str__(self) -> str:
        return f"{self.name} - {self.description}"
