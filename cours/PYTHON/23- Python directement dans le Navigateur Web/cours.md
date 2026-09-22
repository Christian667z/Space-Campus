# Python directement dans le Navigateur Web  
## (WebAssembly • Brython • Pyodide • Skulpt • PyScript)

**Difficulté :** ★★★★★★★★★★++ (niveau recherche / Web Systems / runtime engineering)

---

# Introduction académique

Exécuter Python dans un navigateur web est un défi fondamental en informatique moderne, car le navigateur est nativement conçu pour exécuter :

- JavaScript
- WebAssembly (WASM)

Python doit donc être :
- interprété dans le navigateur, ou
- compilé vers WebAssembly, ou
- simulé via JavaScript runtime

---

## Définition formelle

> Python in-browser = exécution du langage Python dans un environnement sandboxed client-side sans serveur backend.

---

# 1. Contraintes fondamentales du navigateur

---

## 1.1 Modèle de sécurité (Sandbox)

Le navigateur impose :

- pas d’accès direct au système
- pas de filesystem libre
- exécution isolée
- mémoire contrôlée

---

## 1.2 Conséquence

Python ne peut pas fonctionner “nativement”, donc :

\[
Python \neq runtime natif web
\]

---

# 2. Pyodide — Python via WebAssembly ⭐ (le plus important)

---

## 2.1 Définition

Pyodide est une implémentation de Python compilée en WebAssembly.

---

## 2.2 Architecture

```text
Python → CPython → WebAssembly → Browser Runtime
```

---

## 2.3 Avantage majeur

- exécution quasi native
- support NumPy / Pandas
- environnement scientifique complet

---

## 2.4 Exemple Pyodide

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>

<script>
async function runPython() {
    let pyodide = await loadPyodide();

    let result = pyodide.runPython(`
        def f(x):
            return x * x
        f(5)
    `);

    console.log(result);
}

runPython();
</script>
```

---

## 2.5 Analyse académique

- Python s’exécute dans WASM sandbox
- performance proche natif
- idéal pour science web

---

# 3. Brython — Python compilé en JavaScript

---

## 3.1 Définition

Brython traduit Python → JavaScript à l’exécution.

---

## 3.2 Architecture

```text
Python → transpilation → JavaScript → Browser engine
```

---

## 3.3 Exemple

```html
<script src="https://cdn.jsdelivr.net/npm/brython@3.11.0/brython.min.js"></script>

<body onload="brython()">

<script type="text/python">
from browser import document

document <= "Hello from Python in browser"
</script>

</body>
```

---

## 3.4 Analyse

- dépend du moteur JS
- plus lent que Pyodide
- très simple à utiliser

---

# 4. Skulpt — Python éducatif

---

## 4.1 Définition

Skulpt est un interpréteur Python écrit en JavaScript.

---

## 4.2 Usage

- education
- visualisation
- apprentissage Python

---

## 4.3 Exemple

```html
<script src="https://cdn.skulpt.org/skulpt.min.js"></script>

<script type="text/javascript">
Sk.configure({
    output: console.log
});

Sk.misceval.asyncToPromise(function() {
    return Sk.importMainWithBody("<stdin>", false, "print(2+2)");
});
</script>
```

---

## 4.4 Limites

- pas complet CPython
- performance limitée
- usage éducatif principalement

---

# 5. PyScript — Python dans HTML moderne

---

## 5.1 Définition

PyScript permet d’écrire Python directement dans HTML comme JavaScript.

---

## 5.2 Exemple

```html
<html>
<head>
<link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
<script defer src="https://pyscript.net/latest/pyscript.js"></script>
</head>

<body>

<py-script>
print("Hello from PyScript")
</py-script>

</body>
</html>
```

---

## 5.3 Analyse

- abstraction de Pyodide
- intégration UI simple
- idéal prototypes web Python

---

# 6. Comparaison des technologies

---

| Technologie | Base | Performance | Usage |
|---|---|---|---|
| Pyodide | WebAssembly | ⭐⭐⭐⭐⭐ | science / data |
| Brython | JavaScript transpile | ⭐⭐⭐ | web apps simples |
| Skulpt | JS interpreter | ⭐⭐ | éducation |
| PyScript | Pyodide wrapper | ⭐⭐⭐⭐ | web apps rapides |

---

# 7. Architecture Python Web moderne

---

## Modèle réel

```text
Browser
 ├── UI (HTML/CSS)
 ├── Python runtime (Pyodide / PyScript)
 └── WASM layer
```

---

# 8. Interaction Python ↔ DOM

---

## Exemple Pyodide DOM manipulation

```python
from js import document

document.body.innerHTML = "Hello Python Web"
```

---

## Analyse

- Python interagit avec JavaScript DOM API
- bridging JS ↔ Python runtime

---

# 9. Performance et limitations

---

## Problèmes

- mémoire limitée navigateur
- startup time Pyodide
- compatibilité modules C

---

## Contraintes fondamentales

- pas accès hardware direct
- sandbox strict
- dépendance WASM engine

---

# 10. Sécurité (très important)

---

## Risques

- exécution de code arbitraire côté client
- injection JS via Python bridge
- exposition logique métier

---

## Protection

- sandbox strict
- validation input
- CSP (Content Security Policy)

---

# 11. Cas d’usage industriels

---

- notebooks interactifs (Jupyter web)
- data science dans navigateur
- dashboards scientifiques
- IA client-side (light models)
- éducation interactive

---

# 12. Python Web vs Backend Python

---

| Aspect | Backend | Browser |
|---|---|---|
| accès DB | oui | non |
| performance | élevée | limitée |
| sécurité | serveur | sandbox |
| usage | logique métier | UI / science |

---

# 13. Futur du Python web

---

## Tendances

- WASM-first runtimes
- Python full client-side apps
- IA dans navigateur
- edge computing local

---

# Points clés (niveau recherche)

---

- Python ne tourne pas nativement dans le navigateur
- Pyodide = Python compilé en WebAssembly
- Brython = Python converti en JavaScript
- PyScript = abstraction moderne de Pyodide
- Skulpt = interpréteur éducatif JS
- WebAssembly est la clé technologique
- sécurité = sandbox obligatoire
- avenir = Python client-side natif via WASM

---

# EXERCICES (niveau Harvard / Web Systems)

---

## Exercice 1
Pourquoi Python ne peut-il pas s’exécuter nativement dans un navigateur ?

### Correction

Car le navigateur ne supporte que JavaScript et WebAssembly, et impose une sandbox stricte empêchant l’exécution native CPython.

---

## Exercice 2
Pourquoi Pyodide est plus performant que Brython ?

### Correction

Car Pyodide compile CPython vers WebAssembly, alors que Brython transpile Python vers JavaScript interprété.

---

## Exercice 3
Quel est le rôle de WebAssembly ?

### Correction

Fournir un bytecode bas niveau exécutable dans le navigateur avec performance proche du natif.

---

## Exercice 4
Pourquoi PyScript simplifie Pyodide ?

### Correction

Car il encapsule la complexité de l’initialisation et expose une syntaxe HTML directe.

---

## Exercice 5
Pourquoi le navigateur impose une sandbox ?

### Correction

Pour protéger l’utilisateur contre l’accès système non autorisé et les attaques malveillantes.

---

## Exercice 6
Différence Brython vs Pyodide ?

### Correction

Brython = JS runtime  
Pyodide = WASM CPython runtime

---

## Exercice 7
Pourquoi les modules C Python sont problématiques dans le navigateur ?

### Correction

Car ils dépendent de compilation native non compatible WASM sans adaptation.

---

## Exercice 8
Quel est l’avantage principal de Pyodide pour la data science ?

### Correction

Il permet d’utiliser NumPy/Pandas directement dans le navigateur.

---

## Exercice 9
Pourquoi Skulpt est surtout éducatif ?

### Correction

Car il ne supporte pas toutes les fonctionnalités CPython et privilégie la simplicité.

---

## Exercice 10
Quel est le futur du Python dans le navigateur ?

### Correction

Une intégration native via WebAssembly permettant des applications full Python côté client.

---