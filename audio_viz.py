from collections import deque
from typing import Iterable


BLOCKS = "▁▂▃▄▅▆▇█"


def render_sparkline(peaks: Iterable[float], width: int = 60) -> str:
    values = list(peaks)[-width:]
    if not values:
        return ""
    peak_max = max(1e-6, max(values))
    chars = []
    for p in values:
        x = 0.0 if peak_max <= 0 else max(0.0, min(1.0, p / peak_max))
        idx = int(x * (len(BLOCKS) - 1))
        chars.append(BLOCKS[idx])
    return "".join(chars)


class PeakHistory:
    def __init__(self, capacity: int = 600):
        self._deque = deque(maxlen=capacity)

    def add(self, value: float) -> None:
        self._deque.append(float(value))

    def tail(self):
        return list(self._deque)


