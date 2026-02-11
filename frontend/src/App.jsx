import { useState } from 'react'
import axios from 'axios'
import { Search, Loader2, CheckCircle, AlertCircle, ShoppingCart, TrendingDown } from 'lucide-react'

function App() {
  const [query, setQuery] = useState('')
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query) return
    
    setLoading(true)
    setError('')
    setProduct(null)

    try {
      // Pointing to your Render Backend (or localhost if testing locally)
      const { data } = await axios.get(`/api/search?query=${query}`)
      setProduct(data)
    } catch (err) {
      setError('Product not found or scraper failed. Try a specific name.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans selection:bg-blue-100">
      
      {/* --- Header --- */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <TrendingDown className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-gray-900">PriceAtlas</h1>
              <p className="text-xs text-gray-500 font-medium">GLOBAL INTELLIGENCE</p>
            </div>
          </div>
          <div className="text-sm font-medium text-gray-500">v1.0.0 (Beta)</div>
        </div>
      </header>

      {/* --- Main Content --- */}
      <main className="max-w-3xl mx-auto px-4 py-12">
        
        {/* Search Section */}
        <div className="text-center mb-10">
          <h2 className="text-3xl font-extrabold text-gray-900 mb-4">
            Find the Real Price.
          </h2>
          <p className="text-gray-500 mb-8">
            Track prices, detect discounts, and analyze market trends in real-time.
          </p>

          <form onSubmit={handleSearch} className="relative max-w-lg mx-auto">
            <input
              type="text"
              placeholder="Paste URL or search product (e.g., iPhone 15)"
              className="w-full pl-12 pr-4 py-4 rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-lg"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
            <button 
              type="submit" 
              disabled={loading}
              className="absolute right-2 top-2 bottom-2 bg-gray-900 hover:bg-black text-white px-6 rounded-full font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Search'}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-xl flex items-center gap-3 mb-8 border border-red-100">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {/* --- Product Card Result --- */}
        {product && (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
            <div className="md:flex">
              
              {/* Product Image (Left) */}
              <div className="md:w-1/3 bg-gray-50 p-8 flex items-center justify-center relative">
                {product.image ? (
                  <img 
                    src={product.image} 
                    alt={product.title} 
                    className="max-h-48 object-contain mix-blend-multiply" 
                  />
                ) : (
                  <div className="text-gray-300">
                    <ShoppingCart className="w-16 h-16" />
                  </div>
                )}
                <span className="absolute top-4 left-4 bg-white/90 backdrop-blur text-xs font-bold px-2 py-1 rounded shadow-sm">
                  {product.source || 'Amazon'}
                </span>
              </div>

              {/* Product Details (Right) */}
              <div className="p-8 md:w-2/3 flex flex-col justify-between">
                <div>
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <h3 className="text-xl font-bold text-gray-900 leading-tight line-clamp-2" title={product.title}>
                      {product.title}
                    </h3>
                  </div>
                  
                  {/* Status Badge */}
                  <div className="flex items-center gap-2 mb-6">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      <CheckCircle className="w-3 h-3" />
                      Live Data
                    </span>
                    <span className="text-xs text-gray-400">
                      Updated just now
                    </span>
                  </div>
                </div>

                <div className="border-t border-gray-100 pt-6 flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 font-medium mb-1">Current Price</p>
                    <div className="flex items-baseline gap-1">
                      <span className="text-3xl font-black text-gray-900">
                        {product.currency} {product.price?.toLocaleString()}
                      </span>
                    </div>
                  </div>
                  
                  <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold text-sm transition-colors shadow-lg shadow-blue-200">
                    View Deal
                  </button>
                </div>
              </div>

            </div>
          </div>
        )}

      </main>
    </div>
  )
}

export default App