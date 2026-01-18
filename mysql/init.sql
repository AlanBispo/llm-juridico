-- 1. Cria o Banco de Dados
CREATE DATABASE IF NOT EXISTS juridico;
USE juridico;

-- 2. Tabela de Processos
CREATE TABLE IF NOT EXISTS processos_judiciais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resumo_peticao TEXT NOT NULL,
    valor_pedido DECIMAL(10, 2) NOT NULL,
    historico_cliente VARCHAR(255) NOT NULL
);

-- 3. Insere Dados para Teste
INSERT INTO processos_judiciais (resumo_peticao, valor_pedido, historico_cliente) VALUES
(
    'O autor alega que teve seu nome inserido nos órgãos de proteção ao crédito indevidamente por uma fatura de celular já paga.',
    5000.00,
    'Cliente recorrente, nunca teve problemas anteriores com a empresa.'
),
(
    'Reclamação sobre atraso de voo de mais de 12 horas em trecho internacional, gerando perda de conexão e danos morais.',
    12000.50,
    'Passageiro frequente (categoria Platinum), perfil crítico em redes sociais.'
),
(
    'Questionamento de taxas bancárias não contratadas em conta corrente que deveria ser isenta de tarifas.',
    850.00,
    'Cliente novo (6 meses), conta aberta recentemente via aplicativo.'
),
(
    'Pedido de indenização por produto eletrônico entregue com defeito e recusa da loja em realizar a troca no prazo legal.',
    2300.00,
    'Cliente antigo, possui 3 compras anteriores sem incidentes.'
);