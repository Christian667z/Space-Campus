using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using AstaAcademieApp.Core;

namespace AstaAcademieApp.Views
{
    public partial class TerminalPage : Page
    {
        // ── Couleurs ──────────────────────────────────────────────────────────
        private static readonly SolidColorBrush ClrPrompt  = new(Color.FromRgb(0, 255, 255));
        private static readonly SolidColorBrush ClrOutput  = new(Color.FromRgb(0, 255, 65));
        private static readonly SolidColorBrush ClrError   = new(Color.FromRgb(239, 68, 68));
        private static readonly SolidColorBrush ClrInfo    = new(Color.FromRgb(112, 153, 192));
        private static readonly SolidColorBrush ClrSuccess = new(Color.FromRgb(16, 185, 129));
        private static readonly SolidColorBrush ClrWarning = new(Color.FromRgb(245, 158, 11));

        // ── Historique ────────────────────────────────────────────────────────
        private readonly List<string>   _history      = new();
        private          int            _historyIndex = -1;

        private readonly CommandExecutor _executor = new();
        private readonly DispatcherTimer _clockTimer = null!;

        public TerminalPage()
        {
            try
            {
                InitializeComponent();

                PromptLabel.Text = $"{Environment.UserName}@{Environment.MachineName}:~$ ";

                UpdateNativeIndicator();

                _clockTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
                _clockTimer.Tick += (_, _) =>
                {
                    TxtClock.Text = DateTime.Now.ToString("HH:mm:ss");
                    _ = UpdateUptimeSafe();
                };
                _clockTimer.Start();

                PrintBanner();

                Loaded   += (_, _) => CommandInput.Focus();
                Unloaded += (_, _) => _clockTimer.Stop();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"TerminalPage init error: {ex}");
            }
        }

        // ── Banner ────────────────────────────────────────────────────────────
        private void PrintBanner()
        {
            AppendLine("  ╔═══════════════════════════════════════════════╗", ClrSuccess);
            AppendLine("  ║        ASTA ACADÉMIE — TERMINAL v2.0           ║", ClrSuccess);
            AppendLine("  ║       Powered by C# WPF + C++ Native           ║", ClrSuccess);
            AppendLine("  ╚═══════════════════════════════════════════════╝", ClrSuccess);
            AppendLine("", ClrOutput);

            bool sec = SecurityService.Instance.IsNativeAvailable;
            AppendLine(sec
                ? "  [✓] Sécurité : AES-256-GCM C++ natif activé"
                : "  [!] Sécurité : Mode fallback C# (DLL absente)",
                sec ? ClrSuccess : ClrWarning);

            bool met = SystemMetricsService.Instance.IsNativeAvailable;
            AppendLine(met
                ? "  [✓] Métriques : CPU/RAM réels via C++ (PDH/Win32)"
                : "  [!] Métriques : Mode simulé (system_probe.dll absente)",
                met ? ClrSuccess : ClrWarning);

            AppendLine("", ClrOutput);
            AppendLine("  Tapez 'help' pour voir les commandes.  ↑/↓ = historique  Ctrl+L = clear", ClrInfo);
            AppendLine("", ClrOutput);
        }

        // ── Saisie ────────────────────────────────────────────────────────────
        private async void CommandInput_KeyDown(object sender, KeyEventArgs e)
        {
            try
            {
                switch (e.Key)
                {
                    case Key.Enter:
                    {
                        string input = CommandInput.Text.Trim();
                        CommandInput.Text = string.Empty;
                        _historyIndex = -1;

                        if (string.IsNullOrWhiteSpace(input)) { AppendLine("", ClrOutput); return; }

                        if (_history.Count == 0 || _history[0] != input)
                            _history.Insert(0, input);

                        AppendLine($"{PromptLabel.Text}{input}", ClrPrompt);

                        var cmd = CommandParser.Parse(input);
                        if (!cmd.IsValid) return;

                        if (cmd.Name == "history")
                        {
                            AppendLine("  Historique :", ClrInfo);
                            for (int i = 0; i < _history.Count; i++)
                                AppendLine($"  [{i + 1}] {_history[i]}", ClrOutput);
                            AppendLine("", ClrOutput);
                            return;
                        }

                        if (cmd.Name == "clear") { ClearTerminal(); return; }

                        CommandInput.IsEnabled = false;
                        TxtStatus.Text = $"Exécution : {cmd.Name}…";

                        string result = "";
                        try
                        {
                            result = await _executor.ExecuteAsync(cmd);
                        }
                        catch (Exception ex)
                        {
                            AppendLine($"  Erreur : {ex.Message}", ClrError);
                        }
                        finally
                        {
                            TxtStatus.Text = "Prêt.";
                            CommandInput.IsEnabled = true;
                            CommandInput.Focus();
                        }

                        if (!string.IsNullOrEmpty(result))
                            AppendMultiLine(result, ClrOutput);
                        break;
                    }

                    case Key.Up:
                        if (_history.Count == 0) break;
                        _historyIndex = Math.Min(_historyIndex + 1, _history.Count - 1);
                        CommandInput.Text = _history[_historyIndex];
                        CommandInput.CaretIndex = CommandInput.Text.Length;
                        e.Handled = true;
                        break;

                    case Key.Down:
                        _historyIndex = Math.Max(_historyIndex - 1, -1);
                        CommandInput.Text = _historyIndex >= 0 ? _history[_historyIndex] : "";
                        CommandInput.CaretIndex = CommandInput.Text.Length;
                        e.Handled = true;
                        break;

                    case Key.L when (Keyboard.Modifiers & ModifierKeys.Control) != 0:
                        ClearTerminal();
                        e.Handled = true;
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"TerminalPage KeyDown error: {ex.Message}");
            }
        }

        // ── Helpers affichage ─────────────────────────────────────────────────
        private void ClearTerminal()
        {
            TerminalOutput.Document.Blocks.Clear();
            AppendLine("  Terminal effacé.", ClrInfo);
            AppendLine("", ClrOutput);
        }

        private void AppendLine(string text, SolidColorBrush color)
        {
            try
            {
                var para = new Paragraph(new Run(text))
                {
                    Margin     = new Thickness(0),
                    LineHeight = 18,
                    Foreground = color,
                    FontFamily = new FontFamily("Consolas"),
                    FontSize   = 13
                };
                TerminalOutput.Document.Blocks.Add(para);
                TerminalOutput.ScrollToEnd();
            }
            catch { /* silent */ }
        }

        private void AppendMultiLine(string text, SolidColorBrush color)
        {
            if (string.IsNullOrEmpty(text)) return;
            foreach (string line in text.Split('\n'))
                AppendLine(line.TrimEnd('\r'), color);
            AppendLine("", color);
        }

        private async System.Threading.Tasks.Task UpdateUptimeSafe()
        {
            try
            {
                ulong ms = await SystemMetricsService.Instance.GetUptimeMsAsync();
                Dispatcher.Invoke(() => TxtUptime.Text = $"Uptime: {SystemMetricsService.FormatUptime(ms)}");
            }
            catch { /* silent */ }
        }

        private void UpdateNativeIndicator()
        {
            try
            {
                bool ok = SecurityService.Instance.IsNativeAvailable
                       || SystemMetricsService.Instance.IsNativeAvailable;

                if (ok)
                {
                    NativeLabel.Text       = "● C++ NATIF";
                    NativeLabel.Foreground = ClrSuccess;
                    NativeIndicator.Background = new SolidColorBrush(Color.FromArgb(30, 16, 185, 129));
                }
                else
                {
                    NativeLabel.Text       = "● FALLBACK C#";
                    NativeLabel.Foreground = ClrWarning;
                    NativeIndicator.Background = new SolidColorBrush(Color.FromArgb(30, 245, 158, 11));
                }
            }
            catch (Exception ex) { Console.WriteLine($"NativeIndicator error: {ex.Message}"); }
        }
    }
}
