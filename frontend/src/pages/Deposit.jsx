
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import toast from 'react-hot-toast';
import axios from 'axios';

const depositSchema = z.object({
  amount: z.string()
    .min(1, 'Valor é obrigatório')
    .refine(val => {
      const num = parseFloat(val.replace(',', '.'));
      return !isNaN(num) && num > 0;
    }, 'Valor deve ser positivo')
    .refine(val => {
      const num = parseFloat(val.replace(',', '.'));
      return num <= 1000000;
    }, 'Valor máximo: R$ 1.000.000,00')
});

function Deposit() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const accountId = localStorage.getItem('account_id');
  const token = localStorage.getItem('auth_token');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch
  } = useForm({
    resolver: zodResolver(depositSchema),
    defaultValues: {
      amount: ''
    }
  });
  
  const amountValue = watch('amount');
  
  const formatCurrency = (value) => {
    const onlyNumbers = value.replace(/\D/g, '');
    if (!onlyNumbers) return '';
    
    const number = parseInt(onlyNumbers, 10) / 100;
    return number.toLocaleString('pt-BR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  };
  
  const handleAmountChange = (e) => {
    const formatted = formatCurrency(e.target.value);
    setValue('amount', formatted, { shouldValidate: true });
  };
  
  const onSubmit = async (data) => {
    setIsLoading(true);
    
    try {
      const amount = parseFloat(data.amount.replace(/\./g, '').replace(',', '.'));
      
      const response = await axios.post(
        `http://localhost:8000/transactions/${accountId}/deposit`,
        { amount },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      toast.success('Depósito realizado com sucesso!');
      navigate('/dashboard');
      
    } catch (error) {
      if (error.response?.data?.detail) {
        toast.error(error.response.data.detail);
      } else if (error.response?.status === 401) {
        toast.error('Sessão expirada. Faça login novamente.');
        navigate('/login');
      } else if (error.response?.status === 403) {
        toast.error('Não autorizado');
      } else {
        toast.error('Erro ao realizar depósito. Tente novamente.');
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  const quickAmounts = [50, 100, 200, 500, 1000];
  
  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-6">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 p-3 rounded-lg">
              <span className="text-2xl">💰</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Depósito</h1>
              <p className="text-green-100">Adicione dinheiro à sua conta</p>
            </div>
          </div>
        </div>
        
        {/* Content */}
        <div className="p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
            {/* Valor do depósito */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                Valor do Depósito (R$)
              </label>
              
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500 text-2xl">R$</span>
                </div>
                <input
                  type="text"
                  {...register('amount')}
                  onChange={handleAmountChange}
                  className="w-full pl-12 pr-4 py-4 text-3xl border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 text-right font-bold"
                  placeholder="0,00"
                  disabled={isLoading}
                />
              </div>
              
              {errors.amount && (
                <p className="mt-2 text-sm text-red-600">{errors.amount.message}</p>
              )}
              
              {/* Valores rápidos */}
              <div className="mt-6">
                <p className="text-sm text-gray-600 mb-3">Valores rápidos:</p>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                  {quickAmounts.map((amount) => (
                    <button
                      type="button"
                      key={amount}
                      onClick={() => {
                        setValue('amount', amount.toFixed(2).replace('.', ','), {
                          shouldValidate: true
                        });
                      }}
                      className="py-2 px-4 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition"
                    >
                      R$ {amount.toFixed(2).replace('.', ',')}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Informações */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-800 mb-2">ℹ️ Informações</h3>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• O depósito é creditado instantaneamente</li>
                <li>• Não há taxas para depósitos</li>
                <li>• O limite máximo por depósito é de R$ 1.000.000,00</li>
              </ul>
            </div>
            
            {/* Botões */}
            <div className="flex space-x-4 pt-6">
              <button
                type="button"
                onClick={() => navigate('/dashboard')}
                className="flex-1 bg-gray-600 text-white py-3 px-4 rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition font-medium"
                disabled={isLoading}
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isLoading || !amountValue}
                className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-4 rounded-lg hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Processando...
                  </div>
                ) : (
                  'Confirmar Depósito'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Deposit;
