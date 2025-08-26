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
  const [globalSettings, setGlobalSettings] = useState({
    daily_profit_target: '',
    custom_entry_value: '',
    stop_loss_percentage: '0.02', // Default 2%
    selected_assets: [],
    allow_dynamic_stop_loss: true,
  })
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
    
    if (!status.error) {
      setRobotStatus(status)
      setGlobalSettings(prev => ({...prev, ...status.global_settings}))
    }
    if (!balance.error) setBalances(balance)
    if (!log.error) setOperationsLog(log)
    if (!ias.error) setIasStatus(ias)
    setLoading(false)  }

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
          <TabsList className="grid w-full grid-cols-4 bg-white/10 backdrop-blur-sm">
            <TabsTrigger value="balances" className="text-white data-[state=active]:bg-white/20">
              Saldos das Contas
            </TabsTrigger>
            <TabsTrigger value="operations" className="text-white data-[state=active]:bg-white/20">
              Relatório de Operações
            </TabsTrigger>
            <TabsTrigger value="accounts" className="text-white data-[state=active]:bg-white/20">
              Gestão de Contas
            </TabsTrigger>
            <TabsTrigger value="settings" className="text-white data-[state=active]:bg-white/20">
              Configurações Avançadas
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



          <TabsContent value="settings" className="space-y-4">
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardHeader>
                <CardTitle className="text-white">Configurações Globais do Robô</CardTitle>
                <CardDescription className="text-purple-200">
                  Ajuste as configurações que afetam todas as operações do robô.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Valor de Entrada */}
                <div>
                  <label htmlFor="custom_entry_value" className="block text-sm font-medium text-purple-200 mb-1">
                    Valor de Entrada (R$)
                  </label>
                  <input
                    type="number"
                    id="custom_entry_value"
                    className="flex h-10 w-full rounded-md border border-white/30 bg-white/20 px-3 py-2 text-sm text-white placeholder:text-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-900"
                    value={globalSettings.custom_entry_value}
                    onChange={(e) => setGlobalSettings({ ...globalSettings, custom_entry_value: e.target.value })}
                    placeholder="Ex: 50.00"
                  />
                  <p className="text-xs text-purple-300 mt-1">
                    Define um valor fixo para cada entrada. Deixe em branco para que a IA determine.
                  </p>
                </div>

                {/* Meta de Lucro Diário */}
                <div>
                  <label htmlFor="daily_profit_target" className="block text-sm font-medium text-purple-200 mb-1">
                    Meta de Lucro Diário (R$)
                  </label>
                  <input
                    type="number"
                    id="daily_profit_target"
                    className="flex h-10 w-full rounded-md border border-white/30 bg-white/20 px-3 py-2 text-sm text-white placeholder:text-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-900"
                    value={globalSettings.daily_profit_target}
                    onChange={(e) => setGlobalSettings({ ...globalSettings, daily_profit_target: e.target.value })}
                    placeholder="Ex: 100.00"
                  />
                  <p className="text-xs text-purple-300 mt-1">
                    O robô pausará ao atingir esta meta de lucro no dia.
                  </p>
                </div>

                {/* Porcentagem de Stop Loss Configurável */}
                <div>
                  <label htmlFor="stop_loss_percentage" className="block text-sm font-medium text-purple-200 mb-1">
                    Porcentagem de Stop Loss (%)
                  </label>
                  <input
                    type="number"
                    id="stop_loss_percentage"
                    className="flex h-10 w-full rounded-md border border-white/30 bg-white/20 px-3 py-2 text-sm text-white placeholder:text-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-900"
                    value={parseFloat(globalSettings.stop_loss_percentage * 100).toFixed(2)}
                    onChange={(e) => setGlobalSettings({ ...globalSettings, stop_loss_percentage: parseFloat(e.target.value) / 100 })}
                    placeholder="Ex: 2.00"
                    step="0.01"
                  />
                  <p className="text-xs text-purple-300 mt-1">
                    Define a porcentagem de perda máxima antes de fechar a operação.
                  </p>
                </div>

                {/* Seleção Manual de Ativos */}
                <div>
                  <label htmlFor="selected_assets" className="block text-sm font-medium text-purple-200 mb-1">
                    Ativos Selecionados (separados por vírgula)
                  </label>
                  <input
                    type="text"
                    id="selected_assets"
                    className="flex h-10 w-full rounded-md border border-white/30 bg-white/20 px-3 py-2 text-sm text-white placeholder:text-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-900"
                    value={globalSettings.selected_assets.join(', ')}
                    onChange={(e) => setGlobalSettings({ ...globalSettings, selected_assets: e.target.value.split(',').map(s => s.trim().toUpperCase()).filter(s => s) })}
                    placeholder="Ex: BTC_BRL, ETH_BRL"
                  />
                  <p className="text-xs text-purple-300 mt-1">
                    Deixe em branco para que a IA opere em todos os ativos disponíveis.
                  </p>
                </div>

                {/* Alteração de Stop Loss em Meio à Operação */}
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="allow_dynamic_stop_loss"
                    className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                    checked={globalSettings.allow_dynamic_stop_loss}
                    onChange={(e) => setGlobalSettings({ ...globalSettings, allow_dynamic_stop_loss: e.target.checked })}
                  />
                  <label htmlFor="allow_dynamic_stop_loss" className="text-sm font-medium text-purple-200">
                    Permitir ajuste de Stop Loss em operação
                  </label>
                  <p className="text-xs text-purple-300 mt-1">
                    Se ativado, a IA pode ajustar o stop loss de posições abertas para proteger lucros ou minimizar perdas.
                  </p>
                </div>

                <Button 
                  onClick={async () => {
                    setLoading(true);
                    const result = await apiRequest('/settings', {
                      method: 'POST',
                      body: JSON.stringify(globalSettings)
                    });
                    if (!result.error) {
                      alert('Configurações salvas com sucesso!');
                      await loadData();
                    } else {
                      alert('Erro ao salvar configurações: ' + result.error);
                    }
                    setLoading(false);
                  }}
                  disabled={loading}
                  className="w-full bg-purple-600 hover:bg-purple-700"
                >
                  Salvar Configurações
                </Button>
              </CardContent>
            </Card>
          </TabsContent>


