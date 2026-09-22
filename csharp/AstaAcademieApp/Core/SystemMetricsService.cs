using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace AstaAcademieApp.Core
{
    /// <summary>
    /// Service singleton de métriques système.
    /// Appelle system_probe.dll (C++) via P/Invoke pour obtenir CPU, RAM et uptime réels.
    /// Fallback automatique vers données simulées si la DLL est absente.
    /// </summary>
    public sealed class SystemMetricsService
    {
        // ── Singleton ─────────────────────────────────────────────────────────
        private static readonly Lazy<SystemMetricsService> _instance =
            new Lazy<SystemMetricsService>(() => new SystemMetricsService());
        public static SystemMetricsService Instance => _instance.Value;

        /// <summary>True si la DLL C++ native est disponible.</summary>
        public bool IsNativeAvailable { get; private set; }

        // ── P/Invoke ──────────────────────────────────────────────────────────
        private const string Dll = "system_probe.dll";

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern double GetCpuUsage();

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern int GetRamUsage(
            out ulong used_mb, out ulong total_mb, out int percent_used);

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern ulong GetUptimeMs();

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern void GetProcessorName(
            [MarshalAs(UnmanagedType.LPStr)] StringBuilder output, int max_len);

        // ── Init ──────────────────────────────────────────────────────────────
        private SystemMetricsService()
        {
            try   { IsNativeAvailable = GetCpuUsage() >= 0; }
            catch { IsNativeAvailable = false; }
        }

        // ── API publique (async) ──────────────────────────────────────────────

        /// <summary>Retourne l'utilisation CPU en %.</summary>
        public async Task<double> GetCpuPercentAsync() => await Task.Run(() =>
        {
            if (IsNativeAvailable)
            {
                try
                {
                    double v = GetCpuUsage();
                    if (v >= 0) return v;
                }
                catch { }
            }
            // Fallback simulé
            return Random.Shared.Next(5, 40) + Random.Shared.NextDouble();
        });

        /// <summary>Retourne (UsedMB, TotalMB, Percent).</summary>
        public async Task<(ulong UsedMB, ulong TotalMB, int Percent)> GetRamInfoAsync() =>
            await Task.Run(() =>
        {
            if (IsNativeAvailable)
            {
                try
                {
                    int ok = GetRamUsage(out ulong used, out ulong total, out int pct);
                    if (ok != 0) return (used, total, pct);
                }
                catch { }
            }
            // Fallback simulé
            ulong tot = 16384UL;
            int   p   = Random.Shared.Next(40, 70);
            return (tot * (ulong)p / 100, tot, p);
        });

        /// <summary>Retourne l'uptime système en millisecondes.</summary>
        public async Task<ulong> GetUptimeMsAsync() => await Task.Run(() =>
        {
            if (IsNativeAvailable)
            {
                try { return GetUptimeMs(); } catch { }
            }
            return (ulong)Environment.TickCount64;
        });

        /// <summary>Retourne le nom du processeur.</summary>
        public async Task<string> GetProcessorNameAsync() => await Task.Run(() =>
        {
            if (IsNativeAvailable)
            {
                try
                {
                    var sb = new StringBuilder(256);
                    GetProcessorName(sb, 256);
                    string name = sb.ToString().Trim();
                    if (!string.IsNullOrEmpty(name)) return name;
                }
                catch { }
            }
            return "Processor (DLL non disponible)";
        });

        // ── Formatage ─────────────────────────────────────────────────────────

        /// <summary>Formate une durée en ms en "HHh MMm SSs".</summary>
        public static string FormatUptime(ulong ms)
        {
            var ts = TimeSpan.FromMilliseconds(ms);
            return $"{(int)ts.TotalHours:D2}h {ts.Minutes:D2}m {ts.Seconds:D2}s";
        }

        /// <summary>Génère une barre ASCII de progression.</summary>
        public static string MakeBar(int percent, int width = 20)
        {
            int filled = Math.Clamp(percent * width / 100, 0, width);
            return new string('█', filled) + new string('░', width - filled);
        }
    }
}
