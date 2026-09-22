# Algorithmique — Penser Avant de Coder

**Difficulté :** ★★★★★★☆☆☆☆

## Théorie
QU'EST-CE QU'UN ALGORITHME ?
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Un algorithme est une SUITE FINIE et NON-AMBIGUË d'instructions
permettant de résoudre un problème ou d'accomplir une tâche.

Propriétés d'un bon algorithme :
  1. FINITUDE : S'arrête toujours (pas de boucle infinie)
  2. PRÉCISION : Chaque étape est non-ambiguë
  3. ENTRÉES : 0 ou plusieurs données en entrée
  4. SORTIES : Au moins un résultat
  5. EFFECTIVITÉ : Chaque opération est réalisable

STRUCTURES DE CONTRÔLE :
━━━━━━━━━━━━━━━━━━━━━━━

1. SÉQUENCE — Instructions exécutées l'une après l'autre
   DÉBUT
     Instruction 1
     Instruction 2
     Instruction 3
   FIN

2. CONDITION — Branchement selon une condition
   SI (condition) ALORS
     Instructions si VRAI
   SINON
     Instructions si FAUX
   FIN SI

3. BOUCLE TANT QUE — Répétition conditionnelle
   TANT QUE (condition) FAIRE
     Instructions
   FIN TANT QUE

4. BOUCLE POUR — Répétition avec compteur
   POUR i DE 1 À n FAIRE
     Instructions
   FIN POUR

EXEMPLE — Algorithme de la moyenne :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALGORITHME CalculerMoyenne
VARIABLES:
  notes : tableau de réels
  n : entier (nombre de notes)
  somme, moyenne : réels

DÉBUT
  somme ← 0
  POUR i DE 0 À n-1 FAIRE
    somme ← somme + notes[i]
  FIN POUR
  
  SI n > 0 ALORS
    moyenne ← somme / n
    AFFICHER "Moyenne: " + moyenne
  SINON
    AFFICHER "Aucune note!"
  FIN SI
FIN

## Points Clés
- Algorithme = suite finie d'instructions non-ambiguës
- 3 structures: Séquence, Condition, Boucle
- Pseudocode = langage intermédiaire entre français et code
- Toujours penser l'algorithme AVANT d'écrire le code
- Test de l'algorithme sur des cas simples avant implémentation

> **⚠️ Piège Prof :** Attention aux indices de tableaux: en C ils commencent à 0, pas 1. Un tableau de 5 éléments a des indices 0,1,2,3,4. L'élément à l'indice 5 N'EXISTE PAS et provoque un segfault.

## Exercice
**Énoncé :** Écris un algorithme en pseudocode qui demande 5 nombres à l'utilisateur et affiche le plus grand.

<details>
<summary><b>Voir la Correction</b></summary>

✅ VARIABLES: max, n, i: entiers. DÉBUT. max ← 0. POUR i DE 1 À 5: LIRE n. SI n > max ALORS max ← n FIN SI. FIN POUR. AFFICHER 'Maximum: ' + max. FIN

</details>
