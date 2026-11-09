"""
Vista del centro de aprendizaje
"""

import streamlit as st


def render():
    """Renderiza la página del centro de aprendizaje"""
    
    st.markdown('<h1 class="section-header">📚 Centro de Aprendizaje</h1>', unsafe_allow_html=True)
    st.markdown("Refuerza tu conocimiento con contenido estructurado y evaluaciones.")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Módulos de Aprendizaje",
        "❓ Quiz",
        "📝 Ejercicios",
        "📚 Glosario"
    ])
    
    with tab1:
        render_learning_modules()
    
    with tab2:
        render_quiz()
    
    with tab3:
        render_exercises()
    
    with tab4:
        render_glossary()


def render_learning_modules():
    """Renderiza módulos de aprendizaje"""
    
    st.markdown("## 📖 Módulos de Aprendizaje")
    
    modules = [
        {
            "title": "Módulo 1: Fundamentos",
            "topics": [
                "¿Qué es un juego?",
                "Jugadores, estrategias y pagos",
                "Forma normal vs. forma extensiva",
                "Información perfecta e imperfecta"
            ],
            "duration": "30 min"
        },
        {
            "title": "Módulo 2: Equilibrio de Nash",
            "topics": [
                "Definición formal",
                "Encontrar equilibrios puros",
                "Equilibrios mixtos",
                "Unicidad y multiplicidad"
            ],
            "duration": "45 min"
        },
        {
            "title": "Módulo 3: Juegos Secuenciales",
            "topics": [
                "Backward induction",
                "Equilibrio perfecto en subjuegos",
                "Credibilidad de amenazas",
                "Árboles de juego"
            ],
            "duration": "40 min"
        },
        {
            "title": "Módulo 4: Teoría de Juegos Evolutiva",
            "topics": [
                "Dinámicas de replicadores",
                "Estrategias evolutivamente estables (ESS)",
                "Halcón-Paloma",
                "Aplicaciones biológicas"
            ],
            "duration": "50 min"
        },
        {
            "title": "Módulo 5: Juegos Cooperativos",
            "topics": [
                "Función característica",
                "Núcleo (Core)",
                "Valor de Shapley",
                "Negociación de Nash"
            ],
            "duration": "45 min"
        }
    ]
    
    for i, module in enumerate(modules):
        with st.expander(f"{module['title']} ⏱️ {module['duration']}"):
            st.markdown(f"**Temas cubiertos:**")
            for topic in module['topics']:
                st.markdown(f"- {topic}")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                progress_key = f"module_{i}_progress"
                if progress_key not in st.session_state:
                    st.session_state[progress_key] = 0
                
                st.progress(st.session_state[progress_key] / 100)
                st.caption(f"Progreso: {st.session_state[progress_key]}%")
            
            with col2:
                if st.button(f"Comenzar", key=f"start_{i}"):
                    st.session_state[progress_key] = min(100, st.session_state[progress_key] + 25)
                    st.rerun()


def render_quiz():
    """Renderiza cuestionarios"""
    
    st.markdown("## ❓ Evaluación de Conocimientos")
    
    quiz_level = st.selectbox(
        "Nivel de dificultad:",
        ["Básico", "Intermedio", "Avanzado"]
    )
    
    if quiz_level == "Básico":
        questions = [
            {
                "question": "¿Qué es un equilibrio de Nash?",
                "options": [
                    "Una situación donde todos los jugadores están contentos",
                    "Una situación donde ningún jugador puede mejorar cambiando solo su estrategia",
                    "La estrategia que maximiza el bienestar social",
                    "Un empate entre todos los jugadores"
                ],
                "correct": 1,
                "explanation": "Un equilibrio de Nash es cuando ningún jugador tiene incentivo a desviarse unilateralmente."
            },
            {
                "question": "En el Dilema del Prisionero clásico, ¿cuál es el equilibrio de Nash?",
                "options": [
                    "Ambos cooperan",
                    "Ambos traicionan",
                    "Uno coopera, otro traiciona",
                    "No hay equilibrio de Nash"
                ],
                "correct": 1,
                "explanation": "Traicionar es estrategia dominante para ambos, llevando al equilibrio (Traicionar, Traicionar)."
            },
            {
                "question": "¿Qué es una estrategia dominante?",
                "options": [
                    "La estrategia más complicada",
                    "La que siempre gana",
                    "La mejor opción independientemente de lo que hagan los demás",
                    "La estrategia del jugador más fuerte"
                ],
                "correct": 2,
                "explanation": "Una estrategia dominante es la mejor respuesta contra cualquier estrategia del oponente."
            }
        ]
    
    elif quiz_level == "Intermedio":
        questions = [
            {
                "question": "¿Qué caracteriza a un equilibrio perfecto en subjuegos?",
                "options": [
                    "Es un equilibrio de Nash en cada subjuego",
                    "Maximiza los pagos de todos",
                    "No hay estrategias mixtas",
                    "Todos los jugadores cooperan"
                ],
                "correct": 0,
                "explanation": "Un SPE es un equilibrio de Nash que se mantiene en cada punto de decisión del juego."
            },
            {
                "question": "En un juego de suma cero, ¿cuánto suman los pagos de todos los jugadores?",
                "options": [
                    "Depende de las estrategias",
                    "Siempre es positivo",
                    "Siempre es cero",
                    "Siempre es uno"
                ],
                "correct": 2,
                "explanation": "En juegos de suma cero, las ganancias de unos son exactamente las pérdidas de otros."
            }
        ]
    
    else:  # Avanzado
        questions = [
            {
                "question": "¿Cuál es la condición para que una estrategia sea ESS?",
                "options": [
                    "E(s,s) > E(m,s) para todo mutante m",
                    "E(s,s) ≥ E(m,s) y si hay igualdad, E(s,m) > E(m,m)",
                    "Es un equilibrio de Nash puro",
                    "Maximiza el fitness promedio"
                ],
                "correct": 1,
                "explanation": "ESS requiere que la estrategia residente no pueda ser invadida por mutantes raros."
            },
            {
                "question": "El Teorema de Folk en juegos repetidos establece que:",
                "options": [
                    "Solo hay un equilibrio de Nash",
                    "Múltiples resultados pueden sostenerse como equilibrios con suficiente paciencia",
                    "La cooperación nunca es posible",
                    "El último periodo determina todo"
                ],
                "correct": 1,
                "explanation": "Con horizonte infinito y suficiente paciencia, muchos resultados pueden ser equilibrios."
            }
        ]
    
    # Renderizar preguntas
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    for i, q in enumerate(questions):
        st.markdown(f"### Pregunta {i+1}")
        st.markdown(q["question"])
        
        answer = st.radio(
            "Selecciona tu respuesta:",
            q["options"],
            key=f"q_{i}",
            index=None
        )
        
        if answer is not None:
            st.session_state.quiz_answers[i] = q["options"].index(answer)
        
        st.markdown("---")
    
    # Botón de evaluación
    if st.button("📊 Evaluar Respuestas"):
        correct_count = 0
        
        for i, q in enumerate(questions):
            if i in st.session_state.quiz_answers:
                if st.session_state.quiz_answers[i] == q["correct"]:
                    correct_count += 1
                    st.success(f"✅ Pregunta {i+1}: Correcta!")
                else:
                    st.error(f"❌ Pregunta {i+1}: Incorrecta")
                    st.info(f"**Explicación**: {q['explanation']}")
        
        score = (correct_count / len(questions)) * 100
        st.markdown(f"## Puntuación: {score:.0f}%")
        
        if score == 100:
            st.balloons()
            st.success("🎉 ¡Perfecto! Dominas este nivel.")
        elif score >= 70:
            st.success("✅ ¡Buen trabajo! Tienes un buen entendimiento.")
        else:
            st.warning("📚 Revisa el material y vuelve a intentarlo.")


def render_exercises():
    """Renderiza ejercicios prácticos"""
    
    st.markdown("## 📝 Ejercicios Prácticos")
    
    exercise = st.selectbox(
        "Selecciona un ejercicio:",
        [
            "Ejercicio 1: Encontrar Equilibrios de Nash",
            "Ejercicio 2: Analizar Estrategias Dominantes",
            "Ejercicio 3: Backward Induction",
            "Ejercicio 4: Diseñar un Juego"
        ]
    )
    
    if "Ejercicio 1" in exercise:
        st.markdown("""
        ### Ejercicio 1: Encontrar Equilibrios de Nash
        
        Considera el siguiente juego de 2 jugadores:
        
        |  | L | R |
        |---|---|---|
        | **T** | (3,2) | (1,3) |
        | **B** | (2,1) | (4,4) |
        
        **Tareas**:
        1. Identifica las mejores respuestas de cada jugador
        2. Encuentra todos los equilibrios de Nash puros
        3. ¿Existe algún equilibrio mixto?
        """)
        
        with st.expander("💡 Solución"):
            st.markdown("""
            **Análisis**:
            
            **Jugador 1** (filas):
            - Si J2 juega L: mejor respuesta es T (3 > 2)
            - Si J2 juega R: mejor respuesta es B (4 > 1)
            
            **Jugador 2** (columnas):
            - Si J1 juega T: mejor respuesta es R (3 > 2)
            - Si J1 juega B: mejor respuesta es R (4 > 1)
            
            **Equilibrio de Nash**: (B, R) con pagos (4, 4)
            
            R es estrategia dominante para el Jugador 2.
            """)
    
    elif "Ejercicio 2" in exercise:
        st.markdown("""
        ### Ejercicio 2: Analizar Estrategias Dominantes
        
        |  | L | M | R |
        |---|---|---|---|
        | **T** | (1,0) | (3,2) | (0,1) |
        | **M** | (2,3) | (2,1) | (5,2) |
        | **B** | (1,1) | (0,0) | (4,3) |
        
        **Preguntas**:
        1. ¿Tiene el Jugador 1 alguna estrategia dominante?
        2. ¿Tiene el Jugador 2 alguna estrategia dominante?
        3. Aplica eliminación iterativa de estrategias dominadas
        """)
        
        with st.expander("💡 Pista"):
            st.markdown("""
            - Compara cada estrategia fila por fila y columna por columna
            - Una estrategia domina si siempre da mejor o igual pago
            - Elimina dominadas y repite el proceso
            """)
    
    elif "Ejercicio 3" in exercise:
        st.markdown("""
        ### Ejercicio 3: Backward Induction
        
        Juego secuencial:
        1. Jugador 1 elige: Entrar (E) o No Entrar (N)
        2. Si entra, Jugador 2 elige: Pelear (F) o Acomodar (A)
        
        Pagos:
        - N: (0, 5)
        - E → F: (-1, -1)
        - E → A: (2, 2)
        
        **Tarea**: Encuentra el equilibrio perfecto en subjuegos usando backward induction.
        """)
        
        with st.expander("💡 Solución"):
            st.markdown("""
            **Backward Induction**:
            
            1. En el último nodo (decisión de J2 si J1 entró):
               - F da -1, A da 2
               - J2 elegirá A
            
            2. En el primer nodo (decisión de J1):
               - N da 0
               - E da 2 (anticipando que J2 jugará A)
               - J1 elegirá E
            
            **Equilibrio Perfecto**: (E, A) con pagos (2, 2)
            
            La amenaza de "Pelear" por J2 no es creíble.
            """)
    
    else:  # Ejercicio 4
        st.markdown("""
        ### Ejercicio 4: Diseñar un Juego
        
        **Desafío Creativo**: Diseña un juego de 2x2 que tenga exactamente:
        - 2 equilibrios de Nash puros
        - Ambos equilibrios con diferentes pagos totales
        
        Usa la matriz de abajo para tu diseño:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Jugador 1 juega S1, Jugador 2 juega S1**")
            p1_s1s1 = st.number_input("Pago J1:", -10, 10, 3, key="p1_11")
            p2_s1s1 = st.number_input("Pago J2:", -10, 10, 3, key="p2_11")
            
            st.markdown("**Jugador 1 juega S1, Jugador 2 juega S2**")
            p1_s1s2 = st.number_input("Pago J1:", -10, 10, 0, key="p1_12")
            p2_s1s2 = st.number_input("Pago J2:", -10, 10, 0, key="p2_12")
        
        with col2:
            st.markdown("**Jugador 1 juega S2, Jugador 2 juega S1**")
            p1_s2s1 = st.number_input("Pago J1:", -10, 10, 0, key="p1_21")
            p2_s2s1 = st.number_input("Pago J2:", -10, 10, 0, key="p2_21")
            
            st.markdown("**Jugador 1 juega S2, Jugador 2 juega S2**")
            p1_s2s2 = st.number_input("Pago J1:", -10, 10, 2, key="p1_22")
            p2_s2s2 = st.number_input("Pago J2:", -10, 10, 2, key="p2_22")
        
        if st.button("Verificar mi juego"):
            # Lógica simple para verificar equilibrios
            nash_count = 0
            equilibria = []
            
            # Verificar (S1, S1)
            if p1_s1s1 >= p1_s2s1 and p2_s1s1 >= p2_s1s2:
                nash_count += 1
                equilibria.append("(S1, S1)")
            
            # Verificar (S1, S2)
            if p1_s1s2 >= p1_s2s2 and p2_s1s2 >= p2_s1s1:
                nash_count += 1
                equilibria.append("(S1, S2)")
            
            # Verificar (S2, S1)
            if p1_s2s1 >= p1_s1s1 and p2_s2s1 >= p2_s2s2:
                nash_count += 1
                equilibria.append("(S2, S1)")
            
            # Verificar (S2, S2)
            if p1_s2s2 >= p1_s1s2 and p2_s2s2 >= p2_s1s2:
                nash_count += 1
                equilibria.append("(S2, S2)")
            
            if nash_count == 2:
                st.success(f"✅ ¡Excelente! Tu juego tiene {nash_count} equilibrios de Nash: {', '.join(equilibria)}")
            else:
                st.warning(f"Tu juego tiene {nash_count} equilibrios. Intenta ajustar los pagos.")


def render_glossary():
    """Renderiza glosario de términos"""
    
    st.markdown("## 📚 Glosario de Términos")
    
    terms = {
        "Equilibrio de Nash": "Perfil de estrategias donde ningún jugador puede mejorar unilateralmente.",
        "Estrategia Dominante": "Estrategia que siempre es la mejor respuesta, independientemente de las acciones de otros.",
        "Estrategia Dominada": "Estrategia que nunca es óptima, siempre hay otra mejor.",
        "Óptimo de Pareto": "Resultado donde no se puede mejorar a un jugador sin empeorar a otro.",
        "Juego de Suma Cero": "Juego donde las ganancias de unos son las pérdidas de otros.",
        "Información Perfecta": "Cada jugador conoce todas las acciones previas cuando le toca mover.",
        "Equilibrio Perfecto en Subjuegos": "Equilibrio de Nash que se mantiene en cada subjuego.",
        "Backward Induction": "Método para resolver juegos secuenciales desde el final hacia el inicio.",
        "Estrategia Mixta": "Elección probabilística entre estrategias puras.",
        "ESS": "Estrategia Evolutivamente Estable - no puede ser invadida por mutantes.",
        "Dinámicas de Replicadores": "Modelo de cómo evolucionan las frecuencias de estrategias en poblaciones.",
        "Función Característica": "En juegos cooperativos, valor que cada coalición puede asegurar.",
        "Valor de Shapley": "Forma justa de distribuir ganancias considerando contribuciones marginales.",
        "Núcleo (Core)": "Conjunto de asignaciones que no pueden ser mejoradas por ninguna coalición.",
        "Dilema del Prisionero": "Juego donde la racionalidad individual lleva a resultado subóptimo.",
        "Precio de la Anarquía": "Ratio entre óptimo social y equilibrio de Nash.",
        "Diseño de Mecanismos": "Ingeniería inversa: diseñar reglas para lograr objetivos deseados.",
        "Revelación de Preferencias": "Hacer que los agentes revelen honestamente sus valoraciones.",
        "Compatibilidad de Incentivos": "Propiedad donde decir la verdad es la mejor estrategia."
    }
    
    search = st.text_input("🔍 Buscar término:", "")
    
    for term, definition in sorted(terms.items()):
        if search.lower() in term.lower() or search == "":
            with st.expander(f"**{term}**"):
                st.markdown(definition)
    
    st.markdown("---")
    st.info("💡 **Tip**: Usa el buscador para encontrar términos específicos rápidamente.")
