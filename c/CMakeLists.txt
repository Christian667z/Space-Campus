cmake_minimum_required(VERSION 3.12)
project(AstaCrypto VERSION 2.0.0 LANGUAGES C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

include_directories(include)

# Bibliothèque statique pour inclusion directe dans Rust ou C++
add_library(asta_crypto_static STATIC src/asta_crypto.c)
target_include_directories(asta_crypto_static PUBLIC include)

# Bibliothèque dynamique DLL / SO pour P/Invoke C# ou liaisons externes
add_library(asta_crypto SHARED src/asta_crypto.c)
target_include_directories(asta_crypto PUBLIC include)
set_target_properties(asta_crypto PROPERTIES PREFIX "")
