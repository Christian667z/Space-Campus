#pragma once

#include <string>
#include <vector>
#include <memory>
#include <cstdint>

namespace AstaCore {

struct CourseIndexEntry {
    std::string id;
    std::string title;
    std::string subject;
    std::string level;
    uint32_t contentHash;
};

class FastIndexEngine {
public:
    FastIndexEngine();
    ~FastIndexEngine();

    // Ajoute un cours à l'index mémoire haute vitesse
    void AddEntry(const CourseIndexEntry& entry);

    // Recherche multi-critères instantanée
    std::vector<CourseIndexEntry> Search(const std::string& query) const;

    // Nombre d'éléments indexés
    size_t GetTotalIndexed() const;

    // Réinitialise l'index
    void Clear();

private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

// Fonctions exportées en C pour liaison FFI directe avec Rust
extern "C" {
    void* asta_cpp_create_engine();
    void asta_cpp_destroy_engine(void* enginePtr);
    int asta_cpp_index_course(void* enginePtr, const char* id, const char* title, const char* subject, const char* level);
    int asta_cpp_search_count(void* enginePtr, const char* query);
}

} // namespace AstaCore
