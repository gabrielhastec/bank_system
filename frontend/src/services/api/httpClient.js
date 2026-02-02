
import axios from 'axios';

// Configuração base do axios
const httpClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
httpClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de erros
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado ou inválido
      localStorage.removeItem('auth_token');
      localStorage.removeItem('account_id');
      localStorage.removeItem('customer_name');
      window.location.href = '/login';
    }
    
    const message = error.response?.data?.detail || error.message || 'Erro na requisição';
    return Promise.reject(new Error(message));
  }
);

export default httpClient;
