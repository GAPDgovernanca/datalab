# Formulário de Relatório Diário de Ocorrências

## Identificação Geral

1.  **Data da Ocorrência**
    *   Tipo: Date
    *   Descrição: Selecione a data em que a ocorrência aconteceu.
    *   Formato: DD/MM/AAAA
    *   Obrigatório: Sim

2.  **Responsável pelo Registro**
    *   Tipo: Short Text
    *   Descrição: Informe seu nome completo.
    *   Obrigatório: Sim

3.  **Turno**
    *   Tipo: Dropdown
    *   Descrição: Selecione o turno de trabalho.
    *   Opções:
        *   Turno A
        *   Turno B
        *   Turno C
        *   Geral / Diurno
        *   Noturno
    *   Obrigatório: Sim

4.  **Frente / Setor de Trabalho**
    *   Tipo: Dropdown
    *   Descrição: Selecione a frente ou setor de trabalho. Se não estiver na lista, escolha "Outro".
    *   Opções:
        *   Setor P18
        *   Setor P1/2
        *   Setor P3/5
        *   Setor TR9
        *   Frente 13
        *   Frente 83
        *   Frente Berra Rio
        *   Usina
        *   Base/Garagem
        *   Outro
    *   Obrigatório: Sim
    *   Lógica: Se "Outro" for selecionado, mostrar Campo 4.1.

5.  **Especificar Frente/Setor** (Campo 4.1)
    *   Tipo: Short Text
    *   Descrição: Se selecionou "Outro" no campo anterior, especifique aqui a frente ou setor.
    *   Obrigatório: Condicional (se Campo 4 = "Outro")

## Identificação do Equipamento/Evento

6.  **Equipamento Afetado (Nº Frota)**
    *   Tipo: Short Text
    *   Descrição: Informe o número da frota do equipamento (ex: 118, 4208). Deixe em branco se a ocorrência for geral e não envolver um equipamento específico.
    *   Obrigatório: Não

7.  **Tipo de Equipamento**
    *   Tipo: Dropdown
    *   Descrição: Selecione o tipo de equipamento.
    *   Opções:
        *   Colhedora
        *   Trator
        *   Transbordo
        *   Caminhão (Carga/Canavieiro)
        *   Caminhão (Apoio/Oficina/Comboio)
        *   Veículo Leve (Carro/Camionete)
        *   Implemento Agrícola (sem autopropulsão)
        *   Equipamento Industrial (Usina)
        *   Outro
    *   Obrigatório: Condicional (se Campo 6 estiver preenchido, este campo se torna obrigatório)
    *   Lógica: Se "Outro" for selecionado, mostrar Campo 7.1.

8.  **Especificar Tipo de Equipamento** (Campo 7.1)
    *   Tipo: Short Text
    *   Descrição: Se selecionou "Outro" no tipo de equipamento, especifique aqui.
    *   Obrigatório: Condicional (se Campo 7 = "Outro")

9.  **Horímetro Inicial (Se aplicável)**
    *   Tipo: Number
    *   Descrição: Informe o horímetro inicial do equipamento, se aplicável. Use ponto para decimal (ex: 15244.6).
    *   Obrigatório: Não

10. **Horímetro Final (Se aplicável)**
    *   Tipo: Number
    *   Descrição: Informe o horímetro final do equipamento, se aplicável. Use ponto para decimal (ex: 15251.8).
    *   Obrigatório: Não

## Detalhes da Ocorrência

11. **Tipo de Evento Principal**
    *   Tipo: Dropdown
    *   Descrição: Qual a natureza principal da ocorrência?
    *   Opções:
        *   Manutenção Corretiva (Falha/Quebra)
        *   Manutenção Preventiva (Programada/Revisão)
        *   Manutenção Preditiva
        *   Inspeção / Verificação / Diagnóstico
        *   Parada Operacional (Ex: Chuva, Falta de Frente, Usina, Atolamento)
        *   Parada Programada (Equipamento ou Usina)
        *   Abastecimento / Lubrificação / Limpeza Geral
        *   Modificação / Melhoria
        *   Acidente / Incidente (Com ou Sem Danos)
        *   Logística / Movimentação (Ex: Mudança de setor, Saída de caminhões)
        *   Alerta de Sistema (Painel, Computador de Bordo)
        *   Outro
    *   Obrigatório: Sim
    *   Lógica: Se "Outro" for selecionado, mostrar Campo 11.1.

12. **Especificar Tipo de Evento** (Campo 11.1)
    *   Tipo: Short Text
    *   Descrição: Se selecionou "Outro" no tipo de evento, especifique aqui.
    *   Obrigatório: Condicional (se Campo 11 = "Outro")

13. **Sistema/Componente Principal Afetado**
    *   Tipo: Dropdown
    *   Descrição: Qual sistema ou componente principal do equipamento foi afetado?
    *   Opções:
        *   Motor (Bloco, Cabeçote, Turbo, etc.)
        *   Sistema de Arrefecimento (Radiador, Mangueiras, Bomba d'água)
        *   Sistema de Combustível (Bomba, Filtros, Bicos, Tanque, Mangueiras)
        *   Sistema de Lubrificação (Motor, Transmissão, Diferencial)
        *   Transmissão / Caixa de Marchas
        *   Diferencial / Eixos
        *   Sistema Hidráulico (Bombas, Mangueiras, Pistões, Comandos, Filtros)
        *   Sistema Pneumático (Compressor, Válvulas, Mangueiras, Cilindros)
        *   Sistema Elétrico (Alternador, Motor de Partida, Bateria, Chicote, Luzes, Sensores)
        *   Eletrônica Embarcada (Módulos, GPS, Piloto Automático, Auto Tracker)
        *   Rodados (Pneus, Rodas, Cubos, Rolamentos)
        *   Esteiras (Material Rodante, Roletes, Correntes)
        *   Freios (Disco, Pastilha, Lona, Tambor, Cuíca, Válvulas)
        *   Direção (Terminal, Barra, Bomba, Caixa)
        *   Suspensão (Molas, Amortecedores, Bolsas de Ar, Barras)
        *   Estrutura / Chassi / Carenagem
        *   Cabine / Controles Operacionais (Painel, Assento, Alavancas)
        *   Ar Condicionado / Climatização
        *   Implemento - Colhedora: Corte de Base / Divisores de Linha / Extrator Primário / Extrator Secundário / Elevador / Picador / Rolo Alimentador / Flaps / Despontador
        *   Implemento - Trator/Transbordo: Engate / Tomada de Força (TDP) / Braços Hidráulicos / Caçamba / Sistema de Descarga
        *   Implemento - Outros
        *   Ambiental / Climático (Chuva, Solo, Poeira)
        *   Logística / Processo (Fila, Espera, Disponibilidade)
        *   Segurança (EPC, EPI)
        *   Não se aplica (Ocorrência geral)
        *   Outro
    *   Obrigatório: Sim
    *   Lógica: Se "Outro" for selecionado, mostrar Campo 13.1.

14. **Especificar Sistema/Componente** (Campo 13.1)
    *   Tipo: Short Text
    *   Descrição: Se selecionou "Outro" no sistema/componente, especifique aqui.
    *   Obrigatório: Condicional (se Campo 13 = "Outro")

15. **Ação Principal Realizada/Necessária**
    *   Tipo: Dropdown
    *   Descrição: Qual foi a principal ação tomada ou que precisa ser tomada?
    *   Opções:
        *   Troca de Peça/Componente
        *   Reparo / Conserto
        *   Ajuste / Regulagem / Sincronização
        *   Verificação / Inspeção / Diagnóstico
        *   Limpeza / Lavagem
        *   Lubrificação
        *   Abastecimento (Combustível, Óleo, Água, Arla)
        *   Solda / Serralheria
        *   Reaperto
        *   Instalação
        *   Remoção
        *   Modificação / Adaptação
        *   Calibração
        *   Parada de Equipamento/Operação
        *   Reinício de Operação
        *   Movimentação / Deslocamento
        *   Carregamento / Descarregamento
        *   Nenhuma Ação (Apenas Registro/Observação)
        *   Pendente (Aguardando Peça/Serviço/Decisão)
        *   Outro
    *   Obrigatório: Sim
    *   Lógica: Se "Outro" for selecionado, mostrar Campo 15.1.

16. **Especificar Ação Principal** (Campo 15.1)
    *   Tipo: Short Text
    *   Descrição: Se selecionou "Outro" na ação principal, especifique aqui.
    *   Obrigatório: Condicional (se Campo 15 = "Outro")

17. **Descrição Detalhada da Ocorrência**
    *   Tipo: Long Text
    *   Descrição: Descreva em detalhes a ocorrência. Inclua sintomas, possível causa raiz, peças utilizadas (com códigos, se souber), passos da solução, dificuldades encontradas, etc.
    *   Obrigatório: Sim

18. **Número da Ordem de Serviço (OS)**
    *   Tipo: Short Text
    *   Descrição: Se houver uma Ordem de Serviço associada, informe o número (ex: 3112090).
    *   Obrigatório: Não

## Horários e Status

19. **Hora Início da Ocorrência/Serviço**
    *   Tipo: Time
    *   Descrição: Informe a hora em que a ocorrência começou ou o serviço foi iniciado.
    *   Formato: HH:MM
    *   Obrigatório: Sim

20. **Hora Fim da Ocorrência/Serviço**
    *   Tipo: Time
    *   Descrição: Informe a hora em que a ocorrência terminou ou o serviço foi concluído. Deixe em branco se ainda estiver em andamento.
    *   Formato: HH:MM
    *   Obrigatório: Condicional (se Campo 21 = "Concluída")

21. **Status da Ocorrência**
    *   Tipo: Dropdown
    *   Descrição: Qual o status atual desta ocorrência?
    *   Opções:
        *   Concluída
        *   Em Andamento
        *   Pendente (Aguardando Peça)
        *   Pendente (Aguardando Mão de Obra Externa)
        *   Pendente (Aguardando Autorização/Decisão)
        *   Pendente (Transferida para próximo turno/dia)
        *   Programada para Data Futura
        *   Cancelada / Não Procede
    *   Obrigatório: Sim

22. **Observações Adicionais**
    *   Tipo: Long Text
    *   Descrição: Adicione qualquer informação extra relevante (ex: número de caminhões que saíram, condições climáticas específicas não cobertas anteriormente, sugestões).
    *   Obrigatório: Não

23. **Anexar Fotos (Opcional)**
    *   Tipo: File Upload
    *   Descrição: Se desejar, anexe até 3 fotos relacionadas à ocorrência (limite de 5MB por foto).
    *   Obrigatório: Não