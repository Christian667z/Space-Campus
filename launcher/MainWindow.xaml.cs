using System;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Timers;
using System.Windows;
using System.Windows.Threading;

namespace AstaLauncher
{
    public partial class MainWindow : Window
    {
        private Process _backendProcess;
        private DispatcherTimer _metricsTimer;
        private PerformanceCounterHelper _perfHelper;

        public MainWindow()
        {
            InitializeComponent();
            TryStartBackend();
            SetupMetrics();
        }

        private void TryStartBackend()
        {
            try
            {
                var pythonExe = GetPythonPath();
                var backendScript = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "server.py");

                // If we have an embedded or distributed server in build_asta, prefer it
                var buildAstaDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", "dist", "build_asta");
                var shippedServer = Path.Combine(buildAstaDir, "server.py");
                if (File.Exists(shippedServer))
                {
                    // copy to a secure temp location before execution
                    var tempDir = Path.Combine(Path.GetTempPath(), "asta_backend");
                    Directory.CreateDirectory(tempDir);
                    var target = Path.Combine(tempDir, "server.py");
                    File.Copy(shippedServer, target, true);
                    backendScript = target;
                }

                if (!File.Exists(pythonExe) || !File.Exists(backendScript))
                {
                    // Logged elsewhere in the real app
                    return;
                }

                var psi = new ProcessStartInfo
                {
                    FileName = pythonExe,
                    Arguments = $"\"{backendScript}\"",
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    WorkingDirectory = AppDomain.CurrentDomain.BaseDirectory
                };

                _backendProcess = new Process { StartInfo = psi, EnableRaisingEvents = true };
                _backendProcess.Exited += BackendExited;
                _backendProcess.OutputDataReceived += (s, e) => {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        // Append to audit log in UI thread
                        Dispatcher.Invoke(() => AppendAuditLine(e.Data));
                    }
                };
                _backendProcess.ErrorDataReceived += (s, e) => {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        Dispatcher.Invoke(() => AppendAuditLine("ERR: " + e.Data));
                    }
                };

                _backendProcess.Start();
                _backendProcess.BeginOutputReadLine();
                _backendProcess.BeginErrorReadLine();
            }
            catch (Exception ex)
            {
                // log
            }
        }

        private void BackendExited(object sender, EventArgs e)
        {
            Dispatcher.Invoke(() => AppendAuditLine("Backend process exited."));
        }

        private string GetPythonPath()
        {
            // Cherche un python local puis Visual Studio bundled python
            var local = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "venv", "Scripts", "python.exe");
            if (File.Exists(local)) return local;

            var vs = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Microsoft Visual Studio", "Shared", "Python39_64", "python.exe");
            if (File.Exists(vs)) return vs;

            // Fallback: rely on PATH
            return "python.exe";
        }

        protected override void OnClosed(EventArgs e)
        {
            base.OnClosed(e);
            try
            {
                if (_backendProcess != null && !_backendProcess.HasExited)
                {
                    _backendProcess.Kill(true);
                    _backendProcess.WaitForExit(2000);
                }
            }
            catch { }
        }

        private void SetupMetrics()
        {
            _perfHelper = new PerformanceCounterHelper();
            _metricsTimer = new DispatcherTimer();
            _metricsTimer.Interval = TimeSpan.FromSeconds(1);
            _metricsTimer.Tick += (s, e) => {
                try
                {
                    var cpu = _perfHelper.GetCpuUsage();
                    var mem = _perfHelper.GetAvailableMemoryMB();
                    CpuLabel.Content = $"CPU: {cpu:0.0}%";
                    RamLabel.Content = $"RAM libre: {mem:0} MB";
                }
                catch { }
            };
            _metricsTimer.Start();
        }

        private void AppendAuditLine(string line)
        {
            try
            {
                AuditTextBox.AppendText($"[{DateTime.Now:HH:mm:ss}] {line}\n");
                AuditTextBox.ScrollToEnd();
            }
            catch { }
        }

        // AES decryption simple pour localdb.dat
        private byte[] LoadAndDecryptLocalDb(string path, byte[] key, byte[] iv)
        {
            if (!File.Exists(path)) return null;
            try
            {
                var cipher = File.ReadAllBytes(path);
                using (var aes = Aes.Create())
                {
                    aes.Key = key;
                    aes.IV = iv;
                    aes.Mode = CipherMode.CBC;
                    aes.Padding = PaddingMode.PKCS7;
                    using (var ms = new MemoryStream())
                    using (var cs = new CryptoStream(ms, aes.CreateDecryptor(), CryptoStreamMode.Write))
                    {
                        cs.Write(cipher, 0, cipher.Length);
                        cs.FlushFinalBlock();
                        return ms.ToArray();
                    }
                }
            }
            catch
            {
                return null;
            }
        }
    }

    // Helper simple pour métriques (impl. minimale)
    public class PerformanceCounterHelper
    {
        private PerformanceCounter _cpuCounter;
        private PerformanceCounter _memCounter;

        public PerformanceCounterHelper()
        {
            try
            {
                _cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                _cpuCounter.NextValue();
            }
            catch { }
        }

        public float GetCpuUsage()
        {
            try
            {
                return _cpuCounter?.NextValue() ?? 0f;
            }
            catch { return 0f; }
        }

        public float GetAvailableMemoryMB()
        {
            try
            {
                var available = new Microsoft.VisualBasic.Devices.ComputerInfo().AvailablePhysicalMemory;
                return (float)(available / (1024 * 1024));
            }
            catch { return 0f; }
        }
    }
}
