# 🏗️ Arquitectura del Sistema - Teoría de Juegos Aplicada

## Visión General

El proyecto sigue una **arquitectura MVC (Model-View-Controller)** adaptada para aplicaciones Streamlit, con separación clara de responsabilidades y diseño modular.

## Patrones de Diseño Aplicados

### 1. Model-View-Controller (MVC)

```
┌─────────────────────────────────────────────────────┐
│                   app.py (Entry Point)              │
│                   - Configuración                    │
│                   - Routing de páginas               │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼──────┐    ┌──────▼────────┐
│   VIEWS      │    │  CONTROLLERS  │
│  (src/views) │◄───┤(src/controllers)│
│              │    │               │
│ - home       │    │ - game_ctrl   │
│ - games      │    │ - nash_solver │
│ - advanced   │    │ - simulation  │
│ - apps       │    │               │
│ - learning   │    └───────┬───────┘
└──────────────┘            │
                     ┌──────▼──────┐
                     │   MODELS    │
                     │ (src/models)│
                     │             │
                     │ - game      │
                     │ - player    │
                     │ - matrix    │
                     │ - sequential│
                     │ - evolutionary│
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐
                     │   UTILS     │
                     │ (src/utils) │
                     │             │
                     │ - visualizer│
                     │ - calculator│
                     │ - data_loader│
                     └─────────────┘
```

### 2. Abstract Factory Pattern

**Implementación**: Clase `Game` abstracta

```python
# src/models/game.py
class Game(ABC):
    @abstractmethod
    def calculate_payoffs(...): pass
    
    @abstractmethod
    def find_nash_equilibria(...): pass

# Implementaciones concretas:
- MatrixGame
- SequentialGame
- EvolutionaryGame
```

**Ventajas**:
- Facilita añadir nuevos tipos de juegos
- Garantiza interfaz consistente
- Permite polimorfismo

### 3. Strategy Pattern

**Implementación**: Diferentes algoritmos de solución

```python
# Diferentes estrategias para encontrar equilibrios:
- Backward Induction (juegos secuenciales)
- Eliminación iterativa (juegos de matriz)
- Dinámicas de replicadores (juegos evolutivos)
```

### 4. Observer Pattern (implícito)

**Implementación**: Sistema de historial en `Game`

```python
class Game:
    def __init__(self):
        self.history = []  # Observadores del estado
    
    def play_round(self, strategies):
        result = ...
        self.history.append(result)  # Notificar
```

## Estructura de Módulos

### Capa de Modelos (src/models/)

#### game.py - Clase Base Abstracta
```python
Responsabilidades:
- Define interfaz común para todos los juegos
- Gestiona jugadores y historial
- Valida estados del juego
- Provee métodos abstractos obligatorios

Métodos clave:
- calculate_payoffs()
- get_best_response()
- find_nash_equilibria()
- is_nash_equilibrium()
```

#### player.py - Modelo de Jugador
```python
Responsabilidades:
- Encapsula información del jugador
- Gestiona estrategias disponibles
- Acumula pagos
- Dataclass para inmutabilidad parcial

Componentes:
- Player (dataclass)
- StrategyProfile (dataclass)
```

#### matrix_game.py - Juegos de Matriz
```python
Responsabilidades:
- Implementa juegos en forma normal
- Almacena matrices de pagos
- Encuentra equilibrios puros
- Identifica estrategias dominantes
- Verifica óptimo de Pareto

Juegos predefinidos:
- create_prisoners_dilemma()
- create_battle_of_sexes()
- create_matching_pennies()
- create_chicken_game()
- create_stag_hunt()
```

#### sequential_game.py - Juegos Secuenciales
```python
Responsabilidades:
- Representa árboles de decisión
- Implementa backward induction
- Encuentra equilibrios perfectos en subjuegos
- Gestiona nodos y acciones

Componentes:
- GameNode (dataclass)
- SequentialGame (clase)

Juegos predefinidos:
- create_ultimatum_game()
- create_trust_game()
- create_entry_game()
```

#### evolutionary_game.py - Juegos Evolutivos
```python
Responsabilidades:
- Simula dinámicas poblacionales
- Implementa ecuaciones de replicadores
- Calcula fitness y ESS
- Gestiona poblaciones

Componentes:
- Population (dataclass)
- EvolutionaryGame (clase)

Juegos predefinidos:
- create_hawk_dove_game()
- create_rock_paper_scissors_game()
- create_coordination_game()
```

### Capa de Controladores (src/controllers/)

#### game_controller.py - Controlador Principal
```python
Responsabilidades:
- Orquesta flujo del juego
- Gestiona inicialización de jugadores
- Ejecuta rondas
- Genera resúmenes
- Analiza resultados

Flujo típico:
1. set_game()
2. initialize_players()
3. play_round() (repetir)
4. get_game_summary()
```

#### nash_solver.py - Solucionador de Equilibrios
```python
Responsabilidades:
- Encuentra equilibrios puros
- Calcula equilibrios mixtos (2x2)
- Verifica equilibrios
- Analiza pagos esperados

Algoritmos:
- Fuerza bruta para puros
- Método analítico para mixtos 2x2
- Cálculo de pagos esperados
```

#### simulation_controller.py - Simulaciones
```python
Responsabilidades:
- Ejecuta simulaciones evolutivas
- Gestiona poblaciones
- Calcula trayectorias
- Analiza convergencia
- Simula invasiones

Métodos clave:
- run_simulation()
- calculate_trajectory()
- analyze_convergence()
- simulate_invasion()
```

### Capa de Utilidades (src/utils/)

#### visualizer.py - Visualizaciones
```python
Responsabilidades:
- Crea gráficos interactivos con Plotly
- Mapas de calor para matrices
- Árboles de decisión
- Trayectorias evolutivas
- Comparaciones de pagos

Tipos de gráficos:
- Heatmaps
- Line charts
- Bar charts
- Network graphs
- Phase portraits
```

#### calculator.py - Cálculos Avanzados
```python
Responsabilidades:
- Cálculos de teoría de juegos
- Bienestar social
- Coeficiente de Gini
- Valor de Shapley
- Índice de Banzhaf
- Precio de la anarquía

Funciones estáticas:
- calculate_social_welfare()
- calculate_shapley_value()
- calculate_banzhaf_power_index()
- find_maximin_strategy()
```

#### data_loader.py - Gestión de Datos
```python
Responsabilidades:
- Carga configuraciones JSON
- Gestiona datos educativos
- Provee descripciones predefinidas
- Serialización de datos

Métodos:
- load_json()
- save_json()
- get_game_config()
- get_learning_modules()
```

### Capa de Vistas (src/views/)

#### Arquitectura de Vistas

```python
Patrón común:
1. render() - función principal
2. Subdivide en funciones más pequeñas
3. Usa st.components para UI
4. Interactúa con controllers
5. Usa visualizer para gráficos

Ejemplo:
def render():
    st.title("...")
    tabs = st.tabs([...])
    
    with tabs[0]:
        render_section_1()
    with tabs[1]:
        render_section_2()
```

#### home_view.py
- Página de inicio
- Introducción a teoría de juegos
- Conceptos clave
- Navegación guiada

#### classic_games_view.py
- Juegos clásicos interactivos
- Análisis de equilibrios
- Juego interactivo
- Insights educativos

#### advanced_games_view.py
- Juegos evolutivos
- Simulaciones
- Laboratorio personalizado
- Visualizaciones avanzadas

#### applications_view.py
- Casos reales
- Múltiples dominios
- Ejemplos históricos
- Explicaciones técnicas

#### learning_view.py
- Módulos educativos
- Quizzes interactivos
- Ejercicios prácticos
- Glosario

## Flujo de Datos

### 1. Inicio de la Aplicación

```
app.py
  ↓
Inicialización de session_state
  ↓
Renderizado de sidebar (navegación)
  ↓
Routing a vista seleccionada
  ↓
Renderizado de vista específica
```

### 2. Jugar un Juego

```
Usuario selecciona juego
  ↓
Vista carga juego desde models
  ↓
Vista crea GameController
  ↓
Controller inicializa jugadores
  ↓
Usuario elige estrategias (UI)
  ↓
Controller.play_round(strategies)
  ↓
Game.calculate_payoffs()
  ↓
Actualización de UI con resultados
  ↓
Visualizer crea gráficos
  ↓
Presentación al usuario
```

### 3. Simulación Evolutiva

```
Usuario configura parámetros
  ↓
Vista crea EvolutionaryGame
  ↓
Vista crea SimulationController
  ↓
Controller.run_simulation()
  ↓
  Loop: Para cada generación
    - Game.replicator_dynamics_step()
    - Population actualizada
  ↓
Controller.calculate_trajectory()
  ↓
Visualizer.plot_evolutionary_trajectory()
  ↓
Presentación de resultados
```

## Decisiones de Diseño

### 1. ¿Por qué Streamlit?

**Ventajas**:
- Rápido desarrollo de UI
- Interactividad nativa
- Visualizaciones integradas
- Python puro
- Ideal para educación

**Alternativas consideradas**:
- Flask/Django (más complejo)
- Jupyter Notebooks (menos interactivo)
- React + API (sobrecarga)

### 2. ¿Por qué NumPy para matrices?

**Ventajas**:
- Eficiencia computacional
- Operaciones vectorizadas
- Integración con scipy
- Estándar en ciencia de datos

### 3. ¿Por qué Plotly sobre Matplotlib?

**Ventajas**:
- Gráficos interactivos
- Mejor en web
- Hover tooltips nativos
- Zoom y pan integrados

### 4. ¿Por qué dataclasses?

**Ventajas**:
- Menos boilerplate
- Type hints nativos
- Inmutabilidad opcional
- Validación automática

## Principios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada clase tiene una responsabilidad única
- `Game` solo modela juegos
- `Controller` solo orquesta lógica
- `Visualizer` solo crea gráficos

### Open/Closed Principle (OCP)
- `Game` es extensible (nuevos tipos de juegos)
- Sin modificar clase base
- Factory methods para crear juegos

### Liskov Substitution Principle (LSP)
- Cualquier `Game` puede usarse donde se espera la clase base
- Controllers funcionan con cualquier tipo de `Game`

### Interface Segregation Principle (ISP)
- Interfaces pequeñas y específicas
- No se fuerza implementar métodos innecesarios

### Dependency Inversion Principle (DIP)
- Controllers dependen de abstracciones (`Game`)
- No de implementaciones concretas

## Patrones de Testing

### Estructura de Tests

```
tests/
├── test_models.py          # Tests de modelos
├── test_controllers.py     # Tests de controladores
└── conftest.py             # Fixtures compartidas (futuro)
```

### Tipos de Tests

1. **Tests Unitarios**: Funciones individuales
2. **Tests de Integración**: Múltiples componentes
3. **Tests de Regresión**: Prevenir errores conocidos

### Estrategia de Testing

```python
# Arrange (Preparar)
game = create_prisoners_dilemma()

# Act (Actuar)
equilibria = game.find_nash_equilibria()

# Assert (Verificar)
assert len(equilibria) == 1
```

## Performance y Optimización

### Áreas Optimizadas

1. **Cálculos NumPy**: Operaciones vectorizadas
2. **Caché de Streamlit**: `@st.cache_data` para cálculos pesados
3. **Lazy loading**: Datos cargados solo cuando se necesitan

### Áreas de Mejora Futura

1. **Algoritmos de Nash mixtos**: Programación lineal
2. **Simulaciones paralelas**: multiprocessing
3. **Base de datos**: Para historial persistente

## Extensibilidad

### Añadir un Nuevo Tipo de Juego

1. Crear clase en `src/models/`
2. Heredar de `Game`
3. Implementar métodos abstractos
4. Crear factory function
5. Añadir a vista correspondiente

### Añadir Nueva Visualización

1. Método estático en `Visualizer`
2. Retornar `go.Figure` de Plotly
3. Usar en vista apropiada

### Añadir Nuevo Algoritmo

1. Método en `GameCalculator` o nuevo controller
2. Funciones estáticas preferidas
3. Documentar complejidad

## Seguridad y Validación

### Validación de Entrada

```python
# En Player
def __post_init__(self):
    if not self.name:
        raise ValueError("Player must have a name")

# En Population
def __post_init__(self):
    total = sum(self.strategy_frequencies.values())
    if not np.isclose(total, 1.0):
        # Normalizar
        ...
```

### Manejo de Errores

```python
try:
    result = game.calculate_payoffs(profile)
except ValueError as e:
    st.error(f"Error: {e}")
    return
```

## Configuración y Deploy

### Variables de Configuración

- `.streamlit/config.toml`: Tema, puerto, etc.
- `data/*.json`: Configuraciones de datos
- Environment variables: Secretos (futuro)

### Deploy Options

1. **Streamlit Cloud**: Gratis, fácil
2. **Heroku**: Escalable
3. **Docker**: Portable
4. **AWS/GCP**: Producción

## Métricas de Código

```
Complejidad Ciclomática: Baja-Media
Acoplamiento: Bajo
Cohesión: Alta
Líneas por archivo: 200-600 (apropiado)
Funciones por clase: 5-15 (manejable)
```

## Conclusión

La arquitectura está diseñada para:
- ✅ Mantenibilidad
- ✅ Extensibilidad
- ✅ Testabilidad
- ✅ Claridad
- ✅ Performance razonable

Sigue principios SOLID y patrones de diseño establecidos, facilitando futuras mejoras y colaboración.

---

*Documentación de Arquitectura v1.0*
*Teoría de Juegos Aplicada - 2026*
