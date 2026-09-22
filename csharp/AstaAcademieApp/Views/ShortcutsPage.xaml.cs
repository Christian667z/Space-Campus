using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using AstaAcademieApp.Core;
using Newtonsoft.Json.Linq;

namespace AstaAcademieApp.Views
{
    public partial class ShortcutsPage : Page
    {
        public ShortcutsPage()
        {
            try { InitializeComponent(); }
            catch (Exception ex) { Console.WriteLine($"ShortcutsPage init: {ex.Message}"); return; }
            Loaded += async (_, _) => await LoadAllAsync();
        }

        private async System.Threading.Tasks.Task LoadAllAsync()
        {
            try
            {
                var bridge = PythonBridge.Instance;
                bool online = await bridge.IsOnlineAsync();

                Dispatcher.Invoke(() =>
                {
                    TxtStatus.Text = online
                        ? "✅ Données Python en direct"
                        : "⚠️ Backend hors ligne — lance api_bridge.py";
                    TxtStatus.Foreground = online
                        ? new SolidColorBrush(Color.FromRgb(16, 185, 129))
                        : new SolidColorBrush(Color.FromRgb(245, 158, 11));
                });

                if (!online) return;

                var excelTask   = bridge.GetShortcutsExcelAsync();
                var trapsTask   = bridge.GetShortcutsTrapsAsync();
                var linuxTask   = bridge.GetShortcutsLinuxAsync();
                var osiTask     = bridge.GetShortcutsOsiAsync();
                var protosTask  = bridge.GetShortcutsProtocolsAsync();

                await System.Threading.Tasks.Task.WhenAll(excelTask, trapsTask, linuxTask, osiTask, protosTask);

                Dispatcher.Invoke(() =>
                {
                    Bind(ExcelShortcutsList, excelTask.Result, "shortcuts");
                    Bind(ExcelFormulasList,  excelTask.Result, "formulas");
                    Bind(TrapsList,          trapsTask.Result, "traps");
                    Bind(LinuxList,          linuxTask.Result, "commands");
                    Bind(OsiList,            osiTask.Result,   "layers");
                    Bind(ProtocolsList,      protosTask.Result,"protocols");
                });
            }
            catch (Exception ex) { Console.WriteLine($"ShortcutsPage error: {ex.Message}"); }
        }

        private static void Bind(ItemsControl ctrl, JObject? data, string key)
        {
            if (data?[key] is JArray arr)
                ctrl.ItemsSource = arr.ToObject<List<dynamic>>();
        }
    }
}
