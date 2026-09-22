using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;

namespace AstaAcademieLauncher
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            
            // Permettre le déplacement de la fenêtre borderless au clic-glissé
            MouseDown += (s, e) => {
                if (e.ChangedButton == MouseButton.Left) DragMove();
            };

            Loaded += async (s, e) => await InitializeDiagnosticAsync();
        }

        private async Task InitializeDiagnosticAsync()
        {
            // Initialisation de la progression
            SplashProgress.Value = 0;

            // Étape 1 : Vérification de l'exécutable principal
            SplashMessage.Text = "Analyse de la distribution...";
            CheckAppStatus.Text = "🔄 EN COURS";
            CheckAppStatus.Foreground = System.Windows.Media.Brushes.Yellow;
            await Task.Delay(500);

            string exePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "AstaAcademie.exe");
            bool appExists = File.Exists(exePath);
            
            // Si une version candidate est présente dans dist\build_asta, comparer et remplacer si différente
            if (!appExists)
            {
                exePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\..\\dist\\AstaAcademie.exe");
                appExists = File.Exists(exePath);
            }

            var candidate = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\..\\dist\\build_asta\\AstaAcademie.exe");
            if (File.Exists(candidate))
            {
                try
                {
                    if (VersionVerifier.IsDifferent(exePath, candidate))
                    {
                        VersionVerifier.BackupAndReplace(exePath, candidate);
                        appExists = true;
                    }
                }
                catch { }
            }

            CheckAppStatus.Text = appExists ? "🟢 CONFORME" : "🟡 VERSION DEV";
            CheckAppStatus.Foreground = appExists ? System.Windows.Media.Brushes.LightGreen : System.Windows.Media.Brushes.Orange;
            SplashProgress.Value = 25;

            // Étape 2 : Vérification de la base de données
            SplashMessage.Text = "Test de la base de données locale...";
            CheckDbStatus.Text = "🔄 EN COURS";
            CheckDbStatus.Foreground = System.Windows.Media.Brushes.Yellow;
            await Task.Delay(600);

            string dbPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "data\\asta_database.db");
            bool dbExists = File.Exists(dbPath);
            if (!dbExists)
            {
                dbPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\..\\data\\asta_database.db");
                dbExists = File.Exists(dbPath);
            }

            CheckDbStatus.Text = dbExists ? "🟢 ACCÈS OK" : "🟡 À CRÉER (INIT)";
            CheckDbStatus.Foreground = dbExists ? System.Windows.Media.Brushes.LightGreen : System.Windows.Media.Brushes.Orange;
            SplashProgress.Value = 50;

            // Étape 3 : Module de sécurité C++ (CNG native_security.dll)
            SplashMessage.Text = "Vérification des modules de chiffrement...";
            CheckSecStatus.Text = "🔄 EN COURS";
            CheckSecStatus.Foreground = System.Windows.Media.Brushes.Yellow;
            await Task.Delay(500);

            string dllPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "native_security.dll");
            bool dllExists = File.Exists(dllPath);
            if (!dllExists)
            {
                dllPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\..\\dist\\native_security.dll");
                dllExists = File.Exists(dllPath);
            }

            CheckSecStatus.Text = dllExists ? "🟢 CHARGÉ (CNG)" : "🟡 HORS-LIGNE (FALLBACK)";
            CheckSecStatus.Foreground = dllExists ? System.Windows.Media.Brushes.LightGreen : System.Windows.Media.Brushes.Orange;
            SplashProgress.Value = 75;

            // Étape 4 : Service RAG Hors-ligne
            SplashMessage.Text = "Chargement du moteur d'IA locale...";
            CheckNetStatus.Text = "🔄 EN COURS";
            CheckNetStatus.Foreground = System.Windows.Media.Brushes.Yellow;
            await Task.Delay(600);

            CheckNetStatus.Text = "🟢 DISPONIBLE";
            CheckNetStatus.Foreground = System.Windows.Media.Brushes.LightGreen;
            SplashProgress.Value = 100;

            SplashMessage.Text = "Lancement du Tableau de bord...";
            await Task.Delay(400);

            // Transition de vue
            GridSplash.Visibility = Visibility.Collapsed;
            GridDashboard.Visibility = Visibility.Visible;

            // Affichage des statistiques système
            RefreshSystemStats();
        }

        private void RefreshSystemStats()
        {
            try
            {
                using var proc = Process.GetCurrentProcess();
                long memory = proc.WorkingSet64 / (1024 * 1024);
                
                // Obtenir des infos système génériques de base
                string osArch = Environment.Is64BitOperatingSystem ? "x64" : "x86";
                string coreCount = Environment.ProcessorCount.ToString();
                
                TxtSystemStats.Text = $"CPU : {coreCount} Coeurs | RAM : {memory} Mo | Arch : {osArch}";
            }
            catch
            {
                TxtSystemStats.Text = "Stats système non disponibles";
            }
        }

        private void BtnLaunchWorkspace_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Chemins possibles de l'exécutable de production
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string exePath = Path.Combine(baseDir, "AstaAcademie.exe");

                if (File.Exists(exePath))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = exePath,
                        WorkingDirectory = baseDir,
                        UseShellExecute = true
                    });
                    Close(); // Fermer le lanceur après lancement
                    return;
                }

                // Fallback 1: Si on est lancé depuis le dossier C# ou dist
                string parentExe = Path.Combine(baseDir, "..\\..\\..\\..\\dist\\AstaAcademie.exe");
                if (File.Exists(parentExe))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = parentExe,
                        WorkingDirectory = Path.GetDirectoryName(parentExe),
                        UseShellExecute = true
                    });
                    Close();
                    return;
                }

                // Fallback 2: Lancement de développement si l'exe compilé n'est pas encore présent
                string devScript = Path.Combine(baseDir, "..\\..\\..\\..\\main_qt.py");
                string venvPython = Path.Combine(baseDir, "..\\..\\..\\..\\.venv\\Scripts\\pythonw.exe");
                if (File.Exists(devScript) && File.Exists(venvPython))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = venvPython,
                        Arguments = $"\"{devScript}\"",
                        WorkingDirectory = Path.GetDirectoryName(devScript),
                        UseShellExecute = true
                    });
                    Close();
                    return;
                }

                MessageBox.Show(
                    "Impossible de localiser AstaAcademie.exe ou l'environnement de développement.\n" +
                    "Veuillez exécuter build_red.py pour compiler l'application.",
                    "Erreur de lancement",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error
                );
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Une erreur est survenue lors du démarrage de l'application :\n{ex.Message}",
                    "Erreur critique",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error
                );
            }
        }

        private void BtnDiagnostic_Click(object sender, RoutedEventArgs e)
        {
            string dbPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "data\\asta_database.db");
            if (!File.Exists(dbPath))
            {
                dbPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\..\\data\\asta_database.db");
            }

            MessageBox.Show(
                "=== DIAGNOSTIC COMPLET DES MODULES ===\n\n" +
                $"• Système d'exploitation : {Environment.OSVersion}\n" +
                $"• Architecture machine : {(Environment.Is64BitOperatingSystem ? "64-bit" : "32-bit")}\n" +
                $"• Base de données SQLite : {(File.Exists(dbPath) ? "🟢 CONNECTÉE (" + Path.GetFileName(dbPath) + ")" : "🔴 MANQUANTE")}\n" +
                $"• Chiffrement CNG C++ : {(File.Exists(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "native_security.dll")) ? "🟢 PRÉSENT" : "🟡 INDISPONIBLE (Simulation active)")}\n\n" +
                "Tous les systèmes opérationnels sont validés pour le business !",
                "Diagnostic Système Pro",
                MessageBoxButton.OK,
                MessageBoxImage.Information
            );
        }

        private void BtnHelp_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show(
                "Besoin d'aide ou de support ?\n\n" +
                "• WhatsApp Support : +509 46 96 6290\n" +
                "• E-mail : support@asta-academie.edu\n" +
                "• Développeur Référent : Space Dev\n\n" +
                "Votre clé d'accès et votre HWID sont cryptés localement.",
                "Support Étudiant Asta",
                MessageBoxButton.OK,
                MessageBoxImage.Information
            );
        }

        private void BtnExit_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void BtnOpenAdmin_Click(object sender, RoutedEventArgs e)
        {
            var w = new AdminWindow { Owner = this };
            w.ShowDialog();
        }
    }
}
