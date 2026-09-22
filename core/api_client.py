import urllib.request
import urllib.error
import urllib.parse
import json

API_BASE_URL = "http://127.0.0.1:8080/api/v1"
TOKEN = None # Token JWT

def login(nom: str, password: str = "default_pass"):
    """Authentifie l'utilisateur via le backend Go et récupère un JWT."""
    global TOKEN
    try:
        req_data = json.dumps({"nom": nom, "password": password}).encode('utf-8')
        req = urllib.request.Request(f"{API_BASE_URL}/auth/login", data=req_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as r:
            if r.getcode() == 200:
                data = json.loads(r.read().decode('utf-8'))
                TOKEN = data.get("token")
                return data.get("user")
            return None
    except Exception as e:
        print(f"Erreur de connexion API: {e}")
        return None

def _get_headers():
    if TOKEN:
        return {"Authorization": f"Bearer {TOKEN}"}
    return {}

# --- SIEM / Logs ---
def get_api_audit_logs(limit=500, offset=0, level_filter="ALL", search_kw=""):
    try:
        params = {"limit": limit, "offset": offset, "level": level_filter, "search": search_kw}
        query_string = urllib.parse.urlencode(params)
        req = urllib.request.Request(f"{API_BASE_URL}/logs?{query_string}", headers=_get_headers())
        with urllib.request.urlopen(req) as r:
            if r.getcode() == 200:
                return json.loads(r.read().decode('utf-8')) # {"total": X, "logs": [...]}
            return {"total": 0, "logs": []}
    except Exception:
        return {"total": 0, "logs": []}

def get_api_dashboard_metrics():
    try:
        req = urllib.request.Request(f"{API_BASE_URL}/dashboard/metrics", headers=_get_headers())
        with urllib.request.urlopen(req) as r:
            if r.getcode() == 200:
                return json.loads(r.read().decode('utf-8'))
            return None
    except Exception:
        return None

# --- Admin / Users ---
def get_api_users():
    try:
        req = urllib.request.Request(f"{API_BASE_URL}/users", headers=_get_headers())
        with urllib.request.urlopen(req) as r:
            if r.getcode() == 200:
                return json.loads(r.read().decode('utf-8'))
            return []
    except Exception:
        return []

def toggle_api_user_status(user_id, is_active):
    try:
        req_data = json.dumps({"is_active": is_active}).encode('utf-8')
        headers = _get_headers()
        headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(f"{API_BASE_URL}/users/{user_id}/status", data=req_data, headers=headers, method="PATCH")
        with urllib.request.urlopen(req) as r:
            return r.getcode() == 200
    except Exception:
        return False

def delete_api_user(user_id):
    try:
        req = urllib.request.Request(f"{API_BASE_URL}/users/{user_id}", headers=_get_headers(), method="DELETE")
        with urllib.request.urlopen(req) as r:
            return r.getcode() == 200
    except Exception:
        return False
