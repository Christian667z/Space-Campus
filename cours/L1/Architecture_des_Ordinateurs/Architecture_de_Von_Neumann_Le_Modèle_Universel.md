# Architecture de Von Neumann — Le Modèle Universel

**Difficulté :** ★★★★★★★☆☆☆

## Théorie
ARCHITECTURE DE VON NEUMANN (1945)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Principe révolutionnaire : PROGRAMME STOCKÉ EN MÉMOIRE
Avant Von Neumann, le programme était câblé physiquement.
Von Neumann propose de stocker données ET instructions dans la MÊME mémoire.

COMPOSANTS PRINCIPAUX :
┌─────────────────────────────────────────────────────┐
│                    MÉMOIRE CENTRALE                  │
│              (Instructions + Données)                │
└────────────────────┬────────────────────────────────┘
                     │ Bus de données / adresses
┌────────────────────▼────────────────────────────────┐
│                        CPU                          │
│  ┌─────────────────┐     ┌────────────────────────┐ │
│  │    UAL (ALU)    │     │  UC (Unité de Contrôle)│ │
│  │ Calculs & Logique│    │ Séquence les instructions│ │
│  └─────────────────┘     └────────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │   Registres (PC, IR, ACC, MAR, MDR...)          │ │
│  └─────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              PÉRIPHÉRIQUES E/S                      │
│         Clavier, Écran, Disque, Réseau              │
└─────────────────────────────────────────────────────┘

REGISTRES CLÉS DU CPU :
  • PC (Program Counter) : Adresse de la prochaine instruction
  • IR (Instruction Register) : Instruction en cours d'exécution
  • ACC (Accumulateur) : Résultat des calculs
  • MAR (Memory Address Register) : Adresse mémoire à lire/écrire
  • MDR (Memory Data Register) : Donnée lue/écrite en mémoire

CYCLE FETCH-DECODE-EXECUTE :
  1. FETCH   : PC → MAR, lire mémoire → MDR → IR, PC++
  2. DECODE  : UC décode l'instruction dans IR
  3. EXECUTE : UAL exécute l'opération

BOTTLENECK DE VON NEUMANN :
⚠️  CPU et mémoire partagent le MÊME bus → goulot d'étranglement
✅  Solution moderne : Cache L1/L2/L3 pour réduire les accès mémoire

## Points Clés
- Programme stocké en mémoire = innovation de Von Neumann
- CPU = UAL + UC + Registres
- UAL effectue les calculs, UC contrôle la séquence
- PC pointe toujours vers la prochaine instruction
- Cycle: Fetch → Decode → Execute (répété infiniment)

> **⚠️ Piège Prof :** Le Von Neumann Bottleneck : Le prof peut demander pourquoi les ordinateurs modernes ont un cache. Réponse : pour compenser le goulot d'étranglement du bus unique données/instructions.

## Exercice
**Énoncé :** Décris le cycle Fetch-Decode-Execute pour l'instruction: ADD 5, 3 (Addition de 5 et 3)

<details>
<summary><b>Voir la Correction</b></summary>

✅ FETCH: PC donne l'adresse, on lit l'instruction ADD 5,3 en mémoire → IR. PC s'incrémente. DECODE: UC reconnait l'opcode ADD, identifie les opérandes 5 et 3. EXECUTE: UAL additionne 5+3=8, résultat stocké dans ACC.

</details>
