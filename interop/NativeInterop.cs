using System;
using System.Runtime.InteropServices;
using System.Text;

namespace AstaInterop
{
    /// <summary>
    /// Ponts P/Invoke pour l'intégration multi-langages (C, C++, Rust)
    /// dans l'écosystème desktop Asta Campus.
    /// </summary>
    public static class NativeInterop
    {
        private const string C_CRYPTO_DLL = "asta_crypto.dll";
        private const string CPP_ENGINE_DLL = "asta_engine.dll";
        private const string RUST_CORE_DLL = "asta_core.dll";
        private const string SYSTEM_PROBE_DLL = "system_probe.dll";

        #region Module C : asta_crypto.dll (C99)

        [DllImport(C_CRYPTO_DLL, CallingConvention = CallingConvention.Cdecl)]
        public static extern void asta_secure_zero(IntPtr ptr, UIntPtr len);

        [DllImport(C_CRYPTO_DLL, CallingConvention = CallingConvention.Cdecl)]
        public static extern uint asta_compute_checksum(byte[] data, UIntPtr len);

        [DllImport(C_CRYPTO_DLL, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int asta_get_machine_fingerprint(StringBuilder outBuffer, UIntPtr maxLen);

        [DllImport(C_CRYPTO_DLL, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int asta_validate_license_format([MarshalAs(UnmanagedType.LPStr)] string licenseKey);

        #endregion

        #region Module C++17 : asta_engine.dll (Indexation Rapide)

        [DllImport(CPP_ENGINE_DLL, CallingConvention = CallingConvention.Cdecl)]
        public static extern IntPtr asta_cpp_create_engine();

        [DllImport(CPP_ENGINE_DLL, CallingConvention = CallingConvention.Cdecl)]
        public static extern void asta_cpp_destroy_engine(IntPtr enginePtr);

        [DllImport(CPP_ENGINE_DLL, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int asta_cpp_index_course(
            IntPtr enginePtr,
            [MarshalAs(UnmanagedType.LPStr)] string id,
            [MarshalAs(UnmanagedType.LPStr)] string title,
            [MarshalAs(UnmanagedType.LPStr)] string subject,
            [MarshalAs(UnmanagedType.LPStr)] string level);

        [DllImport(CPP_ENGINE_DLL, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int asta_cpp_search_count(
            IntPtr enginePtr,
            [MarshalAs(UnmanagedType.LPStr)] string query);

        #endregion

        #region Module Rust : asta_core.dll (C-ABI)

        [DllImport(RUST_CORE_DLL, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int asta_rust_hash_sha256(
            [MarshalAs(UnmanagedType.LPStr)] string input,
            StringBuilder outBuffer,
            int maxLen);

        [DllImport(RUST_CORE_DLL, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int asta_rust_get_hardware_id(
            StringBuilder outBuffer,
            int maxLen);

        #endregion

        #region Helpers managés sécurisés

        /// <summary>
        /// Récupère l'empreinte matérielle native avec repli sécurisé
        /// </summary>
        public static string GetSafeHardwareId()
        {
            try
            {
                var sb = new StringBuilder(128);
                if (asta_get_machine_fingerprint(sb, (UIntPtr)sb.Capacity) == 0)
                {
                    return sb.ToString();
                }
            }
            catch (DllNotFoundException)
            {
                // Fallback managé si la DLL n'est pas encore déployée
            }
            catch (Exception)
            {
                // Fallback générique
            }

            return "ASTA-MANAGED-" + Environment.MachineName.ToUpperInvariant();
        }

        #endregion
    }
}
