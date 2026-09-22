class EventBus:
    """
    Système de Pub/Sub simple pour centraliser les événements de l'application.
    Permet à différentes parties du code de communiquer sans couplage direct.
    """
    _subscribers = {}

    @classmethod
    def subscribe(cls, event_type: str, callback):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(callback)

    @classmethod
    def unsubscribe(cls, event_type: str, callback):
        if event_type in cls._subscribers:
            try:
                cls._subscribers[event_type].remove(callback)
            except ValueError:
                pass

    @classmethod
    def publish(cls, event_type: str, *args, **kwargs):
        if event_type in cls._subscribers:
            for callback in cls._subscribers[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    import traceback
                    print(f"[EventBus] Erreur dans le callback pour {event_type}: {e}")
                    traceback.print_exc()

# Définition des événements standard de l'application
class AppEvents:
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGOUT = "LOGOUT"
    TOKEN_REFRESH = "TOKEN_REFRESH"
    CACHE_UPDATED = "CACHE_UPDATED"
    OFFLINE_MODE = "OFFLINE_MODE"
    ONLINE_MODE = "ONLINE_MODE"
    SYNC_COMPLETE = "SYNC_COMPLETE"
    THEME_CHANGED = "THEME_CHANGED"
    LANGUAGE_CHANGED = "LANGUAGE_CHANGED"
    NETWORK_ONLINE = "NETWORK_ONLINE"
    NETWORK_OFFLINE = "NETWORK_OFFLINE"
    SYNC_START = "SYNC_START"
