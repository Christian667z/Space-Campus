using System;
using System.Runtime.InteropServices;
using System.Text;

namespace AstaAcademieApp.Core
{
    /// <summary>
    /// Service singleton de sécurité.
    /// Utilise AES-256-GCM natif (native_security.dll via P/Invoke).
    /// Fallback automatique vers XOR + Base64 si la DLL est absente.
    /// </summary>
    public sealed class SecurityService
    {
        // ── Singleton ─────────────────────────────────────────────────────────
        private static readonly Lazy<SecurityService> _instance =
            new Lazy<SecurityService>(() => new SecurityService());
        public static SecurityService Instance => _instance.Value;

        /// <summary>True si la DLL C++ native est chargée et opérationnelle.</summary>
        public bool IsNativeAvailable { get; private set; }

        // ── Clé AES-256 (32 bytes) dérivée de l'identité machine ─────────────
        private static readonly byte[] _key;

        // ── P/Invoke ──────────────────────────────────────────────────────────
        private const string Dll = "native_security.dll";

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern int GetLibraryVersion();

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern int AesGcmEncrypt(
            byte[] plaintext, int ptLen,
            byte[] key,       int keyLen,
            byte[] output,    int outMax);

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern int AesGcmDecrypt(
            byte[] input,  int inLen,
            byte[] key,    int keyLen,
            byte[] output, int outMax);

        // ── Constructeur statique : dérivation de la clé ─────────────────────
        static SecurityService()
        {
            string seed = $"{Environment.MachineName}-{Environment.UserName}-AstaSecure2025";
            byte[] raw  = Encoding.UTF8.GetBytes(seed);
            _key = new byte[32];
            for (int i = 0; i < 32; i++)
                _key[i] = raw[i % raw.Length];
        }

        private SecurityService()
        {
            try   { IsNativeAvailable = GetLibraryVersion() >= 2; }
            catch { IsNativeAvailable = false; }
        }

        // ── API publique ──────────────────────────────────────────────────────

        /// <summary>Chiffre un texte et retourne un string Base64 URL-safe.</summary>
        public string EncryptBase64(string plaintext)
        {
            byte[] data = Encoding.UTF8.GetBytes(plaintext);

            if (IsNativeAvailable)
            {
                try
                {
                    byte[] buf = new byte[data.Length + 64];
                    int    len = AesGcmEncrypt(data, data.Length, _key, 32, buf, buf.Length);
                    if (len > 0)
                    {
                        byte[] result = new byte[len];
                        Array.Copy(buf, result, len);
                        return Convert.ToBase64String(result);
                    }
                }
                catch { /* fall through */ }
            }

            return FallbackXorB64(data);
        }

        /// <summary>Déchiffre un string Base64 et retourne le texte clair.</summary>
        public string DecryptBase64(string cipherBase64)
        {
            try
            {
                byte[] data = Convert.FromBase64String(cipherBase64);

                if (IsNativeAvailable && data.Length >= 28)
                {
                    try
                    {
                        byte[] buf = new byte[data.Length];
                        int    len = AesGcmDecrypt(data, data.Length, _key, 32, buf, buf.Length);
                        if (len > 0)
                            return Encoding.UTF8.GetString(buf, 0, len);
                    }
                    catch { /* fall through */ }
                }

                // Fallback XOR
                return Encoding.UTF8.GetString(XorBytes(data));
            }
            catch
            {
                return "[Erreur de déchiffrement]";
            }
        }

        // ── Helpers privés ────────────────────────────────────────────────────

        private static string FallbackXorB64(byte[] data) =>
            Convert.ToBase64String(XorBytes(data));

        private static byte[] XorBytes(byte[] data)
        {
            byte[] r = new byte[data.Length];
            for (int i = 0; i < data.Length; i++)
                r[i] = (byte)(data[i] ^ _key[i % 32]);
            return r;
        }
    }
}
