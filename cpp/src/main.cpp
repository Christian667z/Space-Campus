#include <pybind11/pybind11.h>
#include <windows.h>
#include <bcrypt.h>
#include <vector>
#include <string>
#include <stdexcept>

#pragma comment(lib, "bcrypt.lib")

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

namespace py = pybind11;

std::vector<unsigned char> AesEncrypt(const std::string& plaintext, const std::string& key) {
    BCRYPT_ALG_HANDLE hAlg = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;
    std::vector<unsigned char> ciphertext;
    
    if (!NT_SUCCESS(BCryptOpenAlgorithmProvider(&hAlg, BCRYPT_AES_ALGORITHM, NULL, 0))) {
        throw std::runtime_error("Erreur BCryptOpenAlgorithmProvider");
    }
    
    if (!NT_SUCCESS(BCryptSetProperty(hAlg, BCRYPT_CHAINING_MODE, (PUCHAR)BCRYPT_CHAIN_MODE_CBC, sizeof(BCRYPT_CHAIN_MODE_CBC), 0))) {
        BCryptCloseAlgorithmProvider(hAlg, 0);
        throw std::runtime_error("Erreur BCryptSetProperty");
    }
    
    // Remplir la clé sur 32 octets (AES-256)
    std::vector<unsigned char> keyBytes(32, 0);
    for(size_t i = 0; i < key.size() && i < 32; i++) {
        keyBytes[i] = key[i];
    }
    
    if (!NT_SUCCESS(BCryptGenerateSymmetricKey(hAlg, &hKey, NULL, 0, keyBytes.data(), 32, 0))) {
        BCryptCloseAlgorithmProvider(hAlg, 0);
        throw std::runtime_error("Erreur BCryptGenerateSymmetricKey");
    }
    
    std::vector<unsigned char> iv(16, 0x42); // IV statique
    DWORD cbData = 0;
    
    // 1ère passe pour obtenir la taille
    BCryptEncrypt(hKey, (PUCHAR)plaintext.data(), plaintext.size(), NULL, iv.data(), iv.size(), NULL, 0, &cbData, BCRYPT_BLOCK_PADDING);
    ciphertext.resize(cbData);
    
    // 2ème passe pour chiffrer
    if (!NT_SUCCESS(BCryptEncrypt(hKey, (PUCHAR)plaintext.data(), plaintext.size(), NULL, iv.data(), iv.size(), ciphertext.data(), ciphertext.size(), &cbData, BCRYPT_BLOCK_PADDING))) {
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlg, 0);
        throw std::runtime_error("Erreur BCryptEncrypt");
    }
    
    BCryptDestroyKey(hKey);
    BCryptCloseAlgorithmProvider(hAlg, 0);
    return ciphertext;
}

std::string AesDecrypt(const std::vector<unsigned char>& ciphertext, const std::string& key) {
    BCRYPT_ALG_HANDLE hAlg = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;
    
    if (!NT_SUCCESS(BCryptOpenAlgorithmProvider(&hAlg, BCRYPT_AES_ALGORITHM, NULL, 0))) {
        throw std::runtime_error("Erreur BCryptOpenAlgorithmProvider");
    }
    
    if (!NT_SUCCESS(BCryptSetProperty(hAlg, BCRYPT_CHAINING_MODE, (PUCHAR)BCRYPT_CHAIN_MODE_CBC, sizeof(BCRYPT_CHAIN_MODE_CBC), 0))) {
        BCryptCloseAlgorithmProvider(hAlg, 0);
        throw std::runtime_error("Erreur BCryptSetProperty");
    }
    
    std::vector<unsigned char> keyBytes(32, 0);
    for(size_t i = 0; i < key.size() && i < 32; i++) {
        keyBytes[i] = key[i];
    }
    
    if (!NT_SUCCESS(BCryptGenerateSymmetricKey(hAlg, &hKey, NULL, 0, keyBytes.data(), 32, 0))) {
        BCryptCloseAlgorithmProvider(hAlg, 0);
        throw std::runtime_error("Erreur BCryptGenerateSymmetricKey");
    }
    
    std::vector<unsigned char> iv(16, 0x42);
    DWORD cbData = 0;
    
    // 1ère passe
    BCryptDecrypt(hKey, (PUCHAR)ciphertext.data(), ciphertext.size(), NULL, iv.data(), iv.size(), NULL, 0, &cbData, BCRYPT_BLOCK_PADDING);
    std::vector<unsigned char> plaintext(cbData);
    
    // 2ème passe
    if (!NT_SUCCESS(BCryptDecrypt(hKey, (PUCHAR)ciphertext.data(), ciphertext.size(), NULL, iv.data(), iv.size(), plaintext.data(), plaintext.size(), &cbData, BCRYPT_BLOCK_PADDING))) {
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlg, 0);
        throw std::runtime_error("Erreur BCryptDecrypt");
    }
    
    BCryptDestroyKey(hKey);
    BCryptCloseAlgorithmProvider(hAlg, 0);
    return std::string(plaintext.begin(), plaintext.begin() + cbData);
}

py::bytes PyEncryptAES(py::bytes data, const std::string& key) {
    std::string str_data = data;
    auto encrypted = AesEncrypt(str_data, key);
    return py::bytes((const char*)encrypted.data(), encrypted.size());
}

py::bytes PyDecryptAES(py::bytes encrypted_data, const std::string& key) {
    std::string str_data = encrypted_data;
    std::vector<unsigned char> vec_data(str_data.begin(), str_data.end());
    auto decrypted = AesDecrypt(vec_data, key);
    return py::bytes(decrypted);
}

PYBIND11_MODULE(core_speed, m) {
    m.doc() = "Module natif de cryptographie AES-256 (C++ Windows CNG)";
    m.def("encrypt_aes256", &PyEncryptAES, "Chiffre des données brutes en AES-256");
    m.def("decrypt_aes256", &PyDecryptAES, "Déchiffre des données brutes en AES-256");
}
