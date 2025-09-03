from typing import Dict, Any

class ExecutionProvider:
    name = "paper"

    async def place_order(self, symbol: str, side: str, qty: float, order_type: str = "market", **kwargs) -> Dict[str, Any]:
        # Paper trading stub
        return {"status": "accepted", "symbol": symbol, "side": side, "qty": qty, "type": order_type}

PROVIDER = ExecutionProvider()
