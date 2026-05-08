-- Criação das tabelas relacionais do projeto Núcleo Analytics.
-- O script recria as tabelas para facilitar execuções locais repetidas.

DROP TABLE IF EXISTS eventos_uso;
DROP TABLE IF EXISTS tickets_suporte;
DROP TABLE IF EXISTS campanhas_marketing;
DROP TABLE IF EXISTS pagamentos;
DROP TABLE IF EXISTS assinaturas;
DROP TABLE IF EXISTS planos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    cliente_id VARCHAR(20) PRIMARY KEY,
    nome_empresa VARCHAR(150) NOT NULL,
    segmento VARCHAR(80) NOT NULL,
    porte_empresa VARCHAR(40) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    data_cadastro DATE NOT NULL,
    status_cliente VARCHAR(40) NOT NULL
);

CREATE TABLE planos (
    plano_id VARCHAR(20) PRIMARY KEY,
    nome_plano VARCHAR(80) NOT NULL,
    valor_mensal NUMERIC(12, 2) NOT NULL CHECK (valor_mensal > 0),
    limite_usuarios INTEGER NOT NULL CHECK (limite_usuarios > 0),
    categoria_plano VARCHAR(60) NOT NULL
);

CREATE TABLE assinaturas (
    assinatura_id VARCHAR(20) PRIMARY KEY,
    cliente_id VARCHAR(20) NOT NULL REFERENCES clientes(cliente_id),
    plano_id VARCHAR(20) NOT NULL REFERENCES planos(plano_id),
    data_inicio DATE NOT NULL,
    data_fim DATE,
    status_assinatura VARCHAR(40) NOT NULL,
    CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE pagamentos (
    pagamento_id VARCHAR(20) PRIMARY KEY,
    assinatura_id VARCHAR(20) NOT NULL REFERENCES assinaturas(assinatura_id),
    cliente_id VARCHAR(20) NOT NULL REFERENCES clientes(cliente_id),
    data_pagamento DATE,
    mes_referencia CHAR(7) NOT NULL,
    valor_pago NUMERIC(12, 2) NOT NULL CHECK (valor_pago >= 0),
    status_pagamento VARCHAR(40) NOT NULL,
    metodo_pagamento VARCHAR(40) NOT NULL
);

CREATE TABLE campanhas_marketing (
    campanha_id VARCHAR(20) PRIMARY KEY,
    nome_campanha VARCHAR(150) NOT NULL,
    canal VARCHAR(80) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    investimento NUMERIC(12, 2) NOT NULL CHECK (investimento >= 0),
    leads_gerados INTEGER NOT NULL CHECK (leads_gerados >= 0),
    clientes_convertidos INTEGER NOT NULL CHECK (clientes_convertidos >= 0),
    CHECK (data_fim >= data_inicio),
    CHECK (clientes_convertidos <= leads_gerados)
);

CREATE TABLE tickets_suporte (
    ticket_id VARCHAR(20) PRIMARY KEY,
    cliente_id VARCHAR(20) NOT NULL REFERENCES clientes(cliente_id),
    data_abertura DATE NOT NULL,
    data_fechamento DATE,
    categoria VARCHAR(80) NOT NULL,
    prioridade VARCHAR(40) NOT NULL,
    status_ticket VARCHAR(40) NOT NULL,
    tempo_resolucao_horas NUMERIC(10, 1) CHECK (tempo_resolucao_horas IS NULL OR tempo_resolucao_horas >= 0),
    satisfacao_cliente INTEGER CHECK (satisfacao_cliente IS NULL OR satisfacao_cliente BETWEEN 1 AND 5),
    CHECK (data_fechamento IS NULL OR data_fechamento >= data_abertura)
);

CREATE TABLE eventos_uso (
    evento_id VARCHAR(20) PRIMARY KEY,
    cliente_id VARCHAR(20) NOT NULL REFERENCES clientes(cliente_id),
    data_evento DATE NOT NULL,
    tipo_evento VARCHAR(80) NOT NULL,
    quantidade_eventos INTEGER NOT NULL CHECK (quantidade_eventos >= 0)
);
