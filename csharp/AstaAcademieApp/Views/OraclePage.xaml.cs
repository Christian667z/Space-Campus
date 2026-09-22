using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using AstaAcademieApp.Core;
using Newtonsoft.Json.Linq;

namespace AstaAcademieApp.Views
{
    public partial class OraclePage : Page
    {
        public OraclePage()
        {
            try { InitializeComponent(); }
            catch (Exception ex) { Console.WriteLine($"OraclePage init: {ex.Message}"); return; }
            Loaded += async (_, _) => await LoadAllAsync();
        }

        private async System.Threading.Tasks.Task LoadAllAsync()
        {
            try
            {
                var bridge = PythonBridge.Instance;

                // Vérifier si le pont est en ligne
                bool online = await bridge.IsOnlineAsync();
                Dispatcher.Invoke(() =>
                {
                    TxtBridgeStatus.Text = online
                        ? "✅ Backend Python connecté — données en direct"
                        : "⚠️ Backend Python hors ligne — lance api_bridge.py pour les données réelles";
                    BridgeStatus.Background = online
                        ? new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromArgb(30, 16, 185, 129))
                        : new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromArgb(30, 245, 158, 11));
                    TxtBridgeStatus.Foreground = online
                        ? new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromRgb(16, 185, 129))
                        : new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromRgb(245, 158, 11));
                });

                // Charger les données en parallèle
                var tipTask   = bridge.GetOracleTipAsync();
                var factTask  = bridge.GetOracleFactAsync();
                var quoteTask = bridge.GetOracleQuoteAsync();
                var timeTask  = bridge.GetOracleTimelineAsync();

                await System.Threading.Tasks.Task.WhenAll(tipTask, factTask, quoteTask, timeTask);

                var (citation, auteur, role) = quoteTask.Result;

                Dispatcher.Invoke(() =>
                {
                    TxtTip.Text         = tipTask.Result;
                    TxtFact.Text        = factTask.Result;
                    TxtQuote.Text       = $"❝ {citation} ❞";
                    TxtQuoteAuthor.Text = string.IsNullOrEmpty(auteur) ? "" : $"— {auteur}, {role}";

                    // Timeline
                    var timeline = timeTask.Result;
                    if (timeline != null)
                    {
                        if (timeline["timeline"] is JArray tl)
                            TimelineList.ItemsSource = tl.ToObject<List<dynamic>>();
                        if (timeline["haiti"] is JArray ht)
                            HaitiList.ItemsSource = ht.ToObject<List<dynamic>>();
                    }
                });
            }
            catch (Exception ex)
            {
                Console.WriteLine($"OraclePage LoadAll error: {ex.Message}");
            }
        }

        private async void BtnNewFact_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                string fact = await PythonBridge.Instance.GetOracleFactAsync();
                TxtFact.Text = fact;
            }
            catch { }
        }

        private async void BtnNewQuote_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var (citation, auteur, role) = await PythonBridge.Instance.GetOracleQuoteAsync();
                TxtQuote.Text       = $"❝ {citation} ❞";
                TxtQuoteAuthor.Text = string.IsNullOrEmpty(auteur) ? "" : $"— {auteur}, {role}";
            }
            catch { }
        }
    }
}
