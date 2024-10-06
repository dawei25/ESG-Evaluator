import React, { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'
import axios from 'axios'

interface Company {
  id: number
  name: string
  esgScore: number
  environmentalScore: number
  socialScore: number
  governanceScore: number
}

interface ESGTrend {
  date: string
  score: number
}

const ESGDashboard: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([])
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null)
  const [esgTrend, setEsgTrend] = useState<ESGTrend[]>([])
  const [weights, setWeights] = useState({ environmental: 0.33, social: 0.33, governance: 0.34 })

  useEffect(() => {
    fetchCompanies()
  }, [])

  useEffect(() => {
    if (selectedCompany) {
      fetchESGTrend(selectedCompany.id)
    }
  }, [selectedCompany])

  const fetchCompanies = async () => {
    try {
      const response = await axios.get('/api/companies')
      setCompanies(response.data)
    } catch (error) {
      console.error('Error fetching companies:', error)
    }
  }

  const fetchESGTrend = async (companyId: number) => {
    try {
      const response = await axios.get(`/api/esg-trend/${companyId}`)
      setEsgTrend(response.data)
    } catch (error) {
      console.error('Error fetching ESG trend:', error)
    }
  }

  const handleCompanyChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const company = companies.find(c => c.id === parseInt(event.target.value))
    setSelectedCompany(company || null)
  }

  const handleWeightChange = (category: keyof typeof weights, value: number) => {
    setWeights(prev => {
      const newWeights = { ...prev, [category]: value }
      const sum = Object.values(newWeights).reduce((a, b) => a + b, 0)
      return Object.fromEntries(
        Object.entries(newWeights).map(([k, v]) => [k, v / sum])
      ) as typeof weights
    })
  }

  const calculateWeightedScore = (company: Company) => {
    return (
      company.environmentalScore * weights.environmental +
      company.socialScore * weights.social +
      company.governanceScore * weights.governance
    ).toFixed(2)
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">ESG Dashboard</h1>
      
      <div className="mb-4">
        <select onChange={handleCompanyChange} className="p-2 border rounded">
          <option value="">Select a company</option>
          {companies.map(company => (
            <option key={company.id} value={company.id}>{company.name}</option>
          ))}
        </select>
      </div>

      {selectedCompany && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-semibold mb-2">ESG Scores</h2>
            <p>Overall: {calculateWeightedScore(selectedCompany)}</p>
            <p>Environmental: {selectedCompany.environmentalScore.toFixed(2)}</p>
            <p>Social: {selectedCompany.socialScore.toFixed(2)}</p>
            <p>Governance: {selectedCompany.governanceScore.toFixed(2)}</p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-semibold mb-2">Customize Weights</h2>
            <div className="flex flex-col space-y-2">
              <label>
                Environmental:
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={weights.environmental}
                  onChange={(e) => handleWeightChange('environmental', parseFloat(e.target.value))}
                  className="w-full"
                />
                {(weights.environmental * 100).toFixed(0)}%
              </label>
              <label>
                Social:
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={weights.social}
                  onChange={(e) => handleWeightChange('social', parseFloat(e.target.value))}
                  className="w-full"
                />
                {(weights.social * 100).toFixed(0)}%
              </label>
              <label>
                Governance:
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={weights.governance}
                  onChange={(e) => handleWeightChange('governance', parseFloat(e.target.value))}
                  className="w-full"
                />
                {(weights.governance * 100).toFixed(0)}%
              </label>
            </div>
          </div>

          <div className="bg-white p-4 rounded shadow md:col-span-2">
            <h2 className="text-xl font-semibold mb-2">ESG Score Trend</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={esgTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="score" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white p-4 rounded shadow md:col-span-2">
            <h2 className="text-xl font-semibold mb-2">ESG Component Comparison</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[selectedCompany]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="environmentalScore" fill="#8884d8" />
                <Bar dataKey="socialScore" fill="#82ca9d" />
                <Bar dataKey="governanceScore" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}

export default ESGDashboard