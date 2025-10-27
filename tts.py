import threading

try:
    import pyttsx3  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyttsx3 = None  # type: ignore


_engine = None
_init_lock = threading.Lock()
_muted = False


def init_tts(rate: int | None = None, voice_name_contains: str | None = None) -> bool:
    """Initialise the TTS engine. Returns True on success.

    If pyttsx3 is not installed or initialisation fails, returns False.
    """
    global _engine
    if _engine is not None:
        return True
    if pyttsx3 is None:
        return False
    with _init_lock:
        if _engine is not None:
            return True
        try:
            engine = pyttsx3.init()
            if rate is not None:
                try:
                    engine.setProperty("rate", int(rate))
                except Exception:
                    pass
            if voice_name_contains:
                try:
                    for v in engine.getProperty("voices"):
                        if voice_name_contains.lower() in (v.name or "").lower():
                            engine.setProperty("voice", v.id)
                            break
                except Exception:
                    pass
            _engine = engine
            return True
        except Exception:
            _engine = None
            return False


def set_muted(muted: bool) -> None:
    """Temporarily mute speech output (e.g., while recording from the mic)."""
    global _muted
    _muted = bool(muted)


def speak(text: str) -> None:
    """Speak the provided text if the engine is initialised and not muted.

    Non-blocking enqueue to avoid stalling the main thread.
    """
    if not text:
        return
    if _engine is None or _muted:
        return
    try:
        _engine.say(text)
        _engine.runAndWait()
    except Exception:
        # Best-effort; swallow errors to avoid crashing the game loop
        pass


def shutdown_tts() -> None:
    """Shut down the TTS engine if initialised."""
    global _engine
    if _engine is None:
        return
    try:
        _engine.stop()
    except Exception:
        pass
    finally:
        _engine = None


def speak_many(texts: list[str]) -> None:
    """Speak multiple strings in one engine run to avoid choppiness on some backends."""
    if _engine is None or _muted:
        return
    try:
        for t in texts:
            if t:
                _engine.say(t)
        _engine.runAndWait()
    except Exception:
        # Fallback to speaking individually if batch fails
        try:
            for t in texts:
                speak(t)
        except Exception:
            pass


