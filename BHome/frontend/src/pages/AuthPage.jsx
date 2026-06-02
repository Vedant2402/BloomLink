import { useState, useEffect } from 'react'
import AuthForm from '../components/AuthForm'
import './pages.css'

const AuthPage = ({ initialMethod = 'login', onAuth }) => {
  const [method, setMethod] = useState(initialMethod)

  useEffect(() => {
    setMethod(initialMethod)
  }, [initialMethod])

  const route = method === 'login' ? 'auth/token/' : 'auth/register/'

  return (
    <div className="page auth-page">
      <AuthForm route={route} method={method} onAuth={onAuth} setMethod={setMethod} />
    </div>
  )
}

export default AuthPage
