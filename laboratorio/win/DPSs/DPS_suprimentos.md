```mermaid
flowchart TD
    subgraph Compras
        A1[Solicitação de Compras] -->|Aprovação Gerente| A2[Aprovação de Solicitação]
        A2 -->|Cotação Iniciada| A3[Processo de Cotação]
        A3 -->|Aprovação Final| A4[Pedido de Compras]
        A4 -->|Enviado ao fornecedor| A5[Pedido Confirmado]
    end

    subgraph Estoque
        B1[Inventário Diário] --> B2[Conferência de Movimentações]
        B2 --> B3[Atualização do ERP]
        B4[Requisições Eletrônicas] -->|Integração com GATEC| B5[Baixa Automática no Estoque]
        B6[Gestão de Consignação] --> B7[Controle de Estoque Mínimo/Máximo]
    end

    subgraph Recebimento_Fiscal
        C1[Entrada de Notas Fiscais] --> C2[Conferência de Tributos]
        C2 -->|Nota Aprovada| C3[Fechamento da Nota]
        C3 -->|Gera Movimentação| C4[Atualização de Estoque]
        C3 -->|Gera Títulos| C5[Contas a Pagar]
        C3 -->|Gera Impostos| C6[Módulo Tributário]
    end

    subgraph Cadastro
        D1[Reestruturação de Produtos] --> D2[Padronização de Informações]
        D3[Cadastro de Fornecedores] --> D2
        D4[Cadastro de Clientes] --> D2
    end

    %% Conexões interprocessuais
    A5 -->|Movimenta Estoque| B1
    A5 -->|Gera Nota Fiscal| C1
    B3 -->|Confirma Inventário| C4
    C4 -->|Atualiza Estoque| B2
