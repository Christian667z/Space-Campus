import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define the old code block
# This covers from def _build_spacecode to the end of def _sc_clear
old_code_start = "    def _build_spacecode(self):"
old_code_end = """    def _sc_clear(self):
        if messagebox.askyesno("Effacer", "Effacer tout le code ?"):
            self.sc_editor.delete("1.0", "end")"""

# Extract the exact old code
start_idx = content.find(old_code_start)
end_idx = content.find(old_code_end) + len(old_code_end)
old_code_block = content[start_idx:end_idx]

new_code_block = """    def _build_spacecode(self):
        frame = ctk.CTkFrame(self.main_area, fg_color=self.C["bg"])
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self._section_header(frame, "💻 SpaceCode — Éditeur Avancé",
                             "Éditeur de code professionnel avec numérotation, indentation automatique et console intégrée.")

        toolbar = ctk.CTkFrame(frame, fg_color=self.C["sidebar"], height=42, corner_radius=0)
        toolbar.grid(row=0, column=0, sticky="ew", padx=0)

        ctk.CTkLabel(toolbar, text="Template :", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tpl_menu = ctk.CTkOptionMenu(toolbar, values=list(HTML_TEMPLATES.keys()),
                                      command=self._sc_load_template,
                                      width=220, height=30,
                                      fg_color=self.C["card"])
        tpl_menu.pack(side="left", padx=5)
        
        ctk.CTkButton(toolbar, text="▶ Run Python",
                      command=self._sc_run_python,
                      fg_color="#3498db", text_color="white",
                      height=30, width=120).pack(side="left", padx=10)
                      
        ctk.CTkButton(toolbar, text="🌐 Aperçu HTML",
                      command=self._sc_preview,
                      fg_color=self.C["success"], text_color="black",
                      height=30, width=130).pack(side="left")
                      
        ctk.CTkButton(toolbar, text="✅ Valider HTML",
                      command=self._sc_validate,
                      fg_color=self.C["accent2"], height=30, width=120).pack(side="left", padx=10)
                      
        ctk.CTkButton(toolbar, text="📋 Copier",
                      command=self._sc_copy,
                      fg_color=self.C["card"], height=30, width=80).pack(side="left")
                      
        ctk.CTkButton(toolbar, text="🗑️ Effacer",
                      command=self._sc_clear,
                      fg_color=self.C["danger"], height=30, width=80).pack(side="left", padx=10)

        editor_container = ctk.CTkFrame(frame, fg_color=self.C["bg"])
        editor_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        editor_container.grid_columnconfigure(1, weight=1)
        editor_container.grid_rowconfigure(0, weight=1)

        self.line_numbers = ctk.CTkTextbox(editor_container, font=("Courier New", 14),
                                         width=40, fg_color=self.C["sidebar"],
                                         text_color=self.C["subtext"], wrap="none",
                                         state="disabled")
        self.line_numbers.grid(row=0, column=0, sticky="ns", pady=5)

        self.sc_editor = ctk.CTkTextbox(editor_container, font=("Courier New", 14),
                                         fg_color="#0d1117", text_color="#e6edf3",
                                         wrap="none")
        self.sc_editor.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        
        # Console de sortie
        console_frame = ctk.CTkFrame(frame, fg_color="#000000", height=150)
        console_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))
        console_frame.grid_propagate(False)
        console_frame.grid_columnconfigure(0, weight=1)
        console_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(console_frame, text="Terminal Output", font=("Consolas", 10, "bold"), text_color="#3498db").grid(row=0, column=0, sticky="w", padx=5)
        self.sc_output = ctk.CTkTextbox(console_frame, font=("Consolas", 12), fg_color="transparent", text_color="#00ff00", wrap="word", state="disabled")
        self.sc_output.grid(row=1, column=0, sticky="nsew", padx=5, pady=2)

        # Bindings pour les numéros de ligne et l'indentation
        self.sc_editor.bind("<KeyRelease>", self._update_line_numbers)
        self.sc_editor.bind("<MouseWheel>", self._update_line_numbers)
        self.sc_editor.bind("<Return>", self._auto_indent)

        self._sc_load_template(list(HTML_TEMPLATES.keys())[0])
        self._update_line_numbers()

    def _update_line_numbers(self, event=None):
        lines = self.sc_editor.get("1.0", "end").count("\\n")
        line_numbers_text = "\\n".join(str(i) for i in range(1, lines + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.configure(state="disabled")
        # Sync scroll
        self.line_numbers.yview_moveto(self.sc_editor.yview()[0])

    def _auto_indent(self, event):
        # Récupérer la ligne précédente
        current_idx = self.sc_editor.index("insert")
        line_num = int(current_idx.split(".")[0])
        if line_num > 1:
            prev_line_text = self.sc_editor.get(f"{line_num-1}.0", f"{line_num-1}.end")
            leading_spaces = len(prev_line_text) - len(prev_line_text.lstrip())
            
            # Ajouter 4 espaces de plus si on finit par ':'
            if prev_line_text.strip().endswith(":"):
                leading_spaces += 4
                
            if leading_spaces > 0:
                self.sc_editor.insert("insert", " " * leading_spaces)
        
        self._update_line_numbers()

    def _sc_load_template(self, name):
        tpl = HTML_TEMPLATES.get(name, {})
        self.sc_editor.delete("1.0", "end")
        self.sc_editor.insert("end", tpl.get("code", "<!-- Template vide -->"))
        self._update_line_numbers()
        
    def _print_to_console(self, text, color="#00ff00"):
        self.sc_output.configure(state="normal")
        self.sc_output.delete("1.0", "end")
        self.sc_output.insert("end", text)
        self.sc_output.configure(state="disabled", text_color=color)

    def _sc_run_python(self):
        code = self.sc_editor.get("1.0", "end").strip()
        self._print_to_console("Exécution en cours...", "#aaaaaa")
        self.update()
        
        import subprocess
        try:
            res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5)
            out = res.stdout
            if res.stderr:
                out += "\\n[ERREURS]\\n" + res.stderr
            if not out.strip(): out = "[Programme terminé sans sortie]"
            self._print_to_console(out, "#00ff00" if not res.stderr else "#ff4444")
        except subprocess.TimeoutExpired:
            self._print_to_console("[ERREUR] Timeout : Le script a pris trop de temps.", "#ff4444")
        except Exception as e:
            self._print_to_console(f"[CRASH]\\n{e}", "#ff4444")

    def _sc_preview(self):
        code = self.sc_editor.get("1.0", "end").strip()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html",
                                         delete=False, encoding="utf-8") as f:
            f.write(code)
            tmp = f.name
        tmp_url = pathlib.Path(tmp).as_posix()
        webbrowser.open(f"file:///{tmp_url}")

    def _sc_validate(self):
        code = self.sc_editor.get("1.0", "end")
        errors = validate_html(code)
        if not errors:
            messagebox.showinfo("✅ HTML Valide", "Aucune erreur détectée dans votre HTML !")
        else:
            messagebox.showwarning("⚠️ Erreurs HTML",
                                   "Erreurs détectées :\\n" + "\\n".join(f"• {e}" for e in errors))

    def _sc_copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.sc_editor.get("1.0", "end"))
        messagebox.showinfo("Copié", "Code copié !")

    def _sc_clear(self):
        if messagebox.askyesno("Effacer", "Effacer tout le code ?"):
            self.sc_editor.delete("1.0", "end")
            self._update_line_numbers()"""

content = content.replace(old_code_block, new_code_block)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Editeur SpaceCode mis à jour avec succès.")
