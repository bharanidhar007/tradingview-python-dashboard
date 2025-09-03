// Minimal UDF-compatible datafeed for TVCL
const base = import.meta.env.VITE_API_BASE

export const UDF = {
  onReady: (cb: any) => {
    fetch(base + '/tv/udf/config').then(r => r.json()).then(cb)
  },
  searchSymbols: async (userInput: string, exchange: string, symbolType: string, onResultReadyCallback: any) => {
    onResultReadyCallback([{ symbol: 'BTCUSDT', full_name: 'BTCUSDT', description: 'Bitcoin', ticker: 'BTCUSDT', type: 'crypto' }])
  },
  resolveSymbol: async (symbolName: string, onSymbolResolvedCallback: any, onResolveErrorCallback: any) => {
    const r = await fetch(base + '/tv/udf/symbols?symbol=' + encodeURIComponent(symbolName))
    const data = await r.json()
    if (data.s === 'error') onResolveErrorCallback('Symbol not found')
    else onSymbolResolvedCallback(data)
  },
  getBars: async (symbolInfo: any, resolution: string, periodParams: any, onHistoryCallback: any, onErrorCallback: any) => {
    const from = Math.floor(periodParams.from)
    const to = Math.floor(periodParams.to)
    const r = await fetch(`${base}/tv/udf/history?symbol=${symbolInfo.ticker}&resolution=${resolution}&from=${from}&to=${to}`)
    const data = await r.json()
    if (data.s === 'no_data') onHistoryCallback([], { noData: true })
    else {
      const bars = data.t.map((t: number, i: number) => ({ time: t*1000, open: data.o[i], high: data.h[i], low: data.l[i], close: data.c[i], volume: data.v[i] }))
      onHistoryCallback(bars, { noData: false })
    }
  },
  subscribeBars: (symbolInfo: any, resolution: string, onRealtimeCallback: any, subscriberUID: string, onResetCacheNeededCallback: any) => {
    const ch = symbolInfo.ticker.toLowerCase() + '@' + resolution
    const ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/api/ws?channel=' + ch)
    ;(window as any).__tv_ws__ = ws
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data)
      if (msg.type === 'candle') {
        onRealtimeCallback({ time: msg.t, open: msg.c, high: msg.c, low: msg.c, close: msg.c, volume: 1 })
      }
    }
  },
  unsubscribeBars: (subscriberUID: string) => {
    const ws: WebSocket | undefined = (window as any).__tv_ws__
    ws?.close()
  },
}
