# Développement de Jeux Vidéo & 3D (Python)  
## Niveau Université / Industrie (Game Engineering & Graphics Programming)

**Difficulté :** ★★★★★★★★★★++

---

# Introduction académique

Le développement de jeux vidéo et la programmation 3D constituent un domaine interdisciplinaire combinant :

- informatique (algorithmes, structures de données)
- mathématiques (algèbre linéaire, géométrie)
- physique (mouvement, collisions)
- ingénierie logicielle (architecture temps réel)
- graphisme (rendu, shaders)

En Python, ce domaine est principalement utilisé pour :
- prototypage rapide
- jeux indépendants
- automatisation 3D (Blender/Maya)
- simulation interactive

---

# 1. Architecture d’un moteur de jeu

---

## 1.1 Définition

Un moteur de jeu est un système logiciel qui gère :

- rendu graphique
- logique du jeu
- physique
- input utilisateur
- audio
- assets (textures, modèles)

---

## 1.2 Loop principale (Game Loop)

Concept fondamental :

\[
\text{Game Loop} = \text{Input} \rightarrow \text{Update} \rightarrow \text{Render}
\]

---

## Exemple conceptuel

```python
while running:
    handle_input()
    update_game()
    render_frame()
```

---

## Interprétation

- Input : clavier, souris, manette
- Update : logique du monde
- Render : affichage écran

---

# 2. Développement 2D avec Pygame

---

## 2.1 Définition

Pygame est une bibliothèque Python pour créer des jeux 2D basés sur des surfaces graphiques.

---

## 2.2 Exemple minimal

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
```

---

## 2.3 Analyse scientifique

- boucle infinie contrôlée
- frame rate limité (60 FPS)
- gestion événements système

---

# 3. Physique de jeu (Game Physics)

---

## 3.1 Mouvement

\[
position = position + vitesse \times temps
\]

---

## Exemple Python

```python
x = 0
velocity = 5

for t in range(10):
    x += velocity
    print(x)
```

---

## 3.2 Gravité

\[
v = v + g \cdot t
\]

---

## Simulation

```python
y = 100
velocity = 0
gravity = -9.8

for frame in range(10):
    velocity += gravity
    y += velocity
    print(y)
```

---

# 4. Collision Detection

---

## 4.1 Définition

Déterminer si deux objets se touchent.

---

## 4.2 Bounding Box (AABB)

```python
def collide(a, b):
    return (
        a["x"] < b["x"] + b["w"] and
        a["x"] + a["w"] > b["x"] and
        a["y"] < b["y"] + b["h"] and
        a["y"] + a["h"] > b["y"]
    )
```

---

## 4.3 Interprétation

Algorithme basé sur géométrie rectangulaire simple.

---

# 5. Introduction à la 3D

---

## 5.1 Espace 3D

Un objet est défini par :

\[
(x, y, z)
\]

---

## 5.2 Projection 3D → 2D

\[
x' = \frac{x}{z}, \quad y' = \frac{y}{z}
\]

---

## Interprétation

Plus un objet est loin (z grand), plus il paraît petit.

---

# 6. Ursina Engine (3D en Python)

---

## 6.1 Définition

Ursina est un moteur 3D simplifié basé sur Python.

---

## 6.2 Exemple

```python
from ursina import *

app = Ursina()

cube = Entity(model='cube', color=color.orange, scale=2)

def update():
    cube.rotation_y += 1

app.run()
```

---

## 6.3 Analyse

- boucle game engine intégrée
- rendu 3D temps réel
- abstraction OpenGL

---

# 7. Mathématiques de la 3D

---

## 7.1 Vecteurs

\[
\vec{v} = (x, y, z)
\]

---

## 7.2 Distance 3D

\[
d = \sqrt{x^2 + y^2 + z^2}
\]

---

## Python

```python
import math

def distance(a, b):
    return math.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2 +
        (a[2]-b[2])**2
    )
```

---

# 8. Scripting Blender (Python avancé)

---

## 8.1 Définition

Blender expose une API Python pour :
- créer des objets
- automatiser des scènes
- générer des animations

---

## 8.2 Exemple Blender

```python
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
```

---

## 8.3 Animation automatique

```python
import bpy

cube = bpy.context.active_object

cube.location = (0, 0, 0)
cube.keyframe_insert(data_path="location", frame=1)

cube.location = (5, 0, 0)
cube.keyframe_insert(data_path="location", frame=50)
```

---

## 8.4 Analyse

- keyframes = interpolation temporelle
- animation = fonction du temps

---

# 9. Scripting Maya (industrie AAA)

---

## Exemple conceptuel

```python
import maya.cmds as cmds

cmds.polyCube()
cmds.move(5, 0, 0)
```

---

## Utilisation

- films (VFX)
- jeux AAA
- animation industrielle

---

# 10. Shaders (niveau avancé)

---

## 10.1 Définition

Un shader est un programme exécuté sur GPU.

---

## Types

- Vertex shader
- Fragment shader

---

## 10.2 Exemple conceptuel

```glsl
gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
```

---

# 11. Performance en jeux vidéo

---

## Problèmes critiques

- FPS drop
- mémoire GPU
- draw calls excessifs

---

## Optimisations

- batching
- culling
- LOD (Level of Detail)
- caching textures

---

# 12. Architecture d’un jeu moderne

---

```text
Game Engine
 ├── Renderer (GPU)
 ├── Physics Engine
 ├── Input System
 ├── Audio Engine
 ├── AI System
 └── Scene Graph
```

---

# 13. IA dans les jeux

---

## Utilisations

- pathfinding (A*)
- comportements NPC
- génération procédurale

---

## Exemple A*

```python
# concept simplifié
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
```

---

# 14. Génération procédurale

---

## Définition

Création automatique de contenu.

---

## Exemple

- terrains
- maps
- objets

---

# 15. Erreurs fréquentes

---

- mauvaise gestion FPS
- collisions inefficaces
- abus de boucles lourdes
- absence d’architecture engine
- non optimisation GPU

---

# Points clés (niveau industrie)

- Game loop = cœur de tout jeu
- physique = mathématique + temps réel
- 3D = vecteurs + matrices
- Blender = automatisation industrielle Python
- GPU = calcul parallèle massif
- optimisation = essentiel pour performance
- IA est intégrée dans les jeux modernes

---

# EXERCICES (niveau Harvard / Game Engineering)

---

## Exercice 1
Explique le rôle du game loop.

### Correction

Le game loop est la boucle centrale qui gère input, logique et rendu de manière continue.

---

## Exercice 2
Pourquoi la gravité est modélisée par une accélération ?

### Correction

Car elle modifie la vitesse en fonction du temps.

---

## Exercice 3
Pourquoi la collision AABB est efficace ?

### Correction

Car elle simplifie la géométrie en rectangles alignés.

---

## Exercice 4
Pourquoi la division par z est utilisée en 3D ?

### Correction

Pour simuler la perspective (projection).

---

## Exercice 5
Rôle de Blender Python API ?

### Correction

Automatiser la création et animation d’objets 3D.

---

## Exercice 6
Différence CPU vs GPU ?

### Correction

CPU = séquentiel  
GPU = parallèle massif

---

## Exercice 7
Pourquoi les shaders sont importants ?

### Correction

Ils définissent le rendu visuel sur GPU.

---

## Exercice 8
Qu’est-ce qu’un scene graph ?

### Correction

Structure hiérarchique des objets dans une scène.

---

## Exercice 9
Pourquoi optimiser les FPS ?

### Correction

Pour garantir fluidité et expérience utilisateur.

---

## Exercice 10
Pourquoi Python est utilisé en jeu vidéo malgré ses limites ?

### Correction

Pour prototypage rapide et scripting d’outils.

---