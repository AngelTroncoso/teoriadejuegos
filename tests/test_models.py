"""
Tests unitarios para los modelos
"""

import pytest
import numpy as np
from src.models.player import Player, StrategyProfile
from src.models.matrix_game import (
    MatrixGame,
    create_prisoners_dilemma,
    create_battle_of_sexes
)
from src.models.evolutionary_game import create_hawk_dove_game, Population


class TestPlayer:
    """Tests para la clase Player"""
    
    def test_player_creation(self):
        """Test de creación de jugador"""
        player = Player(name="Alice", player_id=0)
        assert player.name == "Alice"
        assert player.player_id == 0
        assert player.payoff == 0.0
    
    def test_add_strategy(self):
        """Test de añadir estrategias"""
        player = Player(name="Bob", player_id=1)
        player.add_strategy("Cooperar")
        player.add_strategy("Traicionar")
        assert len(player.strategies) == 2
        assert "Cooperar" in player.strategies
    
    def test_update_payoff(self):
        """Test de actualización de pagos"""
        player = Player(name="Charlie", player_id=2)
        player.update_payoff(5.0)
        assert player.payoff == 5.0
        player.update_payoff(3.0)
        assert player.payoff == 8.0


class TestStrategyProfile:
    """Tests para StrategyProfile"""
    
    def test_profile_creation(self):
        """Test de creación de perfil"""
        profile = StrategyProfile(strategies={0: "A", 1: "B"})
        assert profile.get_strategy(0) == "A"
        assert profile.get_strategy(1) == "B"
    
    def test_payoffs(self):
        """Test de pagos en perfil"""
        profile = StrategyProfile(strategies={0: "A", 1: "B"})
        profile.set_payoff(0, 3.0)
        profile.set_payoff(1, 2.0)
        assert profile.get_payoff(0) == 3.0
        assert profile.get_payoff(1) == 2.0


class TestMatrixGame:
    """Tests para juegos de matriz"""
    
    def test_prisoners_dilemma_creation(self):
        """Test de creación del dilema del prisionero"""
        game = create_prisoners_dilemma()
        assert game.name == "Dilema del Prisionero"
        assert game.num_players == 2
        assert game.payoff_matrix.shape == (2, 2, 2)
    
    def test_prisoners_dilemma_nash(self):
        """Test de equilibrio de Nash en dilema del prisionero"""
        game = create_prisoners_dilemma()
        equilibria = game.find_nash_equilibria()
        
        assert len(equilibria) == 1
        eq = equilibria[0]
        assert eq.get_strategy(0) == "Traicionar"
        assert eq.get_strategy(1) == "Traicionar"
    
    def test_calculate_payoffs(self):
        """Test de cálculo de pagos"""
        game = create_prisoners_dilemma()
        profile = StrategyProfile(strategies={0: "Cooperar", 1: "Cooperar"})
        payoffs = game.calculate_payoffs(profile)
        
        assert payoffs[0] == 3.0
        assert payoffs[1] == 3.0
    
    def test_battle_of_sexes_equilibria(self):
        """Test de múltiples equilibrios"""
        game = create_battle_of_sexes()
        equilibria = game.find_nash_equilibria()
        
        assert len(equilibria) == 2  # Dos equilibrios puros
    
    def test_dominant_strategies(self):
        """Test de estrategias dominantes"""
        game = create_prisoners_dilemma()
        dominant = game.find_dominant_strategies()
        
        assert dominant[0] == "Traicionar"
        assert dominant[1] == "Traicionar"


class TestEvolutionaryGame:
    """Tests para juegos evolutivos"""
    
    def test_hawk_dove_creation(self):
        """Test de creación de juego Halcón-Paloma"""
        game = create_hawk_dove_game(value=4.0, cost=6.0)
        assert len(game.strategies) == 2
        assert "Halcón" in game.strategies
        assert "Paloma" in game.strategies
    
    def test_population_creation(self):
        """Test de creación de población"""
        pop = Population(strategy_frequencies={"A": 0.6, "B": 0.4})
        assert pop.get_frequency("A") == 0.6
        assert pop.get_frequency("B") == 0.4
    
    def test_population_normalization(self):
        """Test de normalización de población"""
        pop = Population(strategy_frequencies={"A": 3.0, "B": 2.0})
        # Debe normalizar a 0.6 y 0.4
        assert np.isclose(pop.get_frequency("A"), 0.6)
        assert np.isclose(pop.get_frequency("B"), 0.4)
    
    def test_fitness_calculation(self):
        """Test de cálculo de fitness"""
        game = create_hawk_dove_game(value=4.0, cost=6.0)
        pop = Population(strategy_frequencies={"Halcón": 0.5, "Paloma": 0.5})
        
        fitness_hawk = game.calculate_fitness("Halcón", pop)
        fitness_dove = game.calculate_fitness("Paloma", pop)
        
        assert isinstance(fitness_hawk, float)
        assert isinstance(fitness_dove, float)


def test_integration_full_game():
    """Test de integración: juego completo"""
    from src.controllers import GameController
    
    game = create_prisoners_dilemma()
    controller = GameController()
    controller.set_game(game)
    controller.initialize_players(["Alice", "Bob"])
    
    result = controller.play_round({0: "Cooperar", 1: "Traicionar"})
    
    assert result['payoffs'][0] == 0.0
    assert result['payoffs'][1] == 5.0
    assert not result['is_nash_equilibrium']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
