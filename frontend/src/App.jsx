import { useState } from 'react'
import axios from 'axios'
import { Search, Loader2, ExternalLink, TrendingUp } from 'lucide-react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query) return

    setLoading(true)
    setError(null)
    setData(null)

    try {
      // Call our Python Backend
      const res = await axios.get(`/api/search?q=${query}`)
      setData(res.data)
    } catch (err) {
      setError("Failed to fetch data. Server might be busy.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
      
      {/* Header */}
      <header className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-4xl font-bold mb-2 text-blue-900">PriceAtlas 🌍</h1>
        <p className="text-gray-500">Global Price Intelligence Platform</p>
      </header>

      {/* Search Box */}
      <div className="max-w-xl mx-auto mb-12">
        <form onSubmit={handleSearch} className="relative flex items-center">
          <input
            type="text"
            className="w-full p-4 pl-12 rounded-full border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search for a product (e.g., iPhone 15)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Search className="absolute left-4 text-gray-400" size={20} />
          <button 
            type="submit" 
            disabled={loading}
            className="absolute right-2 bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : "Search"}
          </button>
        </form>
      </div>

      {/* Results Area */}
      <div className="max-w-4xl mx-auto">
        {error && (
          <div className="p-4 bg-red-100 text-red-700 rounded-lg text-center">
            {error}
          </div>
        )}

        {data && data.result && (
          <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100 flex flex-col md:flex-row animate-fade-in">
            {/* Image Section */}
            <div className="md:w-1/3 p-6 flex items-center justify-center bg-gray-50">
              <img 
                src={data.result.image} 
                alt={data.result.name} 
                className="max-h-64 object-contain mix-blend-multiply"
              />
            </div>

            {/* Details Section */}
            <div className="md:w-2/3 p-8">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-2xl font-bold mb-2 text-gray-900">{data.result.name}</h2>
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase tracking-wider font-semibold">
                    {data.result.source}
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-green-600">₹{data.result.price.toLocaleString()}</p>
                  <p className="text-gray-400 text-sm">Current Price</p>
                </div>
              </div>

              <div className="mt-8 grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-gray-500 text-sm mb-1">Currency</p>
                  <p className="font-semibold">{data.result.currency}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-gray-500 text-sm mb-1">Database Status</p>
                  <p className={`font-semibold ${data.db_status.status === 'success' ? 'text-green-600' : 'text-red-500'}`}>
                    {data.db_status.status === 'success' ? 'Saved ✅' : 'Failed ❌'}
                  </p>
                </div>
              </div>

              <div className="mt-8">
                <a 
                  href={data.result.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-blue-600 hover:text-blue-800 font-semibold"
                >
                  View on Amazon <ExternalLink size={16} className="ml-2" />
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App