"""
Vista de aplicaciones reales de teoría de juegos
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.utils import Visualizer


def render():
    """Renderiza la página de aplicaciones reales"""
    
    st.markdown('<h1 class="section-header">🌍 Aplicaciones Reales</h1>', unsafe_allow_html=True)
    st.markdown("Descubre cómo la teoría de juegos se aplica en el mundo real.")
    
    st.markdown("---")
    
    # Selector de aplicación
    application = st.selectbox(
        "Selecciona un área de aplicación:",
        [
            "🏦 Subastas y Mecanismos de Mercado",
            "💰 Criptomonedas y Blockchain",
            "🗳️ Teoría de Votación",
            "🌐 Diseño de Redes y Protocolos",
            "🏢 Estrategia Empresarial",
            "🌱 Ecología y Biología Evolutiva",
            "⚖️ Negociaciones Internacionales",
            "🎯 Diseño de Mecanismos"
        ]
    )
    
    if "Subastas" in application:
        render_auctions()
    elif "Criptomonedas" in application:
        render_crypto()
    elif "Votación" in application:
        render_voting()
    elif "Redes" in application:
        render_networks()
    elif "Empresarial" in application:
        render_business()
    elif "Ecología" in application:
        render_ecology()
    elif "Negociaciones" in application:
        render_negotiations()
    elif "Mecanismos" in application:
        render_mechanism_design()


def render_auctions():
    """Renderiza aplicación de subastas"""
    
    st.markdown("## 🏦 Subastas y Mecanismos de Mercado")
    
    st.markdown("""
    Las subastas son mecanismos de asignación donde múltiples compradores compiten
    por recursos limitados. La teoría de juegos ayuda a diseñar subastas eficientes.
    """)
    
    # Tipos de subastas
    st.markdown("### Tipos de Subastas")
    
    auction_type = st.radio(
        "Selecciona un tipo:",
        [
            "Subasta de Primer Precio (Sealed-Bid)",
            "Subasta de Segundo Precio (Vickrey)",
            "Subasta Inglesa (Ascendente)",
            "Subasta Holandesa (Descendente)"
        ]
    )
    
    if "Primer Precio" in auction_type:
        st.markdown("""
        **Subasta de Primer Precio**:
        - Todos presentan ofertas selladas simultáneamente
        - El mayor postor gana y paga su oferta
        - **Estrategia**: Ofertar por debajo de tu valoración real (shading)
        
        **Ejemplo**: Subastas de contratos gubernamentales
        """)
        
        # Simulación simple
        st.markdown("#### 🎮 Simulador")
        
        col1, col2 = st.columns(2)
        
        with col1:
            true_value = st.slider("Tu Valoración Real", 10, 100, 50, 5)
        
        with col2:
            bid = st.slider("Tu Oferta", 0, 100, 40, 5)
        
        # Generar ofertas de competidores
        np.random.seed(42)
        num_competitors = 5
        competitor_bids = np.random.randint(20, 60, num_competitors)
        
        max_competitor = max(competitor_bids)
        
        if bid > max_competitor:
            profit = true_value - bid
            st.success(f"✅ ¡Ganaste! Ganancia: ${profit}")
        else:
            st.error(f"❌ Perdiste. La oferta ganadora fue: ${max_competitor}")
        
        st.info(f"**Estrategia óptima**: Oferta alrededor de 2/3 de tu valoración en este contexto")
    
    elif "Segundo Precio" in auction_type:
        st.markdown("""
        **Subasta de Vickrey (Segundo Precio)**:
        - Todos presentan ofertas selladas
        - El mayor postor gana pero paga la segunda oferta más alta
        - **Estrategia dominante**: Ofertar tu valoración real (truthful)
        
        **Ventaja**: Incentiva revelación honesta de preferencias
        
        **Usado en**: Subastas de Google AdWords (GSP)
        """)
        
        st.success("""
        💡 **Insight Clave**: En esta subasta, decir la verdad es una estrategia dominante.
        No hay incentivo para exagerar o subestimar tu valoración.
        """)
    
    elif "Inglesa" in auction_type:
        st.markdown("""
        **Subasta Inglesa (Ascendente)**:
        - El precio sube gradualmente
        - Los postores van abandonando
        - Gana el último que queda
        
        **Características**:
        - Revelación de información durante el proceso
        - Más emocionante y transparente
        
        **Ejemplo**: Christie's, Sotheby's
        """)
    
    else:  # Holandesa
        st.markdown("""
        **Subasta Holandesa (Descendente)**:
        - El precio comienza alto y desciende
        - El primer postor que acepta, gana
        - Equivalente estratégicamente a primer precio
        
        **Ejemplo**: Venta de flores en Holanda, IPOs
        """)
    
    # Caso real
    with st.expander("📊 Caso Real: Subasta del Espectro 3G"):
        st.markdown("""
        **Reino Unido, 2000**
        
        - Subasta de licencias de telecomunicaciones 3G
        - Diseño: Subasta ascendente simultánea
        - Recaudación: £22.5 mil millones (más del esperado)
        
        **Lecciones**:
        - El diseño de la subasta importa enormemente
        - La entrada de competidores nuevos aumentó la competencia
        - Balance entre eficiencia y recaudación
        """)


def render_crypto():
    """Renderiza aplicación en criptomonedas"""
    
    st.markdown("## 💰 Criptomonedas y Blockchain")
    
    st.markdown("""
    La teoría de juegos es fundamental en el diseño de protocolos de blockchain,
    asegurando que los participantes actúen honestamente sin necesidad de confianza.
    """)
    
    # Consenso
    st.markdown("### 🔐 Mecanismos de Consenso")
    
    mechanism = st.radio(
        "Mecanismo:",
        ["Proof of Work (Bitcoin)", "Proof of Stake", "Byzantine Fault Tolerance"]
    )
    
    if "Proof of Work" in mechanism:
        st.markdown("""
        **Proof of Work (Bitcoin)**
        
        **Juego**:
        - Mineros compiten para resolver puzzles criptográficos
        - El ganador propone el siguiente bloque y recibe recompensa
        - Atacar requiere 51% del poder computacional
        
        **Incentivos**:
        - ✅ Minar honestamente: Recompensa de bloque + comisiones
        - ❌ Atacar: Costo computacional > Ganancia esperada
        
        **Nash Equilibrium**: Minería honesta es el equilibrio
        """)
        
        st.code("""
# Análisis simplificado de incentivos
costo_ataque = hash_rate_atacante * costo_electricidad
ganancia_ataque = probabilidad_exito * valor_doble_gasto

# Si costo > ganancia, no vale la pena atacar
        """, language="python")
    
    elif "Proof of Stake" in mechanism:
        st.markdown("""
        **Proof of Stake**
        
        **Juego**:
        - Validadores apuestan (stake) criptomonedas
        - Son seleccionados proporcionalmente a su stake
        - Comportamiento malicioso → pérdida del stake (slashing)
        
        **Ventajas**:
        - Mayor eficiencia energética
        - Castigo directo a comportamiento malicioso
        
        **Problema**: Nothing at Stake
        - En un fork, racional validar ambas cadenas
        - Solución: Penalización explícita
        """)
    
    else:  # BFT
        st.markdown("""
        **Byzantine Fault Tolerance**
        
        Basado en el "Problema de los Generales Bizantinos":
        - n generales deben coordinar un ataque
        - Algunos pueden ser traidores
        - Necesitan consenso a pesar de la presencia de traidores
        
        **Resultado**: Se puede lograr consenso si menos de 1/3 son maliciosos
        
        **Aplicaciones**: Hyperledger, Tendermint
        """)
    
    # Caso de ataque
    with st.expander("⚠️ Caso Real: Ataque del 51%"):
        st.markdown("""
        **Ethereum Classic, 2019**
        
        - Un atacante controló >51% del hash rate
        - Realizó double-spending de ~$1.1 millones
        - Revirtió transacciones mediante reorganización de la cadena
        
        **Lección**: La seguridad depende de la descentralización del poder computacional
        """)


def render_voting():
    """Renderiza teoría de votación"""
    
    st.markdown("## 🗳️ Teoría de Votación")
    
    st.markdown("""
    La teoría de juegos analiza sistemas electorales y sus propiedades estratégicas.
    """)
    
    st.markdown("### Sistemas de Votación")
    
    system = st.selectbox(
        "Sistema:",
        [
            "Pluralidad (First Past the Post)",
            "Votación por Ranking (Borda Count)",
            "Voto Aprobatorio (Approval Voting)",
            "Condorcet",
            "Votación Instantánea (IRV)"
        ]
    )
    
    # Ejemplo con 3 candidatos
    st.markdown("#### Ejemplo: 3 Candidatos, 100 Votantes")
    
    if "Pluralidad" in system:
        st.markdown("""
        **Sistema de Pluralidad**: Cada votante elige un candidato. Gana el que tenga más votos.
        
        **Problemas**:
        - Efecto spoiler
        - Votación estratégica (votar útil)
        - No representa preferencias completas
        """)
        
        # Simulación
        votes = {"Candidato A": 40, "Candidato B": 35, "Candidato C": 25}
        
        fig = go.Figure(data=[
            go.Bar(x=list(votes.keys()), y=list(votes.values()),
                  marker_color=['#FF4B4B', '#4B8BFF', '#4BFF4B'])
        ])
        fig.update_layout(title="Resultados", template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning("""
        **Paradoja**: C podría ser el "consenso" preferido en segunda opción por muchos,
        pero pierde bajo pluralidad.
        """)
    
    elif "Borda" in system:
        st.markdown("""
        **Borda Count**: Los votantes rankean candidatos. Puntos: 1er lugar=3, 2do=2, 3ro=1
        
        **Ventaja**: Considera preferencias completas
        **Desventaja**: Susceptible a manipulación estratégica
        """)
    
    elif "Aprobatorio" in system:
        st.markdown("""
        **Approval Voting**: Cada votante puede aprobar a múltiples candidatos
        
        **Ventajas**:
        - Simple
        - Resistente al spoiler effect
        - Incentiva a candidatos de consenso
        
        **Usado en**: Varias sociedades científicas
        """)
    
    # Teorema de Arrow
    with st.expander("📜 Teorema de Imposibilidad de Arrow"):
        st.markdown("""
        **Kenneth Arrow (Premio Nobel 1972)** demostró que ningún sistema de votación puede
        satisfacer simultáneamente estos criterios deseables:
        
        1. **Universalidad**: Funciona para todas las preferencias posibles
        2. **No Dictadura**: Ningún votante determina el resultado solo
        3. **Independencia de alternativas irrelevantes**: Añadir/quitar un candidato no afecta el orden de otros
        4. **Unanimidad de Pareto**: Si todos prefieren A > B, el sistema también
        
        **Conclusión**: Todo sistema electoral tiene defectos fundamentales
        """)


def render_networks():
    """Renderiza diseño de redes"""
    
    st.markdown("## 🌐 Diseño de Redes y Protocolos")
    
    st.markdown("""
    La teoría de juegos se aplica en el diseño de protocolos de Internet y redes distribuidas.
    """)
    
    st.markdown("### TCP Congestion Control")
    
    st.markdown("""
    **Problema**: Múltiples usuarios comparten ancho de banda limitado
    
    **Sin Control**:
    - Todos transmiten al máximo
    - Congestión y pérdida de paquetes
    - Tragedia de los comunes
    
    **TCP como Juego**:
    - Estrategia: Tasa de transmisión
    - Pago: Throughput - Pérdidas
    - Equilibrio: Algoritmo AIMD (Additive Increase, Multiplicative Decrease)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Estrategia Cooperativa**:
        - Aumentar lentamente
        - Reducir rápido al detectar congestión
        - Beneficio colectivo
        """)
    
    with col2:
        st.markdown("""
        **Estrategia Egoísta**:
        - Transmitir agresivamente
        - Ignorar señales de congestión
        - Perjudica a todos (incluyéndose)
        """)
    
    # Routing games
    st.markdown("### 🛣️ Juegos de Enrutamiento (Braess's Paradox)")
    
    st.markdown("""
    **Paradoja de Braess**: Añadir una carretera puede empeorar el tráfico para todos
    
    **Ejemplo**:
    - 4000 viajeros de A a B
    - Dos rutas iniciales
    - Se añade un atajo
    - Todos lo usan racionalmente
    - El tiempo promedio aumenta
    
    **Lección**: El equilibrio de Nash puede ser ineficiente socialmente (Precio de la Anarquía)
    """)
    
    with st.expander("💡 Aplicaciones Modernas"):
        st.markdown("""
        - **CDNs**: Distribución de contenido
        - **P2P**: BitTorrent incentivos
        - **Routing**: BGP entre ISPs
        - **Cloud Computing**: Asignación de recursos
        """)


def render_business():
    """Renderiza estrategia empresarial"""
    
    st.markdown("## 🏢 Estrategia Empresarial")
    
    st.markdown("""
    Las empresas constantemente juegan juegos estratégicos con competidores, proveedores y clientes.
    """)
    
    case = st.selectbox(
        "Caso de estudio:",
        [
            "Competencia de Precios (Bertrand)",
            "Competencia de Cantidades (Cournot)",
            "Liderazgo de Precios (Stackelberg)",
            "Diferenciación de Productos"
        ]
    )
    
    if "Bertrand" in case:
        st.markdown("""
        ### Competencia de Bertrand (Precios)
        
        **Setup**:
        - Dos empresas con productos idénticos
        - Eligen precios simultáneamente
        - Los consumidores compran al más barato
        
        **Resultado**:
        - Equilibrio: Ambas cobran precio = costo marginal
        - ¡Beneficio = 0 aunque solo haya 2 empresas!
        - "Paradoja de Bertrand"
        """)
        
        st.code("""
# Simulación simple
costo_marginal = 10

precio_empresa_1 = st.slider("Precio Empresa 1", 10, 50, 25)
precio_empresa_2 = st.slider("Precio Empresa 2", 10, 50, 25)

if precio_1 < precio_2:
    ganador = "Empresa 1 (toda la demanda)"
elif precio_2 < precio_1:
    ganador = "Empresa 2 (toda la demanda)"
else:
    ganador = "Empate (dividen la demanda)"
        """, language="python")
    
    elif "Cournot" in case:
        st.markdown("""
        ### Competencia de Cournot (Cantidades)
        
        **Setup**:
        - Empresas eligen cantidades a producir
        - El precio se ajusta según la oferta total
        
        **Equilibrio**:
        - Producción > competencia perfecta
        - Producción < monopolio
        - Beneficios positivos
        
        **Aplicación**: Industrias con capacidad limitada (acero, petróleo)
        """)
    
    elif "Stackelberg" in case:
        st.markdown("""
        ### Liderazgo de Stackelberg
        
        **Setup**:
        - Empresa líder mueve primero (ej: decide capacidad)
        - Seguidores observan y responden
        
        **Ventaja del primer movimiento**:
        - El líder puede comprometerse creíblemente
        - Obtiene mayor participación de mercado
        
        **Ejemplo**: Amazon en e-commerce
        """)
    
    else:  # Diferenciación
        st.markdown("""
        ### Diferenciación de Productos
        
        **Estrategia**: Evitar la competencia directa de precios
        
        **Métodos**:
        - Calidad diferente
        - Características únicas
        - Branding
        - Ubicación geográfica
        
        **Resultado**: Poder de mercado → Precios > costo marginal
        
        **Ejemplo**: Smartphones (Apple vs. Samsung vs. otros)
        """)


def render_ecology():
    """Renderiza aplicaciones en ecología"""
    
    st.markdown("## 🌱 Ecología y Biología Evolutiva")
    
    st.markdown("""
    La teoría de juegos evolutiva explica comportamientos animales y dinámicas ecológicas.
    """)
    
    st.markdown("### Comportamientos Explicados")
    
    behavior = st.selectbox(
        "Comportamiento:",
        [
            "Altruismo y Reciprocidad",
            "Señalización Costosa (Handicap Principle)",
            "Territorialidad",
            "Ratio de Sexos"
        ]
    )
    
    if "Altruismo" in behavior:
        st.markdown("""
        **Altruismo Recíproco**
        
        - ¿Por qué animales ayudan a no-parientes?
        - Dilema del prisionero repetido
        - Estrategia Tit-for-Tat: coopera primero, luego imita
        
        **Ejemplos**:
        - Murciélagos vampiro compartiendo comida
        - Peces limpiadores
        - Primates compartiendo información sobre depredadores
        """)
    
    elif "Señalización" in behavior:
        st.markdown("""
        **Principio del Handicap (Zahavi)**
        
        - Señales costosas son creíbles
        - Solo individuos de alta calidad pueden permitírselas
        
        **Ejemplos**:
        - Cola del pavo real (atrae hembras pesar de ser desventaja)
        - Saltos de gacelas (señal a depredadores: "soy rápida")
        - Cantos complejos de aves
        """)
    
    elif "Territorialidad" in behavior:
        st.markdown("""
        **Defensa de Territorio**
        
        - Juego Halcón-Paloma aplicado a animales
        - Equilibrio: Defender solo si el territorio vale la pena
        - ESS: Mezcla de agresión y retirada
        
        **Ejemplos**:
        - Leones defendiendo territorio
        - Aves con canciones territoriales
        """)
    
    else:  # Ratio de sexos
        st.markdown("""
        **Ratio de Sexos 1:1 (Fisher)**
        
        **Pregunta**: ¿Por qué la mayoría de especies tienen ~50% machos y 50% hembras?
        
        **Explicación (Teoría de Juegos)**:
        - Si hay más hembras, los machos tienen más descendencia
        - Ventaja evolutiva para padres que producen machos
        - Población se equilibra en 50-50
        - ¡ESS!
        
        **Genial**: Explicación puramente estratégica, sin necesidad de "beneficio para la especie"
        """)


def render_negotiations():
    """Renderiza negociaciones internacionales"""
    
    st.markdown("## ⚖️ Negociaciones Internacionales")
    
    st.markdown("""
    Teoría de juegos aplicada a conflictos y cooperación entre naciones.
    """)
    
    st.markdown("### Casos Históricos")
    
    st.markdown("""
    **Crisis de Misiles de Cuba (1962)**
    - Juego de gallina entre USA y USSR
    - Amenazas creíbles y señalización
    - Solución: Compromiso mutuo
    
    **Tratados de Cambio Climático**
    - Dilema del prisionero N-jugadores
    - Tragedia de los comunes global
    - Problema de free-riders
    
    **Tratados de No Proliferación Nuclear**
    - Problema de compromiso creíble
    - Verificación e inspecciones
    - Castigos por violación
    """)


def render_mechanism_design():
    """Renderiza diseño de mecanismos"""
    
    st.markdown("## 🎯 Diseño de Mecanismos")
    
    st.markdown("""
    **Reverse Game Theory**: Diseñar juegos que logren objetivos deseados
    
    **Pregunta**: Dado un objetivo, ¿qué reglas deberíamos establecer para que
    los agentes racionales y egoístas logren ese objetivo?
    """)
    
    st.markdown("### Principios")
    
    st.markdown("""
    **1. Incentive Compatibility**: Las reglas deben alinear incentivos individuales con objetivos sociales
    
    **2. Individual Rationality**: Los participantes deben querer participar voluntariamente
    
    **3. Budget Balance**: No se requieren subsidios externos
    """)
    
    st.success("""
    **Ejemplo Exitoso**: Subasta de Vickrey
    - Objetivo: Asignar eficientemente
    - Mecanismo: Segundo precio
    - Resultado: Revelación honesta es estrategia dominante
    """)
