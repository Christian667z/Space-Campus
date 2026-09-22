# Propositions, Connecteurs et Raisonnement Logique

**Difficulté :** ★★★★★★★☆☆☆

## Théorie
LOGIQUE MATHÉMATIQUE — BASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Une PROPOSITION est un énoncé qui est soit VRAI soit FAUX (pas les deux).
Exemples: "2 + 2 = 4" (vrai), "Python est un langage compilé" (faux)
Non-exemples: "Ferme la porte!" (ordre), "x > 5" (dépend de x)

CONNECTEURS LOGIQUES :
  ¬P       : Négation (NON P)
  P ∧ Q    : Conjonction (P ET Q)
  P ∨ Q    : Disjonction (P OU Q)
  P → Q    : Implication (SI P ALORS Q)
  P ↔ Q    : Équivalence (P SI ET SEULEMENT SI Q)

IMPLICATION P → Q (PIÈGE CLASSIQUE !)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌───┬───┬───────┐
  │ P │ Q │ P → Q │
  ├───┼───┼───────┤
  │ V │ V │   V   │  ← Normal
  │ V │ F │   F   │  ← Promesse non tenue
  │ F │ V │   V   │  ← Surprenant! (faux → vrai = vrai)
  │ F │ F │   V   │  ← Surprenant! (faux → faux = vrai)
  └───┴───┴───────┘

RÈGLE D'OR : P → Q est FAUX seulement quand P est VRAI et Q est FAUX
Analogie: "SI tu travailles ALORS tu réussiras"
  - Si tu travailles et réussis → V (logique)
  - Si tu travailles et échoues → F (promesse non tenue)
  - Si tu ne travailles pas et réussis → V (pas de contradiction)
  - Si tu ne travailles pas et échoues → V (promesse pas violée)

FORMES ÉQUIVALENTES À P → Q :
  Contraposée : ¬Q → ¬P  (équivalente, même valeur de vérité)
  Réciproque  : Q → P    (PAS équivalente!)
  Inverse     : ¬P → ¬Q  (PAS équivalente!)

TAUTOLOGIE vs CONTRADICTION :
  Tautologie    : Toujours vraie   → P ∨ ¬P
  Contradiction : Toujours fausse  → P ∧ ¬P
  Contingence   : Parfois vrai/faux → P ∧ Q

## Points Clés
- Proposition = énoncé vrai ou faux (pas les deux)
- P→Q est FAUX seulement si P=Vrai et Q=Faux
- Contraposée (¬Q→¬P) = équivalente à P→Q
- Réciproque (Q→P) ≠ P→Q (erreur classique!)
- Tautologie = toujours vraie (P∨¬P)

> **⚠️ Piège Prof :** La contraposée EST logiquement équivalente à l'implication originale. La réciproque NE L'EST PAS. Beaucoup d'étudiants confondent les deux!

## Exercice
**Énoncé :** Donne la contraposée et la réciproque de: 'Si tu codes, tu comprends l'informatique'

<details>
<summary><b>Voir la Correction</b></summary>

✅ Original: P→Q (coder → comprendre). Contraposée: ¬Q→¬P = 'Si tu ne comprends pas l'informatique, tu ne codes pas' (ÉQUIVALENTE). Réciproque: Q→P = 'Si tu comprends l'informatique, tu codes' (PAS équivalente).

</details>
