# Modèle OSI et TCP/IP — La Tour de Babel Résolue

**Difficulté :** ★★★★★★★★★☆

## Théorie
MODÈLE OSI — 7 COUCHES
━━━━━━━━━━━━━━━━━━━━━━

OSI = Open Systems Interconnection (ISO, 1984)
Objectif : Permettre à des équipements différents de communiquer.
Mnémotechnique (de bas en haut): 
"Please Do Not Throw Sausage Pizza Away"
(Physical, Data link, Network, Transport, Session, Presentation, Application)

┌────┬─────────────────┬──────────────────────────┬─────────────────┐
│ N° │     Couche      │          Rôle            │    Exemples     │
├────┼─────────────────┼──────────────────────────┼─────────────────┤
│  7 │ Application     │ Interface utilisateur    │ HTTP, FTP, DNS  │
│  6 │ Présentation    │ Format, chiffrement      │ SSL, TLS, JPEG  │
│  5 │ Session         │ Gestion sessions         │ NetBIOS, RPC    │
│  4 │ Transport       │ Fiabilité, ports         │ TCP, UDP        │
│  3 │ Réseau          │ Routage, adressage IP    │ IP, ICMP, ARP   │
│  2 │ Liaison         │ MAC, frames, switch      │ Ethernet, WiFi  │
│  1 │ Physique        │ Bits, câbles, signaux    │ RJ45, Fibre     │
└────┴─────────────────┴──────────────────────────┴─────────────────┘

MODÈLE TCP/IP — 4 COUCHES (PRATIQUE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────┬──────────────────┬──────────────────┐
│    TCP/IP        │   Correspond à   │     OSI          │
├──────────────────┼──────────────────┼──────────────────┤
│ Application      │ ←──────────────→ │ App+Prés+Session │
│ Transport        │ ←──────────────→ │ Transport        │
│ Internet         │ ←──────────────→ │ Réseau           │
│ Accès Réseau     │ ←──────────────→ │ Liaison+Physique │
└──────────────────┴──────────────────┴──────────────────┘

ENCAPSULATION DES DONNÉES :
  Application : DONNÉES
  Transport   : SEGMENT (TCP) / DATAGRAMME (UDP)
  Réseau      : PAQUET (avec IP source/destination)
  Liaison     : FRAME/TRAME (avec MAC source/destination)
  Physique    : BITS (0 et 1 sur le câble)

À chaque couche, on AJOUTE un EN-TÊTE (header) → ENCAPSULATION
À la réception, on RETIRE les en-têtes → DÉSENCAPSULATION

TCP vs UDP :
━━━━━━━━━━━

TCP (Transmission Control Protocol) :
  + Orienté connexion (handshake 3 voies: SYN, SYN-ACK, ACK)
  + Fiable (accusés de réception, retransmission)
  + Contrôle de flux et congestion
  + Ordre garanti
  - Plus lent
  Usage: HTTP, Email, FTP, SSH

UDP (User Datagram Protocol) :
  + Ultra-rapide (pas de connexion)
  + Faible latence
  - Non fiable (pas d'ACK)
  - Ordre non garanti
  Usage: DNS, Streaming, Jeux en ligne, VoIP

## Points Clés
- OSI = 7 couches (théorique), TCP/IP = 4 couches (pratique)
- Mnémotechnique OSI: Please Do Not Throw Sausage Pizza Away
- Encapsulation = ajout d'en-têtes couche par couche
- TCP = fiable + lent, UDP = rapide + non fiable
- Handshake TCP = SYN → SYN-ACK → ACK

> **⚠️ Piège Prof :** Switch vs Routeur vs Hub: Trois équipements DIFFÉRENTS! Hub=répéteur bête (L1), Switch=commutateur intelligent (L2, MAC), Routeur=routeur IP (L3). Un switch ne peut PAS connecter deux réseaux différents — il faut un routeur pour ça.

## Exercice
**Énoncé :** Sur quelle(s) couche(s) OSI opère un switch ? Un routeur ? Un hub ?

<details>
<summary><b>Voir la Correction</b></summary>

✅ HUB: Couche 1 (Physique) — répète les signaux sans intelligence. SWITCH: Couche 2 (Liaison) — achemine selon les adresses MAC. ROUTEUR: Couche 3 (Réseau) — route selon les adresses IP.

</details>
