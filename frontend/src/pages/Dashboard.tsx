import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

interface User {
  id: number
  username: string
  email: string
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }
    const fetchUser = async () => {
      try {
        const response = await api.get('/auth/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setUser(response.data)
      } catch {
        localStorage.removeItem('token')
        navigate('/login')
      }
    }
    fetchUser()
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  if (!user) return <div className="container mx-auto p-8">Loading...</div>

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-primary">Dashboard</h1>
        <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition">
          Logout
        </button>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Welcome, {user.username}!</h2>
        <p className="text-gray-600">Email: {user.email}</p>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-slate-50 rounded">
            <h3 className="font-semibold text-primary">Total Assets</h3>
            <p className="text-2xl font-bold">0</p>
          </div>
          <div className="p-4 bg-slate-50 rounded">
            <h3 className="font-semibold text-primary">Portfolio Value</h3>
            <p className="text-2xl font-bold">$0.00</p>
          </div>
        </div>
      </div>
    </div>
  )
}