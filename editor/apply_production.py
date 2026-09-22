import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update _export_profile
export_old = """    def _export_profile(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="asta_profil_export.json")"""
export_new = """    def _export_profile(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".asta_save",
            filetypes=[("Sauvegarde Asta Académie", "*.asta_save")],
            initialfile="ma_sauvegarde.asta_save")"""
content = content.replace(export_old, export_new)

# 2. Update _import_profile
import_old = '        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("Tous", "*.*")])'
import_new = '        path = filedialog.askopenfilename(filetypes=[("Sauvegarde Asta", "*.asta_save"), ("JSON", "*.json"), ("Tous", "*.*")])'
content = content.replace(import_old, import_new)

# 3. Add Python execution to SpaceCode
sc_old = """    def _sc_preview(self):
        code = self.sc_editor.get("1.0", "end")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html","""
sc_new = """    def _sc_preview(self):
        code = self.sc_editor.get("1.0", "end").strip()
        
        # Détection automatique de Python
        if code.startswith("# PYTHON") or code.startswith("import ") or "print(" in code or "def " in code:
            import subprocess
            try:
                res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5)
                out = res.stdout
                if res.stderr:
                    out += "\\n[ERREURS]\\n" + res.stderr
                if not out: out = "[Aucune sortie]"
                messagebox.showinfo("💻 Résultat Python", out)
            except subprocess.TimeoutExpired:
                messagebox.showwarning("⏳ Timeout", "L'exécution a pris trop de temps (boucle infinie ?)")
            except Exception as e:
                messagebox.showerror("❌ Erreur d'exécution", str(e))
            return
            
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html","""
content = content.replace(sc_old, sc_new)

# 4. Add Global Exception Handler
handler_str = """
def global_exception_handler(exc_type, exc_value, exc_traceback):
    import traceback
    err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log_file = DATA_DIR / "crash_log.txt"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] CRASH:\\n{err_msg}\\n{'-'*50}\\n")
        messagebox.showerror("Erreur Fatale", "Une erreur inattendue s'est produite. Les détails ont été enregistrés dans:\\n" + str(log_file))
    except:
        pass
    sys.exit(1)

sys.excepthook = global_exception_handler

def main():"""
content = content.replace("def main():", handler_str)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Main.py patché avec succès pour la mise en production.")
