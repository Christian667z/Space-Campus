using System;
using System.Diagnostics;
using System.IO;

namespace AstaLauncher.Core
{
    public static class SystemTools
    {
        public static int KillAstaAcademie()
        {
            int killed = 0;
            try
            {
                // Tuer les processus C# et Python associés
                var processes = Process.GetProcesses();
                foreach (var proc in processes)
                {
                    string name = proc.ProcessName.ToLower();
                    if (name.Contains("astaacademie") || (name == "python" && proc.MainWindowTitle.Contains("Asta")))
                    {
                        if (proc.Id != Process.GetCurrentProcess().Id)
                        {
                            proc.Kill();
                            killed++;
                        }
                    }
                }
            }
            catch { }
            return killed;
        }

        public static (string cpu, string ram, string uptime) GetQuickStats()
        {
            try
            {
                using var proc = Process.GetCurrentProcess();
                long memory = proc.WorkingSet64 / (1024 * 1024);
                
                var uptime = DateTime.Now - Process.GetCurrentProcess().StartTime;
                string uptimeStr = $"{(int)uptime.TotalHours}h {uptime.Minutes}m";
                
                return ("~%", $"{memory} MB", uptimeStr);
            }
            catch
            {
                return ("--%", "--%", "--h --m");
            }
        }
    }
}
