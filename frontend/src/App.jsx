import { useState, useEffect } from 'react'
import axios from 'axios'
import { 
  Search, Loader2, AlertCircle, TrendingDown, CheckCircle, 
  Zap, Crown, Package, Globe, BarChart3, MapPin, Layers, BrainCircuit, Factory, Phone 
} from 'lucide-react'
import { AreaChart, Area, ResponsiveContainer } from 'recharts'

function App() {
  const [query, setQuery] = useState('')
  const [intent, setIntent] = useState('single') 
  const [pincode, setPincode] = useState('')     
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [loaderText, setLoaderText] = useState('Initializing Intelligence Engine...')

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query) return
    
    setLoading(true)
    setError('')
    setProducts([])

    const steps = [
      "Connecting to Global Sources...",
      "Analyzing Market Volatility...",
      "Running AI Forecast Models...",
      "Finalizing Market Verdict..."
    ]
    let stepIndex = 0;
    const interval = setInterval(() => {
      setLoaderText(steps[stepIndex % steps.length]);
      stepIndex++;
    }, 800);

    try {
      const { data } = await axios.get(`/api/search?query=${query}&intent=${intent}&pincode=${pincode}`)
      setProducts(data)
    } catch (err) {
      setError('Market Intelligence search failed. Sources might be blocking automated access.')
    } finally {
      clearInterval(interval)
      setLoading(false)
    }
  }

  // --- 🏷️ HYBRID CATEGORIZATION LOGIC ---
  const retailProducts = products.filter(p => p.type !== 'Wholesale' && p.type !== 'B2B');
  const b2bProducts = products.filter(p => p.type === 'Wholesale' || p.type === 'B2B');

  let categories = [];
  
  if (b2bProducts.length > 0) {
      categories.push({ 
          title: "Verified Suppliers & Factories", 
          data: b2bProducts, 
          color: "border-orange-500 text-orange-700", 
          icon: <Factory className="w-4 h-4" /> 
      });
  }
  
  if (retailProducts.length > 0) {
      const sorted = [...retailProducts].sort((a, b) => (a.price || 0) - (b.price || 0));
      const count = sorted.length;
      categories.push(
          { title: "Budget Selection", data: sorted.slice(0, Math.ceil(count / 3)), color: "border-gray-400 text-gray-600", icon: <Package className="w-4 h-4" /> },
          { title: "Value Selection", data: sorted.slice(Math.ceil(count / 3), Math.ceil((2 * count) / 3)), color: "border-blue-500 text-blue-700", icon: <Zap className="w-4 h-4" /> },
          { title: "Premium Selection", data: sorted.slice(Math.ceil((2 * count) / 3)), color: "border-purple-600 text-purple-800", icon: <Crown className="w-4 h-4" /> }
      );
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans pb-20 selection:bg-blue-100">
      
      {/* --- 🧠 INTELLIGENCE LOADER (Built by Narendra Bhandari) --- */}
      {loading && (
        <div className="fixed inset-0 z-[100] bg-white/80 backdrop-blur-md flex flex-col items-center justify-center transition-all">
          <div className="relative">
            <div className="absolute inset-0 bg-blue-500 rounded-full opacity-20 animate-ping"></div>
            <div className="bg-white p-4 rounded-full shadow-xl border border-blue-100 relative z-10">
              <BrainCircuit className="w-12 h-12 text-blue-600 animate-pulse" />
            </div>
          </div>
          <h3 className="mt-6 text-lg font-black text-gray-900 tracking-tight">PriceAtlas AI</h3>
          <p className="text-sm font-bold text-blue-600 uppercase tracking-widest mt-2 animate-pulse">{loaderText}</p>
          <div className="mt-8 px-4 py-2 bg-blue-50 rounded-full border border-blue-100">
            <p className="text-[10px] font-black text-blue-600 uppercase tracking-widest italic">Built by Narendra Bhandari</p>
          </div>
        </div>
      )}

      {/* --- Header --- */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm px-4 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg shadow-blue-200 shadow-lg"><TrendingDown className="text-white w-6 h-6" /></div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-gray-900">PriceAtlas</h1>
              <p className="text-[10px] text-gray-500 font-bold tracking-widest uppercase">Market Intelligence</p>
            </div>
          </div>
          <div className="hidden md:block text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full border border-blue-100">v2.2 ANALYTICS</div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-black mb-4 tracking-tighter text-gray-900 italic">Find the Advantage.</h2>
          <p className="text-gray-500 font-medium mb-8">Real-time arbitrage & AI price forecasting.</p>

          <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto mt-8 bg-white p-2 rounded-3xl shadow-2xl shadow-blue-100/50 border border-gray-100">
            <div className="flex flex-col md:flex-row gap-2">
              <div className="relative md:w-1/4">
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"><Layers className="w-4 h-4" /></div>
                <select value={intent} onChange={(e) => setIntent(e.target.value)} className="w-full pl-9 pr-4 py-4 rounded-2xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-blue-500 text-sm font-bold text-gray-700 outline-none appearance-none cursor-pointer">
                  <option value="single">Single Unit</option>
                  <option value="bulk">Bulk / B2B</option>
                  <option value="wholesale">Wholesale</option>
                </select>
              </div>
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input type="text" placeholder="Search product (e.g. iPhone 15, Laptop)" className="w-full pl-12 pr-4 py-4 rounded-2xl bg-gray-50 focus:bg-white border-transparent focus:ring-2 focus:ring-blue-500 text-lg font-medium outline-none transition-all" value={query} onChange={(e) => setQuery(e.target.value)} />
              </div>
              <button type="submit" disabled={loading} className="bg-gray-900 hover:bg-black text-white px-8 py-4 rounded-2xl font-bold transition-all">
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Search'}
              </button>
            </div>
          </form>
        </div>

        {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl flex items-center gap-3 mb-8 border border-red-100 shadow-sm"><AlertCircle className="w-5 h-5" /><p className="font-bold text-sm">{error}</p></div>}

        <div className="space-y-16">
          {products.length > 0 && categories.map((cat, idx) => cat.data.length > 0 && (
            <div key={idx} className="animate-in fade-in slide-in-from-bottom-8 duration-700 fill-mode-both" style={{ animationDelay: `${idx * 150}ms` }}>
              <div className="flex items-center gap-3 mb-6">
                <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full border-2 font-black uppercase text-[10px] ${cat.color} bg-white shadow-sm`}>{cat.icon} {cat.title}</div>
                <div className="h-px flex-1 bg-gradient-to-r from-gray-200 to-transparent" />
              </div>
              
              <div className="grid gap-6">
                {cat.data.map((item, itemIdx) => {
                  {/* --- 🏭 B2B CARD --- */}
                  if (item.type === 'Wholesale' || item.type === 'B2B') {
                    return (
                        <div key={itemIdx} className="bg-white p-6 rounded-[2rem] border-2 border-orange-100 hover:border-orange-300 shadow-sm hover:shadow-xl transition-all relative overflow-hidden group">
                           <div className="absolute top-0 right-0 bg-orange-500 text-white text-[10px] font-black px-4 py-1.5 rounded-bl-2xl z-10 uppercase tracking-widest">Verified Supplier</div>
                           <div className="md:flex gap-6">
                              <div className="md:w-1/4 flex items-center justify-center bg-gray-50 rounded-2xl p-4">
                                  <img src={item.image || "https://tiimg.tistatic.com/fp/1/007/557/indiamart-logo-584.jpg"} className="max-h-24 object-contain mix-blend-multiply transition-transform group-hover:scale-105" alt="Supplier" />
                              </div>
                              <div className="md:w-3/4">
                                  <div className="flex justify-between items-start mb-4">
                                      <div>
                                          <h3 className="font-bold text-gray-900 text-lg leading-tight">{item.title}</h3>
                                          <p className="text-xs font-bold text-orange-600 mt-1 uppercase tracking-wider">{item.source} • Factory Direct</p>
                                      </div>
                                      <div className="text-right"><p className="text-xl font-black text-gray-900">{item.price}</p></div>
                                  </div>
                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                                      <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                          <p className="text-[10px] font-black text-gray-400 uppercase mb-1">Company</p>
                                          <p className="text-sm font-bold text-gray-800 line-clamp-1">{item.seller}</p>
                                      </div>
                                      <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                          <p className="text-[10px] font-black text-gray-400 uppercase mb-1 flex items-center gap-1"><MapPin className="w-3 h-3"/> Location</p>
                                          <p className="text-sm font-medium text-gray-600 line-clamp-1">{item.address}</p>
                                      </div>
                                  </div>
                                  <div className="flex items-center justify-between border-t border-gray-100 pt-4">
                                      <span className="text-xs font-medium text-gray-400 italic">B2B Trade Intelligence Active</span>
                                      <a href={item.url} target="_blank" rel="noopener noreferrer" className="bg-orange-600 text-white text-xs font-black px-6 py-3 rounded-xl hover:bg-orange-700 transition-colors flex items-center gap-2 shadow-orange-200 shadow-md">
                                          GET QUOTE <Phone className="w-3 h-3" />
                                      </a>
                                  </div>
                              </div>
                           </div>
                        </div>
                    );
                  }

                  {/* --- 🛒 RETAIL CARD (Restoring Analytics) --- */}
                  const isPriceDrop = item.analysis?.score >= 85;
                  const chartData = item.analysis?.price_history && item.analysis.price_history.length > 0 ? item.analysis.price_history.map(h => ({ date: new Date(h.scraped_at).toLocaleDateString(), price: h.price_inr })).reverse() : [];

                  return (
                    <div key={itemIdx} className={`bg-white rounded-[2rem] shadow-sm hover:shadow-xl transition-all duration-300 border-2 overflow-hidden relative group ${isPriceDrop ? 'border-red-500 ring-4 ring-red-50' : 'border-gray-100 hover:border-blue-200'}`}>
                      {isPriceDrop && <div className="absolute top-0 right-0 bg-red-600 text-white text-[10px] font-black px-4 py-1.5 rounded-bl-2xl z-20 animate-pulse shadow-lg tracking-widest uppercase">Elite Deal Detected</div>}
                      <div className="md:flex h-full">
                        <div className={`md:w-1/4 p-8 flex flex-col items-center justify-center relative ${isPriceDrop ? 'bg-red-50/50' : 'bg-gray-50/50'}`}>
                          <div className="w-full aspect-square flex items-center justify-center mb-4"><img src={item.image} alt="" className="max-h-32 object-contain mix-blend-multiply transition-transform group-hover:scale-110 duration-500" /></div>
                          <div className="text-[9px] font-black text-gray-400 uppercase tracking-widest bg-white/60 backdrop-blur-sm px-3 py-1 rounded-full border border-gray-200">{item.source}</div>
                        </div>
                        <div className="p-6 md:w-3/4 flex flex-col justify-between">
                          <div>
                            <div className="flex justify-between items-start gap-4">
                              <h3 className={`text-lg font-black leading-tight mb-2 ${isPriceDrop ? 'text-red-700' : 'text-gray-900'}`}>{item.title}</h3>
                              <div className="text-right">
                                <span className={`text-3xl font-black italic tracking-tighter ${isPriceDrop ? 'text-red-600' : 'text-gray-900'}`}>₹{item.price?.toLocaleString()}</span>
                              </div>
                            </div>
                            {/* Analytics sparkline logic restored */}
                            {chartData.length > 1 ? (
                              <div className="h-16 w-full max-w-xs mb-6 opacity-80 hover:opacity-100 transition-opacity">
                                <ResponsiveContainer width="100%" height="100%">
                                  <AreaChart data={chartData}>
                                    <defs><linearGradient id={`grad-${itemIdx}`} x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor={isPriceDrop ? "#ef4444" : "#3b82f6"} stopOpacity={0.2}/><stop offset="95%" stopColor={isPriceDrop ? "#ef4444" : "#3b82f6"} stopOpacity={0}/></linearGradient></defs>
                                    <Area type="monotone" dataKey="price" stroke={isPriceDrop ? "#ef4444" : "#3b82f6"} strokeWidth={2.5} fill={`url(#grad-${itemIdx})`} />
                                  </AreaChart>
                                </ResponsiveContainer>
                              </div>
                            ) : <div className="h-16 flex items-center mb-6"><p className="text-[10px] text-gray-400 font-medium italic bg-gray-50 px-3 py-1 rounded-lg tracking-wider">⚡ Analyzing market volatility...</p></div>}
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
                              {/* Restored AI Forecast Section */}
                              {item.analysis?.forecast ? (
                                <div className="p-3 bg-blue-50/50 rounded-xl border border-blue-100 hover:border-blue-300 transition-colors">
                                  <div className="flex justify-between items-center mb-1"><p className="text-[9px] font-black text-blue-400 uppercase tracking-widest flex items-center gap-1"><BrainCircuit className="w-3 h-3" /> AI Prediction</p><span className="text-[9px] font-bold bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded">{item.analysis.forecast.confidence}% CONF</span></div>
                                  <div className="flex items-baseline gap-2"><span className={`text-sm font-bold ${item.analysis.forecast.change_pct < 0 ? 'text-green-600' : 'text-blue-700'}`}>{item.analysis.forecast.trend}</span><span className="text-[10px] text-gray-500 font-medium">Target: ₹{item.analysis.forecast.predicted_price.toLocaleString()}</span></div>
                                </div>
                              ) : <div className="p-3 bg-gray-50 rounded-xl border border-dashed border-gray-200 flex items-center justify-center gap-2"><BarChart3 className="w-4 h-4 text-gray-300" /><p className="text-[9px] text-gray-400 font-bold uppercase tracking-tight">Need {3 - (item.analysis?.history_count || 0)} more scans</p></div>}
                              
                              {/* Restored Verdict Label */}
                              <div className={`p-3 rounded-xl border flex flex-col justify-center ${isPriceDrop ? 'bg-red-50 border-red-100' : 'bg-gray-50 border-gray-100'}`}>
                                <p className="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">Market Verdict</p>
                                <p className={`text-xs font-black uppercase tracking-widest ${isPriceDrop ? 'text-red-600' : 'text-gray-900'}`}>{item.analysis?.verdict || "Evaluating"}</p>
                              </div>
                            </div>
                            <div className="flex flex-wrap items-center gap-2">
                              <span className={`text-[10px] font-black px-3 py-1.5 rounded-lg border ${isPriceDrop ? 'bg-red-600 text-white border-red-600' : 'bg-gray-100 text-gray-600 border-gray-200'}`}>SCORE: {item.analysis?.score}</span>
                              <span className="text-[10px] font-bold text-gray-500 uppercase bg-gray-100 border border-gray-200 px-3 py-1.5 rounded-lg">Volatility: {item.analysis?.volatility || 0}%</span>
                            </div>
                          </div>
                          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
                            <span className="text-[10px] text-gray-400 font-bold uppercase">Tracking {item.analysis?.history_count} data points</span>
                            <a href={item.url} target="_blank" rel="noopener noreferrer" className={`text-xs font-black px-6 py-3 rounded-xl flex items-center gap-2 transition-transform active:scale-95 ${isPriceDrop ? 'bg-red-600 text-white shadow-red-200' : 'bg-gray-900 text-white'}`}>{isPriceDrop ? 'SNAG DEAL' : 'VIEW OFFER'} <TrendingDown className="w-3 h-3" /></a>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 pt-12 pb-8 px-4 mt-20">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="bg-blue-600 p-1.5 rounded-lg"><TrendingDown className="text-white w-5 h-5" /></div>
              <h2 className="text-lg font-bold">PriceAtlas</h2>
            </div>
            <p className="text-sm text-gray-500 leading-relaxed font-medium">Advanced market intelligence platform for real-time arbitrage and price forecasting. Find the best deals across retail and wholesale markets instantly.</p>
          </div>
          <div>
            <h3 className="text-xs font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Core Technology</h3>
            <ul className="text-sm text-gray-600 space-y-2 font-bold uppercase tracking-tight">
              <li>AI Forecast Core</li>
              <li>B2B Scraper Engine</li>
              <li>Scorer Analytics</li>
              <li>Forex Exchange Sync</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xs font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Developer</h3>
            <div className="p-5 bg-gray-50 rounded-2xl border border-gray-100">
              <p className="text-sm font-black text-gray-900 uppercase">Narendra Bhandari</p>
              <p className="text-[10px] font-bold text-blue-600 mt-1 uppercase tracking-widest">Full-Stack Data Engineer</p>
            </div>
          </div>
        </div>
        <div className="max-w-6xl mx-auto border-t border-gray-100 pt-8 text-center">
          <p className="text-[10px] font-black text-gray-400 uppercase tracking-[0.3em]">© 2026 PriceAtlas • Built with Precision by Narendra Bhandari</p>
        </div>
      </footer>
    </div>
  )
}

export default App