# PROMPT: ANÁLISE E VISUALIZAÇÃO DE DADOS DE GESTÃO DE FROTAS

## CONTEXTO

Você receberá uma planilha CSV contendo dados de gestão de frota industrial com informações sobre:

- Dados financeiros (orçado vs realizado)
- Dados operacionais (horas/km)
- Informações de equipamentos e reformas
- Métricas de eficiência
- Serviços de terceiros

## ESTRUTURA DA PLANILHA

A planilha está organizada em quatro seções principais, cada uma com características específicas:

### 1. CABEÇALHO E RESUMO (Linhas 1-6)

- Título do documento (linha 1): "ACOMPANHAMENTO JUSTIFICATIVA ORÇAMENTO AUTOMOTIVO"
  
- Resumo financeiro geral:
  
  ```
  Orçado,Abril a Setembro," 9.630.533,00 "
  Realizado,Abril a Setembro," 11.921.210,00 "
  Diferença,," 2.290.677,00 "
  ```
  

### 2. SEÇÃO DE REFORMAS (Linhas 7-42)

Início: Linha que contém "Reformas,Modelo,Orçada Abril a Setembro,Realizada Abril a Setembro,Diferença"
Fim: Linha anterior a "EQUIPAMENTOS MOTORIZADOS"

Estrutura:

```
Reformas,Modelo,Orçada Abril a Setembro,Realizada Abril a Setembro,Diferença
14308,Transbordo, -   ," 25.935,00 ",
12309,Transbordo, -   ," 24.365,00 ",
```

Características:

- Valores monetários com separador de milhares (.) e decimal (,)
- Campos vazios representados por " - " ou campos em branco
- Sempre possui ID do equipamento e modelo

### 3. SEÇÃO DE EQUIPAMENTOS MOTORIZADOS (Linhas 43-120)

Início: Linha que contém "EQUIPAMENTOS MOTORIZADOS"
Fim: Linha anterior a "IMPLEMENTOS"

Estrutura:

```
Frota,Modelo,Classe,Orçado Abril a Setembro,Realizado Abril a Setembro,Falta Realizar,Formato Orçado(mês),Baixas,Antecipação,Estouro,Postergação,Economia,Horas/km Orçadas,Horas/km Realizadas,Diferença,Custo Hora/km Orçada,Custo Hora/km Realizada,Diferença
1914,VW 26.280,Bombeiro," 138.154,50 "," 130.788,78 ",,,,,,,"-7.365,72 "," 2.130,00 "," 2.095,10 ","-34,90",80,"62,43","-17,57"
```

Características:

- Dados operacionais e financeiros combinados
- Inclui métricas de eficiência (custo/hora, taxa de utilização)
- Agrupamento implícito por tipo de equipamento

### 4. SEÇÃO DE IMPLEMENTOS (Linhas 121-230)

Início: Linha que contém "IMPLEMENTOS"
Fim: Linha anterior a "TERCEIROS"

Estrutura:

```
Frota,Modelo,Classe,Orçado Total,Realizado Abril a Setembro,Falta Realizar,Formato Orçado(mês),Baixas,Antecipação,Estouro,Postergação(Reforma),Economia
316,TRANSBORDO,TRANSBORDO," 40.000,00 "," 26.853,87 "," 20.000,00 "," 3.333,33 "," 20.000,00 ",," 6.853,87 ",,
```

### 5. SEÇÃO DE TERCEIROS (Linhas 231 em diante)

Início: Linha que contém "TERCEIROS"
Fim: Final do arquivo

Estrutura:

```
Operação,Valor
Aviação Aerea," 419.643,00 "
Controle Serviços," 12.451,93 "
```

## PARTICULARIDADES DOS DADOS

### 1. FORMATO DOS VALORES

1. Valores Monetários
  
  ```python
  def converter_valor_monetario(valor):
   """
   Converte strings de valores monetários para float
   Exemplos de entrada:
   " 9.630.533,00 "  -> 9630533.00
   " -   "           -> 0.0
   "R$ 1.234,56"     -> 1234.56
   "(1.234,56)"      -> -1234.56
   """
   if isinstance(valor, str):
       # Remove espaços e caracteres especiais
       valor = valor.strip()
       if valor == "-" or not valor:
           return 0.0
  
       # Remove R$ se existir
       valor = valor.replace('R$ ', '')
  
       # Trata valores negativos em parênteses
       is_negative = False
       if valor.startswith('(') and valor.endswith(')'):
           is_negative = True
           valor = valor[1:-1]
  
       # Converte para float
       valor = float(valor.replace('.', '').replace(',', '.'))
  
       return -valor if is_negative else valor
   return valor
  ```
  

# Exemplo de uso:

assert converter_valor_monetario(" 9.630.533,00 ") == 9630533.00
assert converter_valor_monetario(" - ") == 0.0
assert converter_valor_monetario("R$ 1.234,56") == 1234.56
assert converter_valor_monetario("(1.234,56)") == -1234.56

````
2. Valores Numéricos (horas/km)
```python
def converter_valor_numerico(valor):
    """
    Converte strings de valores numéricos para float
    Exemplos de entrada:
    "1.234,56"    -> 1234.56
    "123"         -> 123.0
    " -   "       -> 0.0
    "-123,45"     -> -123.45
    """
    if isinstance(valor, str):
        valor = valor.strip()
        if not valor or valor == "-":
            return 0.0
        return float(valor.replace('.', '').replace(',', '.'))
    return valor

# Exemplo de uso:
assert converter_valor_numerico("1.234,56") == 1234.56
assert converter_valor_numerico("123") == 123.0
assert converter_valor_numerico(" -   ") == 0.0
assert converter_valor_numerico("-123,45") == -123.45
````

### 2. TRATAMENTO DE CÉLULAS VAZIAS E VALIDAÇÃO

```python
def validar_celula(valor):
    """
    Verifica se uma célula está vazia ou contém apenas espaços/traços
    Retorna True se a célula for considerada vazia
    """
    if valor is None:
        return True
    if isinstance(valor, str):
        valor = valor.strip()
        return valor == "" or valor == "-" or valor.isspace()
    return False

def tratar_valor_ausente(valor, tipo='numerico'):
    """
    Trata células vazias e converte valores conforme o tipo
    """
    if validar_celula(valor):
        return 0.0
    if tipo == 'monetario':
        return converter_valor_monetario(valor)
    return converter_valor_numerico(valor)

def validar_linha_completa(linha, tipo_secao):
    """
    Valida se uma linha tem todos os campos obrigatórios conforme a seção
    """
    if not linha or len(linha) < 3:
        return False

    # Validações específicas por seção
    validacoes = {
        'reformas': lambda l: l[0] and l[1],  # ID e Modelo
        'motorizados': lambda l: l[0] and l[1] and l[2],  # Frota, Modelo e Classe
        'implementos': lambda l: l[0] and l[1] and l[2],  # Frota, Modelo e Classe
        'terceiros': lambda l: l[0] and l[1]  # Operação e Valor
    }

    if tipo_secao in validacoes:
        return validacoes[tipo_secao](linha)

    return True

def normalizar_linha(linha, tipo_secao):
    """
    Normaliza uma linha de dados conforme a seção
    """
    if not validar_linha_completa(linha, tipo_secao):
        return None

    normalizadores = {
        'motorizados': {
            'frota': lambda x: str(x).strip(),
            'modelo': lambda x: str(x).strip(),
            'classe': lambda x: str(x).strip(),
            'orcado': lambda x: tratar_valor_ausente(x, 'monetario'),
            'realizado': lambda x: tratar_valor_ausente(x, 'monetario'),
            'horas_orcadas': lambda x: tratar_valor_ausente(x, 'numerico'),
            'horas_realizadas': lambda x: tratar_valor_ausente(x, 'numerico')
        }
        # Adicionar outros normalizadores conforme necessário
    }

    if tipo_secao in normalizadores:
        dados = {}
        for campo, normalizador in normalizadores[tipo_secao].items():
            indice = obter_indice_campo(campo, tipo_secao)
            if indice < len(linha):
                dados[campo] = normalizador(linha[indice])
        return dados

    return None
```

### 3. PROCESSAMENTO DE DADOS

```python
class ProcessadorDados:
    def __init__(self):
        self.secoes = {
            'reformas': [],
            'motorizados': [],
            'implementos': [],
            'terceiros': []
        }

    def identificar_secao(self, linha):
        """
        Identifica a qual seção pertence uma linha
        """
        if isinstance(linha, str):
            if "EQUIPAMENTOS MOTORIZADOS" in linha:
                return "motorizados"
            elif "IMPLEMENTOS" in linha:
                return "implementos"
            elif "TERCEIROS" in linha:
                return "terceiros"
        return None

    def processar_arquivo(self, linhas):
        """
        Processa o arquivo CSV completo
        """
        secao_atual = 'reformas'  # Começa com reformas
        for linha in linhas:
            # Identifica mudança de seção
            nova_secao = self.identificar_secao(linha)
            if nova_secao:
                secao_atual = nova_secao
                continue

            # Processa a linha
            dados = normalizar_linha(linha, secao_atual)
            if dados:
                self.secoes[secao_atual].append(dados)

    def calcular_metricas(self):
        """
        Calcula métricas agregadas para cada seção
        """
        metricas = {}
        for secao, dados in self.secoes.items():
            metricas[secao] = {
                'total_orcado': sum(d.get('orcado', 0) for d in dados),
                'total_realizado': sum(d.get('realizado', 0) for d in dados),
                'quantidade': len(dados)
            }
            if secao == 'motorizados':
                metricas[secao].update({
                    'total_horas_orcadas': sum(d.get('horas_orcadas', 0) for d in dados),
                    'total_horas_realizadas': sum(d.get('horas_realizadas', 0) for d in dados)
                })
        return metricas
```

## OBJETIVO

Desenvolver um sistema de análise e visualização que permita:

### 1. Monitoramento de Desvios Orçamentários

- Variação entre orçado e realizado por classe
- Identificação de maiores desvios
- Análise de tendências de gastos

### 2. Análise de Eficiência Operacional

- Taxa de utilização de equipamentos
- Custo por hora/km operado
- Comparativo de eficiência entre classes

### 3. Gestão de Manutenção

- Custos de manutenção por equipamento
- Frequência de intervenções
- Identificação de equipamentos críticos

### 4. Suporte à Tomada de Decisão

- Indicadores de performance
- Alertas de desvios significativos
- Recomendações baseadas em dados

## IMPLEMENTAÇÃO

### 1. Estrutura de Dados para Visualização

```javascript
const DashboardConfig = {
  // Configuração global
  global: {
    periodo: {
      inicio: 'Abril',
      fim: 'Setembro',
      ano: '2024'
    },
    atualizacao: '5min'
  },

  // Configurações por tipo de visualização
  visualizacoes: {
    financeiro: {
      metricas: ['orcado', 'realizado', 'variacao'],
      agregacoes: ['classe', 'equipamento'],
      alertas: {
        desvio_maximo: 15  // percentual
      }
    },
    operacional: {
      metricas: ['utilizacao', 'custo_hora', 'eficiencia'],

agregacoes: ['diario', 'semanal', 'mensal'],
      alertas: {
        utilizacao_minima: 70,  // percentual
        custo_maximo: 120  // percentual do orçado
      }
    },
    manutencao: {
      metricas: ['custo_manutencao', 'frequencia', 'tempo_parado'],
      agregacoes: ['equipamento', 'classe'],
      alertas: {
        custo_excedido: true,
        tempo_parado_maximo: 48  // horas
      }
    }
  },

  // Componentes do dashboard
  componentes: {
    graficos: ['BarChart', 'LineChart', 'ScatterPlot', 'HeatMap'],
    tabelas: ['DetalheEquipamento', 'ComparativoClasses'],
    indicadores: ['KPIs', 'Alertas', 'Tendencias']
  }
};
```

### 2. Implementação dos Componentes Visuais

```javascript
// Componente principal do dashboard
const Dashboard = () => {
  const [dados, setDados] = useState(null);
  const [filtros, setFiltros] = useState({
    periodo: 'todos',
    classe: 'todas',
    tipo: 'todos'
  });

  // Carregamento e processamento dos dados
  useEffect(() => {
    const carregarDados = async () => {
      const dadosBrutos = await window.fs.readFile('Acompanhamento Justificativa Orçamento2024..csv');
      const dadosProcessados = processarDados(dadosBrutos);
      setDados(dadosProcessados);
    };
    carregarDados();
  }, []);

  return (
    <div className="dashboard">
      <Header>
        <Filtros onChange={setFiltros} />
        <KPIs dados={dados} filtros={filtros} />
      </Header>

      <main className="grid grid-cols-12 gap-4">
        {/* Análise Financeira */}
        <Card className="col-span-8">
          <GraficoComparativo
            dados={dados?.financeiro}
            tipo="orcado-realizado"
          />
        </Card>

        {/* Análise Operacional */}
        <Card className="col-span-4">
          <IndicadoresEficiencia
            dados={dados?.operacional}
          />
        </Card>

        {/* Detalhamento por Equipamento */}
        <Card className="col-span-12">
          <TabelaDetalhamento
            dados={dados?.detalhes}
            filtros={filtros}
          />
        </Card>
      </main>
    </div>
  );
};

// Componentes específicos para cada tipo de análise
const GraficoComparativo = ({ dados, tipo }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={dados}>
        <XAxis dataKey="classe" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="orcado" fill="#8884d8" />
        <Bar dataKey="realizado" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
};

const IndicadoresEficiencia = ({ dados }) => {
  // Cálculo de métricas
  const metricas = calcularMetricas(dados);

  return (
    <div className="grid grid-cols-2 gap-4">
      {metricas.map(metrica => (
        <KPICard
          key={metrica.id}
          titulo={metrica.nome}
          valor={metrica.valor}
          tendencia={metrica.tendencia}
        />
      ))}
    </div>
  );
};
```

### 3. Implementação de Análises e Métricas

```javascript
const calcularMetricas = (dados) => {
  return {
    financeiras: {
      totalOrcado: somatorio(dados, 'orcado'),
      totalRealizado: somatorio(dados, 'realizado'),
      variacaoPercentual: calcularVariacao(dados),
      tendencia: analisarTendencia(dados)
    },
    operacionais: {
      utilizacaoMedia: mediaUtilizacao(dados),
      custoMedioHora: mediaCustoHora(dados),
      eficienciaGlobal: calcularEficiencia(dados)
    },
    manutencao: {
      custoTotal: custosManutencao(dados),
      frequenciaMedia: frequenciaIntervencoes(dados),
      tempoParadoTotal: tempoParado(dados)
    }
  };
};
```

## CRITÉRIOS DE QUALIDADE

1. Performance
  
  - Tempo de carregamento inicial < 2s
  - Atualização de gráficos < 500ms
  - Cache de dados processados
  - Paginação para grandes conjuntos de dados
2. Usabilidade
  
  - Interface responsiva
  - Filtros intuitivos
  - Tooltips informativos
  - Exportação de dados e relatórios
3. Confiabilidade
  
  - Validação de dados na entrada
  - Tratamento de erros robusto
  - Logs de processamento
  - Backup de dados

## RESULTADOS ESPERADOS

1. Dashboard Interativo
  
  - Visualizações dinâmicas
  - Filtros contextuais
  - Drill-down de informações
  - Comparativos temporais
2. Sistema de Alertas
  
  - Notificações de desvios
  - Alertas de manutenção
  - Indicadores de performance
  - Recomendações automáticas
3. Relatórios Automáticos
  
  - Relatórios diários/semanais
  - Exportação em múltiplos formatos
  - Envio automático por email
  - Customização de relatórios
4. Análises Avançadas
  
  - Previsões de custos
  - Análise de tendências
  - Identificação de padrões
  - Recomendações baseadas em dados