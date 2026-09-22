using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;

namespace AstaAcademieApp.Views
{
    public partial class CoursesPage : Page
    {
        private string _currentContent = "";
        private double _fontSize = 14;
        private int    _totalFiles = 0;

        // Chemin du dossier cours/ : cherche depuis l'exe puis depuis le projet
        private static readonly string CoursRoot = FindCoursDir();

        public CoursesPage()
        {
            try { InitializeComponent(); }
            catch (Exception ex) { Console.WriteLine($"CoursesPage init: {ex.Message}"); return; }
            Loaded += (_, _) => BuildTree();
        }

        // ── Recherche du dossier cours/ ───────────────────────────────────────
        private static string FindCoursDir()
        {
            var candidates = new[]
            {
                Path.Combine(AppContext.BaseDirectory, "cours"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "cours"),
                Path.Combine(AppContext.BaseDirectory, "..", "cours"),
                @"C:\Users\DELL\Space-Dev\AstaAcademie\cours",
            };
            return candidates.FirstOrDefault(Directory.Exists) ?? "";
        }

        // ── Construction du TreeView ──────────────────────────────────────────
        private void BuildTree(string filter = "")
        {
            CoursTree.Items.Clear();
            _totalFiles = 0;

            if (!Directory.Exists(CoursRoot))
            {
                var err = new TreeViewItem { Header = "⚠ Dossier cours/ introuvable", Foreground = Brushes.OrangeRed };
                CoursTree.Items.Add(err);
                return;
            }

            var levelIcons = new Dictionary<string, string>
            {
                ["l1"] = "①", ["l2"] = "②", ["l3"] = "③", ["l4"] = "④", ["python"] = "🐍"
            };

            foreach (var dir in Directory.GetDirectories(CoursRoot).OrderBy(d => d))
            {
                string name = Path.GetFileName(dir);
                string icon = levelIcons.TryGetValue(name.ToLower(), out var ic) ? ic : "📁";

                var levelItem = new TreeViewItem
                {
                    Header = $"{icon}  {name}",
                    FontWeight = FontWeights.Bold,
                    Foreground = new SolidColorBrush(Color.FromRgb(16, 185, 129))
                };

                PopulateNode(levelItem, dir, filter);
                if (levelItem.Items.Count > 0 || string.IsNullOrEmpty(filter))
                    CoursTree.Items.Add(levelItem);
            }

            TxtFileCount.Text = $"{_totalFiles} fichier(s) disponible(s)";
        }

        private void PopulateNode(TreeViewItem parent, string dirPath, string filter)
        {
            try
            {
                // Sous-dossiers en premier
                foreach (var sub in Directory.GetDirectories(dirPath).OrderBy(d => d))
                {
                    string name = Path.GetFileName(sub);
                    if (name.StartsWith(".")) continue;

                    var node = new TreeViewItem
                    {
                        Header = $"📂  {name}",
                        Foreground = new SolidColorBrush(Color.FromRgb(180, 200, 220))
                    };
                    PopulateNode(node, sub, filter);
                    if (node.Items.Count > 0 || string.IsNullOrEmpty(filter))
                        parent.Items.Add(node);
                }

                // Fichiers
                var exts = new[] { ".md", ".txt", ".py" };
                foreach (var file in Directory.GetFiles(dirPath).OrderBy(f => f))
                {
                    string ext = Path.GetExtension(file).ToLower();
                    if (!exts.Contains(ext)) continue;

                    string stem = Path.GetFileNameWithoutExtension(file);
                    if (!string.IsNullOrEmpty(filter) &&
                        !stem.Contains(filter, StringComparison.OrdinalIgnoreCase)) continue;

                    string fileIcon = ext == ".md" ? "📄" : ext == ".py" ? "🐍" : "🗒";
                    var item = new TreeViewItem
                    {
                        Header = $"{fileIcon}  {stem}",
                        Tag    = file,
                        Foreground = new SolidColorBrush(Color.FromRgb(200, 210, 225))
                    };
                    parent.Items.Add(item);
                    _totalFiles++;
                }
            }
            catch { /* Accès refusé ignoré */ }
        }

        // ── Sélection d'un fichier ────────────────────────────────────────────
        private void CoursTree_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
        {
            if (e.NewValue is TreeViewItem { Tag: string path } && File.Exists(path))
                LoadFile(path);
        }

        private void LoadFile(string path)
        {
            try
            {
                _currentContent = File.ReadAllText(path, Encoding.UTF8);
                RenderContent(path, _currentContent);

                string stem = Path.GetFileNameWithoutExtension(path);
                TxtBreadcrumb.Text = $"► {stem}";
                TxtBreadcrumb.Foreground = new SolidColorBrush(Color.FromRgb(200, 220, 240));

                int words = _currentContent.Split(' ', '\n', '\t').Length;
                int mins  = Math.Max(1, words / 200);
                TxtWordCount.Text = $"{words:N0} mots · {_currentContent.Length:N0} caractères";
                TxtReadTime.Text  = $"⏱ ~{mins} min de lecture";
            }
            catch (Exception ex)
            {
                TxtContent.Text = $"❌ Erreur de lecture : {ex.Message}";
            }
        }

        // ── Rendu simplifié du Markdown ───────────────────────────────────────
        private void RenderContent(string path, string content)
        {
            string ext = Path.GetExtension(path).ToLower();

            if (ext == ".md")
            {
                // Conversion Markdown basique → texte enrichi
                var sb = new StringBuilder();
                foreach (var rawLine in content.Split('\n'))
                {
                    string line = rawLine.TrimEnd('\r');
                    if (line.StartsWith("# "))
                        sb.AppendLine($"\n═══ {line[2..].ToUpper()} ═══\n");
                    else if (line.StartsWith("## "))
                        sb.AppendLine($"\n▶ {line[3..].TrimStart()}\n");
                    else if (line.StartsWith("### "))
                        sb.AppendLine($"  › {line[4..].TrimStart()}");
                    else if (line.StartsWith("- ") || line.StartsWith("* "))
                        sb.AppendLine($"  • {line[2..]}");
                    else if (line.StartsWith("```"))
                        sb.AppendLine(line.StartsWith("```") && line.Length > 3 ? "" : "─────────────────");
                    else
                        sb.AppendLine(line);
                }
                TxtContent.Text      = sb.ToString();
                TxtContent.FontFamily = new FontFamily("Segoe UI");
                TxtContent.FontSize   = _fontSize;
            }
            else if (ext == ".py")
            {
                TxtContent.Text       = content;
                TxtContent.FontFamily = new FontFamily("Consolas");
                TxtContent.FontSize   = _fontSize - 1;
            }
            else
            {
                TxtContent.Text       = content;
                TxtContent.FontFamily = new FontFamily("Segoe UI");
                TxtContent.FontSize   = _fontSize;
            }

            ReaderScroll.ScrollToTop();
        }

        // ── Recherche ─────────────────────────────────────────────────────────
        private void TxtSearch_TextChanged(object sender, TextChangedEventArgs e)
            => BuildTree(TxtSearch.Text.Trim());

        // ── Toolbar ──────────────────────────────────────────────────────────
        private void BtnFontMinus_Click(object sender, RoutedEventArgs e)
        {
            _fontSize = Math.Max(10, _fontSize - 1);
            TxtContent.FontSize = _fontSize;
        }

        private void BtnFontPlus_Click(object sender, RoutedEventArgs e)
        {
            _fontSize = Math.Min(22, _fontSize + 1);
            TxtContent.FontSize = _fontSize;
        }

        private void BtnCopy_Click(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrEmpty(_currentContent))
                Clipboard.SetText(_currentContent);
        }
    }
}
