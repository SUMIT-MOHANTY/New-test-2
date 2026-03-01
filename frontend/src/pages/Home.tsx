export default function Home() {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl font-bold text-primary">Welcome to Portfolio</h1>
      <p className="mt-4 text-secondary text-lg">Manage your portfolio with ease.</p>
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-primary">Track Assets</h3>
          <p className="mt-2 text-gray-600">Monitor your investments in one place.</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-primary">Analyze Performance</h3>
          <p className="mt-2 text-gray-600">View detailed analytics and reports.</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-primary">Secure Access</h3>
          <p className="mt-2 text-gray-600">Your data is protected with JWT auth.</p>
        </div>
      </div>
    </div>
  )
}