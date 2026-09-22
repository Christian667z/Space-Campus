using System;
using System.Windows;
using AstaAcademieApp.Core;

namespace AstaAcademieApp
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            // Gestionnaire d'exceptions non gérées — affiche l'erreur exacte
            DispatcherUnhandledException += (_, ex) =>
            {
                MessageBox.Show(
                    $"Erreur non gérée :\n\n{ex.Exception.GetType().Name}\n{ex.Exception.Message}\n\n{ex.Exception.StackTrace}",
                    "AstaAcadémie — Erreur",
                    MessageBoxButton.OK, MessageBoxImage.Error);
                ex.Handled = true;
            };

            string dbPath = Config.DbPath;
            Console.WriteLine($"Asta Académie WPF UI Démarrée. DB={dbPath}");
        }
    }
}
