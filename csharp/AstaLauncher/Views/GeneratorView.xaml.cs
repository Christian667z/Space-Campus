using System;
using System.Windows;
using System.Windows.Controls;
using AstaLauncher.Core;

namespace AstaLauncher.Views
{
    public partial class GeneratorView : UserControl
    {
        public GeneratorView()
        {
            InitializeComponent();
        }

        private void Generate_Click(object sender, RoutedEventArgs e)
        {
            string hwid = InputHwid.Text.Trim();
            string nom = InputNom.Text.Trim();

            if (string.IsNullOrEmpty(hwid) || string.IsNullOrEmpty(nom))
            {
                MessageBox.Show("Veuillez entrer le Nom et le HWID.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            // Génération ultra-rapide en C# natif
            string baseKey = KeyGenerator.GenerateLicenseKey(hwid);
            string hackKey = KeyGenerator.GenerateHackingKey(hwid);

            OutputBaseKey.Text = baseKey;
            OutputHackKey.Text = hackKey;

            // Formater pour WhatsApp
            string msg = $"🎓 *Bienvenue dans Asta Académie !*\n\n" +
                         $"Voici tes clés d'activation pour le HWID : `{hwid}`\n\n" +
                         $"🔑 *Clé de Base* :\n`{baseKey}`\n\n" +
                         $"☠️ *Clé Module Hacking* :\n`{hackKey}`\n\n" +
                         $"🚀 Lance l'application et entre ces informations.\n" +
                         $"Bon apprentissage !\n" +
                         $"— *L'Administration*";

            Clipboard.SetText(msg);
            MessageBox.Show("Clés générées avec succès !\nLe message WhatsApp a été copié dans le presse-papier.", "Succès", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }
}
