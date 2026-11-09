# Teoría de Juegos Aplicada: De los Juegos de Mesa a la Solución de Problemas Complejos

## 🎮 Descripción del Proyecto

Aplicación educativa interactiva desarrollada en Python con Streamlit que explora la Teoría de Juegos desde sus fundamentos hasta aplicaciones avanzadas en problemas complejos del mundo real.

## 🚀 Características Principales

- **Juegos Clásicos Interactivos**: Implementación de dilema del prisionero, juego del ultimátum, batalla de los sexos, y más
- **Análisis de Equilibrios**: Cálculo y visualización de equilibrios de Nash
- **Estrategias Evolutivas**: Simulación de dinámicas evolutivas en poblaciones
- **Aplicaciones Reales**: Casos de estudio en economía, política, biología y tecnología
- **Visualizaciones Avanzadas**: Gráficos interactivos con Plotly
- **Sistema de Aprendizaje**: Tutoriales progresivos con evaluaciones

## 📋 Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clonar o descargar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd teoriadejuegos
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
teoriadejuegos/
├── app.py                      # Punto de entrada principal
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación
├── .streamlit/
│   └── config.toml            # Configuración de Streamlit
├── src/
│   ├── models/                # Modelos de datos y lógica de negocio
│   │   ├── __init__.py
│   │   ├── game.py           # Clase base de juegos
│   │   ├── matrix_game.py    # Juegos de matriz
│   │   ├── sequential_game.py # Juegos secuenciales
│   │   ├── evolutionary_game.py # Juegos evolutivos
│   │   └── player.py         # Modelo de jugador
│   ├── controllers/           # Lógica de control
│   │   ├── __init__.py
│   │   ├── game_controller.py
│   │   ├── nash_solver.py
│   │   └── simulation_controller.py
│   ├── views/                 # Componentes de interfaz
│   │   ├── __init__.py
│   │   ├── home_view.py
│   │   ├── classic_games_view.py
│   │   ├── advanced_games_view.py
│   │   ├── applications_view.py
│   │   └── learning_view.py
│   └── utils/                 # Utilidades
│       ├── __init__.py
│       ├── visualizer.py
│       ├── calculator.py
│       └── data_loader.py
├── tests/                     # Tests unitarios
│   ├── __init__.py
│   ├── test_models.py
│   └── test_controllers.py
├── data/                      # Datos y configuraciones
│   ├── games_config.json
│   └── learning_modules.json
├── assets/                    # Recursos estáticos
│   └── images/
└── docs/                      # Documentación adicional
    └── teoria_juegos.md
```

## 🎯 Módulos y Funcionalidades

### 1. Juegos Clásicos
- Dilema del Prisionero
- Juego del Ultimátum
- Batalla de los Sexos
- Juego del Gallina
- Matching Pennies

### 2. Análisis Avanzado
- Equilibrios de Nash (puros y mixtos)
- Estrategias dominantes
- Óptimo de Pareto
- Soluciones cooperativas

### 3. Juegos Evolutivos
- Halcón-Paloma
- Simulación de replicadores
- Estrategias estables evolutivamente (ESS)

### 4. Aplicaciones Reales
- Subastas y mecanismos de mercado
- Negociaciones internacionales
- Teoría de votación
- Diseño de algoritmos distribuidos

## 🧪 Ejecución de Tests

```bash
python -m pytest tests/
```

## 📚 Documentación Adicional

Consulta la carpeta `docs/` para documentación técnica detallada sobre la teoría de juegos implementada.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 👨‍💻 Autor

Proyecto educativo desarrollado como herramienta de aprendizaje de Teoría de Juegos.

## 🙏 Agradecimientos

- A John Nash por sus contribuciones fundamentales a la teoría de juegos
- A la comunidad de Python y Streamlit por sus excelentes herramientas
- A todos los investigadores en teoría de juegos que han hecho posible este conocimiento

---

**¡Explora, aprende y disfruta del fascinante mundo de la Teoría de Juegos! 🎲**
