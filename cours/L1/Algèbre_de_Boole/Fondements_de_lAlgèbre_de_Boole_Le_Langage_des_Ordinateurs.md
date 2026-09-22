# Fondements de l'Algèbre de Boole — Le Langage des Ordinateurs

**Difficulté :** ★★★★★★★☆☆☆

## Théorie
ALGÈBRE DE BOOLE — POURQUOI C'EST CRUCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inventée par George Boole (1854). Appliquée aux circuits par Claude Shannon (1937).
TOUT ordinateur fonctionne avec 2 états: 0 (faux) et 1 (vrai).
L'algèbre de Boole est le FONDEMENT mathématique des circuits logiques.

LES 3 OPÉRATEURS DE BASE :
━━━━━━━━━━━━━━━━━━━━━━━━━

1. NOT (¬, !) — Négation
   ┌───┬──────┐
   │ A │ ¬A   │
   ├───┼──────┤
   │ 0 │  1   │
   │ 1 │  0   │
   └───┴──────┘

2. AND (·, &&) — Conjonction (VRAI seulement si LES DEUX sont vrais)
   ┌───┬───┬───────┐
   │ A │ B │ A · B │
   ├───┼───┼───────┤
   │ 0 │ 0 │   0   │
   │ 0 │ 1 │   0   │
   │ 1 │ 0 │   0   │
   │ 1 │ 1 │   1   │
   └───┴───┴───────┘

3. OR (+, ||) — Disjonction (VRAI si AU MOINS UN est vrai)
   ┌───┬───┬───────┐
   │ A │ B │ A + B │
   ├───┼───┼───────┤
   │ 0 │ 0 │   0   │
   │ 0 │ 1 │   1   │
   │ 1 │ 0 │   1   │
   │ 1 │ 1 │   1   │
   └───┴───┴───────┘

PRIORITÉ DES OPÉRATEURS (TRÈS IMPORTANT) :
  NOT (¬) > AND (·) > OR (+)
  Comme en maths: parenthèses > × > +
  Exemple: A + B·C = A + (B·C)   ← Le AND est prioritaire!

PORTES LOGIQUES DÉRIVÉES :
  NAND : ¬(A·B) — Universelle (peut tout construire)
  NOR  : ¬(A+B) — Universelle aussi
  XOR  : A⊕B = A·¬B + ¬A·B (différent, l'un ou l'autre mais pas les deux)
  XNOR : ¬(A⊕B) (identique, les deux pareils)

LOIS FONDAMENTALES :
  • Identité    : A·1 = A    |  A+0 = A
  • Annulation  : A·0 = 0    |  A+1 = 1
  • Idempotence : A·A = A    |  A+A = A
  • Complément  : A·¬A = 0  |  A+¬A = 1
  • De Morgan 1 : ¬(A·B) = ¬A+¬B
  • De Morgan 2 : ¬(A+B) = ¬A·¬B

## Points Clés
- AND = 1 seulement si les DEUX entrées sont 1
- OR = 1 si AU MOINS UNE entrée est 1
- NOT = inverse la valeur
- Priorité: NOT > AND > OR
- Lois de De Morgan: convertir AND↔OR avec NOT
- NAND et NOR sont des portes universelles

## Exercice
**Énoncé :** Construis la table de vérité pour: F = A·B + ¬A·C (3 variables, 8 lignes)

<details>
<summary><b>Voir la Correction</b></summary>

✅ A=0,B=0,C=0: F=0. A=0,B=0,C=1: F=1. A=0,B=1,C=0: F=0. A=0,B=1,C=1: F=1. A=1,B=0,C=0: F=0. A=1,B=0,C=1: F=0. A=1,B=1,C=0: F=1. A=1,B=1,C=1: F=1.

</details>
