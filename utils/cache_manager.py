from pathlib import Path
from utils.logger import AstaLogger
from security.crypto_manager import load_encrypted_json, save_encrypted_json
import time

class CacheManager:
    """
    Gère le stockage local (cache) pour le mode hors ligne.
    Chiffre les données sensibles si nécessaire.
    """
    _cache_dir = None
    _cache_duration = 3600 * 24 # 24 heures par défaut

    @classmethod
    def initialize(cls, cache_dir: Path):
        cls._cache_dir = cache_dir
        cls._cache_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_cache_file(cls, key: str) -> Path:
        return cls._cache_dir / f"{key}.cache"

    @classmethod
    def set(cls, key: str, data: dict):
        if not cls._cache_dir: return
        file_path = cls._get_cache_file(key)
        payload = {
            "timestamp": time.time(),
            "data": data
        }
        save_encrypted_json(file_path, payload)

    @classmethod
    def get(cls, key: str, max_age: int = None) -> dict:
        if not cls._cache_dir: return None
        file_path = cls._get_cache_file(key)
        
        payload = load_encrypted_json(file_path, None)
        if not payload:
            return None

        age = time.time() - payload.get("timestamp", 0)
        limit = max_age if max_age is not None else cls._cache_duration
        
        if age > limit:
            return None # Expiré
            
        return payload.get("data")

    @classmethod
    def invalidate(cls, key: str):
        if not cls._cache_dir: return
        file_path = cls._get_cache_file(key)
        if file_path.exists():
            file_path.unlink()
