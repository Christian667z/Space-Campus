import threading
import time
import urllib.request
import json
from utils.logger import AstaLogger
from utils.status_manager import StatusManager, AppStatus
from utils.event_bus import EventBus, AppEvents

class HealthManager:
    _thread = None
    _running = False
    _api_url = "http://127.0.0.1:8080/api/v1"

    @classmethod
    def start(cls):
        if cls._running: return
        cls._running = True
        cls._thread = threading.Thread(target=cls._monitor_loop, daemon=True)
        cls._thread.start()

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def _monitor_loop(cls):
        while cls._running:
            try:
                req = urllib.request.Request(f"{cls._api_url}/health")
                with urllib.request.urlopen(req, timeout=3) as r:
                    if r.getcode() == 200:
                        data = json.loads(r.read().decode('utf-8'))
                        if data.get("status") == "ok":
                            if not StatusManager.is_online():
                                StatusManager.set_online(True)
                                StatusManager.set_status(AppStatus.ONLINE)
                                EventBus.publish(AppEvents.NETWORK_ONLINE)
                        else:
                            if StatusManager.is_online():
                                StatusManager.set_online(False)
                                StatusManager.set_status(AppStatus.BACKEND_UNREACHABLE)
                                EventBus.publish(AppEvents.NETWORK_OFFLINE)
                    else:
                        if StatusManager.is_online():
                            StatusManager.set_online(False)
                            StatusManager.set_status(AppStatus.BACKEND_UNREACHABLE)
                            EventBus.publish(AppEvents.NETWORK_OFFLINE)
            except Exception:
                if StatusManager.is_online():
                    StatusManager.set_online(False)
                    StatusManager.set_status(AppStatus.BACKEND_UNREACHABLE)
                    EventBus.publish(AppEvents.NETWORK_OFFLINE)
            
            # Attendre 10 secondes entre chaque ping
            time.sleep(10)
