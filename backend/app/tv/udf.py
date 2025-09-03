from fastapi import APIRouter, Query
from typing import Optional
import time, math, random

router = APIRouter(prefix="/tv/udf", tags=["tv-udf"])

# In a real setup, map symbols to exchange tickers and pull real data
SYMBOLS = {"BTCUSDT": {"ticker": "BTCUSDT", "description": "Bitcoin / Tether USD"}}

@router.get("/config")
async def config():
    return {
        "supports_search": True,
        "supports_group_request": False,
        "supports_marks": True,
        "supports_timescale_marks": True,
        "supports_time": True,
        "exchanges": [{"value": "CRYPTO", "name": "Crypto", "desc": "Crypto"}],
        "symbols_types": [{"name": "crypto", "value": "crypto"}],
        "supported_resolutions": ["1", "5", "15", "60", "240", "1D"]
    }

@router.get("/symbols")
async def symbols(symbol: str):
    s = SYMBOLS.get(symbol.upper())
    if not s: 
        return {"s": "error", "errmsg": "Symbol not found"}
    return {
        "name": s["ticker"],
        "ticker": s["ticker"],
        "description": s["description"],
        "type": "crypto",
        "session": "24x7",
        "exchange": "CRYPTO",
        "listed_exchange": "CRYPTO",
        "timezone": "UTC",
        "has_intraday": True,
        "supported_resolutions": ["1","5","15","60","240","1D"],
        "pricescale": 100,
        "minmov": 1,
        "minmove2": 0
    }

@router.get("/history")
async def history(symbol: str, resolution: str, from_: int = Query(alias="from"), to: int = Query(...)):
    # Demo data: synthetic sine-wave-ish candles. Replace with real OHLCV.
    step = 60 if resolution == "1" else 300 if resolution == "5" else 900
    t = list(range(from_, to, step))
    if not t:
        return {"s": "no_data"}
    o, h, l, c, v = [], [], [], [], []
    for i, ts in enumerate(t):
        base = 30000 + 2000*math.sin(i/10)
        op = base + random.uniform(-50, 50)
        cl = op + random.uniform(-80, 80)
        hi = max(op, cl) + random.uniform(0, 60)
        lo = min(op, cl) - random.uniform(0, 60)
        vol = 10 + random.random()*5
        o.append(round(op, 2)); h.append(round(hi, 2)); l.append(round(lo, 2)); c.append(round(cl, 2)); v.append(round(vol,2))
    return {"s": "ok", "t": t, "o": o, "h": h, "l": l, "c": c, "v": v}

@router.get("/time")
async def time_endpoint():
    return int(time.time())
