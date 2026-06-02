import React from 'react'
import './pages.css'

export default function Register() {
  return (
    <main className="page register-page">
      <h1>Create account</h1>
      <form className="presentational-form" onSubmit={(e) => e.preventDefault()}>
        <label>
          Username
          <input name="username" placeholder="username" />
        </label>
        <label>
          Email
          <input name="email" type="email" placeholder="email" />
        </label>
        <label>
          Password
          <input name="password" type="password" placeholder="password" />
        </label>
        <button type="submit">Register</button>
      </form>
    </main>
  )
}
