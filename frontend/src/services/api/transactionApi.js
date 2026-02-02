
import httpClient from './httpClient';

export const transactionApi = {
  /**
   * Realiza um depósito na conta
   * @param {string} accountId - ID da conta
   * @param {Object} data - Dados do depósito
   * @param {number} data.amount - Valor do depósito
   */
  deposit: (accountId, data) =>
    httpClient.post(`/transactions/${accountId}/deposit`, data),
  
  /**
   * Realiza um saque na conta
   * @param {string} accountId - ID da conta
   * @param {Object} data - Dados do saque
   * @param {number} data.amount - Valor do saque
   */
  withdraw: (accountId, data) =>
    httpClient.post(`/transactions/${accountId}/withdraw`, data),
  
  /**
   * Realiza uma transferência entre contas
   * @param {string} accountId - ID da conta de origem
   * @param {Object} data - Dados da transferência
   * @param {string} data.target_account_id - ID da conta de destino
   * @param {number} data.amount - Valor da transferência
   */
  transfer: (accountId, data) =>
    httpClient.post(`/transactions/${accountId}/transfer`, data),
  
  /**
   * Obtém o extrato da conta
   * @param {string} accountId - ID da conta
   */
  getStatement: (accountId) =>
    httpClient.get(`/transactions/${accountId}/statement`),
  
  /**
   * Obtém o saldo e limites da conta
   * @param {string} accountId - ID da conta
   */
  getBalance: (accountId) =>
    httpClient.get(`/transactions/${accountId}/balance`),
};
