"""
Utilidad para cargar datos y configuraciones
"""

import json
import os
from typing import Dict, List, Any, Optional


class DataLoader:
    """Clase para cargar datos de configuración y contenido educativo"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa el cargador de datos
        
        Args:
            data_dir: Directorio de datos
        """
        self.data_dir = data_dir
    
    def load_json(self, filename: str) -> Optional[Dict]:
        """
        Carga un archivo JSON
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Diccionario con los datos o None si hay error
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None
    
    def save_json(self, data: Dict, filename: str) -> bool:
        """
        Guarda datos en un archivo JSON
        
        Args:
            data: Datos a guardar
            filename: Nombre del archivo
            
        Returns:
            True si se guardó exitosamente
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def get_game_config(self, game_name: str) -> Optional[Dict]:
        """
        Obtiene la configuración de un juego
        
        Args:
            game_name: Nombre del juego
            
        Returns:
            Configuración del juego
        """
        config = self.load_json("games_config.json")
        
        if config and game_name in config:
            return config[game_name]
        
        return None
    
    def get_learning_modules(self) -> List[Dict]:
        """
        Obtiene los módulos de aprendizaje
        
        Returns:
            Lista de módulos
        """
        modules = self.load_json("learning_modules.json")
        return modules.get("modules", []) if modules else []
    
    def get_applications(self) -> List[Dict]:
        """
        Obtiene las aplicaciones reales de teoría de juegos
        
        Returns:
            Lista de aplicaciones
        """
        apps = self.load_json("applications.json")
        return apps.get("applications", []) if apps else []
    
    @staticmethod
    def get_default_game_descriptions() -> Dict[str, str]:
        """
        Retorna descripciones predeterminadas de juegos clásicos
        
        Returns:
            Diccionario de nombre -> descripción
        """
        return {
            "prisoners_dilemma": """
            **Dilema del Prisionero**: Dos criminales son arrestados. Si ambos cooperan 
            (permanecen en silencio), reciben sentencias leves. Si uno traiciona y el otro 
            coopera, el traidor queda libre y el otro recibe sentencia máxima. Si ambos 
            traicionan, ambos reciben sentencias intermedias.
            """,
            "battle_of_sexes": """
            **Batalla de los Sexos**: Una pareja debe decidir a dónde ir. Uno prefiere la 
            ópera, el otro prefiere el fútbol. Lo importante es estar juntos, pero cada uno 
            prefiere su actividad favorita.
            """,
            "matching_pennies": """
            **Matching Pennies**: Juego de suma cero donde un jugador gana si ambas monedas 
            coinciden, y el otro gana si son diferentes.
            """,
            "chicken": """
            **Juego del Gallina**: Dos conductores van uno hacia el otro. El que se desvía 
            es el "gallina". Si ninguno se desvía, ambos sufren las peores consecuencias.
            """,
            "stag_hunt": """
            **Caza del Ciervo**: Los cazadores pueden cooperar para cazar un ciervo (mayor 
            recompensa) o cazar liebres individualmente (recompensa menor pero segura).
            """,
            "hawk_dove": """
            **Halcón-Paloma**: Competencia por recursos. Los halcones pelean, las palomas 
            comparten. Pelear es costoso pero puede dar todo el recurso.
            """,
            "ultimatum": """
            **Juego del Ultimátum**: El primer jugador propone cómo dividir una cantidad. 
            El segundo puede aceptar o rechazar. Si rechaza, nadie recibe nada.
            """,
            "trust": """
            **Juego de la Confianza**: El primer jugador puede enviar dinero que se multiplica. 
            El segundo puede devolver parte del dinero multiplicado o quedárselo todo.
            """
        }
    
    @staticmethod
    def get_equilibrium_concepts() -> Dict[str, str]:
        """
        Retorna definiciones de conceptos de equilibrio
        
        Returns:
            Diccionario de concepto -> definición
        """
        return {
            "nash_equilibrium": """
            **Equilibrio de Nash**: Un perfil de estrategias donde ningún jugador puede 
            mejorar su pago cambiando unilateralmente su estrategia, dadas las estrategias 
            de los demás jugadores.
            """,
            "dominant_strategy": """
            **Estrategia Dominante**: Una estrategia que proporciona mejores pagos que 
            cualquier otra estrategia, independientemente de lo que hagan los demás jugadores.
            """,
            "pareto_optimum": """
            **Óptimo de Pareto**: Un resultado donde no es posible mejorar la situación 
            de un jugador sin empeorar la de al menos otro jugador.
            """,
            "subgame_perfect": """
            **Equilibrio Perfecto en Subjuegos**: Un equilibrio de Nash que representa un 
            equilibrio de Nash en cada subjuego del juego original.
            """,
            "ess": """
            **Estrategia Evolutivamente Estable (ESS)**: Una estrategia que, si es adoptada 
            por la mayoría de la población, no puede ser invadida por ninguna estrategia 
            mutante rara.
            """
        }
