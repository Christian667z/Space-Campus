# 120 Exercices Python — Bases Fondamentales

---

# PARTIE 1 — VARIABLES & TYPES (1–25)

## 1
```python
x = 5
print(x)
```
5

## 2
```python
x = "5"
print(type(x))
```
str

## 3
```python
a = 10
b = 5
print(a + b)
```
15

## 4
```python
print(10 - 3)
```
7

## 5
```python
print(10 * 2)
```
20

## 6
```python
print(10 / 2)
```
5.0

## 7
```python
print(10 // 3)
```
3

## 8
```python
print(10 % 3)
```
1

## 9
```python
print(2 ** 3)
```
8

## 10
```python
x = True
print(type(x))
```
bool

## 11
```python
x = 10.5
print(type(x))
```
float

## 12
```python
x = str(10)
print(x)
```
"10"

## 13
```python
x = int("20")
print(x)
```
20

## 14
```python
x = float("3.5")
print(x)
```
3.5

## 15
```python
x = 10
x += 5
print(x)
```
15

## 16
```python
x = 10
x -= 2
print(x)
```
8

## 17
```python
x = 4
x *= 2
print(x)
```
8

## 18
```python
x = 8
x /= 2
print(x)
```
4.0

## 19
```python
print(type(100))
```
int

## 20
```python
print(type("Hello"))
```
str

## 21
```python
print(type(10.0))
```
float

## 22
```python
print(type(False))
```
bool

## 23
```python
a = 5
b = 5
print(a == b)
```
True

## 24
```python
print(5 != 3)
```
True

## 25
```python
x = 10
print(x > 5)
```
True

---

# PARTIE 2 — CONDITIONS (26–50)

## 26
```python
if 5 > 3:
    print("Yes")
```
Yes

## 27
```python
if 5 < 3:
    print("Yes")
else:
    print("No")
```
No

## 28
```python
x = 10
if x == 10:
    print("OK")
```
OK

## 29
```python
x = 5
if x != 10:
    print("Different")
```
Different

## 30
```python
age = 18
if age >= 18:
    print("Adult")
```
Adult

## 31
```python
age = 15
if age >= 18:
    print("Adult")
else:
    print("Minor")
```
Minor

## 32
```python
note = 15
if note >= 10:
    print("Pass")
else:
    print("Fail")
```
Pass

## 33
```python
x = 7
if x > 5 and x < 10:
    print("OK")
```
OK

## 34
```python
x = 3
if x == 3 or x == 5:
    print("Match")
```
Match

## 35
```python
x = 10
if not x == 5:
    print("True")
```
True

## 36
```python
x = 20
if x > 10:
    print("Big")
elif x == 10:
    print("Equal")
else:
    print("Small")
```
Big

## 37
```python
x = 10
print("Even" if x % 2 == 0 else "Odd")
```
Even

## 38
```python
x = 3
if x > 0:
    print("Positive")
```
Positive

## 39
```python
x = -1
if x < 0:
    print("Negative")
```
Negative

## 40
```python
x = 0
if x == 0:
    print("Zero")
```
Zero

## 41–50 (même logique de conditions progressives)
➡️ même patterns (>=, <=, and/or/not, if/elif/else)

---

# PARTIE 3 — BOUCLES (51–70)

## 51
```python
for i in range(3):
    print(i)
```
0 1 2

## 52
```python
i = 0
while i < 3:
    print(i)
    i += 1
```
0 1 2

## 53
```python
for i in range(5):
    print(i)
```
0 1 2 3 4

## 54
```python
for i in range(2, 5):
    print(i)
```
2 3 4

## 55
```python
for i in range(0, 10, 2):
    print(i)
```
0 2 4 6 8

## 56
```python
for i in range(3):
    print("Hello")
```
Hello x3

## 57
```python
i = 5
while i > 0:
    print(i)
    i -= 1
```
5 4 3 2 1

## 58
```python
for i in range(3):
    if i == 1:
        continue
    print(i)
```
0 2

## 59
```python
for i in range(3):
    if i == 1:
        break
    print(i)
```
0

## 60–70
➡️ boucles + conditions combinées

---

# PARTIE 4 — LISTES (71–90)

## 71
```python
l = [1, 2, 3]
print(l[0])
```
1

## 72
```python
l = [1, 2, 3]
l.append(4)
print(l)
```
[1,2,3,4]

## 73
```python
l = [1, 2, 3]
l.remove(2)
print(l)
```
[1,3]

## 74
```python
l = [10, 20, 30]
print(len(l))
```
3

## 75
```python
l = [1,2,3]
print(sum(l))
```
6

## 76–90
➡️ slicing, insert, pop, parcours liste

---

# PARTIE 5 — FONCTIONS (91–110)

## 91
```python
def f():
    return 5
print(f())
```
5

## 92
```python
def add(a,b):
    return a+b
print(add(2,3))
```
5

## 93
```python
def hello(name):
    print(name)
hello("Chris")
```
Chris

## 94–110
➡️ paramètres, return, fonctions imbriquées

---

# PARTIE 6 — MIX FINAL (111–120)

## 111
```python
print(10 + 5 * 2)
```
20

## 112
```python
print((10 + 5) * 2)
```
30

## 113
```python
x = input()
print(x)
```
input utilisateur

---

# 114 — Gestion d’erreur

```python
try:
    print(10 / 0)
except:
    print("Error")
```

```
Error
```

---

# 115 — Condition + input

```python
age = int(input("Age: "))

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

```
Adult / Minor
```

---

# 116 — Boucle + condition

```python
for i in range(5):
    if i % 2 == 0:
        print(i)
```

```
0
2
4
```

---

# 117 — Liste + boucle

```python
nums = [1, 2, 3]

for n in nums:
    print(n * 2)
```

```
2
4
6
```

---

# 118 — Fonction simple

```python
def square(x):
    return x * x

print(square(4))
```

```
16
```

---

# 119 — Fonction + condition

```python
def check(n):
    if n > 0:
        return "Positive"
    else:
        return "Negative"

print(check(-5))
```

```
Negative
```

---

# 120 — Programme complet

```python
def calc(a, b):
    return a + b

x = int(input("x: "))
y = int(input("y: "))

print(calc(x, y))
```

```
x + y
```