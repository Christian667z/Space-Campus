# Programmation Matérielle & Systèmes Embarqués en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

La programmation matérielle et les systèmes embarqués consistent à utiliser Python pour interagir directement avec le matériel physique.

On passe du logiciel pur au monde réel :
- capteurs,
- moteurs,
- cartes électroniques,
- microcontrôleurs,
- IoT (Internet of Things).

Python est très utilisé grâce à sa simplicité et à des bibliothèques spécialisées.

---

# 1. Qu’est-ce qu’un système embarqué ?

---

# Définition

Un système embarqué est un système informatique intégré dans un appareil physique.

---

# Exemples

- smartphones
- voitures intelligentes
- drones
- robots
- objets connectés (IoT)
- Raspberry Pi

---

# 2. Python et le matériel

---

# Pourquoi Python ?

- simple
- rapide à développer
- riche en bibliothèques
- compatible IoT

---

# Limite

Python n’est pas toujours temps réel strict → on utilise C/C++ pour bas niveau critique.

---

# 3. Raspberry Pi (plateforme principale)

---

# Définition

Le Raspberry Pi est un mini-ordinateur permettant de contrôler du matériel.

---

# Utilisation Python

```python
print("Hello Hardware")
```

---

# 4. GPIO (General Purpose Input Output)

---

# Définition

Les GPIO permettent de contrôler des broches électroniques.

---

# Exemple (Raspberry Pi)

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

GPIO.output(18, True)
time.sleep(1)
GPIO.output(18, False)

GPIO.cleanup()
```

---

# Utilisation

- LED
- moteurs
- capteurs

---

# 5. Capteurs (Sensors)

---

# Définition

Un capteur mesure une valeur physique :
- température
- humidité
- lumière
- mouvement

---

# Exemple capteur température (simulation)

```python
import random

temperature = random.randint(20, 35)

print("Temperature:", temperature)
```

---

# 6. Actionneurs (Actuators)

---

# Définition

Un actionneur effectue une action physique :
- moteur
- LED
- relais

---

# Exemple LED

```python
GPIO.output(18, True)  # ON
GPIO.output(18, False) # OFF
```

---

# 7. PWM (Pulse Width Modulation)

---

# Définition

Permet de contrôler la puissance envoyée à un composant.

---

# Exemple

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 1000)
pwm.start(50)

time.sleep(5)

pwm.stop()
GPIO.cleanup()
```

---

# 8. Communication série (Serial Communication)

---

# Définition

Permet de communiquer entre appareils.

---

# Exemple Arduino ↔ Python

```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

ser.write(b"Hello Arduino")

print(ser.readline())
```

---

# 9. I2C Communication

---

# Définition

Protocole utilisé pour connecter plusieurs capteurs.

---

# Exemple conceptuel

```python
# communication avec capteur I2C
```

---

# Bibliothèque

```python
import smbus
```

---

# 10. SPI Communication

---

# Définition

Communication rapide entre composants.

---

# Utilisation

- écrans
- mémoire
- capteurs rapides

---

# 11. Internet of Things (IoT)

---

# Définition

Connexion des objets physiques à Internet.

---

# Exemple IoT simple

```python
import requests

data = {"temperature": 25}

requests.post("https://api.example.com/data", json=data)
```

---

# 12. Microcontrôleurs (ESP32 / Arduino)

---

# Définition

Petits processeurs intégrés dans les objets.

---

# MicroPython (ESP32)

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)
```

---

# 13. MicroPython vs Python classique

| MicroPython | Python |
|---|---|
| léger | complet |
| embarqué | desktop |
| faible mémoire | riche libs |

---

# 14. Robotique

---

# Exemple simple robot

```python
def move_forward():
    print("Robot moving forward")
```

---

# Utilisation réelle

- drones
- robots industriels
- voitures autonomes

---

# 15. Capteurs avancés

---

# Exemples

- ultrason
- infrarouge
- gyroscope
- accéléromètre

---

# 16. Lecture de capteur (exemple logique)

```python
def read_sensor():
    return 42  # valeur simulée

value = read_sensor()

print("Sensor value:", value)
```

---

# 17. Temps réel (Real-time systems)

---

# Définition

Systèmes qui réagissent immédiatement aux événements.

---

# Exemple

```python
import time

while True:
    print("Checking sensor...")
    time.sleep(0.1)
```

---

# 18. Optimisation embarquée

---

# Techniques

- code léger
- éviter boucles lourdes
- réduire mémoire
- éviter allocations inutiles

---

# 19. Sécurité IoT

---

# Risques

- piratage appareils
- accès réseau non sécurisé
- données interceptées

---

# Protection

- chiffrement
- authentification
- firewall
- tokens sécurisés

---

# 20. Architecture embarquée

---

# Exemple

```text
Device
 ├── Sensors
 ├── Controller (Python)
 ├── Actuators
 └── Network Module
```

---

# 21. Applications réelles

- smart home
- voitures intelligentes
- santé connectée
- agriculture intelligente
- industrie 4.0

---

# 22. Erreurs fréquentes

- mauvaise gestion énergie
- code trop lourd
- absence de sécurité
- mauvaise gestion capteurs
- communication instable

---

# Points Clés

- Python peut contrôler du matériel.
- GPIO permet de gérer les composants.
- IoT connecte les objets à Internet.
- MicroPython est utilisé sur microcontrôleurs.
- Communication série/I2C/SPI est essentielle.
- Les systèmes embarqués doivent être optimisés.
- La sécurité est critique en IoT.
- Le temps réel est important dans la robotique.

---

# Exercice

## Énoncé

Créer :
1. un programme simulant un capteur,
2. une action basée sur la valeur,
3. afficher une alerte si trop élevé.

---

# Correction

```python
import random

temperature = random.randint(15, 40)

print("Temperature:", temperature)

if temperature > 30:
    print("ALERT: Temperature too high!")
else:
    print("Temperature normal")
```