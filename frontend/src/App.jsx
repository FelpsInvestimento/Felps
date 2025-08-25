import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Play, Square, Activity, TrendingUp, DollarSign, Bot, AlertTriangle } from 'lucide-react'
import './App.css'

function App() {
  const [robotStatus, setRobotStatus] = useState({
    is_running: false,
    trading_mode: 'AUTOMATIC',
    accounts_status: {}
  })
  const [balances, setBalances] = useState({})
  const [operationsLog, setOperationsLog] = useState([])
  const [iasStatus, setIasStatus] = useState({ status: 'INACTIVE', message: '' })
  const [loading, setLoading] = useState(false)

  const API_BASE_URL = 'http://localhost:5000/api'

  // Função para fazer requisições à API
  const apiRequest = async (endpoint, options = {}) => {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })
      return await response.json()
    } catch (error) {
      console.error('Erro na API:', error)
      return { error: 'Erro de conexão com o servidor' }
    }
  }

  // Carregar dados iniciais
  const loadData = async () => {
    setLoading(true)
    const [status, balance, log, ias] = await Promise.all([
      apiRequest('/status'),
      apiRequest('/balance'),
      apiRequest('/log'),
      apiRequest('/ias_status')
    ])
    
    if (!status.error) setRobotStatus(status)
    if (!balance.error) setBalances(balance)
    if (!log.error) setOperationsLog(log)
    if (!ias.error) setIasStatus(ias)
    setLoading(false)
  }

  // Iniciar robô
  const startRobot = async () => {
    setLoading(true)
    const result = await apiRequest('/start', { method: 'POST' })
    if (!result.error) {
      await loadData()
    }
    setLoading(false)
  }

  // Parar robô
  const stopRobot = async () => {
    setLoading(true)
    const result = await apiRequest('/stop', { method: 'POST' })
    if (!result.error) {
      await loadData()
    }
    setLoading(false)
  }

  // Alterar modo de negociação
  const changeTradingMode = async (mode) => {
    setLoading(true)
    const result = await apiRequest('/mode', {
      method: 'POST',
      body: JSON.stringify({ mode })
    })
    if (!result.error) {
      await loadData()
    }
    setLoading(false)
  }

  // Carregar dados a cada 30 segundos
  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-6xl font-bold text-white mb-4 tracking-tight">
            FELPS TRADE
          </h1>
          <p className="text-xl text-purple-200 font-medium">
            "EU QUERO, EU POSSO E EU CONSIGO. JÁ DEU CERTO."
          </p>
          <div className="flex items-center justify-center gap-4 mt-6">
            <Badge variant={robotStatus.is_running ? "default" : "secondary"} className="text-lg px-4 py-2">
              <Activity className="w-4 h-4 mr-2" />
              {robotStatus.is_running ? 'ATIVO' : 'INATIVO'}
            </Badge>
            <Badge variant="outline" className="text-lg px-4 py-2 text-white border-white">
              <Bot className="w-4 h-4 mr-2" />
              Modo: {robotStatus.trading_mode}
            </Badge>
          </div>
        </div>

        {/* Controles principais */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Play className="w-5 h-5" />
                Controle do Robô
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2">
                <Button 
                  onClick={startRobot} 
                  disabled={loading || robotStatus.is_running}
                  className="flex-1 bg-green-600 hover:bg-green-700"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Iniciar
                </Button>
                <Button 
                  onClick={stopRobot} 
                  disabled={loading || !robotStatus.is_running}
                  variant="destructive"
                  className="flex-1"
                >
                  <Square className="w-4 h-4 mr-2" />
                  Parar
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Modo de Operação
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={robotStatus.trading_mode} onValueChange={changeTradingMode}>
                <SelectTrigger className="bg-white/20 border-white/30 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="LIGHT">Leve</SelectItem>
                  <SelectItem value="MODERATE">Moderado</SelectItem>
                  <SelectItem value="AGGRESSIVE">Agressivo</SelectItem>
                  <SelectItem value="AUTOMATIC">Automático</SelectItem>
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Bot className="w-5 h-5" />
                Status das IAs
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Badge variant={iasStatus.status === 'OK' ? "default" : "secondary"}>
                  {iasStatus.status === 'OK' ? 'Funcionando' : 'Inativo'}
                </Badge>
                {iasStatus.status === 'OK' && (
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                )}
              </div>
              <p className="text-sm text-purple-200 mt-2">{iasStatus.message}</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs principais */}
        <Tabs defaultValue="balances" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-white/10 backdrop-blur-sm">
            <TabsTrigger value="balances" className="text-white data-[state=active]:bg-white/20">
              Saldos das Contas
            </TabsTrigger>
            <TabsTrigger value="operations" className="text-white data-[state=active]:bg-white/20">
              Relatório de Operações
            </TabsTrigger>
            <TabsTrigger value="accounts" className="text-white data-[state=active]:bg-white/20">
              Gestão de Contas
            </TabsTrigger>
          </TabsList>

          <TabsContent value="balances" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(balances).map(([accountName, accountBalance]) => (
                <Card key={accountName} className="bg-white/10 backdrop-blur-sm border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center gap-2">
                      <DollarSign className="w-5 h-5" />
                      {accountName}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {accountBalance.error ? (
                      <p className="text-red-400">{accountBalance.error}</p>
                    ) : (
                      <div className="space-y-2">
                        {Object.entries(accountBalance).map(([currency, amount]) => (
                          <div key={currency} className="flex justify-between text-sm">
                            <span className="text-purple-200">{currency}:</span>
                            <span className="text-white font-mono">
                              {typeof amount === 'number' ? amount.toFixed(8) : amount}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="operations" className="space-y-4">
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardHeader>
                <CardTitle className="text-white">Últimas Operações</CardTitle>
                <CardDescription className="text-purple-200">
                  Histórico das operações realizadas pelas IAs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {operationsLog.length === 0 ? (
                    <p className="text-purple-200 text-center py-8">
                      Nenhuma operação registrada ainda
                    </p>
                  ) : (
                    operationsLog.slice(-20).reverse().map((operation, index) => (
                      <div key={index} className="bg-white/5 rounded-lg p-3 border border-white/10">
                        <div className="flex items-center justify-between mb-2">
                          <Badge variant="outline" className="text-xs">
                            {operation.account}
                          </Badge>
                          <span className="text-xs text-purple-200">
                            {new Date(operation.timestamp * 1000).toLocaleString()}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant={operation.type === 'BUY' ? 'default' : operation.type === 'SELL' ? 'destructive' : 'secondary'}>
                            {operation.type}
                          </Badge>
                          <span className="text-white font-mono text-sm">{operation.symbol}</span>
                        </div>
                        <p className="text-sm text-purple-200">
                          {typeof operation.details === 'string' ? operation.details : JSON.stringify(operation.details)}
                        </p>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="accounts" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(robotStatus.accounts_status || {}).map(([accountName, accountStatus]) => (
                <Card key={accountName} className="bg-white/10 backdrop-blur-sm border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white">{accountName}</CardTitle>
                    <CardDescription className="text-purple-200">
                      Status da conta e configurações
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <h4 className="text-sm font-medium text-white mb-2">Posições Abertas:</h4>
                      {Object.keys(accountStatus.open_positions || {}).length === 0 ? (
                        <p className="text-sm text-purple-200">Nenhuma posição aberta</p>
                      ) : (
                        <div className="space-y-1">
                          {Object.entries(accountStatus.open_positions).map(([symbol, amount]) => (
                            <div key={symbol} className="flex justify-between text-sm">
                              <span className="text-purple-200">{symbol}:</span>
                              <span className="text-white font-mono">{amount}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-white mb-2">API Key:</h4>
                      <p className="text-xs text-purple-200 font-mono break-all">
                        {accountStatus.api_key_details?.access_key || 'N/A'}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <div className="text-center mt-12 text-purple-200">
          <p className="text-sm">
            FELPS TRADE - Robô de Day Trade 100% Automático com 5 IAs
          </p>
          <p className="text-xs mt-2 opacity-70">
            Operando 24/7 com análise inteligente, compra, venda, stop loss e supervisão
          </p>
        </div>
      </div>
    </div>
  )
}

export default App

