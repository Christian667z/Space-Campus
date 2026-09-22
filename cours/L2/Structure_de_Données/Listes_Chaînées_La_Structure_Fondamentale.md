# Listes Chaînées — La Structure Fondamentale

**Difficulté :** ★★★★★★★★★☆

## Théorie
LISTE CHAÎNÉE — DÉFINITION
━━━━━━━━━━━━━━━━━━━━━━━━━━

Une liste chaînée est une structure où chaque NŒUD contient :
  1. La DONNÉE (valeur stockée)
  2. Un POINTEUR vers le nœud suivant (ou NULL si dernier)

Avantage sur tableau : Taille DYNAMIQUE, insertion/suppression O(1)
Désavantage : Accès séquentiel O(n), mémoire supplémentaire pour pointeurs

REPRÉSENTATION :
  HEAD → [5|→] → [12|→] → [8|→] → [3|NULL]
         Nœud1    Nœud2    Nœud3   Dernier nœud

IMPLÉMENTATION EN C :
━━━━━━━━━━━━━━━━━━━━

typedef struct Noeud {
    int donnee;
    struct Noeud* suivant;
} Noeud;

// Créer un nœud
Noeud* creerNoeud(int val) {
    Noeud* n = (Noeud*)malloc(sizeof(Noeud));
    n->donnee = val;
    n->suivant = NULL;
    return n;
}

// Insérer en tête (O(1))
Noeud* insererTete(Noeud* head, int val) {
    Noeud* n = creerNoeud(val);
    n->suivant = head;
    return n; // Nouveau head
}

// Parcourir la liste (O(n))
void afficher(Noeud* head) {
    Noeud* courant = head;
    while (courant != NULL) {
        printf("%d → ", courant->donnee);
        courant = courant->suivant;
    }
    printf("NULL\n");
}

// Libérer la mémoire (OBLIGATOIRE en C!)
void liberer(Noeud* head) {
    Noeud* temp;
    while (head != NULL) {
        temp = head;
        head = head->suivant;
        free(temp);
    }
}

COMPLEXITÉ :
  Insertion en tête : O(1)
  Insertion en queue : O(n) sans pointeur de queue
  Recherche        : O(n)
  Suppression tête : O(1)
  Accès par index  : O(n)

## Points Clés
- Nœud = donnée + pointeur vers suivant
- HEAD pointe vers le premier nœud
- Dernier nœud a son pointeur à NULL
- Toujours libérer la mémoire avec free() en C
- Insertion tête O(1), accès index O(n)

> **⚠️ Piège Prof :** Memory leak en C: Si tu malloc() sans free() → fuite mémoire. Le programme consomme de plus en plus de RAM. En C, contrairement à Java/Python, il N'Y A PAS de garbage collector — tu dois gérer la mémoire manuellement.

## Exercice
**Énoncé :** Écris une fonction C qui calcule la longueur d'une liste chaînée.

<details>
<summary><b>Voir la Correction</b></summary>

✅ int longueur(Noeud* head) { int count = 0; Noeud* courant = head; while (courant != NULL) { count++; courant = courant->suivant; } return count; }

</details>
