# ⚙️ Programmation C++ — Performance & Contrôle

> "C rend facile de se tirer une balle dans le pied. C++ rend cela plus difficile, mais quand vous le faites, cela arrache toute votre jambe." — Bjarne Stroustrup

## 1. Introduction
Créé en 1983 par Bjarne Stroustrup. C++ est une extension du langage C qui ajoute la Programmation Orientée Objet (POO). Il est utilisé pour les jeux vidéo (Unreal Engine), les systèmes d'exploitation, les navigateurs web, et tout logiciel nécessitant des performances maximales.

## 2. Syntaxe de Base

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Bonjour le monde!" << endl;
    return 0;
}
```

### Variables et Types
C++ est un langage à typage statique fort.

```cpp
int age = 22;
float taille = 1.75f;
double precision = 3.14159265;
char lettre = 'A';
bool est_etudiant = true;
string nom = "Asta"; // nécessite #include <string>
```

### Pointeurs et Références (Le cœur du C++)
C++ vous donne un contrôle direct sur la mémoire (et avec de grands pouvoirs viennent de grandes responsabilités).

```cpp
int variable = 10;
int* pointeur = &variable;  // Stocke l'adresse mémoire de 'variable'
int& reference = variable;  // Un alias pour 'variable'

cout << "Valeur: " << variable << endl;
cout << "Adresse: " << pointeur << endl;
cout << "Valeur via pointeur: " << *pointeur << endl; // Déréférencement
```

## 3. Programmation Orientée Objet

```cpp
class Etudiant {
private:
    string nom;
    int age;

public:
    // Constructeur
    Etudiant(string n, int a) : nom(n), age(a) {}

    void se_presenter() {
        cout << "Je suis " << nom << " et j'ai " << age << " ans." << endl;
    }
};

int main() {
    Etudiant e("Asta", 22);
    e.se_presenter();
    return 0;
}
```

## 4. Gestion de la Mémoire
En C++ classique, vous devez libérer la mémoire allouée dynamiquement.

```cpp
int* tableau = new int[5]; // Allocation
// ... utilisation ...
delete[] tableau;          // Libération obligatoire!
```

> **Conseil Moderne:** Utilisez les *Smart Pointers* (`std::unique_ptr`, `std::shared_ptr`) depuis C++11 pour éviter les fuites de mémoire.
