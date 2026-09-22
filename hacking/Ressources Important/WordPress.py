CONTENT = """\nWordPress

Un mot

En 2021 on comptait [environ 455 000 000 sites WordPress](https://techjury.net/blog/percentage-of-wordpress-websites/). Cela représente *au moins 30% du web*, mais en réalité plutôt *40%* (estimation haute).

WordPress est un framework parfaitement adapté pour *gérer et publier* du contenu sur Internet. C'est un outil versatile qui peut être adapté pour toute taille de projet. Si WordPress peut être utilisé pour *tout faire*, il n'est pas *toujours* la solution la plus adaptée !

Ce framework existe depuis 2004, dans le monde du logiciel libre c'est une éternité.

WordPress est développé et pensé *pour l'utilisateur final* (celui qui publie et gère le contenu), et non pour le développeur. Les utilisateurs se moquent bien de nos outils tant qu'ils ont ce qu'ils demandent. WordPress, à l'instar de LibreOffice ou autre, est devenu un standard de gestion de contenu en ligne que beaucoup de personnes non-techniciennes connaissent bien, utilisent quotidiennement et demandent. C'est donc un énorme avantage de capitWordPressaliser dessus pour les futurs utilisateurs de votre application web.


Doc officielle wordpress.org

Très bien faite, mais peut parfois demander un peu d'experience pour s'y retrouver. Ne pas oublier que de documenter un immense framework qui évolue sans cesse est un immense challenge en soi.

- [Codex](https://codex.wordpress.org/)
- [Wordpress hierarchy](https://developer.wordpress.org/themes/basics/template-hierarchy/)
- [Wordpress coding standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/)
- [Template tags](https://codex.wordpress.org/Template_Tags)
- [Using Permalinks](https://wordpress.org/support/article/using-permalinks/)
- [Data Sanitization/Escaping](https://developer.wordpress.org/themes/theme-security/data-sanitization-escaping/#escaping-with-localization)
- [Localization](https://developer.wordpress.org/apis/handbook/internationalization/localization/)
- [Make Wordpress](https://make.wordpress.org/), un hub centralisés de ressources pour les développeurs Wordpress

Articles

- [WordPress Taxonomies: The Ultimate Guide](https://ithemes.com/blog/wordpress-taxonomies)
- [WordPress Permalinks: The Essential Guide](https://ithemes.com/blog/wordpress-permalinks)

Livres de développement Wordpress

A télécharger sur [pdfdrive](https://www.pdfdrive.com/):

- *[Professional WordPress: Design and Development](https://www.pdfdrive.com/wrox-press-professional-wordpress-design-and-development-3rd-e30698942.html)* de Brad Williams et David Damstra, Edition Wrox, 3rd Edition, 2015
- *[Professional WordPress Plugin Development](https://www.pdfdrive.com/professional-wordpress-plugin-developmen-4074kb-jun-27-2012-120000-am-e42772568.html)* de Brad Williams et Justin Taldock, Edition Wrox, 2nd Edition, 2020
- *[Modern PHP: new features and good practices](https://www.pdfdrive.com/modern-php-e34337192.html)*, Josh Lochart, Edition O'REILLY, 2015

Épisodes de podcasts sur Wordpress

- [070: All things WordPress](https://phproundtable.com/episode/all-things-wordpress), [Tessa Kriesel](https://twitter.com/tessak22?s=20&t=L4nTJJGyh2w5UbPY7aDo9g) présente ici l'état et le futur de Wordpress ainsi que l'histoire de son développement
- [The thing about Wordpress](https://podcast.htmlallthethings.com/e/the-thing-about-wordpress/), Matt y discute des avantages et inconvénients de Wordpress en tant que développeur. Tout ce qui est discuté ici est pertinent

Podcasts dédiés à Wordpress

- [dradcast](http://dradcast.com/)
- [wp watercooler](https://wpwatercooler.com/)

Formations

- [Cours wordpress.org](https://learn.wordpress.org/courses)
- [Building websites with WordPress](https://nmiletic.gumroad.com/l/kSrqD)
- [Learn Wordpress](https://kinsta.com/learn/)
- [Wordpress for beginners training](https://yoast.com/academy/free-training-wordpress-for-beginners/)
- [How to Learn WordPress for Free in a Week (or Less)](https://twitter.com/natmiletic/status/1511711827398258695)
- [Wordpress tutorials](https://www.siteground.com/tutorials/wordpress/)
- [How to](https://wordpress.tv/category/how-to/), video
- [Our wordpress library](https://wpapprentice.com/courses/)
- [Wordpress freecodecamp](https://www.freecodecamp.org/news/tag/wordpress/)
- [Building PHP MVC Framework from Scratch](https://www.youtube.com/watch?v=WKy-N0q3WRo&list=PLLQuc_7jk__Uk_QnJMPndbdKECcTEwTA1), The Codeholic. Pas sur Wordpress mais montre les fonctionnalités de base d'un framework à implémenter

Starter themes

- [underscores](https://underscores.me/)
- [astra](https://fr.wordpress.org/themes/astra/)
- [generate press](https://generatepress.com/)
- [tail press](https://tailpress.io/)

Banque de thèmes

- [colorlib](https://colorlib.com/)
- [themeforest](https://themeforest.net/), des themes wordpress mais pas que

Plugins recommandés

Le plus recommandé est *de limiter au maximum l'usage de plugins pour vos thèmes*. Cela dit certains plugins stables et bien maintenus sont souvent de la partie pour des sites en production

- [Advanced Custom Fields](https://www.advancedcustomfields.com/), et non [SCF](https://www.lemondeinformatique.fr/actualites/lire-wordpress-s-attaque-au-plugin-acf-de-wp-engine-94979.html) !
- [ewww image optimizer](https://wordpress.org/plugins/ewww-image-optimizer/)
- [bulletProof Security](https://wordpress.org/plugins/bulletproof-security/), bonne alternative à WordFence
- [carbon fields](https://carbonfields.net/), alternative gratuite à ACF Pro
- [fakerpress](http://fakerpress.com/r/github), générateur de faux contenu pour tester son thème
- [RankMath](https://rankmath.com/fr/), plugin SEO, bonne alternative à [Yoast](https://yoast.com/)
- [BuddyPress](https://wordpress.org/plugins/buddypress/), plugin pour ajouter une couche réseau social à votre site
- [bbPress](https://wordpress.org/plugins/bbpress/), gestionnaire de forums/fils de discussion
- [W3 Total Cache](https://wordpress.org/plugins/w3-total-cache/), un plugin pour optimiser les performances de Wordpress, complètement agnostique de l'hébergeur. Mise en cache des pages webs etc... Au final, améliore l'experience utilisateur et le SEO de votre site. Vérifiez que votre hébergeur ne vous propose pas déjà un plugin de mise en cache maison avant de l'installer sur votre site en prod

Articles sur la pratique de WordPress et son évolution vers le FSE

- [Testing and Feedback for using block based template parts in classic themes](https://make.wordpress.org/themes/2022/09/12/testing-and-feedback-for-using-block-based-template-parts-in-classic-themes/)
- [The Imaginary Block-vs-Classic Battle in WordPress](https://masterwp.com/the-imaginary-block-vs-classic-battle-in-wordpress/)

Hébergement gratuit

- [Neocities](https://neocities.org/), [Neocities](https://fr.wikipedia.org/wiki/Neocities) est un hébergeur web ayant pour objectif de faciliter la création de sites internet personnels afin d'offrir une alternative aux réseaux sociaux. Il s'inscrit dans la continuité du légendaire [Geocities](https://www.lemonde.fr/technologies/article/2010/11/02/la-memoire-de-geocities-compilee-en-un-fichier_1434450_651865.html), un ancien service d'hébergement web gratuit fondé en 1994, fermé en 2009
- [GitHub Pages](https://pages.github.com/), GitHub offre la possibilité d'héberger un site statique\n"""