from typing import Iterable, Dict, Any, List
import time, random

class StrategyEngine:
    """Boundary for proprietary logic. Only returns rendered values (markers/series points)."""
    def __init__(self):
        self.state: Dict[str, Any] = {}

    def compute_signals(self, symbol: str, timeframe: str, candles: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Placeholder: Random BUY/SELL markers occasionally.
        out = []
        for c in candles:
            if random.random() < 0.02:
                out.append({
                    "timestamp": c["t"],
                    "price": c["c"],
                    "kind": random.choice(["buy", "sell"]),
                })
        return out

ENGINE = StrategyEngine()
