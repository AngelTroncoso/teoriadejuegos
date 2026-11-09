"""
Modelo de Jugador en Teoría de Juegos
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class Player:
    """Representa un jugador en un juego"""
    
    name: str
    player_id: int
    strategies: List[str] = field(default_factory=list)
    payoff: float = 0.0
    is_rational: bool = True
    
    def __post_init__(self):
        """Validación posterior a la inicialización"""
        if not self.name:
            raise ValueError("El jugador debe tener un nombre")
        if self.player_id < 0:
            raise ValueError("El ID del jugador debe ser no negativo")
    
    def add_strategy(self, strategy: str) -> None:
        """
        Añade una estrategia al conjunto de estrategias del jugador
        
        Args:
            strategy: Nombre de la estrategia a añadir
        """
        if strategy not in self.strategies:
            self.strategies.append(strategy)
    
    def get_strategy_count(self) -> int:
        """Retorna el número de estrategias disponibles"""
        return len(self.strategies)
    
    def update_payoff(self, payoff: float) -> None:
        """
        Actualiza el pago acumulado del jugador
        
        Args:
            payoff: Valor del pago a añadir
        """
        self.payoff += payoff
    
    def reset_payoff(self) -> None:
        """Reinicia el pago acumulado a cero"""
        self.payoff = 0.0
    
    def __repr__(self) -> str:
        return f"Player(name='{self.name}', id={self.player_id}, strategies={self.strategies})"
    
    def __str__(self) -> str:
        return f"{self.name} (ID: {self.player_id})"


@dataclass
class StrategyProfile:
    """Perfil de estrategias para todos los jugadores"""
    
    strategies: Dict[int, str]  # player_id -> strategy
    payoffs: Dict[int, float] = field(default_factory=dict)
    
    def get_strategy(self, player_id: int) -> Optional[str]:
        """Obtiene la estrategia de un jugador específico"""
        return self.strategies.get(player_id)
    
    def get_payoff(self, player_id: int) -> Optional[float]:
        """Obtiene el pago de un jugador específico"""
        return self.payoffs.get(player_id)
    
    def set_payoff(self, player_id: int, payoff: float) -> None:
        """Establece el pago para un jugador"""
        self.payoffs[player_id] = payoff
    
    def __repr__(self) -> str:
        return f"StrategyProfile(strategies={self.strategies}, payoffs={self.payoffs})"
