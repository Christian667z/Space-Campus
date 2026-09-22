using System.Windows;
using System.Windows.Controls;
using System.Threading.Tasks;
using AstaLauncher.Core;

namespace AstaLauncher.Views
{
    public partial class DashboardView : UserControl
    {
        public DashboardView()
        {
            InitializeComponent();
            RefreshSys_Click(null, null);
            Loaded += async (s, e) => await LoadDashboardDataAsync();
        }

        private async Task LoadDashboardDataAsync()
        {
            // Login silencieux
            await ApiClient.LoginAsync("SuperAdmin", "Coucou28"); 
            
            // Récupération des vraies métriques depuis le backend Go
            var metrics = await ApiClient.GetDashboardMetricsAsync();
            
            if (metrics != null && metrics.HasValues)
            {
                TxtTotalUsers.Text = metrics["total_users"]?.ToString() ?? "0";
                TxtActiveUsers.Text = metrics["active_users"]?.ToString() ?? "0";
                TxtErrors.Text = metrics["today_errors"]?.ToString() ?? "0";
            }
            else
            {
                TxtTotalUsers.Text = "API";
                TxtActiveUsers.Text = "HORS";
                TxtErrors.Text = "LIGNE";
            }
        }

        private void RefreshSys_Click(object sender, RoutedEventArgs e)
        {
            var stats = SystemTools.GetQuickStats();
            TxtCpu.Text = $"CPU: {stats.cpu}";
            TxtRam.Text = $"RAM: {stats.ram}";
            TxtUptime.Text = $"Uptime: {stats.uptime}";
        }
    }
}
