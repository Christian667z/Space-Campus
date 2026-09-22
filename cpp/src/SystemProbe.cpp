#include <windows.h>
#include <pdh.h>
#include <cstring>

#pragma comment(lib, "pdh.lib")

#ifdef _WIN32
#define EXPORT extern "C" __declspec(dllexport)
#else
#define EXPORT extern "C"
#endif

// ──────────────────────────────────────────────
// État interne PDH (CPU via Performance Counter)
// ──────────────────────────────────────────────
static PDH_HQUERY   s_cpuQuery   = NULL;
static PDH_HCOUNTER s_cpuCounter = NULL;
static bool         s_pdhReady   = false;

static void InitPDH()
{
    if (s_pdhReady) return;
    if (PdhOpenQuery(NULL, 0, &s_cpuQuery) == ERROR_SUCCESS)
    {
        PdhAddEnglishCounterW(s_cpuQuery,
            L"\\Processor(_Total)\\% Processor Time", 0, &s_cpuCounter);
        PdhCollectQueryData(s_cpuQuery); // 1er appel pour initialiser les compteurs
        s_pdhReady = true;
    }
}

// ──────────────────────────────────────────────
// API exportée
// ──────────────────────────────────────────────

/// Retourne l'utilisation CPU globale en % (0.0–100.0), ou -1.0 si indisponible.
EXPORT double GetCpuUsage()
{
    InitPDH();
    if (!s_pdhReady) return -1.0;

    PdhCollectQueryData(s_cpuQuery);

    PDH_FMT_COUNTERVALUE val;
    if (PdhGetFormattedCounterValue(s_cpuCounter, PDH_FMT_DOUBLE, NULL, &val) == ERROR_SUCCESS)
        return val.doubleValue;

    return -1.0;
}

/// Remplit *used_mb, *total_mb et *percent_used depuis GlobalMemoryStatusEx.
/// Retourne 1 si succès, 0 si erreur.
EXPORT int GetRamUsage(
    unsigned long long* used_mb,
    unsigned long long* total_mb,
    int*                percent_used)
{
    if (!used_mb || !total_mb || !percent_used) return 0;

    MEMORYSTATUSEX ms;
    ms.dwLength = sizeof(ms);
    if (!GlobalMemoryStatusEx(&ms)) return 0;

    *total_mb    = ms.ullTotalPhys / (1024ULL * 1024ULL);
    *used_mb     = (ms.ullTotalPhys - ms.ullAvailPhys) / (1024ULL * 1024ULL);
    *percent_used = (int)ms.dwMemoryLoad;
    return 1;
}

/// Uptime système en millisecondes (GetTickCount64).
EXPORT unsigned long long GetUptimeMs()
{
    return GetTickCount64();
}

/// Nom du processeur depuis le registre Windows (ANSI).
EXPORT void GetProcessorName(char* output, int max_len)
{
    if (!output || max_len <= 0) return;
    output[0] = '\0';

    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE,
        "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        0, KEY_READ, &hKey) == ERROR_SUCCESS)
    {
        DWORD size = (DWORD)max_len;
        RegQueryValueExA(hKey, "ProcessorNameString", NULL, NULL, (LPBYTE)output, &size);
        RegCloseKey(hKey);
    }
    if (output[0] == '\0')
        strncpy(output, "Unknown Processor", max_len - 1);
}
