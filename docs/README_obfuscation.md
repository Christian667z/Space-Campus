Obfuscation & Packaging — Asta Académie

1) Backend (Python)
- Installer: pip install pyarmor pyinstaller
- Commande recommandée (PowerShell):
  .\scripts\obfuscate_backend.ps1 -Entry server.py -Out ..\dist\build_asta
- Le script : obfusque avec pyarmor, build avec pyinstaller, ajoute frontend/dist et student_notes dans le binaire.
- Vérifier le fichier SHA256 généré dans dist\build_asta\AstaAcademie.sha256

2) .NET (Launcher)
- Installer ConfuserEx (local)
- Utiliser scripts/obfuscate_dotnet.ps1 (prérequis: Confuser.CLI)
- Signer le binaire si nécessaire

3) Vérifications
- Lancer csharp\AstaAcademieLauncher et vérifier l'onglet Diagnostic
- Comparer SHA256: dist\AstaAcademie.exe vs dist\build_asta\AstaAcademie.exe
- Restaurer le bak si remplacement erroné (fichier .bak.*)

4) Notes de sécurité
- Ne distribuez pas de clés en clair. Utilisez DPAPI / Windows ProtectedData pour stocker secrets.
- Exécutez la génération d'obfuscation sur une machine de build dédiée.
