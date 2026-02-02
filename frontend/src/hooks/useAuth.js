
import { useState, useEffect } from 'react';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [customerName, setCustomerName] = useState('');
  const [accountId, setAccountId] = useState('');
  
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const name = localStorage.getItem('customer_name');
    const account = localStorage.getItem('account_id');
    
    if (token) {
      setIsAuthenticated(true);
      setCustomerName(name || '');
      setAccountId(account || '');
    }
  }, []);
  
  const login = (token, name, accountId) => {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('customer_name', name);
    localStorage.setItem('account_id', accountId);
    setIsAuthenticated(true);
    setCustomerName(name);
    setAccountId(accountId);
  };
  
  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('customer_name');
    localStorage.removeItem('account_id');
    setIsAuthenticated(false);
    setCustomerName('');
    setAccountId('');
  };
  
  return {
    isAuthenticated,
    customerName,
    accountId,
    login,
    logout
  };
}
