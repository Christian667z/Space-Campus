using System.Windows;
using System.Windows.Controls;
using AstaLauncher.Core;

namespace AstaLauncher.Views
{
    public partial class SystemView : UserControl
    {
        public SystemView()
        {
            InitializeComponent();
        }

        private void KillSwitch_Click(object sender, RoutedEventArgs e)
        {
            if (MessageBox.Show("Attention : Ceci va forcer l'arrêt de toutes les instances d'Asta Académie sur cette machine.\nContinuer ?", "KILL SWITCH", MessageBoxButton.YesNo, MessageBoxImage.Warning) == MessageBoxResult.Yes)
            {
                int killed = SystemTools.KillAstaAcademie();
                MessageBox.Show($"Opération terminée. {killed} processus terminés.", "Kill Switch", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }
}
