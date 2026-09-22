fn main() {
    // Tauri build hook
    tauri_build::build();

    // Configuration des ponts FFI vers C/C++ natifs
    println!("cargo:rerun-if-changed=../c/src/asta_crypto.c");
    println!("cargo:rerun-if-changed=../cpp/src/asta_security.cpp");
}
