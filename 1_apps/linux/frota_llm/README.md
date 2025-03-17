# Documento Técnico para Equipe de Desenvolvimento

## 📌 Visão Geral
O projeto atual é um dashboard interativo de gestão operacional e financeira para frotas agrícolas, desenvolvido com Python e Streamlit, conectado a um banco de dados SQLite (`frota.db`).

## 🛠️ Estrutura Modular Atual

O projeto está modularizado em quatro arquivos principais:

### 1. 📂 `db_connection.py`
- Gerencia conexões com o banco de dados SQLite.
- Inclui função para determinar datas padrão para inicialização.

### Funções definidas:
- **`get_db_connection(db_filename: str)`**: estabelece e retorna a conexão com o banco SQLite.
- **`get_date_defaults(conn)`**: obtém datas mínimas e máximas para uso em filtros de interface.

---

### 🗃️ `db_filters.py`
- Centraliza a criação de filtros SQL dinâmicos.
- Implementa cálculos financeiros importantes para o dashboard.

#### Funções presentes:
- **`build_filters(filtros: Dict, alias: str)`**: gera cláusulas condicionais SQL baseadas nos filtros selecionados na interface.
- **`get_unique_values(conn, column_name)`**: retorna valores únicos de colunas dimensionais para filtros.
- **`calcular_multiplicadores(df)`**: gera multiplicadores para indicadores de uso e consumo.
- **`apply_flags(df)`**: sinaliza desempenho financeiro através de ícones de status (🔶, 🟢, 🔴, ⚪).

---

### 📊 `db_dashboard.py`
- Responsável pela visualização gráfica e métricas do dashboard.

Funções principais:
- **`get_filtered_data(filtros)`**: consulta e retorna dados filtrados do banco.
- **`display_metrics(df)`**: exibe métricas-chave no Streamlit.
- **`plot_chart(df)`**: constrói gráficos interativos (Plotly) para análise visual do desempenho.

---

### 🚀 `frota_llm.py` (Arquivo Principal)
- Integra todas as funções dos módulos auxiliares.
- Executa o dashboard operacional diretamente pelo Streamlit.

## 🧩 Fluxo de Trabalho Típico

1. **Usuário acessa a aplicação via navegador**.
2. **Seleciona filtros** na barra lateral (datas, usuários, classes, equipamentos).
3. **Aplicação carrega os dados filtrados** através de consultas SQL.
4. **Cálculos intermediários são feitos** (multiplicadores e flags).
5. **Dados processados** são exibidos visualmente e em tabelas detalhadas.

---

## 🚩 Variáveis e parâmetros críticos:
- **`data_referencia`**: intervalo de datas usado como filtro principal.
- **`id_equipamento`**, **`usuario`**, **`classe`**: filtros dimensionais secundários.
- **Indicadores financeiros**: `total_estimado`, `total_realizado`, `custo_hora_estimado`, `custo_hora_realizado`.
- **Multiplicadores**: indicam desvios e performance operacional.

---

## 🔄 Sugestões para Melhorias Futuras:
- **Performance**: Otimizar consultas SQL, especialmente para grandes volumes de dados.
- **Interatividade**: Adicionar funcionalidades adicionais, como exportação dos dados exibidos para Excel ou CSV diretamente pelo dashboard.
- **Robustez e testes automatizados**: Incluir testes unitários para garantir estabilidade e confiabilidade após futuras alterações.
- **Interface e UX**: Refinar a experiência visual do usuário com feedback visual mais responsivo.

---

## 📌 Recomendações para equipe de desenvolvimento:
- Manter clareza na modularização para facilitar futuras expansões ou correções.
- Seguir padrões claros de nomenclatura e documentação em todas as funções.
- Garantir revisões frequentes do desempenho e otimizações pontuais para manter uma boa performance da aplicação.

