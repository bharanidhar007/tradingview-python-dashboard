import React, { useEffect, useRef, useState } from 'react'
import { loadTV } from '../tv/loader'
import { UDF } from '../tv/udf'

type Props = { symbol: string }

export const TVChart: React.FC<Props> = ({ symbol }) => {
  const container = useRef<HTMLDivElement>(null)
  const [loaded, setLoaded] = useState(false)
  const [tvLoaded, setTvLoaded] = useState(false)

  useEffect(() => {
    let widget: any
    ;(async () => {
      const TradingView = await loadTV()
      if (TradingView && container.current) {
        setTvLoaded(true)
        widget = new TradingView.widget({
          symbol: symbol,
          interval: '1',
          container: container.current,
          datafeed: UDF as any,
          library_path: '/charting_library/',
          locale: 'en',
          autosize: true,
          fullscreen: false,
          timezone: 'Etc/UTC',
          theme: 'Dark',
          disabled_features: ['use_localstorage_for_settings']
        })
        widget.onChartReady(() => setLoaded(true))
      }
    })()
    return () => { /* no-op for demo */ }
  }, [symbol])

  if (!tvLoaded) return <div className="rounded p-3 border">TradingView Library not found. Using fallback below.</div>
  return <div ref={container} style={{ height: 600 }} />
}
