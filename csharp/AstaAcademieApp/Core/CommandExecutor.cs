using System;
using System.IO;
using System.Linq;
using System.Net.NetworkInformation;
using System.Security.Principal;
using System.Threading.Tasks;

namespace AstaAcademieApp.Core
{
    /// <summary>
    /// Exécute les commandes parsées de manière asynchrone.
    /// Utilise SystemMetricsService (C++ natif) et SecurityService (AES-256-GCM).
    /// </summary>
    public class CommandExecutor
    {
        public async Task<string> ExecuteAsync(CommandResult cmd)
        {
            return cmd.Name switch
            {
                "help"     => GetHelp(),
                "user"     => GetUserInfo(),
                "whoami"   => GetUserInfo(),
                "system"   => await GetSystemInfoAsync(),
                "neofetch" => await GetNeofetchAsync(),
                "encode"   => EncodeText(cmd.Arguments),
                "decode"   => DecodeText(cmd.Arguments),
                "ping"     => await PingHostAsync(cmd.Arguments),
                "history"  => "[HISTORY]",   // signal géré par l'UI
                "clear"    => string.Empty,  // signal géré par l'UI
                _          => $"  '{cmd.Name}' : commande introuvable. Tapez 'help'."
            };
        }

        // ── help ──────────────────────────────────────────────────────────────
        private static string GetHelp() => """
╔══════════════════════════════════════════════════════════╗
║          TERMINAL ASTA v2.0 — COMMANDES                  ║
╠══════════════════════════════════════════════════════════╣
║  help              Affiche cette aide                    ║
║  user  / whoami    Infos session Windows                 ║
║  system            Diagnostic complet (CPU/RAM réels)    ║
║  neofetch          Banner système style hacker           ║
║  encode  <texte>   Chiffre en AES-256-GCM (Base64)       ║
║  decode  <base64>  Déchiffre en AES-256-GCM              ║
║  ping    <host>    Ping réseau (ex: ping 8.8.8.8)        ║
║  history           Affiche l'historique des commandes    ║
║  clear             Efface le terminal                    ║
╚══════════════════════════════════════════════════════════╝
""";

        // ── user / whoami ─────────────────────────────────────────────────────
        private static string GetUserInfo()
        {
            string user    = Environment.UserName;
            string machine = Environment.MachineName;
            string domain  = Environment.UserDomainName;
            bool   isAdmin = IsAdministrator();
            string os      = Environment.OSVersion.VersionString;
            int    proc    = Environment.ProcessorCount;

            return $"""
┌──────────────── User / WhoAmI ──────────────────┐
  Utilisateur  : {user}
  Domaine      : {domain}
  Machine      : {machine}
  OS           : {os}
  Processeurs  : {proc} cœur(s) logique(s)
  Admin        : {(isAdmin ? "OUI ✓  (privilèges élevés)" : "NON")}
  Home         : {Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)}
└─────────────────────────────────────────────────┘
""";
        }

        private static bool IsAdministrator()
        {
            using var identity  = System.Security.Principal.WindowsIdentity.GetCurrent();
            var       principal = new WindowsPrincipal(identity);
            return principal.IsInRole(WindowsBuiltInRole.Administrator);
        }

        // ── system ────────────────────────────────────────────────────────────
        private static async Task<string> GetSystemInfoAsync()
        {
            var svc = SystemMetricsService.Instance;

            double cpu            = await svc.GetCpuPercentAsync();
            var    (used, tot, p) = await svc.GetRamInfoAsync();
            ulong  upMs           = await svc.GetUptimeMsAsync();
            string cpuName        = await svc.GetProcessorNameAsync();

            string cpuBar = SystemMetricsService.MakeBar((int)cpu);
            string ramBar = SystemMetricsService.MakeBar(p);
            string disk   = GetDiskInfo();
            string src    = svc.IsNativeAvailable ? "C++ natif ✓" : "Simulé (DLL absente)";

            return $"""
┌──────────────── System Diagnostic ──────────────┐
  Source       : {src}
  OS           : {Environment.OSVersion}
  CPU          : {cpuName}
  CPU Load     : [{cpuBar}] {cpu:F1}%
  RAM          : [{ramBar}] {used} Mo / {tot} Mo ({p}%)
  Uptime       : {SystemMetricsService.FormatUptime(upMs)}
{disk}
└─────────────────────────────────────────────────┘
""";
        }

        private static string GetDiskInfo()
        {
            try
            {
                var drive = DriveInfo.GetDrives()
                    .FirstOrDefault(d => d.IsReady &&
                        d.Name == Path.GetPathRoot(Environment.SystemDirectory));
                if (drive is null) return "  Disque : Non disponible";

                double total  = drive.TotalSize        / 1_073_741_824.0;
                double free   = drive.AvailableFreeSpace / 1_073_741_824.0;
                double used   = total - free;
                int    pct    = (int)(used / total * 100);
                string bar    = SystemMetricsService.MakeBar(pct);
                return $"  Disque {drive.Name,-4}: [{bar}] {used:F1} Go / {total:F1} Go ({pct}%)";
            }
            catch { return "  Disque : Erreur de lecture"; }
        }

        // ── neofetch ──────────────────────────────────────────────────────────
        private static async Task<string> GetNeofetchAsync()
        {
            var svc = SystemMetricsService.Instance;
            string cpuName        = await svc.GetProcessorNameAsync();
            var    (used, tot, p) = await svc.GetRamInfoAsync();
            double cpu            = await svc.GetCpuPercentAsync();
            ulong  upMs           = await svc.GetUptimeMsAsync();

            string user    = Environment.UserName;
            string machine = Environment.MachineName;
            bool   isAdmin = IsAdministrator();

            return $"""
                                         ,,
          ,-``-.               {user}@{machine}
         /  ,-. \   ╔══════════════════════════════╗
        |  (   ) |  ║  OS     : {Environment.OSVersion.Platform}          
        |   `-'  |  ║  Host   : {machine}
         \  ___.'   ║  Shell  : AstaTerm v2.0
          `-----'   ║  CPU    : {cpuName.Trim()[..Math.Min(28, cpuName.Trim().Length)]}
                    ║  CPU%   : {cpu:F1}%
    ASTA ACADÉMIE   ║  RAM    : {used} Mo / {tot} Mo ({p}%)
    ─────────────   ║  Uptime : {SystemMetricsService.FormatUptime(upMs)}
    v2.0.0 | CSharp ║  Admin  : {(isAdmin ? "Oui ✓" : "Non")}
                    ╚══════════════════════════════╝
  ████ ████ ████ ████ ████ ████ ████ ████
""";
        }

        // ── encode / decode ───────────────────────────────────────────────────
        private static string EncodeText(System.Collections.Generic.IReadOnlyList<string> args)
        {
            if (args.Count == 0)
                return "  Usage : encode <texte à chiffrer>";

            string plain    = string.Join(" ", args);
            string cipher   = SecurityService.Instance.EncryptBase64(plain);
            string mode     = SecurityService.Instance.IsNativeAvailable
                              ? "AES-256-GCM (C++ natif)" : "XOR/Base64 (fallback C#)";
            return $"""
┌──────────────── Encode ─────────────────────────┐
  Mode    : {mode}
  Entrée  : {plain}
  Sortie  : {cipher}
└─────────────────────────────────────────────────┘
""";
        }

        private static string DecodeText(System.Collections.Generic.IReadOnlyList<string> args)
        {
            if (args.Count == 0)
                return "  Usage : decode <base64 chiffré>";

            string cipher  = string.Join("", args);
            string plain   = SecurityService.Instance.DecryptBase64(cipher);
            return $"""
┌──────────────── Decode ─────────────────────────┐
  Entrée  : {cipher[..Math.Min(40, cipher.Length)]}...
  Sortie  : {plain}
└─────────────────────────────────────────────────┘
""";
        }

        // ── ping ──────────────────────────────────────────────────────────────
        private static async Task<string> PingHostAsync(
            System.Collections.Generic.IReadOnlyList<string> args)
        {
            string host = args.Count > 0 ? args[0] : "8.8.8.8";
            var sb = new System.Text.StringBuilder();
            sb.AppendLine($"  PING {host} :");

            using var ping = new Ping();
            for (int i = 1; i <= 4; i++)
            {
                try
                {
                    var reply = await ping.SendPingAsync(host, 2000);
                    string status = reply.Status == IPStatus.Success
                        ? $"✓  {reply.RoundtripTime} ms  ttl={reply.Options?.Ttl}"
                        : $"✗  {reply.Status}";
                    sb.AppendLine($"    [{i}] {status}");
                }
                catch (Exception ex)
                {
                    sb.AppendLine($"    [{i}] Erreur : {ex.Message}");
                }
                await Task.Delay(250);
            }
            return sb.ToString();
        }
    }
}