import os
import sys
import time
import threading
from pathlib import Path

import numpy as np  # type: ignore

try:
    import sounddevice as sd  # type: ignore
except Exception:
    sd = None  # type: ignore

try:
    from vosk import Model, KaldiRecognizer  # type: ignore
except Exception:
    Model = None  # type: ignore
    KaldiRecognizer = None  # type: ignore

from audio_viz import render_sparkline, PeakHistory
import tts


_model = None
_model_lock = threading.Lock()


def init_model(model_dir: str | None = None) -> bool:
    global _model
    if _model is not None:
        return True
    if Model is None:
        return False
    model_path = (
        Path(model_dir)
        if model_dir
        else Path("assets/models/vosk/vosk-model-small-en-us-0.15")
    )
    if not model_path.exists():
        return False
    with _model_lock:
        if _model is not None:
            return True
        try:
            _model = Model(str(model_path))
            return True
        except Exception:
            _model = None
            return False


def _peak_from_pcm(data: bytes) -> float:
    if not data:
        return 0.0
    # 16-bit little-endian mono
    pcm = np.frombuffer(data, dtype=np.int16)
    if pcm.size == 0:
        return 0.0
    # normalise to 0..1
    return float(np.max(np.abs(pcm)) / 32768.0)


def listen_for_command(prompt: str = "> ", max_seconds: int = 15, silence_tail_ms: int = 2500) -> str:
    if sd is None or KaldiRecognizer is None:
        return ""
    if _model is None:
        if not init_model():
            return ""

    samplerate = 16000
    channels = 1
    blocksize = 0  # let PortAudio choose
    dtype = "int16"

    recognizer = KaldiRecognizer(_model, samplerate)

    # silence detection based on recent peaks
    history = PeakHistory(capacity=600)
    silence_threshold = 0.05  # peak under 5% considered silence (less aggressive)
    silence_tail = int(silence_tail_ms / 1000 * samplerate)
    bytes_per_sample = 2  # int16
    bytes_tail_needed = silence_tail * bytes_per_sample
    silent_bytes_seen = 0
    # Only start counting silence after we detect activity or a small grace period
    activity_detected = False
    min_listen_ms = 800
    min_listen_s = min_listen_ms / 1000.0

    print("Speak now... (voice input). Press Ctrl+C to cancel.")

    tts.set_muted(True)
    start = time.time()
    result_text = ""
    last_partial_text = ""

    ended = False
    timeout_reached = False

    def callback(indata, frames, time_info, status):  # noqa: N802
        nonlocal result_text, silent_bytes_seen, timeout_reached, activity_detected, last_partial_text
        if ended:
            return
        if status:
            pass
        
        # Check for timeout in callback
        if time.time() - start > max_seconds:
            timeout_reached = True
            return
            
        data_bytes = bytes(indata)
        peak = _peak_from_pcm(data_bytes)
        history.add(peak)

        # redraw sparkline
        spark = render_sparkline(history.tail(), width=60)
        sys.stdout.write("\r" + spark + "\x1b[K")
        sys.stdout.flush()

        # feed recognizer
        try:
            accepted = recognizer.AcceptWaveform(data_bytes)
        except Exception:
            timeout_reached = True
            return

        if accepted:
            if last_partial_text:
                result_text = last_partial_text
        else:
            # track partial text so we can return something even without a final segment
            try:
                import json as _json
                _p = recognizer.PartialResult()
                _pd = _json.loads(_p)
                _pt = (_pd.get("partial") or "").strip()
                if _pt:
                    result_text = _pt
                    last_partial_text = _pt
            except Exception:
                pass

        # silence accumulation
        if peak >= silence_threshold:
            activity_detected = True
            silent_bytes_seen = 0
        else:
            # Count silence only after activity or grace period
            if activity_detected or (time.time() - start) > min_listen_s:
                silent_bytes_seen += len(data_bytes)

    try:
        with sd.RawInputStream(
            samplerate=samplerate,
            blocksize=blocksize,
            device=None,
            dtype=dtype,
            channels=channels,
            callback=callback,
        ):
            while True:
                # Check timeout
                if time.time() - start > max_seconds:
                    timeout_reached = True
                    break
                # Check silence
                if silent_bytes_seen >= bytes_tail_needed:
                    break
                time.sleep(0.05)
            
            # obtain final result
            ended = True
            # Collect one more partial snapshot after we've stopped
            try:
                import json as _json
                _fp = recognizer.PartialResult()
                _fpd = _json.loads(_fp)
                _fpt = (_fpd.get("partial") or "").strip()
                if _fpt:
                    result_text = _fpt
                    last_partial_text = _fpt
            except Exception:
                pass
    except KeyboardInterrupt:
        final_json = None
        timeout_reached = True
    except Exception:
        final_json = None
        timeout_reached = True
    finally:
        tts.set_muted(False)
        sys.stdout.write("\n")
        sys.stdout.flush()

    # parse final result
    if timeout_reached:
        print("Voice input timed out.")

    return (last_partial_text or result_text or "")


