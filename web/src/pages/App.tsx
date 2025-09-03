import React, { useState } from 'react'
import { useAuth } from '../lib/store'
import { TVChart } from '../components/TVChart'
import { LightweightChart } from '../components/LightweightChart'

export const App: React.FC = () => {
  const { loggedIn, login, logout } = useAuth()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('changeme123')
  const [symbol, setSymbol] = useState(import.meta.env.VITE_DEFAULT_SYMBOL || 'BTCUSDT')

  const [tvAvailable, setTvAvailable] = useState<boolean | null>(null)

  return (
    <div style={{ fontFamily: 'Inter, system-ui, sans-serif', padding: 16 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Private Trading Dashboard</h2>
        {loggedIn ? (
          <button onClick={logout}>Logout</button>
        ) : null}
      </header>

      {!loggedIn ? (
        <div style={{ maxWidth: 360, marginTop: 24 }}>
          <h3>Login</h3>
          <div>
            <input placeholder="email" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div>
            <input type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <button onClick={async () => {
            const ok = await login(email, password)
            if (!ok) alert('Login failed')
          }}>Sign in</button>
          <p style={{ marginTop: 8, opacity: 0.7 }}>Dev creds: admin@example.com / changeme123</p>
        </div>
      ) : (
        <>
          <div style={{ margin: '12px 0' }}>
            <input value={symbol} onChange={e => setSymbol(e.target.value)} />
          </div>
          {/* Attempt to show TVCL if present; else fallback to Lightweight */}
          <TVChart symbol={symbol} />
          <div style={{ marginTop: 16 }}>
            <LightweightChart symbol={symbol} />
          </div>
        </>
      )}
    </div>
  )
}
