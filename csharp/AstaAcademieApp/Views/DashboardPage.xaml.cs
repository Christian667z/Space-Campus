using System;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using AstaAcademieApp.Core;
using Newtonsoft.Json.Linq;

namespace AstaAcademieApp.Views
{
    public partial class DashboardPage : Page
    {
        private readonly DispatcherTimer _liveTimer = null!;

        private static readonly string[] _quotes =
        {
            "« L'avenir appartient à ceux qui maîtrisent la donnée et construisent avec audace. »",
            "« La cybersécurité n'est pas un produit, c'est un processus. — B. Schneier »",
            "« Tout bug est une opportunité d'apprendre quelque chose de nouveau. »",
            "« Le code propre fait une chose, et la fait bien. — R.C. Martin »",
            "« La connaissance est la seule ressource qui s'accroît quand on la partage. »",
            "« L'optimisation prématurée est la racine de tout mal. — D. Knuth »",
            "« Un programme sans tests est un programme qui attend de planter. »",
        };
        private int _quoteIndex = 0;
        private const double BarMaxWidth = 200.0;

        public DashboardPage()
        {
            try
            {
                InitializeComponent();
                LoadProfileData();
                UpdateNativeIndicator();

                _liveTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
                _liveTimer.Tick += OnLiveTimerTick;
                _liveTimer.Start();

                Loaded   += (_, _) => _ = SafeRefreshAsync();
                Unloaded += (_, _) => _liveTimer.Stop();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"DashboardPage init error: {ex}");
            }
        }

        // ── Timer tick (safe async void) ──────────────────────────────────────
        private async void OnLiveTimerTick(object? sender, EventArgs e)
        {
            await SafeRefreshAsync();
        }

        private async System.Threading.Tasks.Task SafeRefreshAsync()
        {
            try { await RefreshLiveMonitorAsync(); }
            catch (Exception ex) { Console.WriteLine($"LiveMonitor error: {ex.Message}"); }
        }

        // ── Chargement profil JSON ────────────────────────────────────────────
        private void LoadProfileData()
        {
            try
            {
                if (!File.Exists(Config.ProfilesPath)) return;
                var data = JObject.Parse(File.ReadAllText(Config.ProfilesPath));
                if (data.Count == 0) return;
                var p = data.First?.First;
                if (p == null) return;

                string nom    = p["nom"]?.ToString()    ?? "Étudiant";
                string xp     = p["points"]?.ToString() ?? "0";
                string streak = p["streak"]?.ToString() ?? "0";
                string niveau = p["niveau"]?.ToString() ?? "L2";
                int    badges = (p["badges"] as JArray)?.Count ?? 0;

                TxtWelcome.Text    = $"👋 Bienvenue, {nom} !";
                TxtNiveau.Text     = niveau;
                TxtCardXP.Text     = $"{xp} XP";
                TxtCardStreak.Text = $"{streak} Jours";
                TxtCardBadges.Text = $"{badges} Badge{(badges != 1 ? "s" : "")}";

                if (int.TryParse(xp, out int xpVal)) UpdateXpBars(xpVal);
            }
            catch (Exception ex) { Console.WriteLine($"LoadProfile error: {ex.Message}"); }
        }

        private void UpdateNativeIndicator()
        {
            try
            {
                bool nat = SystemMetricsService.Instance.IsNativeAvailable;
                TxtNativeMode.Text = nat ? "● Mode natif C++" : "● Mode simulé (fallback C#)";
                TxtNativeMode.Foreground = nat
                    ? (System.Windows.Media.Brush)Application.Current.Resources["BrushPrimary"]
                    : new System.Windows.Media.SolidColorBrush(
                        System.Windows.Media.Color.FromRgb(245, 158, 11));
            }
            catch (Exception ex) { Console.WriteLine($"NativeIndicator error: {ex.Message}"); }
        }

        private void UpdateXpBars(int xp)
        {
            double s = Math.Min(xp / 500.0, 1.0);
            BarLun.Height = Math.Max(10, 40  * s);
            BarMar.Height = Math.Max(10, 70  * s);
            BarMer.Height = Math.Max(10, 50  * s);
            BarJeu.Height = Math.Max(10, 120 * s);
            BarVen.Height = Math.Max(10, 90  * s);
            BarSam.Height = Math.Max(10, 30  * (s * 0.5));
            BarDim.Height = Math.Max(10, 20  * (s * 0.3));
        }

        // ── Moniteur live ─────────────────────────────────────────────────────
        private async System.Threading.Tasks.Task RefreshLiveMonitorAsync()
        {
            var svc = SystemMetricsService.Instance;

            double cpu            = await svc.GetCpuPercentAsync();
            var    (used, tot, p) = await svc.GetRamInfoAsync();
            ulong  upMs           = await svc.GetUptimeMsAsync();

            // Retour sur le Dispatcher UI
            Dispatcher.Invoke(() =>
            {
                TxtCpuPct.Text     = $"{cpu:F1} %";
                TxtRamInfo.Text    = $"{used / 1024.0:F1} Go / {tot / 1024.0:F1} Go";
                TxtDashUptime.Text = SystemMetricsService.FormatUptime(upMs);
                TxtDate.Text       = DateTime.Now.ToString("dddd dd MMMM yyyy  •  HH:mm");
                CpuBar.Width       = BarMaxWidth * Math.Clamp(cpu / 100.0, 0, 1);
                RamBar.Width       = BarMaxWidth * Math.Clamp(p   / 100.0, 0, 1);
            });
        }

        // ── Oracle ────────────────────────────────────────────────────────────
        private void BtnOracle_Click(object sender, RoutedEventArgs e)
        {
            _quoteIndex = (_quoteIndex + 1) % _quotes.Length;
            TxtOracle.Text = _quotes[_quoteIndex];
        }
    }
}
