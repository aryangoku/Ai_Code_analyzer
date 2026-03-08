import axios from "axios"

const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000"

export const analyzeRepo = async (url) => {
  const res = await axios.post(`${API}/analyze`, { repo_url: url })
  return res.data
}

export const checkHealth = async () => {
  const res = await axios.get(`${API}/health`)
  return res.data
}