# Modélisation Relationnelle — Théorie et Pratique

**Difficulté :** ★★★★★★★★☆☆

## Théorie
BASES DE DONNÉES RELATIONNELLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inventées par Edgar F. Codd (IBM, 1970) sur la théorie des ensembles.
Principe : données organisées en TABLES avec des RELATIONS entre elles.

TERMINOLOGIE PRÉCISE :
  Relation = Table
  Tuple    = Ligne / Enregistrement
  Attribut = Colonne / Champ
  Domaine  = Ensemble de valeurs possibles d'un attribut

CLÉS :
━━━━━

CLÉ PRIMAIRE (PRIMARY KEY) :
  • Identifie UNIQUEMENT chaque tuple
  • UNIQUE : Pas deux lignes avec la même valeur
  • NON NULL : Obligatoirement renseignée
  • SIMPLE : un attribut | COMPOSITE : plusieurs attributs

CLÉ ÉTRANGÈRE (FOREIGN KEY) :
  • Référence la clé primaire d'une AUTRE table
  • Assure l'INTÉGRITÉ RÉFÉRENTIELLE
  • Valeur doit exister dans la table référencée ou être NULL

FORMES NORMALES (NORMALISATION) :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1NF : Chaque cellule contient UNE SEULE valeur atomique
2NF : 1NF + Tout attribut dépend de TOUTE la clé primaire
3NF : 2NF + Pas de dépendance transitive (A→B→C interdit)

OPÉRATIONS RELATIONNELLES :
  σ (Sélection)    : Filtrer des lignes → WHERE
  π (Projection)   : Sélectionner des colonnes → SELECT col
  ⋈ (Jointure)     : Combiner deux tables → JOIN
  ∪ (Union)        : Réunir deux tables → UNION
  − (Différence)   : Lignes dans A mais pas B → EXCEPT

SQL COMPLET :
━━━━━━━━━━━━

DDL (Data Definition Language) :
  CREATE TABLE, ALTER TABLE, DROP TABLE

DML (Data Manipulation Language) :
  SELECT, INSERT, UPDATE, DELETE

DCL (Data Control Language) :
  GRANT, REVOKE (permissions)

TCL (Transaction Control Language) :
  BEGIN, COMMIT, ROLLBACK, SAVEPOINT

## Points Clés
- Clé primaire = unique + non null + identifie une ligne
- Clé étrangère = référence clé primaire autre table
- Intégrité référentielle = cohérence des relations
- 3 formes normales pour éliminer la redondance
- SQL divisé en DDL, DML, DCL, TCL

> **⚠️ Piège Prof :** DELETE vs TRUNCATE vs DROP: DELETE supprime des lignes avec WHERE (rollback possible). TRUNCATE vide TOUTE la table ultra-rapidement (difficile à annuler). DROP supprime la TABLE ENTIÈRE structure+données. Pas la même chose!

## Exercice
**Énoncé :** Conçois un schéma relationnel pour une école: étudiants, cours, et inscriptions.

<details>
<summary><b>Voir la Correction</b></summary>

✅ ETUDIANT(id_etudiant PK, nom, prenom, date_naissance). COURS(id_cours PK, titre, credits, id_prof FK). INSCRIPTION(id_etudiant FK, id_cours FK, note, date) PK=composite(id_etudiant, id_cours).

</details>
