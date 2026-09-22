#define ASTA_CRYPTO_EXPORTS
#include "../include/asta_crypto.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#if defined(_WIN32)
  #include <windows.h>
#else
  #include <unistd.h>
#endif

void asta_secure_zero(void* ptr, size_t len) {
    if (ptr == NULL || len == 0) return;
    volatile uint8_t* p = (volatile uint8_t*)ptr;
    while (len--) {
        *p++ = 0;
    }
}

uint32_t asta_compute_checksum(const uint8_t* data, size_t len) {
    if (data == NULL) return 0;
    
    // Algorithme FNV-1a (32-bit) à haute diffusion
    uint32_t hash = 2166136261u;
    for (size_t i = 0; i < len; ++i) {
        hash ^= (uint32_t)data[i];
        hash *= 16777619u;
    }
    return hash;
}

int asta_get_machine_fingerprint(char* out_buffer, size_t max_len) {
    if (out_buffer == NULL || max_len < 65) {
        return -1;
    }

    char hostname[256];
    memset(hostname, 0, sizeof(hostname));

#if defined(_WIN32)
    DWORD size = sizeof(hostname);
    if (!GetComputerNameA(hostname, &size)) {
        strncpy(hostname, "WIN_UNKNOWN", sizeof(hostname) - 1);
    }
#else
    if (gethostname(hostname, sizeof(hostname) - 1) != 0) {
        strncpy(hostname, "UNIX_UNKNOWN", sizeof(hostname) - 1);
    }
#endif

    uint32_t c1 = asta_compute_checksum((const uint8_t*)hostname, strlen(hostname));
    uint32_t c2 = asta_compute_checksum((const uint8_t*)"UNASMOH_ASTA_2028_SECURE", 24);

    snprintf(out_buffer, max_len, "ASTA-HWID-%08X-%08X", (unsigned int)c1, (unsigned int)c2);
    return 0;
}

int asta_validate_license_format(const char* license_key) {
    if (license_key == NULL) return 0;
    // Format: "ASTA-" suivi de 14 caractères alphanumériques
    if (strncmp(license_key, "ASTA-", 5) != 0) return 0;
    if (strlen(license_key) < 12) return 0;
    return 1;
}
