import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Info, Calendar, Scale, Clock } from 'lucide-react';

// Definindo a interface para o tipo Curral
interface Curral {
  curral: string;
  imspv: number;
  consumoMS: number;
  pesoEntrada: number;
  pesoAtual: number;
  diasConf: number;
  tipoRacao: string;
  diasRacao: number;
}

// Interface para dados do gráfico
interface PesoDataPoint {
  name: string;
  value: number;
  label: string;
  fill: string; // Adicionado para armazenar a cor
}

// Dados simulados com maior variabilidade
const simulatedData = [
  { CURRAL: 'C01', IMS_PV: 3.25, CONSUMO_MS: 14.6, PESO_ENTRADA: 380, PESO_MEDIO_ATUAL: 520, DIAS_CONF: 75, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 30 },
  { CURRAL: 'C02', IMS_PV: 2.85, CONSUMO_MS: 12.8, PESO_ENTRADA: 410, PESO_MEDIO_ATUAL: 490, DIAS_CONF: 42, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 22 },
  { CURRAL: 'C03', IMS_PV: 3.45, CONSUMO_MS: 15.1, PESO_ENTRADA: 370, PESO_MEDIO_ATUAL: 530, DIAS_CONF: 80, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 35 },
  { CURRAL: 'C04', IMS_PV: 2.05, CONSUMO_MS: 9.2, PESO_ENTRADA: 390, PESO_MEDIO_ATUAL: 435, DIAS_CONF: 25, TIPO_RACAO_ATUAL: 'Crescimento', TIPO_DIAS_RACAO: 25 },
  { CURRAL: 'C05', IMS_PV: 1.85, CONSUMO_MS: 8.5, PESO_ENTRADA: 450, PESO_MEDIO_ATUAL: 465, DIAS_CONF: 20, TIPO_RACAO_ATUAL: 'Adaptação', TIPO_DIAS_RACAO: 20 },
  { CURRAL: 'C06', IMS_PV: 1.65, CONSUMO_MS: 7.2, PESO_ENTRADA: 420, PESO_MEDIO_ATUAL: 440, DIAS_CONF: 15, TIPO_RACAO_ATUAL: 'Adaptação', TIPO_DIAS_RACAO: 15 },
  { CURRAL: 'C07', IMS_PV: 2.95, CONSUMO_MS: 13.0, PESO_ENTRADA: 400, PESO_MEDIO_ATUAL: 505, DIAS_CONF: 60, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 25 },
  { CURRAL: 'C08', IMS_PV: 3.15, CONSUMO_MS: 14.0, PESO_ENTRADA: 380, PESO_MEDIO_ATUAL: 525, DIAS_CONF: 70, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 30 },
  { CURRAL: 'C09', IMS_PV: 2.15, CONSUMO_MS: 9.8, PESO_ENTRADA: 430, PESO_MEDIO_ATUAL: 465, DIAS_CONF: 22, TIPO_RACAO_ATUAL: 'Crescimento', TIPO_DIAS_RACAO: 22 },
  { CURRAL: 'C10', IMS_PV: 3.55, CONSUMO_MS: 15.5, PESO_ENTRADA: 365, PESO_MEDIO_ATUAL: 535, DIAS_CONF: 85, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 40 },
  { CURRAL: 'C11', IMS_PV: 2.25, CONSUMO_MS: 10.5, PESO_ENTRADA: 425, PESO_MEDIO_ATUAL: 470, DIAS_CONF: 28, TIPO_RACAO_ATUAL: 'Crescimento', TIPO_DIAS_RACAO: 28 },
  { CURRAL: 'C12', IMS_PV: 3.35, CONSUMO_MS: 14.8, PESO_ENTRADA: 375, PESO_MEDIO_ATUAL: 515, DIAS_CONF: 72, TIPO_RACAO_ATUAL: 'Terminação', TIPO_DIAS_RACAO: 32 },
];

// Gere mais 88 currais para ter 100 no total (grid 10x10)
for (let i = 13; i <= 100; i++) {
  // Maior variação no IMS_PV (1.5 a 3.8)
  const imspv = 1.5 + Math.random() * 2.3;
  
  // Maior variação no peso de entrada (350 a 450)
  const pesoEntrada = 350 + Math.random() * 100;
  
  // Maior variação no ganho (30 a 180kg)
  const ganho = 30 + Math.random() * 150;
  const pesoAtual = pesoEntrada + ganho;
  
  // Maior variação nos dias de confinamento (10 a 90 dias)
  const diasConf = Math.floor(10 + Math.random() * 80);
  
  let tipoRacao = 'Adaptação';
  if (diasConf > 25) tipoRacao = 'Crescimento';
  if (diasConf > 40) tipoRacao = 'Terminação';
  
  const diasRacao = Math.min(diasConf, tipoRacao === 'Terminação' ? 40 : tipoRacao === 'Crescimento' ? 30 : 15);
  
  simulatedData.push({
    CURRAL: `C${i.toString().padStart(2, '0')}`,
    IMS_PV: imspv,
    CONSUMO_MS: (imspv * pesoAtual / 100),
    PESO_ENTRADA: pesoEntrada,
    PESO_MEDIO_ATUAL: pesoAtual,
    DIAS_CONF: diasConf,
    TIPO_RACAO_ATUAL: tipoRacao,
    TIPO_DIAS_RACAO: diasRacao
  });
}

const IMSPVMosaico = () => {
  const [currais, setCurrais] = useState<Curral[]>([]);
  const [selectedCurral, setSelectedCurral] = useState<Curral | null>(null);
  const [stats, setStats] = useState({ media: 2.4547, desvio: 0.3737 });

  useEffect(() => {
    // Simulação da leitura do arquivo Excel
    const loadData = async () => {
      // Use os dados simulados em vez de ler um arquivo Excel
      const jsonData = simulatedData;
      
      const curraisMap = new Map<string, Curral>();
      jsonData.forEach(row => {
        curraisMap.set(row.CURRAL, {
          curral: row.CURRAL,
          imspv: row.IMS_PV,
          consumoMS: row.CONSUMO_MS,
          pesoEntrada: row.PESO_ENTRADA,
          pesoAtual: row.PESO_MEDIO_ATUAL,
          diasConf: row.DIAS_CONF,
          tipoRacao: row.TIPO_RACAO_ATUAL,
          diasRacao: row.TIPO_DIAS_RACAO
        });
      });
      
      const curraisArray: Curral[] = Array.from(curraisMap.values())
        .sort((a, b) => b.imspv - a.imspv);
      
      setCurrais(curraisArray);
      
      // Calcular estatísticas reais dos dados
      const imspvValues = curraisArray.map(c => c.imspv);
      const media = imspvValues.reduce((sum, val) => sum + val, 0) / imspvValues.length;
      const variances = imspvValues.map(val => Math.pow(val - media, 2));
      const variance = variances.reduce((sum, val) => sum + val, 0) / variances.length;
      const desvio = Math.sqrt(variance);
      
      setStats({ media, desvio });
    };

    loadData();
  }, []);

  const getFaixaColor = (imspv: number): string => {
    if (imspv > stats.media + 2 * stats.desvio) return 'bg-blue-500';
    if (imspv > stats.media + stats.desvio) return 'bg-green-500';
    if (imspv > stats.media) return 'bg-yellow-500';
    if (imspv > stats.media - stats.desvio) return 'bg-orange-400';
    if (imspv > stats.media - 2 * stats.desvio) return 'bg-red-500';
    return 'bg-gray-800';
  };

  const getFaixaLabel = (imspv: number): string => {
    if (imspv > stats.media + 2 * stats.desvio) return 'Muito Alto';
    if (imspv > stats.media + stats.desvio) return 'Alto';
    if (imspv > stats.media) return 'Acima média';
    if (imspv > stats.media - stats.desvio) return 'Abaixo média';
    if (imspv > stats.media - 2 * stats.desvio) return 'Alerta';
    return 'Crítico';
  };

  const renderCell = (curralData: Curral | null) => {
    if (!curralData) return <div className="bg-gray-100 rounded-lg h-full" />;
    
    const bgColor = getFaixaColor(curralData.imspv);
    return (
      <div 
        className={`p-1 sm:p-2 ${bgColor} hover:opacity-80 cursor-pointer transition-all rounded-lg h-full flex items-center justify-center`}
        onClick={() => setSelectedCurral(curralData)}
      >
        <div className="text-white text-center w-full">
          <div className="font-bold text-xs sm:text-lg">{curralData.curral}</div>
          <div className="text-[10px] sm:text-base">{curralData.imspv.toFixed(2)}%</div>
        </div>
      </div>
    );
  };

  const renderDrillDown = () => {
    if (!selectedCurral) return null;

    const pesoData: PesoDataPoint[] = [
      {
        name: 'Peso Entrada',
        value: selectedCurral.pesoEntrada,
        label: 'kg',
        fill: '#16a34a' // Verde mais vibrante
      },
      {
        name: 'Peso Atual',
        value: selectedCurral.pesoAtual,
        label: 'kg',
        fill: '#2563eb' // Azul vibrante
      }
    ];

    return (
      <div className="p-2 sm:p-4 bg-gray-50 rounded-lg mt-4">
        <div className="flex items-center gap-2 mb-4">
          <Info size={16} className="sm:w-5 sm:h-5" />
          <h3 className="font-bold text-sm sm:text-base">
            {selectedCurral.curral} - IMS_PV: {selectedCurral.imspv.toFixed(2)}%
          </h3>
          <span className="text-xs sm:text-sm text-gray-500">
            ({getFaixaLabel(selectedCurral.imspv)})
          </span>
        </div>

        {/* Painel de Indicadores mais compacto em mobile */}
        <div className="grid grid-cols-2 gap-2 sm:gap-4 mb-4 sm:mb-6 p-2 sm:p-4 bg-white rounded-lg shadow-sm">
          <div className="space-y-3 sm:space-y-4">
            <div className="flex items-center gap-2">
              <Scale className="text-blue-500" size={16} />
              <div>
                <div className="text-xs sm:text-sm text-gray-500">Consumo MS</div>
                <div className="font-bold text-sm sm:text-base">{selectedCurral.consumoMS.toFixed(2)} kg/dia</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="text-green-500" size={16} />
              <div>
                <div className="text-xs sm:text-sm text-gray-500">Dias Confinamento</div>
                <div className="font-bold text-sm sm:text-base">{selectedCurral.diasConf} dias</div>
              </div>
            </div>
          </div>
          <div className="space-y-3 sm:space-y-4">
            <div>
              <div className="text-xs sm:text-sm text-gray-500">Tipo de Ração</div>
              <div className="font-bold text-sm sm:text-base">{selectedCurral.tipoRacao}</div>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="text-orange-500" size={16} />
              <div>
                <div className="text-xs sm:text-sm text-gray-500">Dias na Ração</div>
                <div className="font-bold text-sm sm:text-base">{selectedCurral.diasRacao} dias</div>
              </div>
            </div>
          </div>
        </div>

        {/* Gráfico de Pesos com cores vibrantes e eixo Y fixo */}
        <div className="h-48 sm:h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={pesoData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" />
              <YAxis 
                domain={[300, 600]} // Intervalo fixo para o eixo Y
                ticks={[300, 350, 400, 450, 500, 550, 600]} // Marcações específicas
                label={{ 
                  value: 'Peso (kg)', 
                  angle: -90, 
                  position: 'insideLeft', 
                  style: { textAnchor: 'middle', fontSize: '0.75rem' } 
                }}
              />
              <Tooltip 
                formatter={(value: any, name: string) => [
                  `${typeof value === 'number' ? value.toFixed(2) : value} kg`,
                  name
                ]}
              />
              <Bar 
                dataKey="value" 
                name="Peso" 
                barSize={60}
                radius={[8, 8, 0, 0]} 
                fill="#8884d8" // Esta cor será sobrescrita pela propriedade 'fill' de cada item
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Legenda do gráfico */}
        <div className="flex justify-center gap-4 sm:gap-8 mt-2 mb-2 sm:mb-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 sm:w-4 sm:h-4 rounded" style={{ backgroundColor: '#16a34a' }}></div>
            <span className="text-xs sm:text-sm">Peso Entrada</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 sm:w-4 sm:h-4 rounded" style={{ backgroundColor: '#2563eb' }}></div>
            <span className="text-xs sm:text-sm">Peso Atual</span>
          </div>
        </div>

        {/* Indicadores de Variação */}
        <div className="mt-2 sm:mt-4 p-2 sm:p-3 bg-blue-50 rounded-lg">
          <div className="text-xs sm:text-sm text-blue-800">
            Ganho de Peso: {(selectedCurral.pesoAtual - selectedCurral.pesoEntrada).toFixed(2)} kg
          </div>
          <div className="text-xs sm:text-sm text-blue-800">
            Variação: {((selectedCurral.pesoAtual - selectedCurral.pesoEntrada) / selectedCurral.pesoEntrada * 100).toFixed(2)}%
          </div>
          <div className="text-xs sm:text-sm text-blue-800">
            Ganho Diário: {((selectedCurral.pesoAtual - selectedCurral.pesoEntrada) / selectedCurral.diasConf).toFixed(2)} kg/dia
          </div>
        </div>
      </div>
    );
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader className="px-2 py-3 sm:px-6 sm:py-4">
        <CardTitle className="text-xl sm:text-2xl text-center">Mosaico IMS_PV - Confinamento</CardTitle>
        <div className="text-sm text-gray-500 text-center">
          Ingestão de Matéria Seca / Peso Vivo (%)
        </div>
      </CardHeader>
      
      <CardContent className="px-2 sm:px-6">
        {/* Grid com menos colunas em telas pequenas */}
        <div className="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-1 mb-4">
          {currais.slice(0, 100).map((curral, i) => (
            <div key={`curral-${i}`} className="aspect-square">
              {renderCell(curral || null)}
            </div>
          ))}
        </div>

        {/* Legenda em duas colunas em mobile */}
        <div className="grid grid-cols-2 sm:flex sm:flex-wrap gap-2 sm:gap-4 mb-4 text-xs sm:text-sm">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 sm:w-4 sm:h-4 bg-blue-500 rounded"></div>
            <span>Muito Alto (&gt;{(stats.media + 2 * stats.desvio).toFixed(2)}%)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 sm:w-4 sm:h-4 bg-green-500 rounded"></div>
            <span>Alto ({(stats.media + stats.desvio).toFixed(2)}-{(stats.media + 2 * stats.desvio).toFixed(2)}%)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 sm:w-4 sm:h-4 bg-yellow-500 rounded"></div>
            <span>Acima média ({stats.media.toFixed(2)}-{(stats.media + stats.desvio).toFixed(2)}%)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 sm:w-4 sm:h-4 bg-orange-400 rounded"></div>
            <span>Abaixo média ({(stats.media - stats.desvio).toFixed(2)}-{stats.media.toFixed(2)}%)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 sm:w-4 sm:h-4 bg-red-500 rounded"></div>
            <span>Alerta ({(stats.media - 2 * stats.desvio).toFixed(2)}-{(stats.media - stats.desvio).toFixed(2)}%)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 sm:w-4 sm:h-4 bg-gray-800 rounded"></div>
            <span>Crítico (&lt;{(stats.media - 2 * stats.desvio).toFixed(2)}%)</span>
          </div>
        </div>

        {renderDrillDown()}
      </CardContent>
    </Card>
  );
};

export default IMSPVMosaico;