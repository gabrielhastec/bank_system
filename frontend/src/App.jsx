import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import Login from './pages/Login';
import CreateAccount from './pages/CreateAccount';
import Dashboard from './pages/Dashboard';
import Deposit from './pages/Deposit';
import Withdraw from './pages/Withdraw';
import Transfer from './pages/Transfer';
import Statement from './pages/Statement';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

// Instalar: npm install @tanstack/react-query react-hot-toast
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <div className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Navigate to="/login" />} />
              <Route path="/login" element={<Login />} />
              <Route path="/create-account" element={<CreateAccount />} />
              
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              
              <Route path="/deposit" element={
                <ProtectedRoute>
                  <Deposit />
                </ProtectedRoute>
              } />
              
              <Route path="/withdraw" element={
                <ProtectedRoute>
                  <Withdraw />
                </ProtectedRoute>
              } />
              
              <Route path="/transfer" element={
                <ProtectedRoute>
                  <Transfer />
                </ProtectedRoute>
              } />
              
              <Route path="/statement" element={
                <ProtectedRoute>
                  <Statement />
                </ProtectedRoute>
              } />
            </Routes>
          </div>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                style: {
                  background: '#10B981',
                },
              },
              error: {
                duration: 4000,
                style: {
                  background: '#EF4444',
                },
              },
            }}
          />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
