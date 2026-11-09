# Teoría de Juegos: Guía Técnica Completa

## 1. Introducción

La **Teoría de Juegos** es una rama de las matemáticas aplicadas que estudia situaciones de interacción estratégica entre agentes racionales. Fue formalizada por John von Neumann y Oskar Morgenstern en 1944 con su obra "Theory of Games and Economic Behavior".

### 1.1 Definiciones Fundamentales

**Juego**: Una situación de interacción estratégica entre múltiples agentes (jugadores) donde:
- Cada jugador tiene un conjunto de acciones disponibles
- El resultado depende de las acciones de todos los jugadores
- Cada jugador tiene preferencias sobre los resultados

**Componentes de un Juego**:
1. **Jugadores** (N): Conjunto de participantes
2. **Estrategias** (S): Conjunto de acciones disponibles para cada jugador
3. **Pagos** (u): Función de utilidad que asigna un valor a cada combinación de estrategias

## 2. Representación de Juegos

### 2.1 Forma Normal (Estratégica)

Representa juegos donde los jugadores mueven simultáneamente.

**Ejemplo**: Dilema del Prisionero

```
           Jugador 2
           C      T
Jugador 1
    C    (3,3)  (0,5)
    T    (5,0)  (1,1)
```

### 2.2 Forma Extensiva

Representa juegos secuenciales mediante árboles de decisión.

```
        J1
       / \
      E   N
     /     \
    J2     (0,5)
   / \
  F   A
 /     \
(-1,-1) (2,2)
```

## 3. Conceptos de Solución

### 3.1 Equilibrio de Nash

**Definición**: Un perfil de estrategias s* = (s₁*, s₂*, ..., sₙ*) es un Equilibrio de Nash si para todo jugador i:

```
uᵢ(sᵢ*, s₋ᵢ*) ≥ uᵢ(sᵢ, s₋ᵢ*) para todo sᵢ ∈ Sᵢ
```

Donde:
- uᵢ es la función de utilidad del jugador i
- s₋ᵢ* representa las estrategias de todos los demás jugadores

**Propiedades**:
- Puede no existir en estrategias puras
- Siempre existe en estrategias mixtas (Teorema de Nash, 1950)
- No necesariamente es único
- No garantiza optimalidad de Pareto

### 3.2 Estrategia Dominante

**Definición**: Una estrategia sᵢ* domina estrictamente a sᵢ si:

```
uᵢ(sᵢ*, s₋ᵢ) > uᵢ(sᵢ, s₋ᵢ) para todo s₋ᵢ
```

Si todos los jugadores tienen estrategia dominante, el resultado es un **Equilibrio en Estrategias Dominantes** (más fuerte que Nash).

### 3.3 Equilibrio Perfecto en Subjuegos (SPE)

**Definición**: Un equilibrio de Nash que representa un equilibrio de Nash en cada subjuego.

**Método de Solución**: Backward Induction
1. Comenzar desde los nodos terminales
2. Calcular la mejor acción en cada nodo de decisión
3. Propagar hacia atrás hasta la raíz

## 4. Teoría de Juegos Evolutiva

### 4.1 Estrategia Evolutivamente Estable (ESS)

**Definición**: Una estrategia s es ESS si para toda estrategia mutante m ≠ s:

```
E(s,s) > E(m,s)  o
E(s,s) = E(m,s) y E(s,m) > E(m,m)
```

Donde E(x,y) es el pago esperado de jugar x contra y.

### 4.2 Dinámica de Replicadores

La proporción de la población que juega estrategia i evoluciona según:

```
dxᵢ/dt = xᵢ[fᵢ(x) - f̄(x)]
```

Donde:
- xᵢ es la fracción de la población jugando i
- fᵢ(x) es el fitness de la estrategia i
- f̄(x) es el fitness promedio de la población

## 5. Juegos Cooperativos

### 5.1 Función Característica

v: 2^N → ℝ asigna a cada coalición S ⊆ N el valor que puede asegurar.

### 5.2 Valor de Shapley

Reparto justo basado en contribuciones marginales:

```
φᵢ(v) = Σ |S|!(n-|S|-1)!/n! [v(S∪{i}) - v(S)]
      S⊆N\{i}
```

### 5.3 Núcleo (Core)

```
Core(v) = {x ∈ ℝⁿ : Σxᵢ = v(N) y Σxᵢ ≥ v(S) para todo S ⊆ N}
                    i∈N           i∈S
```

## 6. Aplicaciones Avanzadas

### 6.1 Diseño de Mecanismos

**Principio de Revelación**: Todo mecanismo puede ser implementado por uno donde revelar la verdad es estrategia dominante.

**Mecanismo de Vickrey-Clarke-Groves (VCG)**:
- Asignación eficiente
- Pagos = externalidad causada a otros

### 6.2 Juegos Repetidos

**Teorema de Folk**: En juegos infinitamente repetidos con suficiente paciencia, cualquier resultado individualmente racional puede ser sostenido como equilibrio de Nash.

Factor de descuento: δ ∈ (0,1)

Valor presente: V = Σ δᵗuₜ
                   t=0

## 7. Limitaciones y Críticas

1. **Supuesto de Racionalidad**: Los humanos no siempre son perfectamente racionales
2. **Conocimiento Común**: Difícil de lograr en la práctica
3. **Múltiples Equilibrios**: No hay predicción única en muchos juegos
4. **Complejidad Computacional**: Encontrar equilibrios es NP-hard en general

## 8. Herramientas Matemáticas

### 8.1 Punto Fijo de Brouwer

Base del teorema de existencia de Nash: Toda función continua de un conjunto convexo, compacto y no vacío en sí mismo tiene un punto fijo.

### 8.2 Programación Lineal

Usado para encontrar estrategias mixtas maximizando utilidad esperada sujeto a restricciones de probabilidad.

### 8.3 Ecuaciones Diferenciales

Modelan dinámicas evolutivas y convergencia a equilibrios.

## 9. Software y Herramientas

- **Gambit**: Análisis de juegos finitos
- **Python libraries**: Nashpy, Axelrod, scipy
- **Visualización**: NetworkX para árboles de juego

## 10. Referencias Clave

1. von Neumann, J. & Morgenstern, O. (1944). Theory of Games and Economic Behavior
2. Nash, J. (1950). Equilibrium Points in N-Person Games
3. Maynard Smith, J. (1982). Evolution and the Theory of Games
4. Osborne, M. & Rubinstein, A. (1994). A Course in Game Theory
5. Fudenberg, D. & Tirole, J. (1991). Game Theory

---

**Nota**: Esta es una guía técnica. Para aplicaciones prácticas, consulta los módulos interactivos de la aplicación.
