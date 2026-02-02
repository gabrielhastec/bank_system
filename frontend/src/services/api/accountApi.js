
import httpClient from './httpClient';

export const accountApi = {
  // Cria uma nova conta
  createAccount: (data) => 
    httpClient.post('/accounts/', data),
  
  // Faz login
  login: (data) =>
    httpClient.post('/auth/login', data),
  
  // Obtém informações da conta (futuro)
  getAccount: (accountId) =>
    httpClient.get(`/accounts/${accountId}`),
};
