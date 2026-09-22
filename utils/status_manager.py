from utils.event_bus import EventBus, AppEvents

class AppStatus:
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    SYNCING = "SYNCING"
    BACKEND_UNREACHABLE = "BACKEND_UNREACHABLE"
    AUTHENTICATED = "AUTHENTICATED"
    LOADING = "LOADING"
    READY = "READY"

class StatusManager:
    """
    Gère l'état global de l'application (Online, Offline, Syncing...)
    Notifie l'interface utilisateur en cas de changement.
    """
    _current_status = AppStatus.LOADING
    _is_authenticated = False
    _is_online = False

    @classmethod
    def set_status(cls, status: str):
        if cls._current_status != status:
            cls._current_status = status
            # Publish event logic can go here if UI components subscribe directly to Status changes
            # EventBus.publish("STATUS_CHANGED", status)

    @classmethod
    def get_status(cls) -> str:
        return cls._current_status

    @classmethod
    def set_online(cls, is_online: bool):
        if cls._is_online != is_online:
            cls._is_online = is_online
            if is_online:
                cls.set_status(AppStatus.ONLINE)
                EventBus.publish(AppEvents.ONLINE_MODE)
            else:
                cls.set_status(AppStatus.OFFLINE)
                EventBus.publish(AppEvents.OFFLINE_MODE)

    @classmethod
    def is_online(cls) -> bool:
        return cls._is_online

    @classmethod
    def set_authenticated(cls, auth: bool):
        cls._is_authenticated = auth
        if auth:
            cls.set_status(AppStatus.AUTHENTICATED)

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls._is_authenticated
