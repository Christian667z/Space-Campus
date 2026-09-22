using System;
using System.IO;
using System.Security.Cryptography;
using System.Windows;

namespace AstaAcademieLauncher
{
    public static class VersionVerifier
    {
        public static string ComputeSha256(string path)
        {
            if (!File.Exists(path)) return string.Empty;
            using var fs = File.OpenRead(path);
            using var sha = SHA256.Create();
            var hash = sha.ComputeHash(fs);
            return BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant();
        }

        public static bool IsDifferent(string currentPath, string candidatePath)
        {
            var c = ComputeSha256(currentPath);
            var n = ComputeSha256(candidatePath);
            if (string.IsNullOrEmpty(c) || string.IsNullOrEmpty(n)) return true;
            return !string.Equals(c, n, StringComparison.OrdinalIgnoreCase);
        }

        public static void BackupAndReplace(string destPath, string newPath)
        {
            try
            {
                if (File.Exists(destPath))
                {
                    var bak = destPath + ".bak." + DateTime.UtcNow.ToString("yyyyMMddHHmmss");
                    File.Copy(destPath, bak);
                }
                File.Copy(newPath, destPath, true);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Erreur lors du remplacement : " + ex.Message);
            }
        }
    }
}
