cmake_minimum_required(VERSION 3.15)
project(AstaNativeModules)

# ── Pybind11 (pour le module Python AES) ──────────────────────────────────────
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# ── Module Python : core_speed.pyd ────────────────────────────────────────────
pybind11_add_module(core_speed src/main.cpp)
target_link_libraries(core_speed PRIVATE bcrypt)

# ── DLL C# P/Invoke : native_security.dll ─────────────────────────────────────
# Chiffrement AES-256-GCM via Windows CNG
add_library(native_security SHARED src/native_security.cpp)
set_target_properties(native_security PROPERTIES PREFIX "")
target_link_libraries(native_security PRIVATE bcrypt)

# ── DLL C# P/Invoke : system_probe.dll ───────────────────────────────────────
# Métriques système réelles : CPU (PDH), RAM (GlobalMemoryStatusEx), Uptime
add_library(system_probe SHARED src/SystemProbe.cpp)
set_target_properties(system_probe PROPERTIES PREFIX "")
target_link_libraries(system_probe PRIVATE pdh)

# ── Moteur d'indexation C++17 et FFI : asta_engine ───────────────────────────
add_library(asta_engine SHARED src/asta_engine.cpp)
set_target_properties(asta_engine PROPERTIES PREFIX "")
target_include_directories(asta_engine PUBLIC include)

