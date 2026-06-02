import React from 'react'
import './pages.css'

export default function Login() {
  return (
    <main className="page login-page">
      <h1>Log in</h1>
      <form className="presentational-form" onSubmit={(e) => e.preventDefault()}>
        <label>
          Username
          <input name="username" placeholder="username" />
        </label>
        <label>
          Password
          <input name="password" type="password" placeholder="password" />
        </label>
        <button type="submit">Sign in</button>
      </form>
    </main>
  )
}
