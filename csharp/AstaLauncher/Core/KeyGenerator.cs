using System;
using System.Security.Cryptography;
using System.Text;

namespace AstaLauncher.Core
{
    public static class KeyGenerator
    {
        private const string SECRET_SALT = "ASTA_UNASMOH_SPACE_DEV_2024";
        private const string SECRET_SALT_HACKING = "ASTA_HACKING_PREMIUM_2024";

        public static string GenerateLicenseKey(string hwid)
        {
            string rawHwid = hwid.Replace("-", "").ToUpper();
            string combined = $"{rawHwid}{SECRET_SALT}_LICENSE";
            return HashAndFormat(combined);
        }

        public static string GenerateHackingKey(string hwid)
        {
            string rawHwid = hwid.Replace("-", "").ToUpper();
            string combined = $"{rawHwid}{SECRET_SALT_HACKING}_HACKING";
            return HashAndFormat(combined);
        }

        private static string HashAndFormat(string input)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(input));
                StringBuilder builder = new StringBuilder();
                for (int i = 0; i < bytes.Length; i++)
                {
                    builder.Append(bytes[i].ToString("X2"));
                }
                string hash = builder.ToString();
                string key = hash.Substring(0, 20);
                return $"{key.Substring(0, 5)}-{key.Substring(5, 5)}-{key.Substring(10, 5)}-{key.Substring(15, 5)}";
            }
        }
    }
}
