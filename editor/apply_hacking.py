import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix the typo
content = content.replace("k    is_licensed, hwid = check_license_on_startup()", "    is_licensed, hwid = check_license_on_startup()")

# 2. Add imports
import_str = "from security_auth import (check_license_on_startup, verify_license,\n"
new_import_str = "import base64\nfrom security_auth import (load_hacking_license, verify_hacking_key, save_hacking_license, check_license_on_startup, verify_license,\n"
content = content.replace(import_str, new_import_str)

# 3. Add to sidebar
sidebar_search = '("shortcuts", "⚡ Raccourcis"),'
sidebar_replace = '("shortcuts", "⚡ Raccourcis"),\n            ("hacking",   "🏴‍☠️ Hacking"),'
content = content.replace(sidebar_search, sidebar_replace)

# 4. Add to dispatch
dispatch_search = '"shortcuts": self._build_shortcuts,'
dispatch_replace = '"shortcuts": self._build_shortcuts,\n            "hacking":   self._build_hacking,'
content = content.replace(dispatch_search, dispatch_replace)

# 5. Add _build_hacking
hacking_method = """
    def _build_hacking(self):
        # Premium Hacking Tab
        outer = ctk.CTkFrame(self.main_area, fg_color=self.C["bg"])
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(1, weight=1)
        self._section_header(outer, "🏴‍☠️ CyberSécurité & Hacking", "Module Premium : Défis et concepts avancés")

        content_frame = ctk.CTkFrame(outer, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        saved_key = load_hacking_license()
        
        def show_locked():
            for widget in content_frame.winfo_children():
                widget.destroy()
            locked_f = self._card(content_frame, bg=self.C["sidebar"])
            locked_f.pack(expand=True, fill="both", padx=50, pady=50)
            
            ctk.CTkLabel(locked_f, text="🔒 ACCÈS REFUSÉ", font=("Consolas", 32, "bold"), text_color=self.C["danger"]).pack(pady=(40, 10))
            ctk.CTkLabel(locked_f, text="Ce module est verrouillé. Une clé Premium Hacking est requise.", font=("Segoe UI", 14), text_color=self.C["text"]).pack(pady=5)
            
            key_entry = ctk.CTkEntry(locked_f, placeholder_text="A1B2C-3D4E5-F6G7H-8I9J0", width=300, height=40, justify="center")
            key_entry.pack(pady=20)
            
            error_lbl = ctk.CTkLabel(locked_f, text="", text_color=self.C["danger"])
            error_lbl.pack()

            def try_unlock():
                k = key_entry.get().strip()
                if verify_hacking_key(self.hwid, k):
                    save_hacking_license(k)
                    show_unlocked()
                else:
                    error_lbl.configure(text="Clé invalide. Contactez Space sur WhatsApp : +509 35 67 2037")
            
            ctk.CTkButton(locked_f, text="🔓 Valider la Clé", command=try_unlock, fg_color=self.C["accent"], hover_color=self.C["accent2"]).pack(pady=10)
            ctk.CTkLabel(locked_f, text="Pour obtenir une clé Hacking, contactez :\\nWhatsApp : +509 35 67 2037 / +509 46 96 6290", text_color=self.C["subtext"]).pack(pady=(20, 0))

        def show_unlocked():
            for widget in content_frame.winfo_children():
                widget.destroy()
                
            scroll = self._scrollable_frame()
            scroll.pack(in_=content_frame, fill="both", expand=True)
            
            # Lesson 1
            l1 = self._card(scroll)
            ctk.CTkLabel(l1, text="Leçon 1 : Introduction à la Cryptographie Pratique", font=("Segoe UI", 16, "bold"), text_color=self.C["accent"]).pack(anchor="w", pady=(0, 5))
            ctk.CTkLabel(l1, text="La cryptographie moderne utilise des algorithmes comme le SHA-256 (hachage) pour garantir l'intégrité des données, et le chiffrement asymétrique (RSA) pour la confidentialité.\\n\\n🔍 CTF Challenge : Décodez ce message en Base64 pour trouver la 'flag'.\\nMessage : QXN0YUhhY2tpbmcyMDI0", justify="left").pack(anchor="w")
            
            ctf_frame = ctk.CTkFrame(l1, fg_color="transparent")
            ctf_frame.pack(fill="x", pady=10)
            ctf_entry = ctk.CTkEntry(ctf_frame, placeholder_text="Entrez la flag décodée ici", width=250)
            ctf_entry.pack(side="left", padx=5)
            ctf_res = ctk.CTkLabel(ctf_frame, text="")
            
            def check_ctf():
                if ctf_entry.get().strip() == "AstaHacking2024":
                    ctf_res.configure(text="✅ Succès ! Flag valide.", text_color=self.C["success"])
                else:
                    ctf_res.configure(text="❌ Flag incorrecte.", text_color=self.C["danger"])
            ctk.CTkButton(ctf_frame, text="Valider CTF", command=check_ctf, width=100).pack(side="left", padx=5)
            ctf_res.pack(side="left", padx=10)
            
            # Lesson 2
            l2 = self._card(scroll)
            ctk.CTkLabel(l2, text="Leçon 2 : Failles Web (Injection SQL & XSS)", font=("Segoe UI", 16, "bold"), text_color=self.C["accent"]).pack(anchor="w", pady=(0, 5))
            ctk.CTkLabel(l2, text="L'injection (SQLi) se produit quand des données non fiables sont envoyées à un interpréteur en tant que commande.\\nLes XSS (Cross-Site Scripting) permettent à un attaquant d'injecter des scripts clients dans des pages web lues par d'autres utilisateurs.\\n\\n🛠️ Solution : Toujours échapper/sanitiser les entrées utilisateur.", justify="left").pack(anchor="w")
            
            # Lesson 3
            l3 = self._card(scroll)
            ctk.CTkLabel(l3, text="Leçon 3 : Sécurité des Systèmes et Anonymat", font=("Segoe UI", 16, "bold"), text_color=self.C["accent"]).pack(anchor="w", pady=(0, 5))
            ctk.CTkLabel(l3, text="Le terminal (cmd, bash) est l'arme principale du hacker éthique.\\nOutils clés de Kali Linux : Nmap (scan réseau), Metasploit (exploitation), Wireshark (analyse paquet).\\nPour se protéger : VPN, Proxychains (Tor) pour masquer l'IP, et chiffrement local (BitLocker, LUKS).", justify="left").pack(anchor="w")

        if saved_key and verify_hacking_key(self.hwid, saved_key):
            show_unlocked()
        else:
            show_locked()

    def _build_quiz(self):"""
content = content.replace("    def _build_quiz(self):", hacking_method)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Modifications appliquées à main.py avec succès.")
