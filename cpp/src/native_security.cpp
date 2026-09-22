#include <windows.h>
#include <bcrypt.h>
#include <vector>
#include <cstring>

#pragma comment(lib, "bcrypt.lib")

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

#ifdef _WIN32
#define EXPORT extern "C" __declspec(dllexport)
#else
#define EXPORT extern "C"
#endif

/// Version de la bibliothèque native (v2 = AES-256-GCM réel)
EXPORT int GetLibraryVersion() { return 2; }

/// Chiffre avec AES-256-GCM (Windows CNG).
/// Sortie : nonce(12) + tag(16) + ciphertext
/// Retourne le nombre total d'octets écrits, ou -1 si erreur.
EXPORT int AesGcmEncrypt(
    const unsigned char* plaintext, int plaintext_len,
    const unsigned char* key,       int key_len,
    unsigned char*       output,    int output_max_len)
{
    if (!plaintext || !key || !output || key_len < 32) return -1;
    if (output_max_len < plaintext_len + 28) return -1;

    BCRYPT_ALG_HANDLE hAlg = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;
    int result = -1;

    if (!NT_SUCCESS(BCryptOpenAlgorithmProvider(&hAlg, BCRYPT_AES_ALGORITHM, NULL, 0)))
        return -1;

    if (!NT_SUCCESS(BCryptSetProperty(hAlg, BCRYPT_CHAINING_MODE,
        (PUCHAR)BCRYPT_CHAIN_MODE_GCM, sizeof(BCRYPT_CHAIN_MODE_GCM), 0)))
    { BCryptCloseAlgorithmProvider(hAlg, 0); return -1; }

    if (!NT_SUCCESS(BCryptGenerateSymmetricKey(hAlg, &hKey, NULL, 0, (PUCHAR)key, 32, 0)))
    { BCryptCloseAlgorithmProvider(hAlg, 0); return -1; }

    // Nonce aléatoire 12 bytes via CNG
    unsigned char nonce[12];
    BCryptGenRandom(NULL, nonce, 12, BCRYPT_USE_SYSTEM_PREFERRED_RNG);

    unsigned char tag[16] = {0};
    BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO authInfo;
    BCRYPT_INIT_AUTH_MODE_INFO(authInfo);
    authInfo.pbNonce = nonce;
    authInfo.cbNonce = 12;
    authInfo.pbTag   = tag;
    authInfo.cbTag   = 16;

    std::vector<unsigned char> cipherBuf(plaintext_len + 32);
    DWORD cbOut = 0;
    NTSTATUS st = BCryptEncrypt(
        hKey, (PUCHAR)plaintext, plaintext_len, &authInfo,
        NULL, 0, cipherBuf.data(), (ULONG)cipherBuf.size(), &cbOut, 0);

    if (NT_SUCCESS(st)) {
        memcpy(output,      nonce,           12);
        memcpy(output + 12, tag,             16);
        memcpy(output + 28, cipherBuf.data(), cbOut);
        result = 28 + (int)cbOut;
    }

    BCryptDestroyKey(hKey);
    BCryptCloseAlgorithmProvider(hAlg, 0);
    return result;
}

/// Déchiffre avec AES-256-GCM.
/// Entrée : nonce(12) + tag(16) + ciphertext
/// Retourne la longueur du texte clair, ou -1 si erreur / tag invalide.
EXPORT int AesGcmDecrypt(
    const unsigned char* input,   int input_len,
    const unsigned char* key,     int key_len,
    unsigned char*       output,  int output_max_len)
{
    if (!input || !key || !output || input_len < 28 || key_len < 32) return -1;
    int ct_len = input_len - 28;
    if (output_max_len < ct_len) return -1;

    BCRYPT_ALG_HANDLE hAlg = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;
    int result = -1;

    if (!NT_SUCCESS(BCryptOpenAlgorithmProvider(&hAlg, BCRYPT_AES_ALGORITHM, NULL, 0)))
        return -1;

    if (!NT_SUCCESS(BCryptSetProperty(hAlg, BCRYPT_CHAINING_MODE,
        (PUCHAR)BCRYPT_CHAIN_MODE_GCM, sizeof(BCRYPT_CHAIN_MODE_GCM), 0)))
    { BCryptCloseAlgorithmProvider(hAlg, 0); return -1; }

    if (!NT_SUCCESS(BCryptGenerateSymmetricKey(hAlg, &hKey, NULL, 0, (PUCHAR)key, 32, 0)))
    { BCryptCloseAlgorithmProvider(hAlg, 0); return -1; }

    unsigned char tag[16];
    memcpy(tag, input + 12, 16);

    BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO authInfo;
    BCRYPT_INIT_AUTH_MODE_INFO(authInfo);
    authInfo.pbNonce = (PUCHAR)input;
    authInfo.cbNonce = 12;
    authInfo.pbTag   = tag;
    authInfo.cbTag   = 16;

    DWORD cbOut = 0;
    NTSTATUS st = BCryptDecrypt(
        hKey, (PUCHAR)(input + 28), ct_len, &authInfo,
        NULL, 0, output, output_max_len, &cbOut, 0);

    if (NT_SUCCESS(st)) result = (int)cbOut;

    BCryptDestroyKey(hKey);
    BCryptCloseAlgorithmProvider(hAlg, 0);
    return result;
}
