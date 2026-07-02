-- Gerado automaticamente por migrations/gerar_schema.py
-- Não editar à mão — rode o script novamente após mudar os modelos em app/models/.

-- Tabela: itens_cardapio
CREATE TABLE itens_cardapio (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	descricao TEXT, 
	preco NUMERIC(10, 2) NOT NULL, 
	disponivel BOOLEAN, 
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id)
);

-- Tabela: usuarios
CREATE TABLE usuarios (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	senha_hash VARCHAR(255) NOT NULL, 
	papel VARCHAR(20) NOT NULL, 
	ativo BOOLEAN, 
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

-- Tabela: clientes
CREATE TABLE clientes (
	id INTEGER NOT NULL, 
	usuario_id INTEGER NOT NULL, 
	telefone VARCHAR(20), 
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (usuario_id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

-- Tabela: funcionarios
CREATE TABLE funcionarios (
	id INTEGER NOT NULL, 
	usuario_id INTEGER NOT NULL, 
	cargo VARCHAR(50) NOT NULL, 
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (usuario_id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);

-- Tabela: comandas
CREATE TABLE comandas (
	id INTEGER NOT NULL, 
	codigo INTEGER NOT NULL, 
	estado VARCHAR(10) NOT NULL, 
	cliente_id INTEGER, 
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
	fechado_em DATETIME, 
	fechado_por_id INTEGER, 
	pago_em DATETIME, 
	pago_por_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (codigo), 
	FOREIGN KEY(cliente_id) REFERENCES clientes (id), 
	FOREIGN KEY(fechado_por_id) REFERENCES usuarios (id), 
	FOREIGN KEY(pago_por_id) REFERENCES usuarios (id)
);

-- Tabela: itens_comanda
CREATE TABLE itens_comanda (
	id INTEGER NOT NULL, 
	comanda_id INTEGER NOT NULL, 
	item_cardapio_id INTEGER NOT NULL, 
	quantidade INTEGER NOT NULL, 
	preco_unitario NUMERIC(10, 2) NOT NULL, 
	subtotal NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(comanda_id) REFERENCES comandas (id), 
	FOREIGN KEY(item_cardapio_id) REFERENCES itens_cardapio (id)
);

-- Tabela: pagamentos
CREATE TABLE pagamentos (
	id INTEGER NOT NULL, 
	comanda_id INTEGER NOT NULL, 
	forma_pagamento VARCHAR(30) NOT NULL, 
	valor_recebido NUMERIC(10, 2) NOT NULL, 
	troco NUMERIC(10, 2) NOT NULL, 
	registrado_por INTEGER NOT NULL, 
	registrado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (comanda_id), 
	FOREIGN KEY(comanda_id) REFERENCES comandas (id), 
	FOREIGN KEY(registrado_por) REFERENCES usuarios (id)
);
