import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-secondary text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-accent">
          Portfolio
        </Link>
        <div className="space-x-4">
          <Link to="/" className="hover:text-accent transition">Home</Link>
          <Link to="/portfolio" className="hover:text-accent transition">Portfolio</Link>
          <Link to="/login" className="hover:text-accent transition">Login</Link>
          <Link to="/dashboard" className="hover:text-accent transition">Dashboard</Link>
        </div>
      </div>
    </nav>
  )
}