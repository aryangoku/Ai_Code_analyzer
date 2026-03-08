import { createContext, useContext, useState, useEffect } from "react"
import { getMe } from "../api"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("devinsight_token")
    if (!token) {
      setLoading(false)
      return
    }
    getMe()
      .then((data) => setUser(data))
      .catch(() => {
        localStorage.removeItem("devinsight_token")
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const login = (token) => {
    localStorage.setItem("devinsight_token", token)
    getMe().then(setUser).catch(() => setUser(null))
  }

  const logout = () => {
    localStorage.removeItem("devinsight_token")
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
