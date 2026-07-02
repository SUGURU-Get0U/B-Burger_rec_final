# RestauranteSys

Sistema web de gestão de restaurante desenvolvido com Flask para a disciplina de Desenvolvimento Web — PUCPR.

---

## Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| Flask | 3.x | Framework web |
| Flask-Login | 0.6+ | Autenticação e sessão |
| Flask-SQLAlchemy | 3.x | ORM |
| SQLite | — | Banco de dados local |
| Jinja2 | — | Templates HTML |
| Werkzeug | — | Hash de senha |

---

## Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Popular o banco com dados iniciais

```bash
cd restaurante
python migrations/seed.py
```

### 3. Iniciar o servidor

```bash
python run.py
```

Acesse: **http://127.0.0.1:5000/**

---

## Credenciais de acesso

| Papel | E-mail | Senha |
|---|---|---|
| Administrador | admin@rest.com | admin123 |
| Atendente | joao@rest.com | joao123 |
| Cliente | maria@rest.com | maria123 |

---

## Papéis e permissões

```
CLIENTE
  ├── Login / Logout
  ├── Visualizar cardápio
  ├── Criar comanda própria
  ├── Adicionar / remover itens (comanda ABERTA)
  ├── Visualizar subtotal e total da própria comanda
  └── ✗ Não pode: fechar comanda, liquidar pagamento, ver outras comandas

ATENDENTE
  ├── Tudo do CLIENTE (para qualquer mesa/cliente)
  ├── Criar comanda para cliente/mesa
  ├── Fechar comanda (estado → FECHADA)
  └── ✗ Não pode: liquidar pagamento, editar comanda FECHADA

ADMINISTRADOR / CAIXA
  ├── Tudo do ATENDENTE
  ├── Editar comanda FECHADA (adicionar/remover itens)
  ├── Liquidar pagamento (forma, valor recebido, troco → estado PAGA)
  ├── Gerenciar clientes (CRUD)
  ├── Gerenciar funcionários (CRUD)
  └── Gerenciar cardápio (CRUD)
```

---

## Estados da comanda

```
ABERTA ──→ FECHADA ──→ PAGA
  │            │
  │     só Admin edita
  │
Cliente/Atendente adicionam itens
```

---

## Fluxo de demonstração end-to-end

1. **Login como atendente** (`joao@rest.com`)
   - Acesse **Comandas → Nova Comanda**
   - Adicione itens do cardápio com quantidades
   - Visualize subtotal por item e total geral
   - Clique em **Fechar Comanda**

2. **Login como admin** (`admin@rest.com`)
   - Abra a comanda fechada
   - Edite itens se necessário (privilégio exclusivo do admin)
   - Clique em **Liquidar Pagamento**
   - Informe forma de pagamento e valor recebido
   - Confirme e veja o **comprovante** com troco calculado

3. **Login como cliente** (`maria@rest.com`)
   - Crie uma comanda própria
   - Tente acessar uma comanda de outro cliente — acesso negado

---

## Modelo de banco de dados

```
usuarios (id, nome, email, senha_hash, papel, ativo, criado_em)
    │
    ├──[papel=cliente]──→ clientes (id, usuario_id, telefone, criado_em)
    │                         │
    │                         └──→ comandas (id, codigo, estado, cliente_id,
    │                                        criado_em, fechado_em, fechado_por_id,
    │                                        pago_em, pago_por_id)
    │                                   │
    │                                   └──→ itens_comanda (id, comanda_id,
    │                                                        item_cardapio_id,
    │                                                        quantidade,
    │                                                        preco_unitario,
    │                                                        subtotal)
    │
    └──[papel=atendente/admin]──→ funcionarios (id, usuario_id, cargo, criado_em)

itens_cardapio (id, nome, descricao, preco, disponivel, criado_em)

pagamentos (id, comanda_id, forma_pagamento, valor_recebido, troco,
            registrado_por, registrado_em)
```

---

## Estrutura do projeto

```
restaurante/
├── run.py                    # Ponto de entrada do servidor
├── requirements.txt          # Dependências Python
├── app/
│   ├── __init__.py           # create_app() — Application Factory
│   ├── config.py             # Configurações por ambiente
│   ├── extensions.py         # db, login_manager
│   ├── decorators.py         # admin_required
│   ├── models/               # Modelos SQLAlchemy (RA3)
│   ├── static_data/          # store.py — estado em memória (RA2)
│   ├── blueprints/
│   │   ├── auth/             # /auth/login, /auth/logout
│   │   ├── cardapio/         # /cardapio/
│   │   ├── comanda/          # /comanda/*
│   │   ├── pagamento/        # /pagamento/*
│   │   └── admin/            # /admin/* (somente admin)
│   └── templates/            # HTML Jinja2
└── migrations/
    └── seed.py               # Dados iniciais
```

---

## Regras de negócio implementadas

- Código de comanda sempre incremental e único
- Cliente só acessa a própria comanda
- Item indisponível bloqueado no backend (não apenas na interface)
- Quantidade ≤ 0 rejeitada com mensagem de erro
- Comanda sem itens não pode ser fechada
- Comanda FECHADA editável apenas por Administrador
- Liquidação exclusiva de Administrador em comanda FECHADA
- Preço snapshot salvo em `itens_comanda.preco_unitario` no momento da inserção
- Remoção de item do cardápio bloqueada se estiver em uso em comandas
- Timestamps de auditoria: `criado_em`, `fechado_em`, `pago_em`
- Usuário responsável auditado: `fechado_por_id`, `pago_por_id`
