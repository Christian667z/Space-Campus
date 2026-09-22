using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace AstaAcademieApp.Views
{
    public partial class DevSecurityPage : Page
    {
        // ── Modèles ──────────────────────────────────────────────────────────
        private record PortEntry(string Port, string Protocol, string Description);
        private record NmapEntry(string Cmd, string Desc);
        private record EncodingEntry(string Name, string Desc, string Example);

        private class Mission
        {
            public string Id          { get; init; } = "";
            public string Category    { get; init; } = "";
            public string Difficulty  { get; init; } = "";
            public string Title       { get; init; } = "";
            public string Description { get; init; } = "";
            public string Flag        { get; init; } = "";
            public int    Xp          { get; init; }
            public List<string> Hints { get; init; } = new();
            public bool Solved        { get; set; }
            public int  HintIndex     { get; set; }
        }

        // ── État ─────────────────────────────────────────────────────────────
        private List<Mission> _missions = new();
        private Mission?      _current  = null;
        private int           _totalXp  = 0;
        private List<string>  _completed = new();

        // Brushes
        private static readonly SolidColorBrush BrushOk    = new(Color.FromRgb(16, 185, 129));
        private static readonly SolidColorBrush BrushErr   = new(Color.FromRgb(239, 68, 68));
        private static readonly SolidColorBrush BrushWarn  = new(Color.FromRgb(245, 158, 11));

        public DevSecurityPage()
        {
            try { InitializeComponent(); }
            catch (Exception ex) { Console.WriteLine($"DevSecurityPage init: {ex.Message}"); return; }
            Loaded += (_, _) => Init();
        }

        private void Init()
        {
            BuildMissions();
            BuildMissionList();
            LoadReference();
            if (_missions.Count > 0) MissionList.SelectedIndex = 0;
        }

        // ── Construction des missions ─────────────────────────────────────────
        private void BuildMissions()
        {
            string localIp   = GetLocalIp();
            string username  = Environment.UserName;
            string hostname  = Dns.GetHostName();

            _missions = new List<Mission>
            {
                new() { Id="ctf_01", Category="🔍 Reconnaissance", Difficulty="Facile",
                    Title="Mission 01 : Adresse IPv4",
                    Description="Trouvez l'adresse IPv4 locale de cette machine.",
                    Flag=localIp, Xp=50,
                    Hints=new(){"Utilisez `ipconfig` dans le Terminal de l'app.",
                                $"L'adresse commence par : {localIp[..localIp.LastIndexOf('.')]}.*"}},

                new() { Id="ctf_02", Category="🔍 Reconnaissance", Difficulty="Facile",
                    Title="Mission 02 : Nom d'utilisateur",
                    Description="Identifiez le nom de l'utilisateur actuel du système.",
                    Flag=username, Xp=50,
                    Hints=new(){"Commande : `whoami`",
                                $"Votre nom commence par : {username[0]}…"}},

                new() { Id="ctf_03", Category="🔍 Reconnaissance", Difficulty="Facile",
                    Title="Mission 03 : Nom d'hôte",
                    Description="Quel est le nom d'hôte (hostname) de cette machine ?",
                    Flag=hostname, Xp=50,
                    Hints=new(){"Commande : `hostname`",
                                $"Le hostname commence par : {hostname[0]}…"}},

                new() { Id="ctf_04", Category="🔐 Cryptographie", Difficulty="Facile",
                    Title="Mission 04 : Base64 Decode",
                    Description="Décodez ce message Base64 : QXN0YV9IYWNrZXI=",
                    Flag="Asta_Hacker", Xp=75,
                    Hints=new(){"import base64; base64.b64decode('QXN0YV9IYWNrZXI=').decode()",
                                "Le résultat contient un underscore entre deux mots."}},

                new() { Id="ctf_05", Category="🔐 Cryptographie", Difficulty="Moyen",
                    Title="Mission 05 : César Cipher (ROT13)",
                    Description="Déchiffrez ce message (décalage de 13) : Nfgn_Unpxre",
                    Flag="Asta_Hacker", Xp=100,
                    Hints=new(){"ROT13 en Python : import codecs; codecs.decode('Nfgn_Unpxre','rot13')",
                                "Décalage = 13 lettres dans l'alphabet."}},

                new() { Id="ctf_06", Category="🔐 Cryptographie", Difficulty="Difficile",
                    Title="Mission 06 : Hash SHA-256",
                    Description="Quel algorithme produit ce hash ?\ne3b0c44298fc1c149afb4c8996fb92427ae41e4649b934ca495991b7852b855",
                    Flag="SHA-256", Xp=150,
                    Hints=new(){"C'est le hash d'une chaîne VIDE avec un algo standard.",
                                "La réponse est le nom en majuscules avec un tiret."}},

                new() { Id="ctf_07", Category="🌐 Web Security", Difficulty="Moyen",
                    Title="Mission 07 : Code HTTP",
                    Description="Quel code de statut HTTP signifie 'Non Autorisé' (Unauthorized) ?",
                    Flag="401", Xp=75,
                    Hints=new(){"Les codes 4xx sont des erreurs côté client.",
                                "403 = Interdit. La réponse est juste avant."}},

                new() { Id="ctf_08", Category="🌐 Web Security", Difficulty="Difficile",
                    Title="Mission 08 : Injection SQL",
                    Description="Quelle payload classique permet de bypasser un login avec injection SQL ?",
                    Flag="' OR '1'='1", Xp=150,
                    Hints=new(){"La payload exploite une condition toujours vraie dans WHERE.",
                                "Elle commence par une apostrophe et contient OR."}},

                new() { Id="ctf_09", Category="🔬 Forensique", Difficulty="Moyen",
                    Title="Mission 09 : Port SSH",
                    Description="Quel est le numéro de port par défaut du protocole SSH ?",
                    Flag="22", Xp=75,
                    Hints=new(){"SSH = Secure Shell. Port inférieur à 100.",
                                "Il vient juste après le port 21 (FTP)."}},

                new() { Id="ctf_10", Category="🔬 Forensique", Difficulty="Difficile",
                    Title="Mission 10 : La Signature Asta",
                    Description="Tapez exactement la signature d'Asta Académie pour les hackers.",
                    Flag="ASTA_SEC_2024", Xp=200,
                    Hints=new(){"Majuscules, underscores, se termine par l'année de la promo.",
                                "Format : ASTA_XXX_XXXX"}},
            };
        }

        private static string GetLocalIp()
        {
            try
            {
                using var s = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, 0);
                s.Connect("8.8.8.8", 65530);
                return (s.LocalEndPoint as IPEndPoint)?.Address.ToString() ?? "127.0.0.1";
            }
            catch { return "127.0.0.1"; }
        }

        // ── UI des missions ──────────────────────────────────────────────────
        private void BuildMissionList()
        {
            MissionList.Items.Clear();
            foreach (var m in _missions)
            {
                string badge  = m.Solved ? "✅" : "⬜";
                string color  = m.Difficulty == "Facile" ? "#10b981"
                              : m.Difficulty == "Moyen"  ? "#f59e0b" : "#ef4444";
                var item = new ListBoxItem
                {
                    Tag     = m,
                    Content = BuildMissionItem(badge, m.Title, m.Category, m.Xp, color)
                };
                MissionList.Items.Add(item);
            }
            UpdateScore();
        }

        private static FrameworkElement BuildMissionItem(string badge, string title, string cat, int xp, string hexColor)
        {
            var border = new Border
            {
                Background   = new SolidColorBrush(Color.FromArgb(0x0D, 0x10, 0x1A, 0x10)),
                BorderBrush  = new SolidColorBrush(Color.FromArgb(0x33, 0x30, 0x40, 0x30)),
                BorderThickness = new Thickness(1),
                CornerRadius = new CornerRadius(5),
                Padding      = new Thickness(10, 6, 10, 6)
            };
            var sp = new StackPanel();
            sp.Children.Add(new TextBlock
            {
                Text       = $"{badge} {title}",
                FontFamily = new FontFamily("Consolas"),
                FontSize   = 11,
                Foreground = new SolidColorBrush(Color.FromRgb(220, 230, 240)),
                TextWrapping = TextWrapping.Wrap
            });
            sp.Children.Add(new TextBlock
            {
                Text       = $"{cat}  ·  ⭐ {xp} XP",
                FontFamily = new FontFamily("Consolas"),
                FontSize   = 10,
                Foreground = new SolidColorBrush(Color.FromArgb(0xAA, 0xAA, 0xAA, 0xAA)),
                Margin     = new Thickness(0, 2, 0, 0)
            });
            border.Child = sp;
            return border;
        }

        private void MissionList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (MissionList.SelectedItem is ListBoxItem { Tag: Mission m })
                ShowMission(m);
        }

        private void ShowMission(Mission m)
        {
            _current = m;
            TxtMissionCategory.Text  = m.Category;
            TxtMissionTitle.Text     = m.Title;
            TxtMissionDesc.Text      = m.Description;
            TxtMissionXP.Text        = $"⭐ {m.Xp} XP";
            TxtDifficulty.Text       = $"  [{m.Difficulty}]";
            TxtDifficulty.Foreground = m.Difficulty == "Facile" ? BrushOk
                                     : m.Difficulty == "Moyen"  ? BrushWarn : BrushErr;
            TxtMissionStatus.Text    = m.Solved ? "✅ COMPLÉTÉE" : "";
            TxtMissionStatus.Foreground = BrushOk;
            TxtFlag.Text             = "";
            TxtFlagResult.Text       = "";
            HintBorder.Visibility    = Visibility.Collapsed;
            m.HintIndex              = 0;
        }

        // ── Soumission du flag ───────────────────────────────────────────────
        private void BtnSubmitFlag_Click(object sender, RoutedEventArgs e) => CheckFlag();
        private void TxtFlag_KeyDown(object sender, KeyEventArgs e)
        { if (e.Key == Key.Return) CheckFlag(); }

        private void CheckFlag()
        {
            if (_current == null) return;
            string answer = TxtFlag.Text.Trim();

            if (string.Equals(answer, _current.Flag, StringComparison.OrdinalIgnoreCase))
            {
                if (!_current.Solved)
                {
                    _current.Solved = true;
                    _totalXp       += _current.Xp;
                    _completed.Add($"✅ +{_current.Xp} XP  —  {_current.Title}");
                    BuildMissionList();
                    // Re-select current
                    for (int i = 0; i < MissionList.Items.Count; i++)
                        if (MissionList.Items[i] is ListBoxItem li && li.Tag == _current)
                        { MissionList.SelectedIndex = i; break; }
                }
                TxtFlagResult.Text       = "✅ CORRECT ! Bien joué, hacker.";
                TxtFlagResult.Foreground = BrushOk;
            }
            else
            {
                TxtFlagResult.Text       = "❌ Flag incorrect. Essaie encore ou utilise un indice.";
                TxtFlagResult.Foreground = BrushErr;
            }
        }

        // ── Indice ──────────────────────────────────────────────────────────
        private void BtnHint_Click(object sender, RoutedEventArgs e)
        {
            if (_current == null || _current.Hints.Count == 0) return;
            int idx = Math.Min(_current.HintIndex, _current.Hints.Count - 1);
            TxtHint.Text        = $"💡 Indice {idx + 1}/{_current.Hints.Count} : {_current.Hints[idx]}";
            HintBorder.Visibility = Visibility.Visible;
            _current.HintIndex  = Math.Min(_current.HintIndex + 1, _current.Hints.Count - 1);
        }

        // ── Score ────────────────────────────────────────────────────────────
        private void UpdateScore()
        {
            int done = _missions.Count(m => m.Solved);
            TxtTotalScore.Text = $"🏆 Score : {_totalXp} XP";
            TxtProgress.Text   = $"{done} / {_missions.Count} missions";

            CompletedList.ItemsSource = null;
            CompletedList.ItemsSource = _completed;
            TxtNoCompleted.Visibility = _completed.Count == 0
                ? Visibility.Visible : Visibility.Collapsed;
        }

        // ── Référence sécurité ───────────────────────────────────────────────
        private void LoadReference()
        {
            PortsList.ItemsSource = new List<PortEntry>
            {
                new("21",   "FTP",      "File Transfer Protocol — transfert de fichiers"),
                new("22",   "SSH",      "Secure Shell — accès terminal chiffré"),
                new("23",   "Telnet",   "Accès distant non chiffré (obsolète)"),
                new("25",   "SMTP",     "Simple Mail Transfer Protocol — envoi d'email"),
                new("53",   "DNS",      "Domain Name System — résolution de noms"),
                new("80",   "HTTP",     "HyperText Transfer Protocol — web non chiffré"),
                new("110",  "POP3",     "Post Office Protocol — réception d'email"),
                new("143",  "IMAP",     "Internet Message Access Protocol — email"),
                new("443",  "HTTPS",    "HTTP Secure — web chiffré TLS/SSL"),
                new("3306", "MySQL",    "Base de données MySQL"),
                new("3389", "RDP",      "Remote Desktop Protocol — bureau distant Windows"),
                new("5432", "PostgreSQL","Base de données PostgreSQL"),
                new("6379", "Redis",    "Cache Redis"),
                new("8080", "HTTP-Alt", "Port HTTP alternatif / proxy"),
                new("27017","MongoDB",  "Base de données MongoDB"),
            };

            NmapList.ItemsSource = new List<NmapEntry>
            {
                new("nmap -sV target",       "Détection de version des services"),
                new("nmap -sC target",       "Scripts NSE par défaut"),
                new("nmap -p- target",       "Scanner tous les 65 535 ports"),
                new("nmap -O target",        "Détection du système d'exploitation"),
                new("nmap -A target",        "Scan agressif (OS + version + scripts)"),
                new("nmap --open target",    "Afficher uniquement les ports ouverts"),
                new("nmap -sU -p 53 target", "Scan UDP sur le port DNS"),
                new("nmap -Pn target",       "Ignorer le ping (host peut sembler éteint)"),
            };

            EncodingList.ItemsSource = new List<EncodingEntry>
            {
                new("Base64",    "Encodage binaire→texte ASCII",           "SGVsbG8= → Hello"),
                new("ROT13",     "Chiffre de César avec décalage de 13",   "Nfgn → Asta"),
                new("MD5",       "Hash 128 bits (non sécurisé)",            "128 bits, cassable"),
                new("SHA-1",     "Hash 160 bits (déprécié)",               "160 bits"),
                new("SHA-256",   "Hash 256 bits (standard actuel)",         "256 bits, sûr"),
                new("SHA-512",   "Hash 512 bits (haute sécurité)",          "512 bits"),
                new("bcrypt",    "Hash pour mots de passe + salt",          "Recommandé passwords"),
                new("URL Encode","%XX remplace les caractères spéciaux",   "espace = %20"),
                new("Hex",       "Encodage hexadécimal 0-9 A-F",            "41 = A (ASCII)"),
            };
        }
    }
}
