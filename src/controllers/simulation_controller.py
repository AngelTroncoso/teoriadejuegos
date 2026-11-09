"""
Controlador para simulaciones evolutivas y dinámicas
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from src.models import EvolutionaryGame
from src.models.evolutionary_game import Population


class SimulationController:
    """Controlador para gestionar simulaciones evolutivas"""
    
    def __init__(self, game: EvolutionaryGame):
        """
        Inicializa el controlador de simulación
        
        Args:
            game: Juego evolutivo a simular
        """
        self.game = game
        self.current_population: Optional[Population] = None
        self.simulation_history: List[Population] = []
    
    def create_uniform_population(self) -> Population:
        """
        Crea una población con frecuencias uniformes
        
        Returns:
            Población uniforme
        """
        n_strategies = len(self.game.strategies)
        freq = 1.0 / n_strategies
        
        return Population(
            strategy_frequencies={s: freq for s in self.game.strategies},
            generation=0
        )
    
    def create_custom_population(self, frequencies: Dict[str, float]) -> Population:
        """
        Crea una población con frecuencias personalizadas
        
        Args:
            frequencies: Diccionario de estrategia -> frecuencia
            
        Returns:
            Población personalizada
        """
        # Validar que todas las estrategias estén presentes
        for strategy in self.game.strategies:
            if strategy not in frequencies:
                frequencies[strategy] = 0.0
        
        return Population(
            strategy_frequencies=frequencies,
            generation=0
        )
    
    def run_simulation(self, initial_population: Population, 
                      generations: int = 100, dt: float = 0.1) -> List[Population]:
        """
        Ejecuta una simulación evolutiva
        
        Args:
            initial_population: Población inicial
            generations: Número de generaciones
            dt: Paso de tiempo
            
        Returns:
            Historia de poblaciones
        """
        self.current_population = initial_population
        self.simulation_history = self.game.simulate_evolution(
            initial_population, generations, dt
        )
        
        return self.simulation_history
    
    def get_population_at_generation(self, generation: int) -> Optional[Population]:
        """
        Obtiene el estado de la población en una generación específica
        
        Args:
            generation: Número de generación
            
        Returns:
            Población en esa generación o None
        """
        if 0 <= generation < len(self.simulation_history):
            return self.simulation_history[generation]
        return None
    
    def calculate_trajectory(self) -> Dict[str, List[float]]:
        """
        Calcula la trayectoria de frecuencias de cada estrategia
        
        Returns:
            Diccionario de estrategia -> lista de frecuencias por generación
        """
        trajectory = {strategy: [] for strategy in self.game.strategies}
        
        for population in self.simulation_history:
            for strategy in self.game.strategies:
                trajectory[strategy].append(population.get_frequency(strategy))
        
        return trajectory
    
    def find_stable_states(self, tolerance: float = 0.001) -> List[Tuple[int, Population]]:
        """
        Encuentra estados estables en la simulación
        
        Args:
            tolerance: Tolerancia para considerar un estado estable
            
        Returns:
            Lista de tuplas (generación, población) en estados estables
        """
        stable_states = []
        
        for i in range(1, len(self.simulation_history)):
            prev_pop = self.simulation_history[i - 1]
            curr_pop = self.simulation_history[i]
            
            # Calcular distancia entre poblaciones
            distance = sum(
                abs(curr_pop.get_frequency(s) - prev_pop.get_frequency(s))
                for s in self.game.strategies
            )
            
            if distance < tolerance:
                stable_states.append((i, curr_pop))
        
        return stable_states
    
    def analyze_convergence(self) -> Dict[str, any]:
        """
        Analiza la convergencia de la simulación
        
        Returns:
            Análisis de convergencia
        """
        if len(self.simulation_history) < 2:
            return {}
        
        # Calcular velocidad de cambio
        changes = []
        for i in range(1, len(self.simulation_history)):
            prev = self.simulation_history[i - 1]
            curr = self.simulation_history[i]
            
            change = sum(
                abs(curr.get_frequency(s) - prev.get_frequency(s))
                for s in self.game.strategies
            )
            changes.append(change)
        
        # Determinar si converge
        recent_changes = changes[-10:] if len(changes) >= 10 else changes
        avg_recent_change = np.mean(recent_changes)
        
        converged = avg_recent_change < 0.001
        
        # Estado final
        final_pop = self.simulation_history[-1]
        
        analysis = {
            'converged': converged,
            'average_recent_change': avg_recent_change,
            'final_frequencies': final_pop.strategy_frequencies,
            'final_fitness': final_pop.total_fitness,
            'dominant_strategy': max(
                final_pop.strategy_frequencies.items(),
                key=lambda x: x[1]
            )[0] if final_pop.strategy_frequencies else None,
            'changes_over_time': changes
        }
        
        return analysis
    
    def compare_initial_conditions(self, populations: List[Population],
                                  generations: int = 100) -> List[Dict]:
        """
        Compara la evolución desde diferentes condiciones iniciales
        
        Args:
            populations: Lista de poblaciones iniciales
            generations: Número de generaciones a simular
            
        Returns:
            Lista de resultados de cada simulación
        """
        results = []
        
        for idx, pop in enumerate(populations):
            # Ejecutar simulación
            history = self.game.simulate_evolution(pop, generations)
            
            # Analizar resultado
            final_pop = history[-1]
            trajectory = {
                strategy: [p.get_frequency(strategy) for p in history]
                for strategy in self.game.strategies
            }
            
            results.append({
                'initial_id': idx,
                'initial_frequencies': pop.strategy_frequencies,
                'final_frequencies': final_pop.strategy_frequencies,
                'trajectory': trajectory,
                'final_fitness': final_pop.total_fitness
            })
        
        return results
    
    def calculate_phase_portrait_2d(self, resolution: int = 20) -> Dict:
        """
        Calcula el retrato de fase para juegos con 2 estrategias
        
        Args:
            resolution: Resolución de la malla
            
        Returns:
            Datos del retrato de fase
        """
        if len(self.game.strategies) != 2:
            return {}
        
        s1, s2 = self.game.strategies
        
        # Crear malla de puntos
        freqs = np.linspace(0, 1, resolution)
        vector_field = []
        
        for freq_s1 in freqs:
            freq_s2 = 1 - freq_s1
            
            # Crear población
            pop = Population(
                strategy_frequencies={s1: freq_s1, s2: freq_s2}
            )
            
            # Calcular dirección del flujo
            fitness_s1 = self.game.calculate_fitness(s1, pop)
            fitness_s2 = self.game.calculate_fitness(s2, pop)
            avg_fitness = self.game.calculate_average_fitness(pop)
            
            # Ecuación de replicadores
            dx = freq_s1 * (fitness_s1 - avg_fitness)
            
            vector_field.append({
                'freq_s1': freq_s1,
                'freq_s2': freq_s2,
                'dx': dx,
                'fitness_s1': fitness_s1,
                'fitness_s2': fitness_s2
            })
        
        return {
            'strategies': [s1, s2],
            'vector_field': vector_field
        }
    
    def identify_evolutionarily_stable_strategies(self) -> List[str]:
        """
        Identifica estrategias evolutivamente estables (ESS)
        
        Returns:
            Lista de ESS
        """
        return self.game.find_evolutionarily_stable_strategies()
    
    def simulate_invasion(self, resident_strategy: str, mutant_strategy: str,
                         mutant_fraction: float = 0.01, 
                         generations: int = 100) -> Dict:
        """
        Simula la invasión de una estrategia mutante
        
        Args:
            resident_strategy: Estrategia residente
            mutant_strategy: Estrategia mutante
            mutant_fraction: Fracción inicial de mutantes
            generations: Generaciones a simular
            
        Returns:
            Resultado de la invasión
        """
        # Crear población inicial
        frequencies = {s: 0.0 for s in self.game.strategies}
        frequencies[resident_strategy] = 1 - mutant_fraction
        frequencies[mutant_strategy] = mutant_fraction
        
        initial_pop = Population(strategy_frequencies=frequencies)
        
        # Ejecutar simulación
        history = self.game.simulate_evolution(initial_pop, generations)
        
        # Analizar resultado
        final_pop = history[-1]
        mutant_increased = (
            final_pop.get_frequency(mutant_strategy) > mutant_fraction
        )
        
        return {
            'resident': resident_strategy,
            'mutant': mutant_strategy,
            'initial_mutant_fraction': mutant_fraction,
            'final_mutant_fraction': final_pop.get_frequency(mutant_strategy),
            'mutant_increased': mutant_increased,
            'invasion_successful': final_pop.get_frequency(mutant_strategy) > 0.5,
            'history': history
        }
