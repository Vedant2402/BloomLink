import React, { useState } from 'react'
import api, { setAuthToken } from '../api'
import '../pages/pages.css'

export default function AuthForm({ route = 'auth/token/', method = 'login', onAuth, setMethod }) {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      if (method === 'login') {
        const res = await api.post(`/chat/${route}`, { username, password })
        const { access, refresh } = res.data
        localStorage.setItem('accessToken', access)
        localStorage.setItem('refreshToken', refresh)
        setAuthToken(access)
        if (onAuth) onAuth()
      } else {
        await api.post(`/chat/${route}`, { username, password, email })
        // switch to login after successful register
        if (setMethod) setMethod('login')
      }
    } catch (err) {
      setError(err.response?.data || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-card">
      <header>
        <button onClick={() => setMethod('login')} className={method === 'login' ? 'active' : ''}>Login</button>
        <button onClick={() => setMethod('register')} className={method === 'register' ? 'active' : ''}>Register</button>
      </header>

      {error && (
        <div className="error">
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(error)}</pre>
        </div>
      )}

      <form className="presentational-form" onSubmit={handleSubmit}>
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} name="username" placeholder="username" />
        </label>

        {method === 'register' && (
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} name="email" type="email" placeholder="email" />
          </label>
        )}

        <label>
          Password
          <input value={password} onChange={(e) => setPassword(e.target.value)} name="password" type="password" placeholder="password" />
        </label>

        <button type="submit" disabled={loading}>{loading ? 'Working...' : (method === 'login' ? 'Sign in' : 'Register')}</button>
      </form>
    </div>
  )
}
