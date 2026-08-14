import axios from 'axios';




const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';


const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000 // 10 seconds
})


export async function analyzeUrl(url) {
    const response = await apiClient.post('/api/analyze', { url });
    return response.data;
}


export async function getScanHistory() {
    const response = await apiClient.get('/api/history');
    return response.data;
}


export async function deleteScan(scanId) {
    await apiClient.delete(`/api/history/${scanId}`);
}