#ifndef ASTA_CRYPTO_H
#define ASTA_CRYPTO_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#if defined(_WIN32) || defined(__CYGWIN__)
  #ifdef ASTA_CRYPTO_EXPORTS
    #define ASTA_API __declspec(dllexport)
  #else
    #define ASTA_API __declspec(dllimport)
  #endif
#else
  #if __GNUC__ >= 4
    #define ASTA_API __attribute__((visibility("default")))
  #else
    #define ASTA_API
  #endif
#endif

/**
 * Nettoie de manière sécurisée une zone mémoire contenant des clés ou mots de passe
 * afin d'éviter qu'ils ne persistent dans les dumps mémoire ou le swap.
 */
ASTA_API void asta_secure_zero(void* ptr, size_t len);

/**
 * Calcule une empreinte de contrôle (checksum 32-bit polynomiale)
 * pour valider l'intégrité d'une licence ou d'un fichier de cours hors-ligne.
 */
ASTA_API uint32_t asta_compute_checksum(const uint8_t* data, size_t len);

/**
 * Dérive une clé d'empreinte matérielle (Hardware Machine ID)
 * sous forme de chaîne hexadécimale terminée par null (au moins 65 octets requis).
 * 
 * @param out_buffer Buffer de sortie fourni par l'appelant
 * @param max_len Taille maximale du buffer
 * @return 0 en cas de succès, code d'erreur négatif sinon.
 */
ASTA_API int asta_get_machine_fingerprint(char* out_buffer, size_t max_len);

/**
 * Valide si une clé de licence correspond au format Asta Académie (ASTA-PROMO-XXXX-XXXX)
 */
ASTA_API int asta_validate_license_format(const char* license_key);

#ifdef __cplusplus
}
#endif

#endif /* ASTA_CRYPTO_H */
