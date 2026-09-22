# CSS3 — Mise en Forme et Layout

**Difficulté :** ★★★★★★☆☆☆☆

## Théorie
CSS3 — CASCADE STYLE SHEETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS contrôle l'APPARENCE visuelle du HTML.
Séparation des rôles : HTML (structure) + CSS (présentation)

SÉLECTEURS CSS — HIÉRARCHIE DE SPÉCIFICITÉ :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Inline style   (1000pts) : style="color:red"      ← Priorité MAX
  #id            (100pts)  : #monId { color: red; }
  .classe        (10pts)   : .maClasse { color: red;}
  balise         (1pt)     : p { color: red; }       ← Priorité MIN

RÈGLE : En cas de conflit, la SPÉCIFICITÉ la plus haute gagne.
Si égalité, la règle déclarée EN DERNIER gagne (cascade).

BOX MODEL — TOUT ÉLÉMENT EST UNE BOÎTE :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌────────────────────────────────┐
  │           MARGIN               │ ← Espace ENTRE éléments
  │  ┌──────────────────────────┐  │
  │  │         BORDER           │  │ ← Bordure visible
  │  │  ┌────────────────────┐  │  │
  │  │  │     PADDING        │  │  │ ← Espace intérieur
  │  │  │  ┌──────────────┐  │  │  │
  │  │  │  │   CONTENT    │  │  │  │ ← Le contenu réel
  │  │  │  └──────────────┘  │  │  │
  │  │  └────────────────────┘  │  │
  │  └──────────────────────────┘  │
  └────────────────────────────────┘

box-sizing: border-box ← TOUJOURS utiliser!
  Sans: width=content seulement (confus)
  Avec: width=content+padding+border (intuitif)

FLEXBOX — LAYOUT 1D :
━━━━━━━━━━━━━━━━━━━━

.container {
  display: flex;
  justify-content: center;    /* Axe principal */
  align-items: center;        /* Axe secondaire */
  gap: 20px;
  flex-wrap: wrap;
}

GRID — LAYOUT 2D :
━━━━━━━━━━━━━━━━━

.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

## Points Clés
- Spécificité: Inline(1000) > #id(100) > .classe(10) > balise(1)
- Box model: Content + Padding + Border + Margin
- box-sizing: border-box à toujours utiliser
- Flexbox = 1D (ligne ou colonne), Grid = 2D
- justify-content = axe principal, align-items = axe croisé

> **⚠️ Piège Prof :** margin: auto vs text-align: center: margin: 0 auto centre un BLOC horizontalement. text-align: center centre le CONTENU texte inline. Pour centrer verticalement, il faut Flexbox ou Grid — il n'y a pas de vertical-align simple pour les blocs!

## Exercice
**Énoncé :** Écris le CSS pour centrer un div de 300x200px horizontalement et verticalement dans la page.

<details>
<summary><b>Voir la Correction</b></summary>

✅ body { display: flex; justify-content: center; align-items: center; min-height: 100vh; } .box { width: 300px; height: 200px; }

</details>
