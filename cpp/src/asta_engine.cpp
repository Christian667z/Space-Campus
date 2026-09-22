#include "../include/asta_engine.hpp"
#include <algorithm>
#include <cctype>

namespace AstaCore {

static std::string ToLower(const std::string& str) {
    std::string lower = str;
    std::transform(lower.begin(), lower.end(), lower.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return lower;
}

class FastIndexEngine::Impl {
public:
    std::vector<CourseIndexEntry> entries;

    std::vector<CourseIndexEntry> Search(const std::string& query) const {
        std::string qLower = ToLower(query);
        std::vector<CourseIndexEntry> results;

        for (const auto& item : entries) {
            if (qLower.empty() ||
                ToLower(item.title).find(qLower) != std::string::npos ||
                ToLower(item.subject).find(qLower) != std::string::npos ||
                ToLower(item.level).find(qLower) != std::string::npos) {
                results.push_back(item);
            }
        }
        return results;
    }
};

FastIndexEngine::FastIndexEngine() : pImpl(std::make_unique<Impl>()) {}
FastIndexEngine::~FastIndexEngine() = default;

void FastIndexEngine::AddEntry(const CourseIndexEntry& entry) {
    pImpl->entries.push_back(entry);
}

std::vector<CourseIndexEntry> FastIndexEngine::Search(const std::string& query) const {
    return pImpl->Search(query);
}

size_t FastIndexEngine::GetTotalIndexed() const {
    return pImpl->entries.size();
}

void FastIndexEngine::Clear() {
    pImpl->entries.clear();
}

// Implémentations des fonctions FFI C
extern "C" {

void* asta_cpp_create_engine() {
    return new FastIndexEngine();
}

void asta_cpp_destroy_engine(void* enginePtr) {
    if (enginePtr != nullptr) {
        delete static_cast<FastIndexEngine*>(enginePtr);
    }
}

int asta_cpp_index_course(void* enginePtr, const char* id, const char* title, const char* subject, const char* level) {
    if (enginePtr == nullptr || id == nullptr || title == nullptr) {
        return -1;
    }
    auto* engine = static_cast<FastIndexEngine*>(enginePtr);
    CourseIndexEntry entry;
    entry.id = id;
    entry.title = title;
    entry.subject = subject ? subject : "";
    entry.level = level ? level : "";
    entry.contentHash = 0;
    engine->AddEntry(entry);
    return 0;
}

int asta_cpp_search_count(void* enginePtr, const char* query) {
    if (enginePtr == nullptr || query == nullptr) {
        return 0;
    }
    auto* engine = static_cast<FastIndexEngine*>(enginePtr);
    auto results = engine->Search(query);
    return static_cast<int>(results.size());
}

} // extern "C"

} // namespace AstaCore
