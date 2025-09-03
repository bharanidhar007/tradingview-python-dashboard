from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query, HTTPException, Cookie
from fastapi import status
from typing import Dict, Any, List
import asyncio, time, math, random
from app.auth.security import decode_token
from app.strategy.engine import ENGINE

router = APIRouter(tags=["private"])

def _require_user(access_token: str | None) -> str:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token")
    payload = decode_token(access_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload["sub"]

@router.get("/signals")
async def get_signals(symbol: str, timeframe: str = "1", start: int | None = None, end: int | None = None, access_token: str | None = Cookie(default=None)):
    _ = _require_user(access_token)
    # Fake candles for demo
    start = start or int(time.time()) - 3600*24
    end = end or int(time.time())
    t = list(range(start, end, 60))
    candles = [{"t": ts*1000, "c": 30000 + 1000*math.sin(i/20)} for i, ts in enumerate(t)]
    sigs = ENGINE.compute_signals(symbol, timeframe, candles)
    return {"symbol": symbol, "timeframe": timeframe, "signals": sigs}

@router.post("/orders")
async def place_order(symbol: str, side: str, qty: float, order_type: str = "market", access_token: str | None = Cookie(default=None)):
    _ = _require_user(access_token)
    # Stubbed paper response
    return {"status": "accepted", "symbol": symbol, "side": side, "qty": qty, "type": order_type}

@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, channel: str):
    await websocket.accept()
    try:
        # Stream synthetic candles + occasional signals
        i = 0
        while True:
            now = int(time.time())
            price = 30000 + 500*math.sin(i/10) + random.uniform(-20, 20)
            msg = {"type": "candle", "t": now*1000, "c": round(price,2), "symbol": channel.split("@")[0], "tf": channel.split("@")[1] if "@" in channel else "1m"}
            await websocket.send_json(msg)
            if random.random() < 0.05:
                await websocket.send_json({"type": "signal", "kind": random.choice(["buy","sell"]), "t": now*1000, "price": round(price,2)})
            await asyncio.sleep(1)
            i += 1
    except WebSocketDisconnect:
        return
