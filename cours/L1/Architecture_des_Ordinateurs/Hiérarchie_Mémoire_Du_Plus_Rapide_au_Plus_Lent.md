# Hiérarchie Mémoire — Du Plus Rapide au Plus Lent

**Difficulté :** ★★★★★★☆☆☆☆

## Théorie
PYRAMIDE DE LA MÉMOIRE
━━━━━━━━━━━━━━━━━━━━━

Plus on monte = Plus RAPIDE, Plus CHER, Plus PETIT
Plus on descend = Plus LENT, Moins cher, Plus GRAND

        ┌─────────────────┐
        │   REGISTRES     │  ← Nanoseconde, quelques KB
        │  (dans le CPU)  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   CACHE L1/L2   │  ← 1-10 ns, 64KB - 4MB
        │   (dans le CPU) │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │      RAM        │  ← 50-100 ns, 4GB - 64GB
        │  (barrette DDR) │  VOLATILE
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   SSD / HDD     │  ← ms, 256GB - 4TB
        │  (stockage)     │  NON-VOLATILE
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   CLOUD / BANDE │  ← secondes/minutes, Petaoctets
        └─────────────────┘

DIFFÉRENCE CRITIQUE : Volatile vs Non-Volatile
  VOLATILE (RAM, Cache) : Perd le contenu à l'extinction
  NON-VOLATILE (ROM, SSD, HDD) : Garde le contenu

TYPES DE RAM :
  • DRAM (Dynamic RAM) : Doit être rafraîchie, moins chère, RAM principale
  • SRAM (Static RAM) : Pas de rafraîchissement, ultra-rapide, coûteuse → Cache
  • DDR4/DDR5 : DRAM moderne, double taux de transfert

TYPES DE ROM :
  • ROM : Lecture seule, fixe depuis la fabrication
  • PROM : Programmable une fois
  • EPROM : Effaçable par UV
  • EEPROM : Effaçable électriquement (clé USB, SSD)

## Points Clés
- Plus rapide = plus petit, plus cher, plus près du CPU
- RAM = volatile (perd à extinction), HDD = non-volatile
- Cache L1 > L2 > L3 en vitesse, L3 > L2 > L1 en taille
- SRAM (cache) vs DRAM (RAM principale)
- ROM contient le BIOS/firmware

> **⚠️ Piège Prof :** Attention: Le prof peut dire que le BIOS est stocké dans une ROM. C'est exact — mais les BIOS modernes (UEFI) utilisent de la FLASH (type d'EEPROM), pas une ROM stricte.

## Exercice
**Énoncé :** Classe ces mémoires du plus rapide au plus lent: HDD, Cache L1, RAM DDR4, Registres CPU, SSD

<details>
<summary><b>Voir la Correction</b></summary>

✅ 1. Registres CPU (picosecondes) 2. Cache L1 (~1 ns) 3. RAM DDR4 (~50 ns) 4. SSD (~0.1 ms) 5. HDD (~10 ms)

</details>
