import axios from "axios"

const API="http://127.0.0.1:8000"

export const analyzeRepo = async(url)=>{

const res = await axios.post(`${API}/analyze`,{
repo_url:url
})

return res.data
}