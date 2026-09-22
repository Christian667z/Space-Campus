import urllib.request
import urllib.error
import json
from pathlib import Path
from utils.logger import AstaLogger
from security.crypto_manager import load_encrypted_json, save_encrypted_json
from utils.status_manager import StatusManager, AppStatus
from utils.event_bus import EventBus, AppEvents

class AuthManager:
    """
    Gère la session JWT (access_token en RAM, refresh_token stocké localement).
    """
    _access_token = None
    _api_url = "http://127.0.0.1:8080/api/v1"
    _session_file = None

    @classmethod
    def initialize(cls, session_file_path: Path):
        cls._session_file = session_file_path
        # On tente de restaurer la session via le refresh token
        cls._restore_session()

    @classmethod
    def _restore_session(cls):
        if not cls._session_file or not cls._session_file.exists():
            return
        
        data = load_encrypted_json(cls._session_file, {})
        refresh_token = data.get("refresh_token")
        user_id = data.get("user_id")

        if user_id:
            # Authentifié localement !
            StatusManager.set_authenticated(True)
            StatusManager.set_online(False)
            
            # Si on a un refresh_token, on tente de le rafraichir en arrière-plan
            if refresh_token:
                import threading
                threading.Thread(target=cls.refresh_access_token, args=(user_id, refresh_token), daemon=True).start()

    @classmethod
    def get_access_token(cls):
        return cls._access_token

    @classmethod
    def get_headers(cls):
        if cls._access_token:
            return {"Authorization": f"Bearer {cls._access_token}"}
        return {}

    @classmethod
    def _offline_register(cls, nom: str, password: str) -> tuple[bool, str]:
        from database.db_manager import DBManager
        user_id = DBManager.create_user(nom, password)
        if user_id != -1:
            return True, "Compte créé localement (hors-ligne)."
        return False, "Ce nom est déjà utilisé (hors-ligne)."

    @classmethod
    def _offline_login(cls, nom: str, password: str) -> tuple[bool, str]:
        from database.db_manager import DBManager
        success, user_id = DBManager.verify_password(nom, password)
        
        if success:
            StatusManager.set_authenticated(True)
            StatusManager.set_online(False)
            EventBus.publish(AppEvents.LOGIN_SUCCESS, {"id": user_id, "nom": nom, "offline": True})
            return True, "Connecté en mode hors-ligne."
            
        if user_id == -2:
            return False, "Votre compte a été bloqué par l'Administrateur."
            
        # Check if user exists but wrong password vs doesn't exist
        user = DBManager.get_user_by_name(nom)
        if user:
            return False, "Mot de passe incorrect."
            
        # Le compte n'existe pas localement, on le crée automatiquement (Auto-Register Offline)
        reg_success, reg_msg = cls._offline_register(nom, password)
        if reg_success:
            # On relance le login pour s'authentifier
            return cls._offline_login(nom, password)
        
        return False, "Impossible de créer le compte localement."

    @classmethod
    def login(cls, nom: str, password: str, device_name: str) -> tuple[bool, str]:
        # 1. Offline Auth (Instantané)
        success, msg = cls._offline_login(nom, password)
        
        # 2. Si succès, on lance une tentative de récupération du JWT en arrière-plan
        if success:
            import threading
            def _fetch_jwt():
                try:
                    import urllib.request, json
                    req_data = json.dumps({"nom": nom, "password": password, "device_name": device_name}).encode('utf-8')
                    req = urllib.request.Request(f"{cls._api_url}/auth/login", data=req_data, headers={'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req, timeout=3) as r:
                        if r.getcode() == 200:
                            data = json.loads(r.read().decode('utf-8'))
                            cls._access_token = data.get("access_token")
                            StatusManager.set_online(True)
                except Exception:
                    pass
            threading.Thread(target=_fetch_jwt, daemon=True).start()
            
        return success, msg

    @classmethod
    def register(cls, nom: str, password: str) -> tuple[bool, str]:
        # 1. Offline Register (Instantané)
        success, msg = cls._offline_register(nom, password)
        
        # 2. Si succès, on l'envoie en arrière-plan vers le Go backend via la file d'attente (déjà fait dans db_manager)
        return success, msg

    @classmethod
    def refresh_access_token(cls, user_id: int, refresh_token: str) -> bool:
        try:
            req_data = json.dumps({
                "user_id": user_id,
                "refresh_token": refresh_token,
                "device_name": "Asta_Desktop_App"
            }).encode('utf-8')
            req = urllib.request.Request(f"{cls._api_url}/auth/refresh", data=req_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=3) as r:
                if r.getcode() == 200:
                    data = json.loads(r.read().decode('utf-8'))
                    cls._access_token = data.get("access_token")
                    new_refresh_token = data.get("refresh_token")
                    
                    # Sauvegarder le nouveau refresh_token
                    save_encrypted_json(cls._session_file, {
                        "refresh_token": new_refresh_token,
                        "user_id": user_id
                    })
                    
                    StatusManager.set_authenticated(True)
                    StatusManager.set_online(True)
                    EventBus.publish(AppEvents.TOKEN_REFRESH)
                    return True
        except urllib.error.HTTPError as e:
            # Refresh token expiré ou invalide
            cls.logout()
            return False
        except Exception as e:
            AstaLogger.error(f"Impossible de rafraichir le token : {e}")
            return False

    @classmethod
    def logout(cls):
        try:
            req = urllib.request.Request(f"{cls._api_url}/auth/logout", method="POST", headers=cls.get_headers())
            urllib.request.urlopen(req, timeout=3)
        except:
            pass
        cls._access_token = None
        if cls._session_file and cls._session_file.exists():
            cls._session_file.unlink()
        StatusManager.set_authenticated(False)
        EventBus.publish(AppEvents.LOGOUT)

    @classmethod
    def auth_request(cls, method: str, endpoint: str, **kwargs):
        """
        Effectue une requête authentifiée. Si 401, tente de rafraichir le token et rejoue la requête.
        Retourne un dictionnaire (JSON) ou None si echec.
        """
        headers = kwargs.get("headers", {})
        headers.update(cls.get_headers())
        if 'json' in kwargs:
            data = json.dumps(kwargs.pop('json')).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        else:
            data = kwargs.get('data')

        url = f"{cls._api_url}{endpoint}"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=3) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                AstaLogger.error("Token expiré ou invalide. Tentative de rafraîchissement...")
                # On essaie de rafraichir
                session_data = load_encrypted_json(cls._session_file, {})
                refresh_token = session_data.get("refresh_token")
                user_id = session_data.get("user_id")

                if refresh_token and user_id and cls.refresh_access_token(user_id, refresh_token):
                    # Réussite du refresh, on rejoue
                    headers.update(cls.get_headers())
                    req = urllib.request.Request(url, data=data, headers=headers, method=method)
                    try:
                        with urllib.request.urlopen(req, timeout=3) as r2:
                            return json.loads(r2.read().decode('utf-8'))
                    except Exception:
                        return None
                else:
                    AstaLogger.error("Impossible de rafraichir le token. Déconnexion.")
                    cls.logout()
                    return None
            return None
        except Exception:
            return None
