import React, { useState } from 'react';

const HeatmapCell = ({ value }) => {
  const getColor = (val) => {
    if (val === 0) return 'bg-gray-200'; // valor vazio
    if (val === 1) return 'bg-red-500';   // vermelho escuro
    if (val === 2) return 'bg-red-300';   // vermelho mais claro
    if (val === 3) return 'bg-gray-400';  // cinza
    if (val === 4) return 'bg-blue-400';  // azul médio
    return 'bg-blue-600';                 // azul escuro para 5
  };

  return (
    <td className={`${getColor(value)} w-12 h-12 text-center border border-gray-100 text-white`}>
      {value > 0 ? value : '-'}
    </td>
  );
};

const Heatmap = () => {
  const [title, setTitle] = useState('Assessment Heatmap');
  const [rows, setRows] = useState(10);
  const [cols, setCols] = useState(10);
  const [data, setData] = useState(Array(10).fill(Array(10).fill(0)));
  const [inputData, setInputData] = useState('');

  // Função para processar os dados do textarea
  const processData = () => {
    try {
      // Converte string em matriz de números
      const newData = inputData
        .trim()
        .split('\n')
        .map(row => row.split(/[,\s]+/).map(cell => cell === '-' ? 0 : Number(cell)));
      
      setData(newData);
      setRows(newData.length);
      setCols(newData[0].length);
    } catch (error) {
      alert('Erro ao processar dados. Verifique o formato.');
    }
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="p-2 border rounded mb-2 w-full"
          placeholder="Digite o título"
        />
        <textarea
          className="w-full p-2 border rounded mb-2"
          rows="10"
          placeholder="Cole seus dados aqui (números separados por espaço ou vírgula, use '-' para valores vazios)"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
        />
        <button
          onClick={processData}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Atualizar Heatmap
        </button>
      </div>

      <div className="overflow-x-auto">
        <div className="mb-4 text-lg font-bold">{title}</div>
        <table className="border-collapse">
          <thead>
            <tr>
              <th className="p-2">Questions</th>
              <th className="p-2">Self</th>
              {Array.from({ length: cols - 1 }, (_, i) => (
                <th key={i} className="p-2">L{i + 1}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i}>
                <td className="p-2 font-medium">Q{i + 1}</td>
                {row.map((value, j) => (
                  <HeatmapCell key={j} value={value} />
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        <div className="mt-4 flex items-center gap-2">
          <span className="text-sm">Score Legend:</span>
          {[1, 2, 3, 4, 5].map(value => (
            <div key={value} className="flex items-center gap-1">
              <div className={`w-6 h-6 ${
                value === 1 ? 'bg-red-500' : 
                value === 2 ? 'bg-red-300' : 
                value === 3 ? 'bg-gray-400' : 
                value === 4 ? 'bg-blue-400' : 
                'bg-blue-600'
              } border border-gray-200 text-white flex items-center justify-center`}>
                <span className="text-sm">{value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Heatmap;