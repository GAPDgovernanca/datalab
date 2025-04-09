import { useState } from 'react';
import { LineChart, Line, BarChart, Bar, Cell, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { User, Settings, Database, Clock, ArrowRight, Upload, Activity, TrendingUp, TrendingDown, DollarSign, Calendar, Target, Download, Bell, RefreshCw, ChevronDown, Info, Check, AlertTriangle, ExternalLink } from 'lucide-react';

const CattleAnalysisApp = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [isSimulating, setIsSimulating] = useState(false);
  const [hasResults, setHasResults] = useState(false);
  const [showTip, setShowTip] = useState(null);
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);
  
  // Estado para parâmetros de entrada
  const [inputParams, setInputParams] = useState({
    purchasePrice: 320, // Preço de compra unitário por arroba (R$/@)
    initialWeight: 15, // Peso médio inicial (arrobas)
    marketAdjustment: 0, // Ágio/desconto relativo ao mercado (%)
    weightGainRate: 0.8, // Taxa de ganho de peso
    confinementTime: 90, // Tempo de confinamento (dias)
    financialCost: 0.8, // Custo financeiro sobre capital investido (%)
    iterations: 10000 // Número de iterações para simulação
  });

  // Dados simulados para visualização
  const mockProfitDistribution = [
    { valor: -1000, frequencia: 50 },
    { valor: -500, frequencia: 150 },
    { valor: 0, frequencia: 450 },
    { valor: 500, frequencia: 1200 },
    { valor: 1000, frequencia: 2500 },
    { valor: 1500, frequencia: 3000 },
    { valor: 2000, frequencia: 1800 },
    { valor: 2500, frequencia: 650 },
    { valor: 3000, frequencia: 200 },
  ];

  const mockSensitivityData = [
    { variable: 'Preço de venda', impact: 0.85, color: '#2563EB' },
    { variable: 'Taxa de ganho de peso', impact: 0.65, color: '#10B981' },
    { variable: 'Preço de compra', impact: 0.45, color: '#DC2626' },
    { variable: 'Custo financeiro', impact: 0.25, color: '#F59E0B' },
    { variable: 'Tempo de confinamento', impact: 0.15, color: '#8B5CF6' },
  ];

  const mockScatterData = Array.from({ length: 300 }, () => {
    const precoVenda = 290 + Math.random() * 80;
    return {
      precoVenda,
      // Ajustar dados aleatórios para mostrar correlação mais clara
      lucro: precoVenda * 15 - 3800 + (Math.random() * 1000 - 500)
    };
  }).sort((a, b) => a.precoVenda - b.precoVenda);

  // Simular processamento
  const runSimulation = () => {
    setIsSimulating(true);
    // Simulando tempo de processamento (< 5s conforme requisito)
    setTimeout(() => {
      setIsSimulating(false);
      setHasResults(true);
    }, 3000);
  };

  // Simular exportação
  const exportData = (format) => {
    alert(`Exportando dados em formato ${format}...`);
  };

  // Calcular valor estimado (utilizado em vários lugares)
  const calculatedFinalWeight = (inputParams.initialWeight + inputParams.weightGainRate * inputParams.confinementTime / 30).toFixed(2);
  const calculatedPotentialPercent = 78;

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Meta tag para melhor experiência mobile */}
      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
      
      {/* Header */}
      <header className="bg-green-800 text-white p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <Target className="mr-3" size={24} />
            <h1 className="text-xl font-bold">Análise de Sensibilidade | Negociação de Gado</h1>
          </div>
          <div className="flex items-center space-x-3">
            <div className="hidden md:flex items-center bg-green-700 bg-opacity-50 rounded-full px-3 py-1">
              <Activity className="mr-2 text-green-300" size={16} />
              <span className="text-green-100">Mercado: B3 +1.2%</span>
            </div>
            <button className="p-2 rounded-full hover:bg-green-700 transition-colors">
              <Settings size={20} />
            </button>
            <div className="flex items-center bg-green-700 rounded-full px-3 py-1">
              <User size={18} className="mr-2" />
              <span className="ml-1">Usuário</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 container mx-auto p-3 md:p-4 overflow-auto">
        <div className="bg-white rounded-lg shadow-md p-4 md:p-6 mb-6 border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span>Parâmetros da Simulação</span>
            <button 
              className="ml-2 text-gray-500 hover:text-blue-600"
              onClick={() => alert('Dica: Ajuste os parâmetros para simular diferentes cenários de negociação de gado.')}
            >
              <Info size={16} />
            </button>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
            {/* Dados de Compra */}
            <div className="border rounded-lg p-4 transition-shadow hover:shadow-md bg-white relative">
              <div className="absolute -top-3 -left-3 bg-blue-600 rounded-full p-2 shadow-md">
                <DollarSign size={16} className="text-white" />
              </div>
              <h3 className="font-medium text-lg mb-3 text-blue-800 pl-2 border-l-4 border-blue-600">Dados de Compra</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Preço de compra (R$/@)</span>
                    <div className="relative group">
                      <Info size={14} className="text-gray-400 cursor-pointer" />
                      <div className="absolute right-0 w-48 p-2 text-xs bg-gray-800 text-white rounded-lg hidden group-hover:block z-10">
                        Preço médio pago por arroba do boi na compra.
                      </div>
                    </div>
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">R$</span>
                    </div>
                    <input 
                      type="number" 
                      className="pl-10 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                      value={inputParams.purchasePrice}
                      onChange={(e) => setInputParams({...inputParams, purchasePrice: parseFloat(e.target.value)})}
                    />
                  </div>
                </div>
                
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Peso médio inicial (arrobas)</span>
                  </label>
                  <input 
                    type="number" 
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    step="0.1"
                    value={inputParams.initialWeight}
                    onChange={(e) => setInputParams({...inputParams, initialWeight: parseFloat(e.target.value)})}
                  />
                </div>
                
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Ágio/desconto ao mercado (%)</span>
                  </label>
                  <input 
                    type="number" 
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={inputParams.marketAdjustment}
                    onChange={(e) => setInputParams({...inputParams, marketAdjustment: parseFloat(e.target.value)})}
                  />
                </div>
              </div>
            </div>
            
            {/* Função de Crescimento */}
            <div className="border rounded-lg p-4 transition-shadow hover:shadow-md bg-white relative">
              <div className="absolute -top-3 -left-3 bg-green-600 rounded-full p-2 shadow-md">
                <TrendingUp size={16} className="text-white" />
              </div>
              <h3 className="font-medium text-lg mb-3 text-green-800 pl-2 border-l-4 border-green-600">Função de Crescimento</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Taxa de ganho de peso (@/dia)</span>
                    <div className="relative group">
                      <Info size={14} className="text-gray-400 cursor-pointer" />
                      <div className="absolute right-0 w-48 p-2 text-xs bg-gray-800 text-white rounded-lg hidden group-hover:block z-10">
                        Média do ganho diário de peso em arrobas.
                      </div>
                    </div>
                  </label>
                  <div className="mt-1 relative">
                    <input 
                      type="number" 
                      className="block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
                      step="0.01"
                      value={inputParams.weightGainRate}
                      onChange={(e) => setInputParams({...inputParams, weightGainRate: parseFloat(e.target.value)})}
                    />
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">@/dia</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Tempo de confinamento (dias)</span>
                  </label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Calendar size={16} className="text-gray-400" />
                    </div>
                    <input 
                      type="number" 
                      className="pl-10 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
                      value={inputParams.confinementTime}
                      onChange={(e) => setInputParams({...inputParams, confinementTime: parseInt(e.target.value)})}
                    />
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">dias</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Desvio padrão do ganho</span>
                    <button
                      className="text-blue-500 hover:text-blue-700 text-xs font-medium flex items-center"
                      onClick={() => alert('Parâmetro que modela a incerteza no ganho de peso dos animais.')}
                    >
                      Saiba mais
                    </button>
                  </label>
                  <input 
                    type="number" 
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
                    step="0.01"
                    placeholder="0.05"
                  />
                </div>
              </div>
            </div>
            
            {/* Custos e Preços */}
            <div className="border rounded-lg p-4 transition-shadow hover:shadow-md bg-white relative">
              <div className="absolute -top-3 -left-3 bg-purple-600 rounded-full p-2 shadow-md">
                <Activity size={16} className="text-white" />
              </div>
              <h3 className="font-medium text-lg mb-3 text-purple-800 pl-2 border-l-4 border-purple-600">Dados de Mercado</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Custo financeiro (% a.m.)</span>
                  </label>
                  <input 
                    type="number" 
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                    step="0.01"
                    value={inputParams.financialCost}
                    onChange={(e) => setInputParams({...inputParams, financialCost: parseFloat(e.target.value)})}
                  />
                </div>
                
                <div className="space-y-2">
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Preços Futuros</span>
                  </label>
                  <div className="flex space-x-2">
                    <button 
                      className="flex items-center flex-1 px-3 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-md hover:from-blue-700 hover:to-blue-800 shadow-sm transition-all"
                    >
                      <Database size={16} className="mr-2" />
                      <span>Obter B3</span>
                    </button>
                    <button 
                      className="flex items-center flex-1 px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 shadow-sm transition-all"
                    >
                      <Upload size={16} className="mr-2" />
                      <span>Importar</span>
                    </button>
                  </div>
                </div>
                
                <div>
                  <label className="flex justify-between text-sm font-medium text-gray-700">
                    <span>Número de iterações</span>
                  </label>
                  <select 
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                    value={inputParams.iterations}
                    onChange={(e) => setInputParams({...inputParams, iterations: parseInt(e.target.value)})}
                  >
                    <option value="1000">1.000 iterações</option>
                    <option value="5000">5.000 iterações</option>
                    <option value="10000">10.000 iterações</option>
                    <option value="50000">50.000 iterações</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          
          {/* Opções avançadas */}
          <div className="mt-4">
            <button 
              className="flex items-center text-sm text-gray-600 hover:text-gray-800"
              onClick={() => setShowAdvancedOptions(!showAdvancedOptions)}
            >
              <ChevronDown 
                size={16} 
                className={`mr-1 transition-transform ${showAdvancedOptions ? 'transform rotate-180' : ''}`} 
              />
              Opções avançadas
            </button>
            
            {showAdvancedOptions && (
              <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4 border-t pt-4 border-gray-200">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Modelo de crescimento
                  </label>
                  <select className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                    <option>Linear</option>
                    <option>Gompertz</option>
                    <option>Von Bertalanffy</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Correlação preços
                  </label>
                  <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.01" 
                    defaultValue="0.7"
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Sem correlação</span>
                    <span>Correlação perfeita</span>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Previsão de peso e botão de simulação */}
          <div className="mt-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="w-full md:w-1/2 bg-blue-50 rounded-lg p-3 border border-blue-200">
              <div className="flex justify-between items-center mb-1">
                <div className="flex items-center">
                  <Activity className="text-blue-600 mr-2" size={16} />
                  <span className="text-gray-700 font-medium text-sm">Previsão de peso final:</span>
                </div>
                <span className="text-lg font-bold text-blue-800">{calculatedFinalWeight} @</span>
              </div>
              
              <div className="w-full bg-blue-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '70%' }}></div>
              </div>
              <div className="flex justify-between text-xs text-gray-600 mt-1">
                <span>{inputParams.initialWeight} @</span>
                <span>Esperado: {calculatedFinalWeight} @</span>
              </div>
            </div>
            
            <button 
              className={`w-full md:w-auto flex items-center justify-center px-6 py-3 text-lg font-medium rounded-lg 
                ${isSimulating ? 'bg-gray-500' : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'} 
                text-white shadow-lg transition-all transform hover:scale-105 active:scale-95`}
              onClick={runSimulation}
              disabled={isSimulating}
            >
              {isSimulating ? (
                <>
                  <Clock className="animate-spin mr-2" size={22} />
                  <span>Simulando...</span>
                  <div className="ml-3 bg-white bg-opacity-20 px-2 py-0.5 rounded text-xs">
                    {Math.floor(Math.random() * 80) + 20}%
                  </div>
                </>
              ) : (
                <>
                  <ArrowRight className="mr-2" size={22} />
                  <span>Executar Simulação</span>
                </>
              )}
            </button>
          </div>
        </div>
        
        {/* Resultados */}
        {hasResults && (
          <div className="bg-white rounded-lg shadow-md p-4 md:p-6 border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">Resultados da Análise</h2>
            
            {/* Abas */}
            <div className="border-b border-gray-200 mb-6 overflow-x-auto scrollbar-hide">
              <div className="flex w-full min-w-max">
                <button 
                  className={`px-4 py-2 text-center whitespace-nowrap ${activeTab === 0 ? 'border-b-2 border-green-600 text-green-700 font-medium' : 'text-gray-500 hover:text-gray-700'}`}
                  onClick={() => setActiveTab(0)}
                  aria-current={activeTab === 0 ? "page" : undefined}
                >
                  Distribuição do Lucro
                </button>
                <button 
                  className={`px-4 py-2 text-center whitespace-nowrap ${activeTab === 1 ? 'border-b-2 border-green-600 text-green-700 font-medium' : 'text-gray-500 hover:text-gray-700'}`}
                  onClick={() => setActiveTab(1)}
                  aria-current={activeTab === 1 ? "page" : undefined}
                >
                  Análise de Sensibilidade
                </button>
                <button 
                  className={`px-4 py-2 text-center whitespace-nowrap ${activeTab === 2 ? 'border-b-2 border-green-600 text-green-700 font-medium' : 'text-gray-500 hover:text-gray-700'}`}
                  onClick={() => setActiveTab(2)}
                  aria-current={activeTab === 2 ? "page" : undefined}
                >
                  Correlações
                </button>
              </div>
            </div>
            
            <div className="mb-6">
              {/* Distribuição do Lucro */}
              {activeTab === 0 && (
                <div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg shadow-sm border border-green-200">
                      <h3 className="text-sm font-medium text-gray-700 mb-1">Lucro Médio</h3>
                      <p className="text-2xl font-bold text-green-600">R$ 1.458,32</p>
                      <div className="mt-2 flex items-center text-sm">
                        <TrendingUp size={14} className="text-green-600 mr-1" />
                        <span className="text-green-700">+12% do esperado</span>
                      </div>
                    </div>
                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg shadow-sm border border-blue-200">
                      <h3 className="text-sm font-medium text-gray-700 mb-1">Desvio Padrão</h3>
                      <p className="text-2xl font-bold text-blue-600">R$ 689,25</p>
                      <div className="mt-2 flex items-center text-sm">
                        <span className="text-blue-700">Variabilidade moderada</span>
                      </div>
                    </div>
                    <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg shadow-sm border border-purple-200">
                      <h3 className="text-sm font-medium text-gray-700 mb-1">Probabilidade de Lucro</h3>
                      <p className="text-2xl font-bold text-purple-600">87,5%</p>
                      <div className="mt-2 flex items-center text-sm">
                        <Check size={14} className="text-green-600 mr-1" />
                        <span className="text-purple-700">Risco baixo</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="h-72 mb-4">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={mockProfitDistribution}
                        margin={{ top: 20, right: 30, left: 20, bottom: 10 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                        <XAxis 
                          dataKey="valor" 
                          label={{ value: 'Lucro (R$)', position: 'insideBottom', offset: 0 }} 
                          tickFormatter={(value) => `${value}`}
                        />
                        <YAxis 
                          label={{ value: 'Frequência', angle: -90, position: 'insideLeft' }}
                        />
                        <Tooltip 
                          formatter={(value) => [`${value} ocorrências`, 'Frequência']} 
                          labelFormatter={(value) => `Lucro: R$ ${value}`}
                          contentStyle={{ backgroundColor: 'white', borderRadius: '8px', border: '1px solid #e0e0e0', padding: '10px' }}
                        />
                        <ReferenceLine x={0} stroke="#d1d5db" strokeWidth={2} />
                        <Bar dataKey="frequencia">
                          {mockProfitDistribution.map((entry, index) => (
                            <Cell 
                              key={`cell-${index}`} 
                              fill={entry.valor < 0 ? '#EF4444' : '#10B981'} 
                              fillOpacity={0.7 + (index / mockProfitDistribution.length) * 0.3}
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="mt-2 bg-yellow-50 p-3 rounded-md border-l-4 border-yellow-500">
                    <div className="flex items-start">
                      <AlertTriangle size={16} className="text-yellow-600 mr-2 mt-1 flex-shrink-0" />
                      <p className="text-sm text-yellow-800">
                        <strong>Interpretação:</strong> A distribuição mostra que a maioria das simulações (87,5%) resultam em lucro positivo. 
                        O lucro médio de R$ 1.458,32 por cabeça indica um cenário favorável para este investimento.
                      </p>
                    </div>
                  </div>
                  
                  <div className="mt-4 bg-gray-100 p-3 rounded-lg">
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium">Aproveitamento de potencial</span>
                      <span className="text-sm font-medium">{calculatedPotentialPercent}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div className="bg-green-600 h-2.5 rounded-full" style={{ width: `${calculatedPotentialPercent}%` }}></div>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">
                      Ajustando suas variáveis, você pode aumentar seu lucro em até {100 - calculatedPotentialPercent}%
                    </p>
                  </div>
                </div>
              )}
              
              {/* Análise de Sensibilidade */}
              {activeTab === 1 && (
                <div>
                  <div className="bg-purple-50 p-3 rounded-md mb-4 border-l-4 border-purple-500">
                    <p className="text-purple-800">
                      <strong>O que é este gráfico?</strong> Mostra o impacto de cada variável no resultado final. Quanto maior a barra, maior a influência da variável no lucro do seu negócio.
                    </p>
                  </div>
                  
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={mockSensitivityData}
                        layout="vertical"
                        margin={{ top: 20, right: 30, left: 100, bottom: 10 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f0f0f0" />
                        <XAxis 
                          type="number" 
                          domain={[0, 1]} 
                          tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                        />
                        <YAxis 
                          dataKey="variable" 
                          type="category" 
                          tick={{ fill: '#4B5563', fontSize: 13 }}
                        />
                        <Tooltip 
                          formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Impacto Relativo']}
                          contentStyle={{ 
                            backgroundColor: 'white', 
                            borderRadius: '8px', 
                            border: '1px solid #e0e0e0',
                            padding: '10px'
                          }}
                        />
                        <ReferenceLine x={0.5} stroke="#d1d5db" strokeDasharray="3 3" />
                        <Bar 
                          dataKey="impact" 
                          radius={[0, 4, 4, 0]}
                          onClick={(data) => setShowTip(showTip === data.variable ? null : data.variable)}
                        >
                          {mockSensitivityData.map((entry, index) => (
                            <Cell 
                              key={`cell-${index}`} 
                              fill={entry.color}
                              cursor="pointer"
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  
                  {/* Tooltips interativos que aparecem ao clicar nas barras */}
                  {showTip === 'Preço de venda' && (
                    <div className="mt-2 bg-blue-50 p-3 rounded-md border border-blue-200 relative">
                      <button 
                        className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
                        onClick={() => setShowTip(null)}
                      >
                        ✕
                      </button>
                      <h4 className="font-medium text-blue-800 mb-1">Preço de venda</h4>
                      <p className="text-sm text-blue-900">
                        Este é o fator mais importante para seu lucro. A cada R$10 de aumento no preço/@, seu lucro aumenta em média R$1.500 por lote.
                      </p>
                      <div className="mt-2 text-xs text-blue-700 flex items-center">
                        <ExternalLink size={12} className="mr-1" />
                        <a href="#" className="underline">Ver estratégias para melhorar preço de venda</a>
                      </div>
                    </div>
                  )}
                  
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-lg border shadow-sm">
                      <h4 className="text-base font-medium text-gray-700 mb-2">Como interpretar este gráfico</h4>
                      <ul className="space-y-3 text-sm text-gray-600">
                        <li className="flex items-start">
                          <div className="w-3 h-3 mt-1 mr-2 rounded-full bg-blue-600"></div>
                          <span><strong className="text-blue-600">Preço de venda</strong>: Principal fator para aumentar o lucro. Foque em estratégias de comercialização e momento de venda.</span>
                        </li>
                        <li className="flex items-start">
                          <div className="w-3 h-3 mt-1 mr-2 rounded-full bg-green-600"></div>
                          <span><strong className="text-green-600">Taxa de ganho de peso</strong>: Segundo fator mais importante. Invista em nutrição animal e genética.</span>
                        </li>
                        <li className="flex items-start">
                          <div className="w-3 h-3 mt-1 mr-2 rounded-full bg-red-600"></div>
                          <span><strong className="text-red-600">Preço de compra</strong>: Impacto moderado a alto. Estratégias de compra podem fazer diferença significativa.</span>
                        </li>
                      </ul>
                    </div>
                    
                    <div className="bg-white p-4 rounded-lg border shadow-sm">
                      <h4 className="text-base font-medium text-gray-700 mb-2">Estratégias Recomendadas</h4>
                      <div className="space-y-3">
                        <div className="flex items-center">
                          <div className="rounded-full bg-green-100 p-2 mr-3">
                            <TrendingUp size={16} className="text-green-600" />
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-800">Acompanhe mercado futuro da B3</p>
                            <p className="text-xs text-gray-500">Plano de venda baseado nos melhores momentos</p>
                          </div>
                        </div>
                        <div className="flex items-center">
                          <div className="rounded-full bg-blue-100 p-2 mr-3">
                            <Activity size={16} className="text-blue-600" />
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-800">Otimize nutrição animal</p>
                            <p className="text-xs text-gray-500">Melhor custo-benefício para ganho de peso</p>
                          </div>
                        </div>
                        <div className="flex items-center">
                          <div className="rounded-full bg-purple-100 p-2 mr-3">
                            <RefreshCw size={16} className="text-purple-600" />
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-800">Avalie simulações periódicas</p>
                            <p className="text-xs text-gray-500">Ajuste estratégia conforme mercado</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 bg-gray-50 p-3 rounded-lg border border-gray-200">
                    <div className="text-xs text-gray-500 space-y-1">
                      <div className="flex justify-between">
                        <span>Média do setor:</span>
                        <div className="flex items-center">
                          <span>Preço de venda: 65% </span>
                          <span className="ml-1 text-green-600 text-xs">▲20%</span>
                        </div>
                      </div>
                      <div className="flex justify-between">
                        <span>Sua simulação anterior:</span>
                        <div className="flex items-center">
                          <span>Preço de venda: 79% </span>
                          <span className="ml-1 text-green-600 text-xs">▲6%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Correlações */}
              {activeTab === 2 && (
                <div>
                  <div className="bg-blue-50 p-3 rounded-md mb-4 border-l-4 border-blue-500">
                    <p className="text-blue-800">
                      <strong>Interpretação:</strong> Este gráfico mostra a relação entre o preço de venda e o lucro obtido. Cada ponto representa uma simulação, e a linha de tendência indica que preços maiores geralmente resultam em lucros maiores.
                    </p>
                  </div>
                  
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <ScatterChart
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="precoVenda" 
                          name="Preço" 
                          unit="/@" 
                          label={{ value: 'Preço de Venda (R$/@)', position: 'bottom' }}
                          domain={['dataMin - 5', 'dataMax + 5']}
                          tickFormatter={(value) => `R${value}`}
                        />
                        <YAxis 
                          dataKey="lucro" 
                          name="Lucro" 
                          unit="" 
                          label={{ value: 'Lucro (R$)', angle: -90, position: 'left' }}
                          tickFormatter={(value) => `R${value}`}
                        />
                        <Tooltip 
                          cursor={{ strokeDasharray: '3 3' }} 
                          formatter={(value, name) => {
                            if (name === "lucro") {
                              return [`R$ ${value.toFixed(2)}`, 'Lucro Esperado']
                            }
                            return [`R$ ${value.toFixed(2)}/@`, 'Preço de Venda']
                          }}
                          contentStyle={{ 
                            backgroundColor: 'white', 
                            borderRadius: '8px', 
                            border: '1px solid #e0e0e0',
                            padding: '10px'
                          }}
                        />
                        <ReferenceLine y={0} stroke="#d1d5db" />
                        <Scatter 
                          name="Simulações" 
                          data={mockScatterData} 
                          fill="#10B981" 
                          fillOpacity={0.6}
                        />
                        <Line 
                          type="monotone" 
                          dataKey="lucro" 
                          data={
                            // Criar linha de tendência com 10 pontos
                            Array.from({ length: 10 }, (_, i) => {
                              const precoVenda = 290 + (i * 8);
                              return {
                                precoVenda,
                                lucro: precoVenda * 15 - 3800
                              };
                            })
                          }
                          stroke="#1E40AF"
                          strokeWidth={2}
                          dot={false}
                        />
                      </ScatterChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-3 rounded-lg border shadow-sm">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">Correlação</h4>
                      <p className="text-lg font-bold text-blue-600">+0.92 (muito forte)</p>
                      <p className="text-xs text-gray-500">O preço de venda explica 84% da variação no lucro</p>
                    </div>
                    
                    <div className="bg-white p-3 rounded-lg border shadow-sm">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">Ponto de Equilíbrio</h4>
                      <p className="text-lg font-bold text-green-600">R$ 253,33/@</p>
                      <p className="text-xs text-gray-500">Preço mínimo para obter lucro</p>
                    </div>
                    
                    <div className="bg-white p-3 rounded-lg border shadow-sm">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">Impacto</h4>
                      <p className="text-lg font-bold text-purple-600">R$ 150 por @ adicional</p>
                      <p className="text-xs text-gray-500">Cada R$ 10/@ aumenta o lucro em R$ 1.500</p>
                    </div>
                  </div>
                  
                  <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
                    <h4 className="font-medium text-green-800 mb-2 flex items-center">
                      <Check size={16} className="mr-2" />
                      Oportunidade de otimização
                    </h4>
                    <p className="text-sm text-green-700">
                      Com base nas análises, sugerimos focar na negociação de venda no momento em que o preço estiver acima de R$ 330/@, o que 
                      resultaria em um lucro esperado 15% maior que a média do mercado.
                    </p>
                    <button className="mt-2 text-xs text-white bg-green-600 px-3 py-1 rounded-md hover:bg-green-700 transition-colors">
                      Ver plano detalhado
                    </button>
                  </div>
                </div>
              )}
            </div>
            
            {/* Exportação e controles */}
            <div className="border-t border-gray-200 pt-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div className="flex flex-col md:flex-row items-start md:items-center gap-3">
                <button 
                  className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 transition-colors"
                  onClick={() => alert('Salvando simulação no histórico...')}
                >
                  <Database size={16} className="mr-2" />
                  Salvar no Histórico
                </button>
                <div className="text-sm text-gray-500 flex items-center">
                  <Clock size={14} className="mr-1" />
                  Última análise: 09/04/2025 - 14:32
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                <div className="bg-gray-100 p-2 rounded-md">
                  <span className="text-xs text-gray-500 block mb-1">Exportar Relatório</span>
                  <div className="flex space-x-1">
                    <button 
                      className="flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-50 transition-colors"
                      onClick={() => exportData('PDF')}
                    >
                      <Download size={14} className="mr-1 text-red-600" />
                      <span className="text-sm">PDF</span>
                    </button>
                    <button 
                      className="flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-50 transition-colors"
                      onClick={() => exportData('Excel')}
                    >
                      <Download size={14} className="mr-1 text-green-600" />
                      <span className="text-sm">Excel</span>
                    </button>
                  </div>
                </div>
                
                <div className="bg-gray-100 p-2 rounded-md">
                  <span className="text-xs text-gray-500 block mb-1">Exportar Dados</span>
                  <div className="flex space-x-1">
                    <button 
                      className="flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-50 transition-colors"
                      onClick={() => exportData('CSV')}
                    >
                      <Download size={14} className="mr-1 text-blue-600" />
                      <span className="text-sm">CSV</span>
                    </button>
                    <button 
                      className="flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-50 transition-colors"
                      onClick={() => exportData('JSON')}
                    >
                      <Download size={14} className="mr-1 text-purple-600" />
                      <span className="text-sm">JSON</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-gray-100 to-gray-200 text-gray-600 py-4 border-t">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <div className="flex items-center mb-1">
                <Target className="mr-2 text-green-700" size={20} />
                <span className="font-semibold text-gray-700">Aplicativo de Análise de Sensibilidade para Negociação de Gado</span>
              </div>
              <p className="text-sm text-gray-500">&copy; 2025 - Todos os direitos reservados</p>
            </div>
            
            <div className="flex flex-wrap justify-center gap-3">
              <div className="text-center">
                <h4 className="text-xs font-medium text-gray-700 mb-1">Performance</h4>
                <p className="text-xs text-gray-500">Tempo de simulação: &lt; 5s para 10.000 iterações</p>
              </div>
              
              <div className="text-center">
                <h4 className="text-xs font-medium text-gray-700 mb-1">Suporte</h4>
                <p className="text-xs text-gray-500">help@analisegado.com</p>
              </div>
              
              <div className="text-center">
                <h4 className="text-xs font-medium text-gray-700 mb-1">Versão</h4>
                <p className="text-xs text-gray-500">v1.2.4 | Atualizado: 02/04/2025</p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default CattleAnalysisApp;