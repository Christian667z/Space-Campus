# Informatique Quantique (Quantum Computing) — Cours Complet 

**Difficulté :** ★★★★★★★★★★ (Très avancé)

---

# Introduction

L’informatique quantique est un domaine de l’informatique qui utilise les lois de la mécanique quantique pour traiter l’information.

Contrairement à l’informatique classique (bits 0 ou 1), l’informatique quantique utilise des **qubits** capables d’être dans plusieurs états en même temps.

---

# 1. Différence entre classique et quantique

| Informatique classique | Informatique quantique |
|---|---|
| Bit (0 ou 1) | Qubit (0 et 1 simultanément) |
| Déterministe | Probabiliste |
| Calcul séquentiel | Superposition + parallélisme quantique |

---

# 2. Le Qubit

---

## Définition

Un qubit est l’unité de base de l’information quantique.

Il peut être :
- |0⟩
- |1⟩
- ou une combinaison des deux

---

## Superposition

```text
|ψ⟩ = α|0⟩ + β|1⟩
```

où :
- α et β sont des probabilités
- |α|² + |β|² = 1

---

# 3. Superposition

---

Un qubit peut exister dans plusieurs états en même temps.

### Exemple intuitif :
- Bit classique = pièce posée (pile ou face)
- Qubit = pièce en rotation

---

# 4. Intrication (Entanglement)

---

## Définition

Deux qubits peuvent être liés instantanément, même à distance.

---

## Exemple

Si un qubit change, l’autre change aussi immédiatement.

---

## Importance

- Téléportation quantique
- Cryptographie
- Calcul parallèle massif

---

# 5. Mesure quantique

---

Quand on mesure un qubit :
- la superposition disparaît
- on obtient 0 ou 1

---

## Exemple

```text
Avant mesure : 70% |0⟩ + 30% |1⟩
Après mesure : 0 OU 1
```

---

# 6. Portes quantiques (Quantum Gates)

---

## Définition

Les portes quantiques manipulent les qubits.

---

## 6.1 Hadamard Gate (H)

Crée la superposition.

```text
|0⟩ → superposition
```

---

## 6.2 Pauli-X (équivalent NOT)

```text
|0⟩ → |1⟩
|1⟩ → |0⟩
```

---

## 6.3 CNOT Gate

Utilisée pour l’intrication.

---

# 7. Circuit quantique

---

## Exemple simple

```text
|0⟩ → H → mesure
```

Résultat :
- 50% 0
- 50% 1

---

# 8. Algorithmes quantiques

---

# 8.1 Algorithme de Grover

- accélère la recherche
- passe de O(n) à O(√n)

---

# 8.2 Algorithme de Shor

- factorisation rapide
- menace la cryptographie RSA

---

# 9. Informatique quantique vs classique

---

| Domaine | Quantique avantage |
|---|---|
| Recherche | Très rapide |
| Cryptographie | Très puissant |
| Simulation moléculaire | Exact |
| IA | potentiel futur |

---

# 10. Langages quantiques

---

- Qiskit (IBM)
- Cirq (Google)
- Q# (Microsoft)

---

# 11. Python et informatique quantique

---

## Exemple avec Qiskit

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(1, 1)

qc.h(0)
qc.measure(0, 0)

print(qc)
```

---

# 12. Simulation quantique

---

## Exemple simple

```python
from qiskit import Aer, execute
from qiskit import QuantumCircuit

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')

job = execute(qc, backend, shots=1000)
result = job.result()

print(result.get_counts())
```

---

# 13. Applications réelles

---

- cryptographie
- médecine (simulation moléculaire)
- finance
- intelligence artificielle
- optimisation complexe

---

# 14. Limites actuelles

---

- instabilité des qubits
- erreurs fréquentes
- matériel coûteux
- température ultra basse requise
- peu de qubits disponibles

---

# 15. Concepts avancés

---

## Décohérence

Perte d’état quantique à cause de l’environnement.

---

## Correction d’erreurs quantiques

Système pour corriger les erreurs naturelles des qubits.

---

# 16. Architecture quantique

---

```text
Utilisateur
   ↓
Circuit quantique
   ↓
Ordinateur quantique
   ↓
Résultat probabiliste
```

---

# 17. Erreurs fréquentes

---

- confondre superposition et duplication
- penser que les qubits sont des bits classiques
- oublier la probabilité
- ignorer la décohérence

---

# 18. Bonnes pratiques

---

- penser en probabilités
- simuler avant exécution réelle
- comprendre les portes quantiques
- maîtriser les circuits simples avant avancé

---

# 19. Résumé du cours

---

- un qubit = 0 + 1 simultané
- superposition = plusieurs états
- intrication = liaison instantanée
- mesure = destruction de superposition
- portes = manipulation des qubits
- algorithmes quantiques = accélération massive

---

# 20. Exercices (10)

---

## Exercice 1
Qu’est-ce qu’un qubit ?

### Correction
Un bit quantique pouvant être 0 et 1 simultanément.

---

## Exercice 2
Que fait la porte Hadamard ?

### Correction
Elle crée une superposition.

---

## Exercice 3
Que se passe-t-il lors de la mesure ?

### Correction
La superposition disparaît.

---

## Exercice 4
Différence bit vs qubit ?

### Correction
Bit = 0 ou 1, qubit = probabiliste.

---

## Exercice 5
À quoi sert l’intrication ?

### Correction
Relier deux qubits instantanément.

---

## Exercice 6
Quel algorithme accélère la recherche ?

### Correction
Algorithme de Grover.

---

## Exercice 7
Quel algorithme menace RSA ?

### Correction
Algorithme de Shor.

---

## Exercice 8
Pourquoi la décohérence est un problème ?

### Correction
Elle détruit les états quantiques.

---

## Exercice 9
Quel langage utilise IBM ?

### Correction
Qiskit.

---

## Exercice 10
Pourquoi l’informatique quantique est puissante ?

### Correction
Car elle utilise superposition + intrication.

---

# Conclusion

L’informatique quantique représente une révolution majeure.

Elle n’est pas une amélioration de l’informatique classique, mais une **nouvelle manière de calculer** basée sur les lois de la physique.

---