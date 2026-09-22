import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys
import webbrowser
import tempfile
import pathlib
import threading
import subprocess
import re
from pathlib import Path
from PIL import Image, ImageTk

from security.security_auth import *
from core.logic_tools import *
from core.space_code import *
from utils.logger import AstaLogger
from core.config import DATA_DIR, APP_NAME, VERSION

# Mots-clés pour la coloration syntaxique
SYNTAX_PATTERNS = {
    "Python": {
        "keywords": r'\b(def|class|return|if|elif|else|while|for|try|except|import|from|as|with|pass|break|continue|True|False|None|and|or|not|in|is|lambda|yield|global|nonlocal|assert|async|await)\b',
        "strings": r'(".*?"|\'.*?\')',
        "comments": r'(#.*)',
        "functions": r'\b([a-zA-Z_]\w*)\s*(?=\()',
        "numbers": r'\b(\d+\.?\d*)\b',
        "decorators": r'(@[a-zA-Z_]\w*)'
    },
    "HTML": {
        "tags": r'(<\/?[a-zA-Z0-9]+)',
        "attributes": r'([a-zA-Z-]+)(?=\=)',
        "strings": r'(".*?")',
        "comments": r'(<!--.*?-->)'
    },
    "CSS": {
        "selectors": r'^([^\{]+)(?=\{)',
        "properties": r'([a-zA-Z-]+)(?=:)',
        "values": r':\s*([^;]+)(?=;)',
        "comments": r'(/\*.*?\*/)'
    }
}

COLORS_SYNTAX = {
    "keywords": "#c678dd", # Violet
    "strings": "#98c379",  # Vert
    "comments": "#5c6370", # Gris
    "functions": "#61afef",# Bleu
    "numbers": "#d19a66",  # Orange
    "decorators": "#e06c75",# Rouge
    "tags": "#e06c75",
    "attributes": "#d19a66",
    "selectors": "#e06c75",
    "properties": "#56b6c2",
    "values": "#98c379"
}

class SpacecodeMixin:
    def _build_spacecode(self):
        frame = ctk.CTkFrame(self.main_area, fg_color=self.C["bg"])
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        # Header
        hdr = ctk.CTkFrame(frame, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew")
        self._section_header(hdr, "💻 SpaceCode PRO MAX", "Éditeur de code professionnel avec explorateur, onglets et console interactive.")

        # Maintenance message
        msg_frame = ctk.CTkFrame(frame, fg_color=self.C["card"], corner_radius=15)
        msg_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(msg_frame, text="🚧 Module en maintenance", font=("Segoe UI", 24, "bold"), text_color=self.C["warning"]).pack(pady=(30, 10))
        ctk.CTkLabel(msg_frame, text="Le module SpaceCode est temporairement désactivé pour des raisons de sécurité.\nIl sera réintroduit dans une future mise à jour (Sandboxed).", font=("Segoe UI", 14), text_color=self.C["subtext"]).pack(pady=(0, 30), padx=40)

    def _sc_refresh_explorer(self):
        for widget in self.explorer_scroll.winfo_children():
            widget.destroy()
            
        try:
            files = list(self.workspace_dir.iterdir())
            for f in sorted(files, key=lambda x: (not x.is_dir(), x.name.lower())):
                icon = "📁" if f.is_dir() else "📄"
                color = self.C["accent"] if f.suffix == ".py" else "#ff8c00" if f.suffix == ".html" else "#3498db" if f.suffix == ".css" else self.C["text"]
                btn = ctk.CTkButton(self.explorer_scroll, text=f"{icon} {f.name}", font=("Segoe UI", 11),
                                    fg_color="transparent", text_color=color, anchor="w",
                                    command=lambda p=str(f): self._sc_open_file(p))
                btn.pack(fill="x", pady=1)
        except Exception as e:
            AstaLogger.error(f"Erreur explorateur: {e}")

    def _sc_new_file(self):
        dialog = ctk.CTkInputDialog(text="Nom du fichier (ex: index.html):", title="Nouveau fichier")
        filename = dialog.get_input()
        if filename:
            path = self.workspace_dir / filename
            if not path.exists():
                path.write_text("", encoding="utf-8")
                self._sc_refresh_explorer()
                self._sc_open_file(str(path))
            else:
                messagebox.showerror("Erreur", "Le fichier existe déjà.")

    def _sc_open_file(self, file_path):
        if not os.path.isfile(file_path): return
        
        if file_path not in self.open_files:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
                self.open_files[file_path] = content
                self.breakpoints[file_path] = set()
                self._sc_create_editor(file_path)
                self._sc_create_tab(file_path)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier:\n{e}")
                return
                
        self._sc_switch_to_file(file_path)

    def _sc_create_tab(self, file_path):
        name = Path(file_path).name
        btn = ctk.CTkButton(self.tabs_frame, text=name, width=100, corner_radius=0,
                            command=lambda: self._sc_switch_to_file(file_path))
        btn.pack(side="left", padx=2, fill="y")
        # Stocker le bouton pour pouvoir le mettre en surbrillance
        if not hasattr(self, "tab_buttons"): self.tab_buttons = {}
        self.tab_buttons[file_path] = btn

    def _sc_create_editor(self, file_path):
        editor = tk.Text(self.editors_container, font=("Courier New", 14), bg="#0d1117", fg="#e6edf3",
                         insertbackground="#e6edf3", undo=True, wrap="none", relief="flat")
        
        # Scrollbars
        y_scroll = ctk.CTkScrollbar(self.editors_container, command=editor.yview)
        x_scroll = ctk.CTkScrollbar(self.editors_container, command=editor.xview, orientation="horizontal")
        editor.configure(yscrollcommand=lambda *args: (y_scroll.set(*args), self._sc_sync_line_numbers()))
        editor.configure(xscrollcommand=x_scroll.set)
        
        editor.y_scroll_widget = y_scroll
        editor.x_scroll_widget = x_scroll
        
        # Bindings
        editor.bind("<KeyRelease>", self._sc_on_key_release)
        editor.bind("<Return>", self._sc_auto_indent)
        editor.bind("<Button-1>", self._sc_sync_line_numbers)
        editor.bind("<MouseWheel>", self._sc_sync_line_numbers)
        
        # Configuration des tags de syntaxe
        for tag_name, color in COLORS_SYNTAX.items():
            editor.tag_configure(tag_name, foreground=color)
            
        editor.insert("1.0", self.open_files[file_path])
        self.editors[file_path] = editor
        
        # Coloration initiale
        self._sc_highlight_syntax(editor, file_path)

    def _sc_switch_to_file(self, file_path):
        if self.current_file and self.current_file in self.editors:
            self.editors[self.current_file].grid_forget()
            if hasattr(self.editors[self.current_file], "y_scroll_widget"):
                self.editors[self.current_file].y_scroll_widget.grid_forget()
                self.editors[self.current_file].x_scroll_widget.grid_forget()
                
            if self.current_file in self.tab_buttons:
                self.tab_buttons[self.current_file].configure(fg_color=self.C["sidebar"])
                
        self.current_file = file_path
        editor = self.editors[file_path]
        
        editor.grid(row=0, column=1, sticky="nsew", padx=5)
        editor.y_scroll_widget.grid(row=0, column=2, sticky="ns")
        editor.x_scroll_widget.grid(row=1, column=1, sticky="ew")
        
        if file_path in self.tab_buttons:
            self.tab_buttons[file_path].configure(fg_color=self.C["accent"])
            
        # Update Status Bar
        ext = Path(file_path).suffix.lower()
        lang = "Python" if ext == ".py" else "HTML" if ext == ".html" else "CSS" if ext == ".css" else "Text"
        self.sc_status_lang.configure(text=lang)
        
        self._sc_sync_line_numbers()
        self._sc_update_cursor_pos()

    def _sc_on_key_release(self, event=None):
        self._sc_sync_line_numbers()
        self._sc_update_cursor_pos()
        if self.current_file:
            editor = self.editors[self.current_file]
            self.open_files[self.current_file] = editor.get("1.0", "end-1c")
            self._sc_highlight_syntax(editor, self.current_file)

    def _sc_auto_indent(self, event):
        if not self.current_file: return
        editor = self.editors[self.current_file]
        current_idx = editor.index("insert")
        line_num = int(current_idx.split(".")[0])
        
        if line_num > 1:
            prev_line_text = editor.get(f"{line_num-1}.0", f"{line_num-1}.end")
            leading_spaces = len(prev_line_text) - len(prev_line_text.lstrip())
            
            if prev_line_text.strip().endswith(":"):
                leading_spaces += 4
                
            if leading_spaces > 0:
                editor.insert("insert", " " * leading_spaces)
                
        self._sc_sync_line_numbers()
        return "break" # Empêcher le retour à la ligne par défaut car on vient de le faire

    def _sc_sync_line_numbers(self, event=None):
        if not self.current_file: return
        
        editor = self.editors[self.current_file]
        self.line_numbers_canvas.delete("all")
        
        i = editor.index("@0,0")
        while True :
            dline= editor.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            
            # Dessiner le numéro
            self.line_numbers_canvas.create_text(30, y, anchor="ne", text=linenum, font=("Courier New", 12), fill=self.C["subtext"])
            
            # Dessiner le breakpoint si présent
            if int(linenum) in self.breakpoints[self.current_file]:
                self.line_numbers_canvas.create_oval(5, y+2, 15, y+12, fill="#ff4444", outline="#ff4444")
                
            i = editor.index("%s+1line" % i)

    def _sc_toggle_breakpoint(self, event):
        if not self.current_file: return
        editor = self.editors[self.current_file]
        i = editor.index(f"@0,{event.y}")
        linenum = int(i.split(".")[0])
        
        if linenum in self.breakpoints[self.current_file]:
            self.breakpoints[self.current_file].remove(linenum)
        else:
            self.breakpoints[self.current_file].add(linenum)
        self._sc_sync_line_numbers()

    def _sc_update_cursor_pos(self):
        if not self.current_file: return
        editor = self.editors[self.current_file]
        pos = editor.index("insert")
        line, col = pos.split(".")
        self.sc_status_pos.configure(text=f"Ln {line}, Col {col}")

    def _sc_highlight_syntax(self, editor, file_path):
        ext = Path(file_path).suffix.lower()
        lang = "Python" if ext == ".py" else "HTML" if ext in [".html", ".htm"] else "CSS" if ext == ".css" else None
        
        if not lang: return
        
        text = editor.get("1.0", "end-1c")
        
        # Supprimer les anciens tags
        for tag_name in COLORS_SYNTAX.keys():
            editor.tag_remove(tag_name, "1.0", "end")
            
        rules = SYNTAX_PATTERNS.get(lang, {})
        for tag_name, pattern in rules.items():
            for match in re.finditer(pattern, text, re.MULTILINE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                editor.tag_add(tag_name, start, end)

    def _sc_save_file(self):
        if not self.current_file: return
        try:
            content = self.editors[self.current_file].get("1.0", "end-1c")
            Path(self.current_file).write_text(content, encoding="utf-8")
            self.open_files[self.current_file] = content
            # Petit feedback
            self.sc_status_enc.configure(text="Sauvegardé ✅")
            self.main_editor_area.after(2000, lambda: self.sc_status_enc.configure(text="UTF-8"))
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de la sauvegarde:\n{e}")

    def _sc_find(self, event=None):
        if not self.current_file: return
        query = self.sc_search_var.get()
        editor = self.editors[self.current_file]
        editor.tag_remove("search", "1.0", "end")
        
        if query:
            editor.tag_configure("search", background="#4fc3f7", foreground="black")
            idx = "1.0"
            while True:
                idx = editor.search(query, idx, nocase=1, stopindex="end")
                if not idx: break
                lastidx = f"{idx}+{len(query)}c"
                editor.tag_add("search", idx, lastidx)
                idx = lastidx

    # --- TERMINAL INTERACTIF ---
    
    def _sc_run_python(self):
        if not self.current_file or not self.current_file.endswith(".py"):
            messagebox.showwarning("Attention", "Veuillez ouvrir un fichier Python (.py) pour l'exécuter.")
            return
            
        self._sc_save_file() # Auto-save before run
        
        self.sc_term_text.delete("1.0", "end")
        self.sc_term_text.insert("end", f"> Exécution de {Path(self.current_file).name}...\n\n")
        self.sc_stop_btn.pack(side="left", padx=5)
        
        def run_thread():
            try:
                env = os.environ.copy()
                python_exe = sys.executable
                self._sc_process = subprocess.Popen(
                    [python_exe, "-u", self.current_file], # -u force stdout to be unbuffered
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env,
                    cwd=str(self.workspace_dir)
                )
                
                # Lire la sortie en continu
                while getattr(self, "_sc_process", None):
                    try:
                        char = self._sc_process.stdout.read(1)
                        if not char: break
                        self.main_editor_area.after(0, lambda c=char: self._sc_term_append(c))
                    except Exception:
                        break
                        
                self.main_editor_area.after(0, self._sc_term_finished)
            except Exception as e:
                self.main_editor_area.after(0, lambda: self._sc_term_append(f"\n[ERREUR] {e}\n"))

        threading.Thread(target=run_thread, daemon=True).start()

    def _sc_term_append(self, text):
        self.sc_term_text.insert("end", text)
        self.sc_term_text.see("end")

    def _sc_term_finished(self):
        self.sc_stop_btn.pack_forget()
        self._sc_term_append("\n[Processus terminé]")
        self._sc_process = None

    def _sc_stop_python(self):
        if getattr(self, "_sc_process", None):
            try:
                self._sc_process.kill()
            except: pass
            self._sc_process = None
            self._sc_term_append("\n[Arrêté par l'utilisateur]\n")
        self.sc_stop_btn.pack_forget()

    def _sc_term_send_input(self, event):
        """Permet à l'utilisateur de taper et d'envoyer à stdin"""
        if getattr(self, "_sc_process", None) and self._sc_process.poll() is None:
            # Récupérer la dernière ligne
            current_line = self.sc_term_text.get("insert linestart", "insert lineend")
            # Extraire juste ce que l'utilisateur vient de taper (très basique)
            # En réalité on envoie toute la ligne au process
            try:
                self._sc_process.stdin.write(current_line + "\n")
                self._sc_process.stdin.flush()
            except Exception as e:
                self._sc_term_append(f"\n[Erreur Input] {e}\n")
        return "break" # Empêcher le comportement par défaut de Text widget

    def _sc_preview(self):
        if not self.current_file or not self.current_file.endswith((".html", ".htm")):
            messagebox.showwarning("Attention", "Ouvrez un fichier HTML pour l'aperçu.")
            return
        self._sc_save_file()
        webbrowser.open(f"file:///{pathlib.Path(self.current_file).as_posix()}")

    def _sc_validate(self):
        if not self.current_file or not self.current_file.endswith((".html", ".htm")):
            messagebox.showinfo("Validation", "La validation n'est dispo que pour HTML.")
            return
        code = self.editors[self.current_file].get("1.0", "end")
        errors = validate_html(code)
        if len(errors) == 1 and "valide" in errors[0]:
            messagebox.showinfo("✅ HTML Valide", errors[0])
        else:
            messagebox.showwarning("⚠️ Erreurs HTML", "\n".join(f"• {e}" for e in errors))
