using System;
using System.IO;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using Newtonsoft.Json.Linq;
using AstaAcademieApp.Core;

namespace AstaAcademieApp
{
    public partial class MainWindow : Window
    {
        private readonly DispatcherTimer _clockTimer = null!;

        public MainWindow()
        {
            InitializeComponent();

            try { LoadProfileData(); }
            catch (Exception ex) { Console.WriteLine($"LoadProfile error: {ex.Message}"); }

            try { UpdateNativeIndicator(); }
            catch (Exception ex) { Console.WriteLine($"NativeIndicator error: {ex.Message}"); }

            // Horloge en direct
            _clockTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
            _clockTimer.Tick += (_, _) => TxtTopClock.Text = DateTime.Now.ToString("HH:mm:ss");
            _clockTimer.Start();
            TxtTopClock.Text = DateTime.Now.ToString("HH:mm:ss");

            // Navigation initiale vers le Dashboard
            Navigate(() => new Views.DashboardPage());
        }

        // ── Helper navigation sécurisé ────────────────────────────────────────
        private void Navigate(Func<System.Windows.Controls.Page> pageFactory)
        {
            try
            {
                var page = pageFactory();
                MainFrame.Navigate(page);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur de navigation :\n{ex.GetType().Name}\n{ex.Message}",
                    "AstaAcadémie", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        // ── Indicateur DLL native ─────────────────────────────────────────────
        private void UpdateNativeIndicator()
        {
            bool sec = SecurityService.Instance.IsNativeAvailable;
            bool met = SystemMetricsService.Instance.IsNativeAvailable;

            if (sec || met)
            {
                TopNativeLabel.Text = "● C++ NATIF";
                TopNativeLabel.Foreground = new SolidColorBrush(Color.FromRgb(16, 185, 129));
                TopNativeIndicator.Background = new SolidColorBrush(Color.FromArgb(30, 16, 185, 129));
            }
            else
            {
                TopNativeLabel.Text = "● FALLBACK C#";
                TopNativeLabel.Foreground = new SolidColorBrush(Color.FromRgb(245, 158, 11));
                TopNativeIndicator.Background = new SolidColorBrush(Color.FromArgb(30, 245, 158, 11));
            }
        }

        // ── Interactions fenêtre ──────────────────────────────────────────────
        private void TopBar_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
                try { DragMove(); } catch { /* fenêtre minimisée */ }
        }

        private void BtnMinimize_Click(object sender, RoutedEventArgs e)
            => WindowState = WindowState.Minimized;

        private void BtnClose_Click(object sender, RoutedEventArgs e)
            => Application.Current.Shutdown();

        // ── Chargement profil sidebar ─────────────────────────────────────────
        private void LoadProfileData()
        {
            if (!File.Exists(Config.ProfilesPath)) return;
            var data = JObject.Parse(File.ReadAllText(Config.ProfilesPath));
            if (data.Count == 0) return;
            var p = data.First?.First;
            if (p == null) return;
            TxtXP.Text     = p["points"]?.ToString() ?? "0";
            TxtStreak.Text = p["streak"]?.ToString() ?? "0";
        }

        // ═════════════════════════════════════════════════════════════════════
        //  NAVIGATION HANDLERS — tous sécurisés par Navigate()
        // ═════════════════════════════════════════════════════════════════════

        private void BtnNavDashboard_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.DashboardPage());

        private void BtnNavSpaceAI_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.SpaceAiPage());

        private void BtnNavOracle_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.OraclePage());

        private void BtnNavTools_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.PlaceholderPage("Outils"));

        private void BtnNavCourses_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.CoursesPage());

        private void BtnNavShortcuts_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.ShortcutsPage());

        private void BtnNavDevSecurity_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.DevSecurityPage());

        private void BtnNavTerminal_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.TerminalPage());

        private void BtnNavQuiz_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.QuizPage());

        private void BtnNavNotes_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.NotesPage());

        private void BtnNavGrades_Click(object sender, RoutedEventArgs e)
            => Navigate(() => new Views.PlaceholderPage("Moyennes"));
    }
}