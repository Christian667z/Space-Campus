use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int};
use crate::security::SecurityManager;

/// Pont C FFI pour le calcul de hachage SHA-256
#[no_mangle]
pub extern "C" fn asta_rust_hash_sha256(input: *const c_char, out_buffer: *mut c_char, max_len: c_int) -> c_int {
    if input.is_null() || out_buffer.is_null() || max_len < 65 {
        return -1;
    }

    let c_str = unsafe { CStr::from_ptr(input) };
    let slice = match c_str.to_str() {
        Ok(s) => s,
        Err(_) => return -2,
    };

    let hash_hex = SecurityManager::hash_sha256(slice.as_bytes());
    let c_hash = match CString::new(hash_hex) {
        Ok(c) => c,
        Err(_) => return -3,
    };

    unsafe {
        std::ptr::copy_nonoverlapping(c_hash.as_ptr(), out_buffer, 65.min(max_len as usize));
    }
    0
}

/// Pont C FFI pour récupérer l'empreinte matérielle de la machine
#[no_mangle]
pub extern "C" fn asta_rust_get_hardware_id(out_buffer: *mut c_char, max_len: c_int) -> c_int {
    if out_buffer.is_null() || max_len < 65 {
        return -1;
    }

    let hw_id = SecurityManager::get_hardware_fingerprint();
    let c_hw = match CString::new(hw_id) {
        Ok(c) => c,
        Err(_) => return -2,
    };

    unsafe {
        std::ptr::copy_nonoverlapping(c_hw.as_ptr(), out_buffer, 65.min(max_len as usize));
    }
    0
}

/// Pont C FFI pour libérer les buffers alloués par Rust si nécessaire
#[no_mangle]
pub extern "C" fn asta_rust_free_string(s: *mut c_char) {
    if !s.is_null() {
        unsafe {
            let _ = CString::from_raw(s);
        }
    }
}
