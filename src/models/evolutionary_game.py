"""
Implementación de juegos evolutivos y dinámicas de replicadores
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from .game import Game
from .player import StrategyProfile


@dataclass
class Population:
    """Representa una población con distribución de estrategias"""
    strategy_frequencies: Dict[str, float]  # estrategia -> frecuencia
    total_fitness: float = 0.0
    generation: int = 0
    
    def __post_init__(self):
        """Valida que las frecuencias sumen 1"""
        total = sum(self.strategy_frequencies.values())
        if not np.isclose(total, 1.0):
            # Normalizar
            self.strategy_frequencies = {
                s: f / total for s, f in self.strategy_frequencies.items()
            }
    
    def get_frequency(self, strategy: str) -> float:
        """Obtiene la frecuencia de una estrategia"""
        return self.strategy_frequencies.get(strategy, 0.0)
    
    def update_frequency(self, strategy: str, new_frequency: float) -> None:
        """Actualiza la frecuencia de una estrategia"""
        self.strategy_frequencies[strategy] = new_frequency
    
    def copy(self) -> 'Population':
        """Crea una copia de la población"""
        return Population(
            strategy_frequencies=self.strategy_frequencies.copy(),
            total_fitness=self.total_fitness,
            generation=self.generation
        )


class EvolutionaryGame(Game):
    """Juego evolutivo con dinámicas de replicadores"""
    
    def __init__(self, name: str, description: str, strategies: List[str], 
                 payoff_function: Callable[[str, str], float]):
        """
        Inicializa un juego evolutivo
        
        Args:
            name: Nombre del juego
            description: Descripción del juego
            strategies: Lista de estrategias disponibles
            payoff_function: Función que calcula el pago de jugar estrategia i contra j
        """
        super().__init__(name, description, num_players=2)  # Juegos simétricos de 2 jugadores
        
        self.strategies = strategies
        self.payoff_function = payoff_function
        self.population_history: List[Population] = []
        
        # Construir matriz de pagos
        self.payoff_matrix = np.zeros((len(strategies), len(strategies)))
        for i, s1 in enumerate(strategies):
            for j, s2 in enumerate(strategies):
                self.payoff_matrix[i, j] = payoff_function(s1, s2)
    
    def calculate_payoffs(self, strategy_profile: StrategyProfile) -> Dict[int, float]:
        """
        Calcula pagos para un encuentro específico
        
        Args:
            strategy_profile: Perfil de estrategias
            
        Returns:
            Diccionario de pagos
        """
        s1 = strategy_profile.get_strategy(0)
        s2 = strategy_profile.get_strategy(1)
        
        payoff_1 = self.payoff_function(s1, s2)
        payoff_2 = self.payoff_function(s2, s1)
        
        return {0: payoff_1, 1: payoff_2}
    
    def get_best_response(self, player_id: int, others_strategies: Dict[int, str]) -> str:
        """
        Calcula la mejor respuesta contra una estrategia específica
        
        Args:
            player_id: ID del jugador
            others_strategies: Estrategias de otros jugadores
            
        Returns:
            Mejor estrategia
        """
        opponent_strategy = list(others_strategies.values())[0]
        best_payoff = float('-inf')
        best_strategy = self.strategies[0]
        
        for strategy in self.strategies:
            payoff = self.payoff_function(strategy, opponent_strategy)
            if payoff > best_payoff:
                best_payoff = payoff
                best_strategy = strategy
        
        return best_strategy
    
    def find_nash_equilibria(self) -> List[StrategyProfile]:
        """
        Encuentra equilibrios de Nash puros en el juego simétrico
        
        Returns:
            Lista de equilibrios
        """
        equilibria = []
        
        for s1 in self.strategies:
            for s2 in self.strategies:
                # Verificar si (s1, s2) es equilibrio de Nash
                profile = StrategyProfile(strategies={0: s1, 1: s2})
                
                if self.is_nash_equilibrium(profile):
                    payoffs = self.calculate_payoffs(profile)
                    profile.payoffs = payoffs
                    equilibria.append(profile)
        
        return equilibria
    
    def calculate_fitness(self, strategy: str, population: Population) -> float:
        """
        Calcula el fitness de una estrategia en una población
        
        Args:
            strategy: Estrategia a evaluar
            population: Población actual
            
        Returns:
            Fitness esperado
        """
        fitness = 0.0
        strategy_idx = self.strategies.index(strategy)
        
        for opponent_strategy, frequency in population.strategy_frequencies.items():
            opponent_idx = self.strategies.index(opponent_strategy)
            fitness += frequency * self.payoff_matrix[strategy_idx, opponent_idx]
        
        return fitness
    
    def calculate_average_fitness(self, population: Population) -> float:
        """
        Calcula el fitness promedio de la población
        
        Args:
            population: Población actual
            
        Returns:
            Fitness promedio
        """
        avg_fitness = 0.0
        
        for strategy, frequency in population.strategy_frequencies.items():
            fitness = self.calculate_fitness(strategy, population)
            avg_fitness += frequency * fitness
        
        return avg_fitness
    
    def replicator_dynamics_step(self, population: Population, dt: float = 0.1) -> Population:
        """
        Ejecuta un paso de la dinámica de replicadores
        
        Args:
            population: Población actual
            dt: Paso de tiempo
            
        Returns:
            Nueva población después del paso
        """
        new_pop = population.copy()
        avg_fitness = self.calculate_average_fitness(population)
        
        for strategy in self.strategies:
            current_freq = population.get_frequency(strategy)
            strategy_fitness = self.calculate_fitness(strategy, population)
            
            # Ecuación de replicadores: dx/dt = x * (f(x) - f_avg)
            delta = current_freq * (strategy_fitness - avg_fitness) * dt
            new_freq = max(0.0, min(1.0, current_freq + delta))
            
            new_pop.update_frequency(strategy, new_freq)
        
        # Renormalizar
        total = sum(new_pop.strategy_frequencies.values())
        for strategy in self.strategies:
            new_pop.strategy_frequencies[strategy] /= total
        
        new_pop.total_fitness = self.calculate_average_fitness(new_pop)
        new_pop.generation = population.generation + 1
        
        return new_pop
    
    def simulate_evolution(self, initial_population: Population, 
                          generations: int = 100, dt: float = 0.1) -> List[Population]:
        """
        Simula la evolución de la población
        
        Args:
            initial_population: Población inicial
            generations: Número de generaciones
            dt: Paso de tiempo
            
        Returns:
            Historia de poblaciones
        """
        self.population_history = [initial_population]
        current_pop = initial_population
        
        for _ in range(generations):
            current_pop = self.replicator_dynamics_step(current_pop, dt)
            self.population_history.append(current_pop)
        
        return self.population_history
    
    def find_evolutionarily_stable_strategies(self) -> List[str]:
        """
        Encuentra estrategias evolutivamente estables (ESS)
        
        Returns:
            Lista de ESS
        """
        ess_list = []
        
        for candidate in self.strategies:
            is_ess = True
            candidate_idx = self.strategies.index(candidate)
            
            # Verificar condiciones ESS
            for mutant in self.strategies:
                if mutant == candidate:
                    continue
                
                mutant_idx = self.strategies.index(mutant)
                
                # Pago de candidato contra sí mismo vs mutante contra candidato
                payoff_cc = self.payoff_matrix[candidate_idx, candidate_idx]
                payoff_mc = self.payoff_matrix[mutant_idx, candidate_idx]
                
                # Primera condición: E(c,c) >= E(m,c)
                if payoff_cc < payoff_mc:
                    is_ess = False
                    break
                
                # Si son iguales, verificar segunda condición
                if np.isclose(payoff_cc, payoff_mc):
                    payoff_cm = self.payoff_matrix[candidate_idx, mutant_idx]
                    payoff_mm = self.payoff_matrix[mutant_idx, mutant_idx]
                    
                    # Segunda condición: E(c,m) > E(m,m)
                    if payoff_cm <= payoff_mm:
                        is_ess = False
                        break
            
            if is_ess:
                ess_list.append(candidate)
        
        return ess_list
    
    def is_stable_equilibrium(self, population: Population, epsilon: float = 0.01) -> bool:
        """
        Verifica si una población está en equilibrio estable
        
        Args:
            population: Población a verificar
            epsilon: Tolerancia para considerar estabilidad
            
        Returns:
            True si está en equilibrio estable
        """
        avg_fitness = self.calculate_average_fitness(population)
        
        for strategy, frequency in population.strategy_frequencies.items():
            if frequency > epsilon:
                strategy_fitness = self.calculate_fitness(strategy, population)
                if not np.isclose(strategy_fitness, avg_fitness, atol=epsilon):
                    return False
        
        return True


def create_hawk_dove_game(value: float = 4.0, cost: float = 6.0) -> EvolutionaryGame:
    """
    Crea el juego Halcón-Paloma (Hawk-Dove)
    
    Args:
        value: Valor del recurso
        cost: Costo de pelear
        
    Returns:
        Juego Halcón-Paloma
    """
    def payoff_function(s1: str, s2: str) -> float:
        if s1 == "Halcón" and s2 == "Halcón":
            return (value - cost) / 2
        elif s1 == "Halcón" and s2 == "Paloma":
            return value
        elif s1 == "Paloma" and s2 == "Halcón":
            return 0
        else:  # Paloma vs Paloma
            return value / 2
    
    return EvolutionaryGame(
        name="Halcón-Paloma",
        description=f"Competencia por un recurso de valor {value}. Pelear cuesta {cost}.",
        strategies=["Halcón", "Paloma"],
        payoff_function=payoff_function
    )


def create_rock_paper_scissors_game() -> EvolutionaryGame:
    """Crea el juego Piedra-Papel-Tijera evolutivo"""
    def payoff_function(s1: str, s2: str) -> float:
        if s1 == s2:
            return 0
        elif (s1 == "Piedra" and s2 == "Tijera") or \
             (s1 == "Papel" and s2 == "Piedra") or \
             (s1 == "Tijera" and s2 == "Papel"):
            return 1
        else:
            return -1
    
    return EvolutionaryGame(
        name="Piedra-Papel-Tijera",
        description="Versión evolutiva del clásico juego de manos.",
        strategies=["Piedra", "Papel", "Tijera"],
        payoff_function=payoff_function
    )


def create_coordination_game(high_payoff: float = 5.0, low_payoff: float = 2.0) -> EvolutionaryGame:
    """
    Crea un juego de coordinación
    
    Args:
        high_payoff: Pago por coordinación en estrategia alta
        low_payoff: Pago por coordinación en estrategia baja
        
    Returns:
        Juego de coordinación
    """
    def payoff_function(s1: str, s2: str) -> float:
        if s1 == s2 == "A":
            return high_payoff
        elif s1 == s2 == "B":
            return low_payoff
        else:
            return 0
    
    return EvolutionaryGame(
        name="Juego de Coordinación",
        description="Ambos jugadores se benefician de coordinarse, pero hay dos equilibrios.",
        strategies=["A", "B"],
        payoff_function=payoff_function
    )
