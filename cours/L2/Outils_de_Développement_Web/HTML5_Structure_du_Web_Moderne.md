# HTML5 — Structure du Web Moderne

**Difficulté :** ★★★★★☆☆☆☆☆

## Théorie
HTML5 — HYPERTEXT MARKUP LANGUAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTML n'est PAS un langage de programmation — c'est un langage de BALISAGE.
Il structure le CONTENU, pas le comportement.

STRUCTURE D'UNE PAGE HTML5 :
━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!DOCTYPE html>          ← Déclare HTML5 (obligatoire)
<html lang="fr">         ← Racine du document
  <head>                 ← Métadonnées (non affichées)
    <meta charset="UTF-8">          ← Encodage des caractères
    <meta name="viewport" ...>      ← Responsive design
    <title>Titre</title>            ← Titre onglet navigateur
    <link rel="stylesheet" href=""> ← CSS externe
  </head>
  <body>                 ← Contenu visible
    ...
  </body>
</html>

BALISES SÉMANTIQUES HTML5 (IMPORTANT !) :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Avant HTML5 : tout était des <div>
Avec HTML5 : balises avec SENS
  <header>   : En-tête de la page ou section
  <nav>      : Menu de navigation
  <main>     : Contenu principal (une seule fois)
  <article>  : Contenu autonome (blog post, news)
  <section>  : Regroupement thématique
  <aside>    : Contenu secondaire (sidebar)
  <footer>   : Pied de page

POURQUOI SÉMANTIQUE ? 
  1. SEO : Google comprend mieux la structure
  2. Accessibilité : Lecteurs d'écran pour malvoyants
  3. Maintenabilité : Code plus lisible

ATTRIBUTS ESSENTIELS :
  id       : Identifiant UNIQUE dans la page
  class    : Groupe d'éléments pour CSS/JS
  href     : Lien vers URL (<a>)
  src      : Source d'une ressource (<img>, <script>)
  alt      : Texte alternatif pour images (accessibilité)
  style    : CSS inline (à éviter)
  data-*   : Attributs personnalisés HTML5

## Points Clés
- HTML = langage de BALISAGE, pas de programmation
- <!DOCTYPE html> obligatoire en HTML5
- head = métadonnées, body = contenu visible
- Balises sémantiques: header, nav, main, article, section, footer
- id = unique, class = réutilisable

> **⚠️ Piège Prof :** Différence <b> vs <strong> et <i> vs <em>: <b> et <i> sont purement visuels (gras, italique). <strong> indique une importance sémantique, <em> une emphase. Pour les lecteurs d'écran et le SEO, <strong> et <em> ont du sens, pas <b> et <i>.

## Exercice
**Énoncé :** Crée la structure HTML5 d'un blog avec: en-tête, navigation, 2 articles, sidebar et pied de page.

<details>
<summary><b>Voir la Correction</b></summary>

✅ <!DOCTYPE html><html><head><meta charset='UTF-8'><title>Mon Blog</title></head><body><header><h1>Mon Blog</h1></header><nav><a href='#'>Accueil</a></nav><main><article>Article 1</article><article>Article 2</article></main><aside>Sidebar</aside><footer>© 2025</footer></body></html>

</details>
