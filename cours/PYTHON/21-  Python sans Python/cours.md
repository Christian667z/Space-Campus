# Python sans Python — Compilateurs alternatifs & exécution haute performance  
## (Mojo • PyPy • Stackless Python)

**Difficulté :** ★★★★★★★★★★++ (niveau recherche / systèmes / compilation)

---

# Introduction académique

Le paradigme “Python sans Python” fait référence à l’exécution ou la réimplémentation de Python via des moteurs alternatifs visant :

- l’optimisation extrême des performances,
- la réduction de la latence d’exécution,
- la concurrence massive,
- ou la compilation vers des architectures bas niveau.

Dans ce contexte, Python cesse d’être uniquement un langage interprété, et devient une **spécification logique exécutée par différents moteurs**.

---

# 1. Vision globale : Python n’est pas un seul runtime

---

## Définition importante

Le langage Python est une **spécification**, pas une implémentation unique.

Implémentations connues :

- CPython (référence officielle)
- PyPy (JIT)
- Stackless Python (microthreads)
- Mojo (nouvelle génération compilée)

---

## Interprétation académique

On distingue :

\[
\text{Langage} \neq \text{Runtime}
\]

---

# 2. PyPy — Python avec JIT (Just-In-Time Compilation)

---

# 2.1 Définition

PyPy est une implémentation alternative de Python utilisant un **JIT compiler**.

👉 Il compile dynamiquement le code en machine code pendant l’exécution.

---

# 2.2 Principe scientifique

Au lieu de :

```text
Python → bytecode → interprétation (CPython)
```

PyPy fait :

```text
Python → analyse runtime → compilation JIT → machine code
```

---

# 2.3 Pourquoi PyPy est plus rapide ?

## Optimisations internes :

- inline caching
- escape analysis
- loop unrolling
- trace-based compilation

---

# 2.4 Exemple (transparent)

```python
def f(n):
    s = 0
    for i in range(n):
        s += i
    return s

print(f(10_000_000))
```

👉 Aucun changement de code requis  
👉 PyPy optimise automatiquement les boucles chaudes

---

# 2.5 Limites

- startup plus lent
- compatibilité partielle avec C extensions
- gain dépend du type de programme

---

# 3. Stackless Python — Concurrence massive

---

# 3.1 Définition

Stackless Python est une version modifiée de Python qui supprime la pile d’appel native C pour permettre :

> des millions de micro-threads (tasklets)

---

# 3.2 Concept fondamental

Au lieu de threads OS lourds :

| Modèle | Coût |
|---|---|
| Thread OS | lourd |
| Asyncio | moyen |
| Stackless tasklets | ultra léger |

---

# 3.3 Microthreads (Tasklets)

```python
import stackless

def task(name):
    print("Task:", name)

stackless.tasklet(task)("A")
stackless.tasklet(task)("B")

stackless.run()
```

---

# 3.4 Analyse

- chaque tasklet = coroutine légère
- scheduling coopératif
- mémoire minimale par tâche

---

# 3.5 Applications

- jeux massivement concurrents
- simulations (agents)
- systèmes distribués
- moteurs temps réel

---

# 4. Mojo — “Python compilé comme du C++”

---

# 4.1 Définition

Mojo est un langage moderne conçu pour :

> conserver la syntaxe Python tout en atteignant des performances proches du C++ / CUDA.

---

# 4.2 Philosophie

Mojo vise à résoudre le problème historique :

> Python est facile mais lent.

---

# 4.3 Différence fondamentale

| Python classique | Mojo |
|---|---|
| interprété | compilé |
| dynamique | typage optionnel fort |
| lent CPU | optimisé GPU/CPU |
| CPython runtime | MLIR / LLVM backend |

---

# 4.4 Exemple Mojo (style Python)

```python
fn add(a: Int, b: Int) -> Int:
    return a + b

print(add(2, 3))
```

---

# 4.5 Analyse technique

Mojo introduit :

- typage statique optionnel
- compilation LLVM
- vectorisation automatique
- support GPU natif

---

# 4.6 Pourquoi Mojo est révolutionnaire ?

Parce qu’il fusionne :

- simplicité Python
- performance C++
- accélération IA (GPU-first design)

---

# 5. Comparaison des 3 systèmes

---

| Technologie | Objectif | Performance | Usage |
|---|---|---|---|
| PyPy | accélération Python existant | ★★★★☆ | apps générales |
| Stackless | concurrence massive | ★★★★☆ | simulation / MMO |
| Mojo | remplacement haute perf | ★★★★★ | IA / HPC |

---

# 6. Modèle mental unifié

---

On peut voir ces systèmes comme :

\[
\text{Python} = \text{Spécification}
\]

et :

- PyPy = optimisation runtime
- Stackless = optimisation concurrence
- Mojo = compilation totale

---

# 7. Impact sur l’architecture logicielle

---

## 7.1 Changement de paradigme

Avant :

```text
Python = scripting only
```

Après :

```text
Python ecosystem = multi-runtime performance stack
```

---

## 7.2 Choix d’architecture

- CPU-heavy → Mojo
- legacy Python → PyPy
- concurrency-heavy → Stackless / asyncio

---

# 8. Limites générales

---

- fragmentation des écosystèmes
- compatibilité des bibliothèques
- maturité variable (Mojo encore jeune)
- debugging complexe
- portabilité non uniforme

---

# 9. Applications industrielles

---

- intelligence artificielle (Mojo)
- simulation massive (Stackless)
- optimisation backend (PyPy)
- finance haute fréquence
- moteurs de jeu
- systèmes distribués

---

# 10. Points clés (niveau recherche)

---

- Python n’est pas un runtime unique
- PyPy introduit compilation JIT dynamique
- Stackless permet micro-concurrence massive
- Mojo transforme Python en langage compilé HPC
- performance dépend du modèle d’exécution, pas du langage seul

---

# EXERCICES (niveau Harvard / systèmes avancés)

---

## Exercice 1
Pourquoi PyPy peut être plus rapide que CPython ?

### Correction

Car il compile les parties “chaudes” du code en machine code via JIT, réduisant le coût de l’interprétation répétée.

---

## Exercice 2
Pourquoi Stackless Python peut gérer des millions de tâches ?

### Correction

Car les tasklets ne dépendent pas du système d’exploitation et ont une empreinte mémoire très faible.

---

## Exercice 3
Différence fondamentale entre Python et Mojo ?

### Correction

Python est interprété dynamiquement, Mojo est compilé statiquement avec backend LLVM.

---

## Exercice 4
Pourquoi le JIT est efficace sur les boucles ?

### Correction

Car les boucles exécutent les mêmes instructions plusieurs fois, permettant une optimisation runtime.

---

## Exercice 5
Pourquoi Python classique est limité pour HPC ?

### Correction

À cause du GIL, de l’interprétation et du manque de compilation native.

---

## Exercice 6
Stackless vs asyncio ?

### Correction

Stackless = microthreads natifs  
Asyncio = event loop basé sur coroutines Python

---

## Exercice 7
Pourquoi Mojo est important pour l’IA ?

### Correction

Car il permet d’exécuter du code Python-like avec performance GPU native.

---

## Exercice 8
Quel est le rôle de LLVM dans Mojo ?

### Correction

Compiler le code en instructions machine optimisées multi-plateformes.

---

## Exercice 9
PyPy est-il compatible avec toutes les librairies Python ?

### Correction

Non, surtout limité avec certaines extensions C.

---

## Exercice 10
Quel est le futur de Python selon ces technologies ?

### Correction

Un écosystème multi-runtime où performance et simplicité coexistent via différents backends.

---