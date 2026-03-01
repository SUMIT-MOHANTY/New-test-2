import { useState, useEffect } from 'react'
import api from '../services/api'

interface PortfolioItem {
  id: number
  name: string
  symbol: string
  quantity: number
  current_price: number
}

export default function Portfolio() {
  const [items, setItems] = useState<PortfolioItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await api.get('/portfolio/items', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setItems(response.data)
      } catch {
        setItems([])
      } finally {
        setLoading(false)
      }
    }
    fetchPortfolio()
  }, [])

  if (loading) {
    return <div className="container mx-auto p-8">Loading...</div>
  }

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold text-primary">Portfolio</h1>
      {items.length === 0 ? (
        <p className="mt-4 text-gray-600">No portfolio items yet. Add some from your dashboard.</p>
      ) : (
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item) => (
            <div key={item.id} className="bg-white p-4 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold">{item.name}</h3>
              <p className="text-gray-500">{item.symbol}</p>
              <div className="mt-2 flex justify-between">
                <span>Qty: {item.quantity}</span>
                <span className="text-accent font-bold">${item.current_price}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}