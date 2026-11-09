"""
Implementación de juegos secuenciales (forma extensiva)
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import numpy as np
from .game import Game
from .player import StrategyProfile


@dataclass
class GameNode:
    """Nodo en el árbol de juego"""
    node_id: int
    player_id: int  # -1 para nodos terminales
    parent: Optional['GameNode'] = None
    children: Dict[str, 'GameNode'] = field(default_factory=dict)
    payoffs: Optional[Dict[int, float]] = None
    information_set: Optional[str] = None
    
    def is_terminal(self) -> bool:
        """Verifica si es un nodo terminal"""
        return len(self.children) == 0
    
    def add_child(self, action: str, child: 'GameNode') -> None:
        """Añade un nodo hijo"""
        self.children[action] = child
        child.parent = self


class SequentialGame(Game):
    """Juego en forma extensiva (secuencial)"""
    
    def __init__(self, name: str, description: str, num_players: int):
        """
        Inicializa un juego secuencial
        
        Args:
            name: Nombre del juego
            description: Descripción del juego
            num_players: Número de jugadores
        """
        super().__init__(name, description, num_players)
        self.root: Optional[GameNode] = None
        self.nodes: Dict[int, GameNode] = {}
        self.next_node_id = 0
    
    def create_node(self, player_id: int, information_set: Optional[str] = None) -> GameNode:
        """
        Crea un nuevo nodo en el juego
        
        Args:
            player_id: ID del jugador que mueve en este nodo (-1 para terminal)
            information_set: Conjunto de información al que pertenece
            
        Returns:
            Nuevo nodo creado
        """
        node = GameNode(
            node_id=self.next_node_id,
            player_id=player_id,
            information_set=information_set
        )
        self.nodes[node.node_id] = node
        self.next_node_id += 1
        return node
    
    def set_root(self, node: GameNode) -> None:
        """Establece el nodo raíz del árbol"""
        self.root = node
    
    def set_terminal_payoffs(self, node: GameNode, payoffs: Dict[int, float]) -> None:
        """
        Establece los pagos para un nodo terminal
        
        Args:
            node: Nodo terminal
            payoffs: Pagos para cada jugador
        """
        if not node.is_terminal():
            raise ValueError("Solo se pueden establecer pagos en nodos terminales")
        node.payoffs = payoffs
    
    def calculate_payoffs(self, strategy_profile: StrategyProfile) -> Dict[int, float]:
        """
        Calcula los pagos siguiendo un perfil de estrategias desde la raíz
        
        Args:
            strategy_profile: Perfil de estrategias
            
        Returns:
            Pagos finales
        """
        if self.root is None:
            raise ValueError("El juego no tiene un nodo raíz definido")
        
        current_node = self.root
        path = []
        
        # Navegar por el árbol siguiendo las estrategias
        while not current_node.is_terminal():
            player_id = current_node.player_id
            strategy = strategy_profile.get_strategy(player_id)
            
            if strategy not in current_node.children:
                raise ValueError(f"Estrategia '{strategy}' no disponible en nodo {current_node.node_id}")
            
            path.append((current_node.node_id, strategy))
            current_node = current_node.children[strategy]
        
        return current_node.payoffs.copy()
    
    def get_best_response(self, player_id: int, others_strategies: Dict[int, str]) -> str:
        """
        Calcula la mejor respuesta usando backward induction
        
        Args:
            player_id: ID del jugador
            others_strategies: Estrategias de los otros jugadores
            
        Returns:
            Mejor estrategia
        """
        # Para juegos secuenciales, esto es más complejo
        # Implementación simplificada: evaluar todas las estrategias posibles
        best_payoff = float('-inf')
        best_strategy = None
        
        # Obtener todas las acciones posibles del jugador
        player_actions = self._get_player_actions(player_id)
        
        for action in player_actions:
            strategies = others_strategies.copy()
            strategies[player_id] = action
            profile = StrategyProfile(strategies=strategies)
            
            try:
                payoffs = self.calculate_payoffs(profile)
                if payoffs[player_id] > best_payoff:
                    best_payoff = payoffs[player_id]
                    best_strategy = action
            except ValueError:
                continue
        
        return best_strategy if best_strategy else player_actions[0] if player_actions else ""
    
    def find_nash_equilibria(self) -> List[StrategyProfile]:
        """
        Encuentra equilibrios de Nash usando backward induction
        
        Returns:
            Lista de equilibrios de Nash
        """
        if self.root is None:
            return []
        
        # Backward induction
        subgame_perfect_path = self._backward_induction(self.root)
        
        if subgame_perfect_path:
            equilibria = [StrategyProfile(strategies=subgame_perfect_path)]
            return equilibria
        
        return []
    
    def _backward_induction(self, node: GameNode) -> Optional[Dict[int, str]]:
        """
        Implementa backward induction para encontrar el equilibrio perfecto en subjuegos
        
        Args:
            node: Nodo desde el cual comenzar
            
        Returns:
            Diccionario de estrategias óptimas
        """
        if node.is_terminal():
            return {}
        
        player_id = node.player_id
        best_action = None
        best_payoff = float('-inf')
        best_continuation = None
        
        for action, child in node.children.items():
            continuation = self._backward_induction(child)
            
            if child.is_terminal():
                payoff = child.payoffs[player_id]
            else:
                # Necesitamos evaluar la continuación
                if continuation:
                    temp_profile = StrategyProfile(strategies=continuation)
                    payoffs = self.calculate_payoffs(temp_profile)
                    payoff = payoffs.get(player_id, float('-inf'))
                else:
                    payoff = float('-inf')
            
            if payoff > best_payoff:
                best_payoff = payoff
                best_action = action
                best_continuation = continuation
        
        if best_action and best_continuation is not None:
            result = best_continuation.copy()
            result[player_id] = best_action
            return result
        
        return None
    
    def _get_player_actions(self, player_id: int) -> List[str]:
        """Obtiene todas las acciones posibles de un jugador"""
        actions = set()
        
        def traverse(node: GameNode):
            if node.player_id == player_id:
                actions.update(node.children.keys())
            for child in node.children.values():
                traverse(child)
        
        if self.root:
            traverse(self.root)
        
        return list(actions)
    
    def get_game_tree_dict(self) -> Dict:
        """
        Convierte el árbol de juego a un diccionario serializable
        
        Returns:
            Diccionario representando el árbol
        """
        def node_to_dict(node: GameNode) -> Dict:
            result = {
                'id': node.node_id,
                'player': node.player_id,
                'is_terminal': node.is_terminal()
            }
            
            if node.is_terminal() and node.payoffs:
                result['payoffs'] = node.payoffs
            else:
                result['actions'] = {
                    action: node_to_dict(child)
                    for action, child in node.children.items()
                }
            
            return result
        
        if self.root:
            return node_to_dict(self.root)
        return {}


def create_ultimatum_game(total_amount: float = 10.0) -> SequentialGame:
    """
    Crea el juego del Ultimátum
    
    Args:
        total_amount: Cantidad total a dividir
        
    Returns:
        Juego del Ultimátum
    """
    game = SequentialGame(
        name="Juego del Ultimátum",
        description=f"El Jugador 1 propone cómo dividir ${total_amount}. El Jugador 2 acepta o rechaza.",
        num_players=2
    )
    
    # Crear árbol de decisión
    root = game.create_node(player_id=0)  # Jugador 1 propone
    game.set_root(root)
    
    # Diferentes propuestas posibles
    offers = [
        (8, 2),   # Jugador 1 ofrece $2 al Jugador 2
        (7, 3),
        (6, 4),
        (5, 5),   # División equitativa
    ]
    
    for offer in offers:
        p1_gets, p2_gets = offer
        offer_label = f"Ofrecer ${p2_gets}"
        
        # Nodo de decisión del Jugador 2
        response_node = game.create_node(player_id=1)
        root.add_child(offer_label, response_node)
        
        # Jugador 2 acepta
        accept_node = game.create_node(player_id=-1)
        game.set_terminal_payoffs(accept_node, {0: float(p1_gets), 1: float(p2_gets)})
        response_node.add_child("Aceptar", accept_node)
        
        # Jugador 2 rechaza
        reject_node = game.create_node(player_id=-1)
        game.set_terminal_payoffs(reject_node, {0: 0.0, 1: 0.0})
        response_node.add_child("Rechazar", reject_node)
    
    return game


def create_trust_game(initial_amount: float = 10.0, multiplier: float = 3.0) -> SequentialGame:
    """
    Crea el juego de la Confianza (Trust Game)
    
    Args:
        initial_amount: Cantidad inicial
        multiplier: Factor de multiplicación
        
    Returns:
        Juego de la Confianza
    """
    game = SequentialGame(
        name="Juego de la Confianza",
        description="El Jugador 1 decide cuánto enviar. El monto se multiplica. El Jugador 2 decide cuánto devolver.",
        num_players=2
    )
    
    root = game.create_node(player_id=0)  # Jugador 1 decide cuánto enviar
    game.set_root(root)
    
    # Opciones de envío
    send_amounts = [0, initial_amount / 2, initial_amount]
    
    for send in send_amounts:
        send_label = f"Enviar ${send:.1f}"
        
        if send == 0:
            # Si no envía nada, el juego termina
            terminal = game.create_node(player_id=-1)
            game.set_terminal_payoffs(terminal, {0: initial_amount, 1: 0.0})
            root.add_child(send_label, terminal)
        else:
            # El Jugador 2 recibe send * multiplier
            received = send * multiplier
            remaining_p1 = initial_amount - send
            
            # Jugador 2 decide cuánto devolver
            return_node = game.create_node(player_id=1)
            root.add_child(send_label, return_node)
            
            # Opciones de devolución
            return_amounts = [0, received / 2, received]
            
            for return_amt in return_amounts:
                return_label = f"Devolver ${return_amt:.1f}"
                terminal = game.create_node(player_id=-1)
                
                final_p1 = remaining_p1 + return_amt
                final_p2 = received - return_amt
                
                game.set_terminal_payoffs(terminal, {0: final_p1, 1: final_p2})
                return_node.add_child(return_label, terminal)
    
    return game


def create_entry_game() -> SequentialGame:
    """Crea el juego de Entrada al Mercado"""
    game = SequentialGame(
        name="Juego de Entrada al Mercado",
        description="Una empresa decide si entrar al mercado. La empresa establecida decide si luchar o acomodar.",
        num_players=2
    )
    
    root = game.create_node(player_id=0)  # Entrante decide
    game.set_root(root)
    
    # Entrante no entra
    no_entry = game.create_node(player_id=-1)
    game.set_terminal_payoffs(no_entry, {0: 0.0, 1: 5.0})
    root.add_child("No Entrar", no_entry)
    
    # Entrante entra -> Establecida decide
    incumbent_node = game.create_node(player_id=1)
    root.add_child("Entrar", incumbent_node)
    
    # Establecida acomoda
    accommodate = game.create_node(player_id=-1)
    game.set_terminal_payoffs(accommodate, {0: 2.0, 1: 2.0})
    incumbent_node.add_child("Acomodar", accommodate)
    
    # Establecida lucha
    fight = game.create_node(player_id=-1)
    game.set_terminal_payoffs(fight, {0: -1.0, 1: -1.0})
    incumbent_node.add_child("Luchar", fight)
    
    return game
