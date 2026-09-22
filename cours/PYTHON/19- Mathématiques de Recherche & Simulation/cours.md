# Mathématiques de Recherche & Simulation (Python Scientifique Avancé)

**Difficulté :** ★★★★★★★★★★ (Niveau Recherche / Master / PhD débutant)

---

# Introduction académique

Les mathématiques de recherche appliquées à l’informatique scientifique consistent à utiliser des outils computationnels pour :
- modéliser des systèmes physiques,
- résoudre des équations complexes,
- simuler des phénomènes naturels,
- analyser des structures biologiques,
- automatiser des calculs symboliques et numériques.

En science moderne, Python est devenu un langage central car il relie :
- mathématiques appliquées,
- simulation numérique,
- intelligence scientifique,
- recherche interdisciplinaire.

---

# 1. Calcul Scientifique Avancé (SciPy)

---

## 1.1 Définition formelle

Le calcul scientifique numérique consiste à approximer des solutions de problèmes mathématiques continus :

- équations différentielles (ODE / PDE)
- optimisation
- intégration numérique
- systèmes dynamiques

---

## 1.2 Exemple fondamental : équation différentielle

On considère une équation classique :

\[
\frac{dy}{dt} = -ky
\]

(solution d’un système de décroissance exponentielle)

---

## 1.3 Résolution avec SciPy

```python
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# dy/dt = -k y
def model(t, y):
    k = 0.5
    return -k * y

solution = solve_ivp(model, (0, 10), [10], t_eval=np.linspace(0, 10, 100))

plt.plot(solution.t, solution.y[0])
plt.title("Exponential Decay Simulation")
plt.show()
```

---

## 1.4 Analyse scientifique

Ce modèle représente :
- désintégration radioactive
- refroidissement thermique
- décroissance biologique

---

## 1.5 Interprétation avancée

La solution numérique approxime :

\[
y(t) = y_0 e^{-kt}
\]

SciPy ne “résout pas symboliquement”, mais **approxime dynamiquement**.

---

# 2. Systèmes dynamiques non linéaires

---

## Exemple : système de Lorenz

\[
\frac{dx}{dt} = \sigma(y - x)
\]
\[
\frac{dy}{dt} = x(\rho - z) - y
\]
\[
\frac{dz}{dt} = xy - \beta z
\]

---

## Simulation Python

```python
def lorenz(t, state):
    x, y, z = state
    sigma = 10
    rho = 28
    beta = 8/3

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return [dx, dy, dz]
```

---

## Interprétation

Ce système est chaotique :
- sensible aux conditions initiales
- imprévisible à long terme
- base de la théorie du chaos

---

# 3. Calcul Symbolique (SymPy)

---

## 3.1 Définition

Le calcul symbolique consiste à manipuler des expressions mathématiques exactes.

Contrairement à SciPy :
- SciPy = numérique
- SymPy = analytique

---

## 3.2 Variables symboliques

```python
import sympy as sp

x = sp.Symbol('x')
```

---

## 3.3 Dérivation symbolique

```python
f = x**2 + 3*x + 2
sp.diff(f, x)
```

Résultat :

\[
2x + 3
\]

---

## 3.4 Intégration symbolique

```python
sp.integrate(x**2, x)
```

Résultat :

\[
\frac{x^3}{3}
\]

---

## 3.5 Résolution d’équations

```python
sp.solve(x**2 - 4, x)
```

Résultat :
\[
x = -2, 2
\]

---

## 3.6 Interprétation scientifique

SymPy est utilisé pour :
- mathématiques théoriques
- preuve symbolique
- physique analytique
- optimisation exacte

---

# 4. Bioinformatique (BioPython)

---

## 4.1 Définition

La bioinformatique utilise des algorithmes pour analyser :
- ADN
- ARN
- protéines
- séquences biologiques

---

## 4.2 ADN comme structure informatique

ADN = chaîne de caractères :

```text
A, T, C, G
```

---

## 4.3 Exemple BioPython

```python
from Bio.Seq import Seq

dna = Seq("ATGCGTACGTTAGC")

print(dna)
print(dna.complement())
print(dna.reverse_complement())
```

---

## 4.4 Analyse scientifique

- A ↔ T
- C ↔ G

Cela permet :
- reconstruction génétique
- analyse mutationnelle

---

## 4.5 Traduction ADN → Protéine

```python
from Bio.Seq import Seq

dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
protein = dna.translate()

print(protein)
```

---

## 4.6 Interprétation

- ADN → codons
- codons → acides aminés
- protéines → fonctions biologiques

---

# 5. Simulation scientifique intégrée

---

## Exemple hybride

```python
import numpy as np
from scipy.integrate import solve_ivp

def population(t, y):
    r = 0.3
    return r * y

sol = solve_ivp(population, (0, 10), [100])

print(sol.y[0])
```

---

## Interprétation

Modélise :
- croissance population
- dynamique écologique
- propagation virus

---

# 6. Comparaison des outils scientifiques

| Domaine | Outil | Nature |
|---|---|---|
| Simulation | SciPy | numérique |
| Math symbolique | SymPy | analytique |
| Bioinformatique | BioPython | biologique |
| Data science | NumPy/Pandas | statistique |

---

# 7. Limites scientifiques

---

- approximation numérique ≠ solution exacte
- modèles sensibles aux paramètres
- complexité computationnelle élevée
- dépendance aux bibliothèques
- erreurs d’arrondi machine

---

# 8. Bonnes pratiques de recherche

---

- valider résultats analytiques et numériques
- comparer plusieurs modèles
- normaliser les données
- vérifier stabilité numérique
- documenter les hypothèses

---

# 9. Applications réelles

---

- physique quantique
- climatologie
- génétique
- finance quantitative
- astrophysique
- intelligence artificielle scientifique

---

# 10. Points clés (niveau recherche)

---

- SciPy = simulation numérique d’équations différentielles
- SymPy = manipulation symbolique exacte
- BioPython = analyse biologique computationnelle
- la science moderne repose sur hybridation numérique + analytique
- les modèles sont toujours des approximations du réel

---

# EXERCICES (niveau Harvard / recherche)

---

## Exercice 1 — ODE (SciPy)

Résoudre :

\[
\frac{dy}{dt} = -2y
\]

### Correction

```python
def model(t, y):
    return -2 * y
```

Solution théorique :

\[
y(t) = y_0 e^{-2t}
\]

---

## Exercice 2 — Interprétation

Pourquoi les solutions numériques ne sont-elles pas exactes ?

### Correction

Car les solveurs utilisent des approximations discrètes (méthodes de Runge-Kutta).

---

## Exercice 3 — SymPy dérivation

Calculer la dérivée de \( x^3 + 2x \)

### Correction

```python
sp.diff(x**3 + 2*x, x)
```

Résultat :
\[
3x^2 + 2
\]

---

## Exercice 4 — SymPy intégration

Intégrer \( x^2 \)

### Correction

```python
sp.integrate(x**2, x)
```

Résultat :
\[
\frac{x^3}{3}
\]

---

## Exercice 5 — ADN complémentaire

Pourquoi A se lie avec T ?

### Correction

Structure chimique des bases azotées permettant stabilité de la double hélice.

---

## Exercice 6 — BioPython

Que fait translate() ?

### Correction

Convertit ADN → protéines via codons.

---

## Exercice 7 — Modélisation

Quel type de système est Lorenz ?

### Correction

Système chaotique non linéaire.

---

## Exercice 8 — Chaos

Pourquoi les systèmes chaotiques sont imprévisibles ?

### Correction

Sensibilité extrême aux conditions initiales.

---

## Exercice 9 — Différence SciPy vs SymPy

### Correction

SciPy = approximation numérique  
SymPy = solution exacte symbolique

---

## Exercice 10 — Application réelle

Donner un domaine scientifique utilisant ces outils.

### Correction

Physique, biologie, finance quantitative, IA scientifique.

---