
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { transactionApi } from '../services/api/transactionApi';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

function Dashboard() {
  const accountId = localStorage.getItem('account_id');
  const customerName = localStorage.getItem('customer_name');
  
  const [balance, setBalance] = useState('R$ 0,00');
  
  // Busca o extrato para mostrar últimas transações
  const { data: statement, isLoading } = useQuery({
    queryKey: ['statement', accountId],
    queryFn: () => transactionApi.getStatement(accountId),
    enabled: !!accountId,
  });
  
  // Calcula saldo baseado nas transações
  useEffect(() => {
    if (statement?.data?.transactions) {
      let total = 0;
      statement.data.transactions.forEach(transaction => {
        const amount = parseFloat(transaction.amount);
        if (transaction.type === 'deposit') {
          total += amount;
        } else if (transaction.type === 'withdrawal' || transaction.type === 'transfer') {
          total -= amount;
        }
      });
      setBalance(total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
    }
  }, [statement]);
  
  const getTransactionIcon = (type) => {
    switch (type) {
      case 'deposit': return '💰';
      case 'withdrawal': return '💳';
      case 'transfer': return '🔄';
      default: return '📝';
    }
  };
  
  const getTransactionColor = (type) => {
    switch (type) {
      case 'deposit': return 'text-green-600';
      case 'withdrawal': return 'text-red-600';
      case 'transfer': return 'text-blue-600';
      default: return 'text-gray-600';
    }
  };
  
  return (
    <div className="space-y-8">
      {/* Banner de boas-vindas */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-2">Olá, {customerName}!</h1>
        <p className="text-blue-100">Bem-vindo ao seu Banco Digital</p>
        <div className="mt-4 text-2xl font-bold">
          Saldo atual: {balance}
        </div>
        <p className="text-sm text-blue-200 mt-2">
          Conta: {accountId}
        </p>
      </div>
      
      {/* Cards de ações rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link
          to="/deposit"
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-green-200"
        >
          <div className="text-4xl mb-4">💰</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Depósito</h3>
          <p className="text-gray-600 text-sm">Adicione dinheiro à sua conta</p>
        </Link>
        
        <Link
          to="/withdraw"
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-red-200"
        >
          <div className="text-4xl mb-4">💳</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Saque</h3>
          <p className="text-gray-600 text-sm">Retire dinheiro da sua conta</p>
        </Link>
        
        <Link
          to="/transfer"
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-blue-200"
        >
          <div className="text-4xl mb-4">🔄</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Transferência</h3>
          <p className="text-gray-600 text-sm">Envie dinheiro para outra conta</p>
        </Link>
        
        <Link
          to="/statement"
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-purple-200"
        >
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Extrato</h3>
          <p className="text-gray-600 text-sm">Veja seu histórico de transações</p>
        </Link>
      </div>
      
      {/* Últimas transações */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Últimas Transações</h2>
        
        {isLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Carregando transações...</p>
          </div>
        ) : statement?.data?.transactions?.length > 0 ? (
          <div className="space-y-4">
            {statement.data.transactions.slice(0, 5).map((transaction, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <div className="flex items-center space-x-4">
                  <span className="text-2xl">{getTransactionIcon(transaction.type)}</span>
                  <div>
                    <p className={`font-medium ${getTransactionColor(transaction.type)}`}>
                      {transaction.type === 'deposit' && 'Depósito'}
                      {transaction.type === 'withdrawal' && 'Saque'}
                      {transaction.type === 'transfer' && 'Transferência'}
                    </p>
                    <p className="text-sm text-gray-500">
                      {format(new Date(transaction.occurred_at), "dd 'de' MMMM 'às' HH:mm", { locale: ptBR })}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`font-bold ${getTransactionColor(transaction.type)}`}>
                    {transaction.type === 'deposit' ? '+' : '-'}
                    {parseFloat(transaction.amount).toLocaleString('pt-BR', {
                      style: 'currency',
                      currency: 'BRL'
                    })}
                  </p>
                </div>
              </div>
            ))}
            
            {statement.data.transactions.length > 5 && (
              <div className="text-center pt-4">
                <Link
                  to="/statement"
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                  Ver todas as transações →
                </Link>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p className="text-lg">Nenhuma transação realizada ainda</p>
            <p className="text-sm mt-2">Realize seu primeiro depósito para começar!</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
