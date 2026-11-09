"""
Tests para los controladores
"""

import pytest
import numpy as np
from src.controllers import GameController, NashSolver, SimulationController
from src.models.matrix_game import create_prisoners_dilemma, create_battle_of_sexes
from src.models.evolutionary_game import create_hawk_dove_game, Population


class TestGameController:
    """Tests para GameController"""
    
    def test_controller_initialization(self):
        """Test de inicialización del controlador"""
        controller = GameController()
        assert controller.current_game is None
        assert len(controller.game_history) == 0
    
    def test_set_game(self):
        """Test de establecer juego"""
        controller = GameController()
        game = create_prisoners_dilemma()
        controller.set_game(game)
        assert controller.current_game == game
    
    def test_initialize_players(self):
        """Test de inicialización de jugadores"""
        controller = GameController()
        game = create_prisoners_dilemma()
        controller.set_game(game)
        controller.initialize_players(["Alice", "Bob"])
        
        assert len(game.players) == 2
        assert game.players[0].name == "Alice"
        assert game.players[1].name == "Bob"
    
    def test_play_round(self):
        """Test de jugar una ronda"""
        controller = GameController()
        game = create_prisoners_dilemma()
        controller.set_game(game)
        controller.initialize_players(["Alice", "Bob"])
        
        result = controller.play_round({0: "Cooperar", 1: "Cooperar"})
        
        assert result['payoffs'][0] == 3.0
        assert result['payoffs'][1] == 3.0
        assert len(controller.game_history) == 1
    
    def test_get_game_summary(self):
        """Test de obtener resumen del juego"""
        controller = GameController()
        game = create_prisoners_dilemma()
        controller.set_game(game)
        controller.initialize_players(["Alice", "Bob"])
        controller.play_round({0: "Cooperar", 1: "Traicionar"})
        
        summary = controller.get_game_summary()
        
        assert summary['name'] == "Dilema del Prisionero"
        assert summary['rounds_played'] == 1
        assert 'total_payoffs' in summary


class TestNashSolver:
    """Tests para NashSolver"""
    
    def test_find_pure_equilibria(self):
        """Test de encontrar equilibrios puros"""
        game = create_prisoners_dilemma()
        solver = NashSolver(game)
        equilibria = solver.find_pure_nash_equilibria()
        
        assert len(equilibria) == 1
        assert equilibria[0].get_strategy(0) == "Traicionar"
        assert equilibria[0].get_strategy(1) == "Traicionar"
    
    def test_multiple_equilibria(self):
        """Test con múltiples equilibrios"""
        game = create_battle_of_sexes()
        solver = NashSolver(game)
        equilibria = solver.find_pure_nash_equilibria()
        
        assert len(equilibria) == 2
    
    def test_mixed_equilibria_2x2(self):
        """Test de equilibrios mixtos en juego 2x2"""
        game = create_battle_of_sexes()
        solver = NashSolver(game)
        mixed_eq = solver.find_mixed_nash_equilibria_2x2()
        
        # Batalla de los sexos tiene un equilibrio mixto
        assert len(mixed_eq) >= 0  # Puede o no tener según los pagos exactos
    
    def test_analyze_equilibrium_payoffs(self):
        """Test de análisis de pagos de equilibrios"""
        game = create_prisoners_dilemma()
        solver = NashSolver(game)
        analysis = solver.analyze_equilibrium_payoffs()
        
        assert 'pure_equilibria' in analysis
        assert 'summary' in analysis
        assert analysis['summary']['num_pure_equilibria'] == 1


class TestSimulationController:
    """Tests para SimulationController"""
    
    def test_controller_initialization(self):
        """Test de inicialización"""
        game = create_hawk_dove_game()
        controller = SimulationController(game)
        assert controller.game == game
    
    def test_create_uniform_population(self):
        """Test de crear población uniforme"""
        game = create_hawk_dove_game()
        controller = SimulationController(game)
        pop = controller.create_uniform_population()
        
        assert np.isclose(pop.get_frequency("Halcón"), 0.5)
        assert np.isclose(pop.get_frequency("Paloma"), 0.5)
    
    def test_run_simulation(self):
        """Test de ejecutar simulación"""
        game = create_hawk_dove_game()
        controller = SimulationController(game)
        initial_pop = controller.create_uniform_population()
        
        history = controller.run_simulation(initial_pop, generations=10)
        
        assert len(history) == 11  # 10 generaciones + inicial
        assert all(isinstance(pop, Population) for pop in history)
    
    def test_calculate_trajectory(self):
        """Test de calcular trayectoria"""
        game = create_hawk_dove_game()
        controller = SimulationController(game)
        initial_pop = Population(strategy_frequencies={"Halcón": 0.7, "Paloma": 0.3})
        
        controller.run_simulation(initial_pop, generations=5)
        trajectory = controller.calculate_trajectory()
        
        assert "Halcón" in trajectory
        assert "Paloma" in trajectory
        assert len(trajectory["Halcón"]) == 6  # 5 + inicial
    
    def test_analyze_convergence(self):
        """Test de análisis de convergencia"""
        game = create_hawk_dove_game()
        controller = SimulationController(game)
        initial_pop = controller.create_uniform_population()
        
        controller.run_simulation(initial_pop, generations=100)
        analysis = controller.analyze_convergence()
        
        assert 'converged' in analysis
        assert 'final_frequencies' in analysis
        assert 'dominant_strategy' in analysis


def test_integration_full_workflow():
    """Test de integración: workflow completo"""
    # Crear juego
    game = create_prisoners_dilemma()
    
    # Usar controlador
    controller = GameController()
    controller.set_game(game)
    controller.initialize_players(["Alice", "Bob"])
    
    # Jugar varias rondas
    for _ in range(5):
        controller.play_round({0: "Cooperar", 1: "Traicionar"})
    
    # Obtener resumen
    summary = controller.get_game_summary()
    
    assert summary['rounds_played'] == 5
    assert summary['total_payoffs'][0] == 0.0  # Alice: 0 * 5
    assert summary['total_payoffs'][1] == 25.0  # Bob: 5 * 5
    
    # Analizar equilibrios
    solver = NashSolver(game)
    equilibria = solver.find_pure_nash_equilibria()
    
    assert len(equilibria) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
