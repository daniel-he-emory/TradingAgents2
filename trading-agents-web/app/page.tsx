'use client'

import { useState } from 'react'

type AgentStrategy = 'conservative' | 'moderate' | 'aggressive' | 'momentum' | 'value'

interface TradeResult {
  symbol: string
  action: 'BUY' | 'SELL' | 'HOLD'
  quantity: number
  price: number
  confidence: number
  reasoning: string
}

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null)
  const [ticker, setTicker] = useState('')
  const [strategy, setStrategy] = useState<AgentStrategy>('conservative')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<TradeResult[]>([])

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile)
      setTicker('')
    }
  }

  const handleRunAgents = async () => {
    if (!file && !ticker.trim()) {
      alert('Please upload a CSV file or enter a stock ticker')
      return
    }

    setLoading(true)
    
    // Placeholder backend call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock results
    const mockResults: TradeResult[] = [
      {
        symbol: ticker || 'AAPL',
        action: 'BUY',
        quantity: 100,
        price: 185.50,
        confidence: 0.87,
        reasoning: 'Strong technical indicators show bullish momentum with RSI oversold conditions and positive earnings sentiment.'
      },
      {
        symbol: ticker || 'AAPL',
        action: 'HOLD',
        quantity: 0,
        price: 185.50,
        confidence: 0.72,
        reasoning: 'Risk management suggests maintaining current position due to market volatility and upcoming earnings uncertainty.'
      }
    ]
    
    setResults(mockResults)
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Trading Agents Platform
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload market data or enter a stock ticker to get AI-powered trading recommendations
            from our intelligent agent strategies.
          </p>
        </div>

        {/* Main Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Input Section */}
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Data Input</h2>
              
              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload CSV File
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="csvFile"
                  />
                  <label htmlFor="csvFile" className="cursor-pointer">
                    <div className="text-gray-400 mb-2">
                      <svg className="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </div>
                    <p className="text-sm text-gray-600">
                      {file ? file.name : 'Click to upload or drag and drop CSV file'}
                    </p>
                  </label>
                </div>
              </div>

              {/* OR Divider */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">OR</span>
                </div>
              </div>

              {/* Stock Ticker Input */}
              <div>
                <label htmlFor="ticker" className="block text-sm font-medium text-gray-700 mb-2">
                  Stock Ticker Symbol
                </label>
                <input
                  type="text"
                  id="ticker"
                  value={ticker}
                  onChange={(e) => {
                    setTicker(e.target.value.toUpperCase())
                    if (e.target.value) setFile(null)
                  }}
                  placeholder="e.g., AAPL, TSLA, MSFT"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={!!file}
                />
              </div>
            </div>

            {/* Strategy Selection */}
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Agent Strategy</h2>
              
              <div>
                <label htmlFor="strategy" className="block text-sm font-medium text-gray-700 mb-2">
                  Choose Trading Strategy
                </label>
                <select
                  id="strategy"
                  value={strategy}
                  onChange={(e) => setStrategy(e.target.value as AgentStrategy)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="conservative">Conservative - Low risk, steady returns</option>
                  <option value="moderate">Moderate - Balanced risk/reward</option>
                  <option value="aggressive">Aggressive - High risk, high potential returns</option>
                  <option value="momentum">Momentum - Follow market trends</option>
                  <option value="value">Value - Undervalued stock opportunities</option>
                </select>
              </div>

              {/* Strategy Description */}
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="font-medium text-blue-900 mb-2">Strategy Details</h3>
                <p className="text-sm text-blue-700">
                  {strategy === 'conservative' && 'Focuses on stable, dividend-paying stocks with low volatility and capital preservation.'}
                  {strategy === 'moderate' && 'Balances growth and stability with diversified positions across market caps.'}
                  {strategy === 'aggressive' && 'Targets high-growth opportunities with higher risk tolerance for maximum returns.'}
                  {strategy === 'momentum' && 'Identifies and follows strong price trends using technical analysis indicators.'}
                  {strategy === 'value' && 'Seeks undervalued companies with strong fundamentals trading below intrinsic value.'}
                </p>
              </div>
            </div>
          </div>

          {/* Run Button */}
          <div className="mt-8 text-center">
            <button
              onClick={handleRunAgents}
              disabled={loading || (!file && !ticker.trim())}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Running Agents...
                </div>
              ) : (
                'Run Trading Agents'
              )}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Trading Recommendations</h2>
            
            <div className="space-y-6">
              {results.map((result, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <span className="text-2xl font-bold text-gray-800">{result.symbol}</span>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        result.action === 'BUY' ? 'bg-green-100 text-green-800' :
                        result.action === 'SELL' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {result.action}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-6 mt-2 lg:mt-0">
                      {result.quantity > 0 && (
                        <div className="text-center">
                          <p className="text-sm text-gray-500">Quantity</p>
                          <p className="font-semibold">{result.quantity}</p>
                        </div>
                      )}
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Price</p>
                        <p className="font-semibold">${result.price}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Confidence</p>
                        <p className="font-semibold">{(result.confidence * 100).toFixed(0)}%</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-800 mb-2">AI Reasoning</h4>
                    <p className="text-gray-600">{result.reasoning}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}