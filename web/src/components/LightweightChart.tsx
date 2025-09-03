import React, { useEffect, useRef } from 'react'
import { createChart, IChartApi, UTCTimestamp } from 'lightweight-charts'

type Props = { symbol: string }
export const LightweightChart: React.FC<Props> = ({ symbol }) => {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!ref.current) return
    const chart = createChart(ref.current, { height: 500 })
    const series = chart.addCandlestickSeries()
    const ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/api/ws?channel=' + symbol.toLowerCase() + '@1m')
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data)
      if (msg.type === 'candle') {
        series.update({ time: Math.floor(msg.t/1000) as UTCTimestamp, open: msg.c, high: msg.c, low: msg.c, close: msg.c })
      }
    }
    return () => { ws.close(); chart.remove() }
  }, [symbol])
  return <div ref={ref} />
}
