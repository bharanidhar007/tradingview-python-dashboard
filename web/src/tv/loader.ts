export async function loadTV(): Promise<any | null> {
  // Try to detect TradingView Charting Library under /charting_library
  const exists = await fetch('/charting_library/charting_library.js', { method: 'HEAD' })
    .then(r => r.ok)
    .catch(() => false)
  if (exists) {
    await new Promise<void>((resolve) => {
      const s = document.createElement('script')
      s.src = '/charting_library/charting_library.js'
      s.onload = () => resolve()
      document.body.appendChild(s)
    })
    // @ts-ignore
    return (window as any).TradingView || null
  }
  return null
}
