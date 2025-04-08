import React from 'react';
import './App.css';
import './globals.css'; // Importante: Importar o globals.css
import IMSPVMosaico from './components/mosaico/imspv-mosaico-drill';

function App() {
  return (
    <div className="App min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <IMSPVMosaico />
    </div>
  );
}

export default App;