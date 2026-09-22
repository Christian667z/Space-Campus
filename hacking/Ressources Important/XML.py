CONTENT = """\nXML

Un mot sur le XML

Le standard [XML](https://www.w3.org/XML/) (*eXtensible Markup Language*) est extrêmement puissant pour construire des documents robustes, échangeables et faciles à maintenir (lire et écrire) dans le temps. Contrairement aux idées reçues, il n'est pas *mort* et [n' a pas vocation à être remplacé par JSON](https://codepunk.io/xml-vs-json-why-json-sucks/) car les deux standards n'ont pas du tout la même histoire, ni les mêmes ambitions. Loin de là...

XML est un format universel pouvant être lu facilement par des humains et par des machines. XML est né en 1998 du standard SGML (qui a donné l'*application HTML*, un sous-ensemble du standard SGML, plus simple et plus permissif adapté au web). XML est également une simplification du standard SGML.

Son but initial était de faire office de standard pour conserver les documents numériques dans un format indépendant des machines, des OS ou des supports physiques. L'idée du W3C était de créer un standard qui permettra de lire votre document sur une techno inconnue dans 2000 ans. C'est un projet fascinant. Il était avant tout destiné à des documents narratifs (rapports, articles, catalogues). Il est basé sur la séparation stricte du contenu et de la forme.

Les développeurs s'en sont emparés ensuite pour faire du maintien d'enregistrement pour leurs applications, ce qui n'avait pas été envisagé dans sa conception initiale.

XML s'accompagne d'autres standards comme

- [XPath](http://www.xmlfacile.com/guide_xml/xpath_1.php5), un standard qui permet de requêter la structure XML pour naviguer dans la structure de données et la manipuler
- [XQuery](https://www.w3schools.com/xml/xml_xquery.asp), un standard qui permet de reqûeter l'abre via un *langage déclaratif* (le pied) comme le SQL
- [XSLT](https://www.w3schools.com/xml/xml_xslt.asp), standard plus avancé que le CSS pour mettre en forme les données XML pour la publication (vers un autre fichier XML, le web, le papier, etc.). Permet également de modifier l'affichage d'éléments, de les réorganiser etc...
- [DTD](https://www.w3schools.com/xml/xml_dtd.asp), pour la validation des données par un schéma
- et d'autres encore (XML Schema, etc.)...

Tous ces standards font d'XML un outil à avoir dans sa poche lorsque l'on a besoin d'échanger ou de construire des structures de données complexes et *validables*, ou de produire des documents indépendemment de leurs usages (web, présentation, impression papier, etc.).

Apprendre le XML et ses standards associés

- [XML Tutorial, W3C Schools](https://www.w3schools.com/xml/)
- [XML Facile !](http://www.xmlfacile.com/)
- [XML in a nutshell, A Desktop Quick Reference](https://www.pdfdrive.com/xml-in-a-nutshell-e54427253.html)
- [La DTD et son langage XML](https://www.cairn.info/revue-ela-2005-1-page-73.htm), article publié par [cairn.info](https://www.cairn.info/), pour le domaine de l'édition

Applications XML de prestige

- [Docbook](https://docbook.org/), application XML dédiée à la publication de documents, principalement des articles et des livres d'informatique mais pas que. Le projet a originellement été développé par l'éditeur O'Reilly pour ses éditeurs, il est aujourd'hui maintenu par [OASIS OPEN](https://www.oasis-open.org/), un groupe de collaboration travaillant et maintenant des standards
- [Dita Open Toolkit](https://www.dita-ot.org/), implémentation open-source du [standard Dita](https://fr.wikipedia.org/wiki/Darwin_Information_Typing_Architecture), *the Darwin Information Typing Architecture*, projet également maintenu par OASIS OPEN. C'est un framework de documentation et de publication technique où l'on va pouvoir développer et maintenir une source de vérité pour la publier vers différents formats (PDF, HTML, Markdown, etc.)
\n"""