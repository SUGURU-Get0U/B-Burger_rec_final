from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    def __init__(self, id, nome, email, senha, papel):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha)
        self.papel = papel  # 'cliente' | 'atendente' | 'admin'

    # --- contrato Flask-Login ---
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


# Usuários pré-cadastrados (substitui o banco no RA2)
# O underscore é uma convenção Python que significa:
#  "este dado é interno, não importe diretamente de fora". 
# Quem precisar de usuários
# deve usar as funções buscar_usuario_por_email e buscar_usuario_por_id 
_usuarios = [
    Usuario(1, "Admin Caixa",    "admin@rest.com", "admin123", "admin"),
    Usuario(2, "João Atendente", "joao@rest.com",  "joao123",  "atendente"),
    Usuario(3, "Maria Cliente",  "maria@rest.com", "maria123", "cliente"),
]


_proximo_id_usuario = 4  # seed já tem IDs 1, 2, 3


def buscar_usuario_por_email(email):
    return next((u for u in _usuarios if u.email == email), None)


def buscar_usuario_por_id(id):
    return next((u for u in _usuarios if u.id == int(id)), None)


def listar_clientes():
    return [u for u in _usuarios if u.papel == 'cliente']


def listar_funcionarios():
    return [u for u in _usuarios if u.papel in ('atendente', 'admin')]


def criar_usuario(nome, email, senha, papel):
    global _proximo_id_usuario
    usuario = Usuario(_proximo_id_usuario, nome, email, senha, papel)
    _usuarios.append(usuario)
    _proximo_id_usuario += 1
    return usuario


def editar_usuario(id, nome, email):
    usuario = buscar_usuario_por_id(id)
    if usuario:
        usuario.nome  = nome
        usuario.email = email
    return usuario


def remover_usuario(id):
    global _usuarios
    _usuarios = [u for u in _usuarios if u.id != int(id)]


# ---------------------------------------------------------------------------
# Cardápio
# ---------------------------------------------------------------------------

class ItemCardapio:
    def __init__(self, id, nome, descricao, preco, disponivel):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco            # float — ex: 28.90
        self.disponivel = disponivel  # True | False


_itens = [
    ItemCardapio(1, "X-Burguer",    "Hambúrguer artesanal",   28.90, True),
    ItemCardapio(2, "Fritas",       "Porção de batata frita", 15.00, True),
    ItemCardapio(3, "Refrigerante", "Lata 350ml",              7.50, True),
    ItemCardapio(4, "Suco de Uva",  "Copo 300ml",              9.00, False),
]


_proximo_id_item = 5  # seed já tem IDs 1–4


def listar_itens():
    return _itens


def buscar_item_por_id(id):
    return next((i for i in _itens if i.id == int(id)), None)


def criar_item(nome, descricao, preco, disponivel):
    global _proximo_id_item
    item = ItemCardapio(_proximo_id_item, nome, descricao, float(preco), disponivel)
    _itens.append(item)
    _proximo_id_item += 1
    return item


def editar_item(id, nome, descricao, preco, disponivel):
    item = buscar_item_por_id(id)
    if item:
        item.nome       = nome
        item.descricao  = descricao
        item.preco      = float(preco)
        item.disponivel = disponivel
    return item


def remover_item(id):
    global _itens
    _itens = [i for i in _itens if i.id != int(id)]


# ---------------------------------------------------------------------------
# Comandas
# ---------------------------------------------------------------------------

class ItemComanda:
    """Um item do cardápio dentro de uma comanda, com quantidade e subtotal."""
    def __init__(self, item_cardapio, quantidade):
        self.item_cardapio_id = item_cardapio.id
        self.nome             = item_cardapio.nome
        self.preco_unitario   = item_cardapio.preco   # snapshot do preço atual
        self.quantidade       = quantidade
        self.subtotal         = item_cardapio.preco * quantidade


class Comanda:
    def __init__(self, id, cliente_id=None):
        self.id         = id
        self.codigo     = id          # no RA2 código == id (incremental)
        self.estado     = 'aberta'    # 'aberta' | 'fechada' | 'paga'
        self.cliente_id = cliente_id  # None se criada por atendente/admin
        self.itens      = []          # lista de ItemComanda

    @property
    def total(self):
        return sum(i.subtotal for i in self.itens)


# Dicionário { id: Comanda } — acesso O(1) por ID
_comandas = {}
_proximo_id_comanda = 1


def criar_comanda(cliente_id=None):
    global _proximo_id_comanda # global server para indicar a mudanca da variavel que existe fora da funcao
    comanda = Comanda(_proximo_id_comanda, cliente_id=cliente_id)
    _comandas[comanda.id] = comanda
    _proximo_id_comanda += 1
    return comanda


def buscar_comanda_por_id(id):
    return _comandas.get(int(id))


def listar_comandas():
    return list(_comandas.values())


def listar_comandas_do_cliente(cliente_id):
    return [c for c in _comandas.values() if c.cliente_id == cliente_id]
