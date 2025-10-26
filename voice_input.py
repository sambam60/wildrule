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


def listen_for_command(prompt: str = "> ", max_seconds: int = 15, silence_tail_ms: int = 1200) -> str:
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
    silence_threshold = 0.15  # peak under 1.5% considered silence (more sensitive)
    silence_tail = int(silence_tail_ms / 1000 * samplerate)
    bytes_per_sample = 2  # int16
    bytes_tail_needed = silence_tail * bytes_per_sample
    silent_bytes_seen = 0

    print("Speak now... (voice input). Press Ctrl+C to cancel.")

    tts.set_muted(True)
    start = time.time()
    result_text = ""

    ended = False
    timeout_reached = False

    def callback(indata, frames, time_info, status):  # noqa: N802
        nonlocal result_text, silent_bytes_seen, timeout_reached
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
        if recognizer.AcceptWaveform(data_bytes):
            # We got a segment, try to read final result in outer loop
            pass

        # silence accumulation
        if peak < silence_threshold:
            silent_bytes_seen += len(data_bytes)
        else:
            silent_bytes_seen = 0

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
            try:
                final_json = recognizer.FinalResult()
            except Exception:
                final_json = None
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
    if not final_json:
        if timeout_reached:
            print("Voice input timed out.")
        return ""
    try:
        import json

        data = json.loads(final_json)
        text = (data.get("text") or "").strip()
        return text
    except Exception:
        return ""


