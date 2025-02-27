```mermaid
flowchart TD;
    subgraph ERP_Processo
        A[Empresas Ativas no ERP] -->|Replica Modelo Existente| B[Regime Tributário];
        B -->|Lucro Real & Lucro Presumido| C[Orçamentos];
        C -->|Não Utilizado pelo Cliente| D[Vendas e Pedidos];
        D -->|Pedidos Cadastrados Manualmente| E[Notas Fiscais];
    end
    
    subgraph NotasFiscais_Processo
        E -->|Integração Financeiro & Fiscal| F[Emissão de Notas];
        F -->|Operações Diversas| G[Escrituração de Notas Fiscais];
        G -->|Módulo de Suprimentos| H[Notas Fiscais de Saída];
        H -->|Volume: 200/mês| I[Relatórios Específicos];
    end
    
    subgraph Integrações
        J[Integração com GAtec] -->|Suporte Necessidades Específicas| K[Relatórios Contratos de Soja];
        K -->|Possível Adaptação no ERP| L[Gestão de Contratos];
        L -->|Eficiência no Processo| M[Controle de Custos];
    end
    
    E -->|Ligação com Contratos/Pedidos| L;
    I -->|Base para Avaliação Financeira| M;
    ```