import { useEffect, useState } from 'react'

type HealthStatus = 'checking' | 'connected' | 'unreachable'

function App() {
  const [status, setStatus] = useState<HealthStatus>('checking')

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

    fetch(`${apiUrl}/health`)
      .then((res) => {
        if (!res.ok) throw new Error('Health check failed')
        return res.json()
      })
      .then(() => setStatus('connected'))
      .catch(() => setStatus('unreachable'))
  }, [])

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 text-slate-900">
      <h1 className="text-3xl font-semibold">Briefly</h1>
      <p className="mt-2 text-slate-500">Transform conversations into actionable insights.</p>
      <p className="mt-6 text-sm">
        Backend status:{' '}
        <span
          className={
            status === 'connected'
              ? 'text-green-600 font-medium'
              : status === 'unreachable'
                ? 'text-red-600 font-medium'
                : 'text-slate-400'
          }
        >
          {status}
        </span>
      </p>
    </div>
  )
}

export default App
