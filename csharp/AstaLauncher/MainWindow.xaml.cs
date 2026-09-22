using System.Windows;
using AstaLauncher.Views;

namespace AstaLauncher
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            
            // Ouvrir le Dashboard par défaut
            MainContent.Content = new DashboardView();
        }

        private void NavDashboard_Click(object sender, RoutedEventArgs e)
        {
            MainContent.Content = new DashboardView();
        }

        private void NavUsers_Click(object sender, RoutedEventArgs e)
        {
            MainContent.Content = new UsersView();
        }

        private void NavLogs_Click(object sender, RoutedEventArgs e)
        {
            MainContent.Content = new LogsView();
        }

        private void NavSys_Click(object sender, RoutedEventArgs e)
        {
            MainContent.Content = new SystemView();
        }

        private void NavGen_Click(object sender, RoutedEventArgs e)
        {
            MainContent.Content = new GeneratorView();
        }
    }
}
