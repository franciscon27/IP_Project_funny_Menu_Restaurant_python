"""
RESTAURANTE ITALIANO - SISTEMA DE MENU INTERATIVO

Aplicação em PyGame para gestão de pedidos de um restaurante italiano.
Permite aos clientes visualizar o menu, adicionar/remover itens e finalizar pedidos.
"""

import pygame
import sys

# ================================
# CONFIGURAÇÕES INICIAIS DO PYGAME
# ================================

# Inicializar o sistema PyGame
pygame.init()

# Configurações da tela (agora responsiva)
INFO = pygame.display.Info()
LARGURA = min(1400, INFO.current_w - 100)
ALTURA = min(900, INFO.current_h - 100)
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Restaurante Italiano - Menu do Dia")

# Cores (paleta de quadro de giz)
COR_FUNDO = (30, 30, 40)  # Cor escura de fundo (simula quadro negro)
COR_TEXTO = (240, 240, 240)  # Cor do giz branco
COR_TEXTO_SECUNDARIO = (180, 220, 180)  # Cor do giz verde claro
COR_DESTAQUE = (255, 200, 100)  # Cor do giz amarelo
COR_BORDA = (80, 60, 40)  # Cor da moldura de madeira
COR_BOTAO = (100, 80, 60)  # Cor dos botões
COR_BOTAO_HOVER = (130, 100, 70)  # Cor dos botões ao passar mouse

# Cores da scrollbar
COR_SCROLLBAR = (120, 100, 80, 180)  # Com transparência
COR_SCROLLBAR_HOVER = (150, 130, 110, 220)
COR_SCROLLBAR_BG = (60, 50, 40, 100)

# Cores para pop-up
COR_POPUP_FUNDO = (20, 20, 30, 240)  # Fundo semi-transparente
COR_POPUP_BORDA = (255, 200, 100)  # Borda amarela
COR_POPUP_TEXTO = (240, 240, 240)  # Texto branco

# Fontes (simulando escrita à mão)
pygame.font.init()
FONTE_TITULO = pygame.font.SysFont("comicsansms", 48, bold=True)
FONTE_CATEGORIA = pygame.font.SysFont("comicsansms", 32, bold=True)
FONTE_ITEM = pygame.font.SysFont("comicsansms", 28)
FONTE_PRECO = pygame.font.SysFont("comicsansms", 26)
FONTE_BOTAO = pygame.font.SysFont("comicsansms", 30, bold=True)
FONTE_PEDIDO = pygame.font.SysFont("comicsansms", 24)
FONTE_POPUP = pygame.font.SysFont("comicsansms", 24)
FONTE_POPUP_PEQUENA = pygame.font.SysFont("comicsansms", 22)

# ================================
# Dados do restaurante
# ================================

menu = (
    # Entradas
    ("Bruschetta al Pomodoro", 5.50, "Entradas"),
    ("Carpaccio di Manzo", 9.50, "Entradas"),
    ("Insalata Caprese", 7.00, "Entradas"),

    # Especialidades do Chef
    ("Ossobuco alla Milanese", 17.50, "Especialidades do Chef"),
    ("Saltimbocca alla Romana", 16.00, "Especialidades do Chef"),
    ("Risotto ai Funghi Porcini", 15.50, "Especialidades do Chef"),

    # Pastas
    ("Spaghetti alla Carbonara", 13.00, "Pastas"),
    ("Tagliatelle al Ragù Bolognese", 13.50, "Pastas"),
    ("Lasagna alla Bolognese", 14.00, "Pastas"),
    ("Penne all'Arrabbiata", 11.50, "Pastas"),

    # Pizza
    ("Pizza Margherita", 9.00, "Pizza"),
    ("Pizza Quattro Formaggi", 11.00, "Pizza"),
    ("Pizza Prosciutto e Funghi", 11.50, "Pizza"),
    ("Pizza Diavola", 12.00, "Pizza"),

    # Bebidas
    ("Acqua Naturale", 1.50, "Bebidas"),
    ("Acqua Frizzante", 1.80, "Bebidas"),
    ("Vino Rosso della Casa (copo)", 4.50, "Bebidas"),
    ("Vino Bianco della Casa (copo)", 4.50, "Bebidas"),
    ("Caffè Espresso", 1.50, "Bebidas"),
    ("Cappuccino", 2.00, "Bebidas"),

    # Sobremesas
    ("Tiramisù", 5.00, "Sobremesas"),
    ("Panna Cotta ai Frutti di Bosco", 5.50, "Sobremesas"),
    ("Gelato Artigianale (2 sabores)", 4.50, "Sobremesas"),
    ("Cannolo Siciliano", 4.80, "Sobremesas"),
)

pedido = []

# ================================
# Variáveis de estado
# ================================

scroll_y = 0  # Posição atual do scroll no menu
scroll_pedido_y = 0  # Posição atual do scroll no pedido
scroll_conta_y = 0  # Posição atual do scroll na conta
estado_atual = "menu"  # "menu", "pedido", "conta"
item_selecionado = None  # Índice do item selecionado no menu
item_pedido_selecionado = None  # Índice do item selecionado no pedido
quantidade_a_remover = 1  # Quantidade a remover no pop-up
popup_visivel = False  # Controla se o pop-up está visível
item_para_remover = None  # Informação do item a remover (quando em pop-up)
popup_tipo = None  # Tipo de pop-up: "remover" ou "pagamento"
metodo_pagamento = None  # Método de pagamento escolhido: "numerario" ou "cartao"

# ================================
# Classes para a interface
# ================================

class Botao:
    """
    Representa um botão interativo com efeito hover.
    Muda de cor quando o mouse passa por cima e executa uma ação quando clicado.
    """
    def __init__(self, x, y, largura, altura, texto, acao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao = acao  # Função a executar quando o botão é clicado
        self.cor_normal = COR_BOTAO
        self.cor_hover = COR_BOTAO_HOVER
        self.cor_atual = self.cor_normal
        
    def desenhar(self, tela):
        """Desenha o botão com preenchimento, borda e texto centrado."""
        # Desenhar fundo do botão com cantos arredondados
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=10)
        # Desenhar borda do botão
        pygame.draw.rect(tela, COR_TEXTO, self.rect, 3, border_radius=10)
        
        # Renderizar e desenhar texto centrado no botão
        texto_surf = FONTE_BOTAO.render(self.texto, True, COR_TEXTO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)
        
    def verificar_clique(self, pos):
        """
        Verifica se o botão foi clicado e executa a ação associada.
        Retorna True se o clique foi sobre o botão, False caso contrário.
        """
        if self.rect.collidepoint(pos):
            if self.acao:
                self.acao()
            return True
        return False
        
    def atualizar(self, pos_mouse):
        """Atualiza a cor do botão baseado na posição do mouse (hover effect)."""
        if self.rect.collidepoint(pos_mouse):
            self.cor_atual = self.cor_hover
        else:
            self.cor_atual = self.cor_normal

class ItemMenu:
    """
    Representa um item do menu (prato/bebida) com nome, preço e categoria.
    Pode ser selecionado e tem métodos para desenho e detecção de clique.
    """
    def __init__(self, nome, preco, categoria, index):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
        self.index = index
        self.selecionado = False  # Indica se o item está selecionado
        self.rect = None  # Retângulo de clique (definido no desenho)
        
    def desenhar(self, tela, x, y):
        """Desenha o item do menu com nome, preço e indicador de seleção."""
        # Mudar cor se o item está selecionado
        cor = COR_DESTAQUE if self.selecionado else COR_TEXTO
        
        # Desenhar nome do prato à esquerda
        nome_surf = FONTE_ITEM.render(self.nome, True, cor)
        tela.blit(nome_surf, (x, y))
        
        # Desenhar preço à direita
        preco_texto = f"{self.preco:.2f}€"
        preco_surf = FONTE_PRECO.render(preco_texto, True, COR_TEXTO_SECUNDARIO)
        preco_rect = preco_surf.get_rect()
        preco_rect.right = tela.get_width() - 120
        preco_rect.top = y
        tela.blit(preco_surf, preco_rect)
        
        # Definir retângulo para detecção de clique
        self.rect = pygame.Rect(x-10, y-5, tela.get_width() - 140, 40)
        
        # Desenhar retângulo de seleção se item está selecionado
        if self.selecionado:
            pygame.draw.rect(tela, (255, 255, 255, 50), self.rect, 2, border_radius=5)

class Scrollbar:
    """
    Implementa uma barra de scroll personalizada para scroll vertical.
    Suporta clique do mouse, arrastamento e scroll com roda do mouse.
    """
    def __init__(self, x, y, altura, conteudo_altura):
        self.x = x  # Posição X da scrollbar
        self.y = y  # Posição Y da scrollbar
        self.altura = altura  # Altura disponível da scrollbar
        self.conteudo_altura = conteudo_altura  # Altura total do conteúdo
        self.largura = 12  # Largura da scrollbar
        self.scroll_y = 0  # Posição atual do scroll (pixels)
        self.scroll_max = max(0, conteudo_altura - altura)  # Scroll máximo
        self.arrastando = False  # Se o utilizador está arrastando a scrollbar
        self.hover = False  # Se o mouse está sobre a scrollbar
        
    def atualizar(self, pos_mouse, eventos):
        """
        Processa eventos de mouse (cliques, movimento, roda) e atualiza a posição de scroll.
        Retorna a posição atual de scroll em pixels.
        """
        self.hover = False
        
        if self.scroll_max > 0:
            # Calcular dimensões do "thumb" (a parte arrastável da scrollbar)
            thumb_altura = max(30, (self.altura ** 2) / self.conteudo_altura)
            thumb_y = self.y + (self.scroll_y / self.scroll_max) * (self.altura - thumb_altura)
            thumb_rect = pygame.Rect(self.x, thumb_y, self.largura, thumb_altura)
            
            # Verificar se mouse está sobre o thumb
            self.hover = thumb_rect.collidepoint(pos_mouse)
            
            # Processar eventos de mouse
            for event in eventos:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and thumb_rect.collidepoint(pos_mouse):
                        # Iniciar arrastamento
                        self.arrastando = True
                        self.offset_arrasto = pos_mouse[1] - thumb_y
                    elif event.button == 4:  # Scroll para cima
                        self.scroll_y = max(0, self.scroll_y - 40)
                    elif event.button == 5:  # Scroll para baixo
                        self.scroll_y = min(self.scroll_max, self.scroll_y + 40)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.arrastando = False
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.arrastando:
                        # Calcular nova posição de scroll baseada no movimento do mouse
                        mouse_rel_y = pos_mouse[1] - self.y - self.offset_arrasto
                        percent = mouse_rel_y / (self.altura - thumb_altura)
                        self.scroll_y = percent * self.scroll_max
                        # Limitar scroll aos valores mínimo e máximo
                        self.scroll_y = max(0, min(self.scroll_max, self.scroll_y))
        
        return self.scroll_y
    
    def desenhar(self, tela):
        """Desenha a scrollbar e o seu thumb na tela."""
        if self.scroll_max <= 0:
            return  # Não desenhar se não há scroll necessário
        
        # Desenhar fundo da scrollbar (com transparência)
        bg_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        s = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        s.fill(COR_SCROLLBAR_BG)
        tela.blit(s, bg_rect)
        
        # Desenhar thumb (a parte arrastável)
        thumb_altura = max(30, (self.altura ** 2) / self.conteudo_altura)
        thumb_y = self.y + (self.scroll_y / self.scroll_max) * (self.altura - thumb_altura)
        thumb_rect = pygame.Rect(self.x, thumb_y, self.largura, thumb_altura)
        
        # Mudar cor do thumb se está em hover ou sendo arrastado
        thumb_color = COR_SCROLLBAR_HOVER if self.hover or self.arrastando else COR_SCROLLBAR
        s_thumb = pygame.Surface((self.largura, thumb_altura), pygame.SRCALPHA)
        s_thumb.fill(thumb_color)
        tela.blit(s_thumb, thumb_rect)
        
        # Desenhar borda do thumb
        pygame.draw.rect(tela, COR_TEXTO, thumb_rect, 1, border_radius=3)

# ================================
# Funções do sistema
# ================================

def agrupar_itens_pedido():
    """
    Agrupa e ordena os itens do pedido por categoria, contando quantidades.
    
    Retorna uma lista de tuplas: (nome, preco, categoria, quantidade)
    ordenadas por categoria (segundo a ordem do restaurante) e posição no menu.
    """
    if not pedido:
        return []

    # Contar quantidades de cada item único
    contagem = {}
    for nome, preco, categoria in pedido:
        chave = (nome, preco, categoria)
        contagem[chave] = contagem.get(chave, 0) + 1

    # Definir ordem das categorias
    ordem_categorias = [
        "Entradas",
        "Especialidades do Chef",
        "Pastas",
        "Pizza",
        "Bebidas",
        "Sobremesas",
    ]

    # Criar índice de posição dos itens no menu original
    indice_menu = {}
    for idx, (nome, preco, categoria) in enumerate(menu):
        indice_menu[(nome, preco, categoria)] = idx

    # Preparar lista com índices de ordenação
    itens_ordenados = []
    for (nome, preco, categoria), quantidade in contagem.items():
        idx_cat = ordem_categorias.index(categoria) if categoria in ordem_categorias else 999
        idx_menu = indice_menu.get((nome, preco, categoria), 999)
        itens_ordenados.append((idx_cat, idx_menu, nome, preco, categoria, quantidade))

    # Ordenar por categoria e depois por posição no menu
    itens_ordenados.sort()
    return [(nome, preco, categoria, quantidade) for _, _, nome, preco, categoria, quantidade in itens_ordenados]

def calcular_total_pedido():
    """Calcula e retorna o total de preço de todos os itens no pedido."""
    return sum(preco for _, preco, _ in pedido)

def sair_programa():
    """Fecha a aplicação e sai do programa."""
    pygame.quit()
    sys.exit()

# ================================
# INICIALIZAÇÃO E GESTÃO DE ESTADO
# ================================

# Listas globais para guardar objetos da interface
botoes = []  # Lista de botões da interface
itens_menu_obj = []  # Lista de objetos ItemMenu
scrollbar = None  # Scrollbar do menu
scrollbar_pedido = None  # Scrollbar do pedido
scrollbar_conta = None  # Scrollbar da conta
itens_pedido_obj = []  # Lista de dicionários dos itens do pedido

def criar_botoes():
    """
    Cria os botões apropriados baseado no estado atual da aplicação.
    Diferentes estados (menu, pedido, conta) têm diferentes botões.
    """
    global botoes
    
    botoes.clear()
    # Calcular dimensões responsivas dos botões
    botao_largura = min(200, LARGURA // 6 - 20)
    espacamento = (LARGURA - (4 * botao_largura)) // 5
    
    if estado_atual == "menu":
        # Botões do menu principal: Ver Pedido, Adicionar, Finalizar, Sair
        botoes.append(Botao(espacamento, ALTURA - 100, botao_largura, 60, "Ver Pedido", mudar_para_pedido))
        botoes.append(Botao(espacamento * 2 + botao_largura, ALTURA - 100, botao_largura, 60, "Adicionar", adicionar_item_ui))
        botoes.append(Botao(espacamento * 3 + botao_largura * 2, ALTURA - 100, botao_largura, 60, "Finalizar", finalizar_pedido_ui))
        botoes.append(Botao(espacamento * 4 + botao_largura * 3, ALTURA - 100, botao_largura, 60, "Sair", sair_programa))
        
    elif estado_atual == "pedido":
        # Botões da tela do pedido: Voltar, Remover, Limpar, Finalizar
        botoes.append(Botao(espacamento, ALTURA - 100, botao_largura, 60, "Voltar", mudar_para_menu))
        botoes.append(Botao(espacamento * 2 + botao_largura, ALTURA - 100, botao_largura, 60, "Remover", iniciar_remocao))
        botoes.append(Botao(espacamento * 3 + botao_largura * 2, ALTURA - 100, botao_largura, 60, "Limpar", limpar_pedido))
        botoes.append(Botao(espacamento * 4 + botao_largura * 3, ALTURA - 100, botao_largura, 60, "Finalizar", finalizar_pedido_ui))
    
    elif estado_atual == "conta":
        # Botões da tela da conta: Novo Pedido, Sair
        botao_largura_pequeno = min(180, LARGURA // 4 - 20)
        espacamento_conta = (LARGURA - (2 * botao_largura_pequeno)) // 3
        botoes.append(Botao(espacamento_conta, ALTURA - 100, botao_largura_pequeno, 60, "Novo Pedido", novo_pedido))
        botoes.append(Botao(espacamento_conta * 2 + botao_largura_pequeno, ALTURA - 100, botao_largura_pequeno, 60, "Sair", sair_programa))

def criar_itens_menu():
    """Cria objetos ItemMenu a partir dos dados"""
    global itens_menu_obj, scrollbar
    
    itens_menu_obj.clear()
    for i, (nome, preco, categoria) in enumerate(menu):
        itens_menu_obj.append(ItemMenu(nome, preco, categoria, i))
    
    altura_conteudo = calcular_altura_conteudo_menu()
    scrollbar = Scrollbar(LARGURA - 40, 120, ALTURA - 220, altura_conteudo)

def criar_itens_pedido():
    """Cria objetos para os itens do pedido (para seleção)"""
    global itens_pedido_obj, scrollbar_pedido
    
    itens_pedido_obj.clear()
    itens_agrupados = agrupar_itens_pedido()
    
    for i, (nome, preco, categoria, quantidade) in enumerate(itens_agrupados):
        item_obj = {
            'nome': nome,
            'preco': preco,
            'categoria': categoria,
            'quantidade': quantidade,
            'index': i,
            'selecionado': False,
            'rect': None
        }
        itens_pedido_obj.append(item_obj)
    
    # Calcular altura do conteúdo do pedido para a scrollbar (INCLUINDO O TOTAL)
    altura_conteudo = calcular_altura_conteudo_pedido()
    scrollbar_pedido = Scrollbar(LARGURA - 40, 120, ALTURA - 220, altura_conteudo)

def criar_conta_scrollbar():
    """Cria a scrollbar para a tela da conta"""
    global scrollbar_conta
    
    altura_conteudo = calcular_altura_conteudo_conta()
    scrollbar_conta = Scrollbar(LARGURA - 40, 120, ALTURA - 220, altura_conteudo)

def calcular_altura_conteudo_menu():
    """Calcula a altura total do conteúdo do menu"""
    altura = 0
    categoria_atual = None
    
    for nome, preco, categoria in menu:
        if categoria != categoria_atual:
            categoria_atual = categoria
            altura += 50
        altura += 45
    
    return altura

def calcular_altura_conteudo_pedido():
    """Calcula a altura total do conteúdo do pedido (INCLUINDO TOTAL)"""
    if not pedido:
        return 100  # Altura mínima para mensagem "pedido vazio"
    
    altura = 60  # Altura do título "SEU PEDIDO"
    categoria_atual = None
    
    for nome, preco, categoria, quantidade in agrupar_itens_pedido():
        if categoria != categoria_atual:
            categoria_atual = categoria
            altura += 50  # Espaço para categoria
        altura += 45  # Espaço para item
    # Adicionar espaço para linha separadora, total e espaço extra para evitar
    # que o total fique coberto pelos botões na parte inferior da tela.
    # 80 = 20 (espaço) + 30 (linha) + 30 (total); + espaco_botao para garantir visualização
    espaco_botao = 140  # espaço reservado para rodapé/botões
    altura += 80 + espaco_botao

    return altura

def calcular_altura_conteudo_conta():
    """Calcula a altura total do conteúdo da conta"""
    if not pedido:
        return 100  # Altura mínima
    
    altura = 80  # Altura do título "CONTA FINAL"
    
    for nome, preco, categoria, quantidade in agrupar_itens_pedido():
        altura += 45  # Espaço para cada item
    
    # Adicionar espaço para linha separadora, total e mensagem
    altura += 140
    
    return altura

# ================================
# AÇÕES DOS BOTÕES E NAVEGAÇÃO
# ================================

def mudar_para_pedido():
    """Muda o estado da aplicação para visualizar o pedido atual."""
    global estado_atual, scroll_y, item_selecionado, item_pedido_selecionado, scroll_pedido_y
    estado_atual = "pedido"
    scroll_y = 0
    scroll_pedido_y = 0
    item_selecionado = None
    item_pedido_selecionado = None
    criar_botoes()
    criar_itens_pedido()

def mudar_para_menu():
    """Muda o estado da aplicação de volta para o menu."""
    global estado_atual, item_selecionado, scroll_y, item_pedido_selecionado
    estado_atual = "menu"
    item_selecionado = None
    item_pedido_selecionado = None
    scroll_y = 0
    criar_botoes()

def novo_pedido():
    """
    Limpa o pedido atual e volta ao menu, permitindo iniciar um novo pedido.
    Chamado após o cliente finalizar e ver a conta.
    """
    global estado_atual, pedido, item_selecionado, scroll_y, scroll_conta_y, metodo_pagamento
    estado_atual = "menu"
    pedido.clear()
    item_selecionado = None
    scroll_y = 0
    scroll_conta_y = 0
    metodo_pagamento = None  # Resetar método de pagamento para próximo pedido
    criar_botoes()

def adicionar_item_ui():
    """Adiciona o item do menu selecionado ao pedido."""
    if item_selecionado is not None:
        item = menu[item_selecionado]
        pedido.append(item)
        # Resetar seleção visual no menu após adicionar
        for item_obj in itens_menu_obj:
            item_obj.selecionado = False

def iniciar_remocao():
    """
    Inicia o processo de remoção de um item do pedido.
    Se o item tem apenas 1 unidade, remove diretamente.
    Se tem múltiplas, abre um pop-up para escolher a quantidade.
    """
    global popup_visivel, popup_tipo, item_para_remover, quantidade_a_remover
    
    if item_pedido_selecionado is not None:
        item_info = itens_pedido_obj[item_pedido_selecionado]
        quantidade_total = item_info['quantidade']
        
        if quantidade_total == 1:
            # Remover diretamente se é apenas 1 unidade
            remover_item_pedido(item_info)
        else:
            # Abrir pop-up para escolher quantidade
            popup_visivel = True
            popup_tipo = "remover"
            item_para_remover = item_info
            quantidade_a_remover = 1

def remover_item_pedido(item_info, quantidade=1):
    """
    Remove um número específico de unidades de um item do pedido.
    Atualiza o estado e a interface após remover.
    """
    global pedido, item_pedido_selecionado
    
    nome = item_info['nome']
    preco = item_info['preco']
    categoria = item_info['categoria']
    
    # Contar quantas unidades foram removidas
    removidos = 0
    nova_lista = []
    
    # Percorrer o pedido e remover apenas as unidades necessárias
    for item in pedido:
        item_nome, item_preco, item_categoria = item
        
        # Se é o item a remover e ainda não removemos o suficiente, skip
        if (item_nome == nome and item_preco == preco and 
            item_categoria == categoria and removidos < quantidade):
            removidos += 1
            continue
        
        nova_lista.append(item)
    
    # Atualizar pedido com a nova lista
    pedido.clear()
    pedido.extend(nova_lista)
    
    # Recriar lista de itens do pedido com update visual
    item_pedido_selecionado = None
    criar_itens_pedido()

def confirmar_remocao():
    """Confirma a remoção com a quantidade especificada no pop-up."""
    global popup_visivel, popup_tipo, quantidade_a_remover, item_para_remover
    
    if item_para_remover:
        # Verificar se quantidade é válida
        if 1 <= quantidade_a_remover <= item_para_remover['quantidade']:
            remover_item_pedido(item_para_remover, quantidade_a_remover)
    
    # Fechar pop-up e resetar valores
    popup_visivel = False
    popup_tipo = None
    item_para_remover = None
    quantidade_a_remover = 1

def cancelar_remocao():
    """Cancela o processo de remoção e fecha o pop-up."""
    global popup_visivel, popup_tipo, item_para_remover, quantidade_a_remover
    popup_visivel = False
    popup_tipo = None
    item_para_remover = None
    quantidade_a_remover = 1

def limpar_selecao():
    """Remove a seleção visual de todos os itens do menu."""
    global item_selecionado
    item_selecionado = None
    for item_obj in itens_menu_obj:
        item_obj.selecionado = False

def limpar_pedido():
    """Limpa todos os itens do pedido e redefine o estado."""
    global pedido, item_pedido_selecionado
    pedido.clear()
    item_pedido_selecionado = None
    criar_itens_pedido()

def abrir_popup_pagamento():
    """Abre o pop-up para o utilizador escolher o método de pagamento."""
    global popup_visivel, popup_tipo
    popup_visivel = True
    popup_tipo = "pagamento"

def confirmar_pagamento_numerario():
    """Confirma pagamento em numerário e vai para a conta."""
    global metodo_pagamento, popup_visivel, popup_tipo, estado_atual, scroll_conta_y
    metodo_pagamento = "numerario"
    popup_visivel = False
    popup_tipo = None
    estado_atual = "conta"
    scroll_conta_y = 0
    criar_botoes()
    criar_conta_scrollbar()

def confirmar_pagamento_cartao():
    """Confirma pagamento em cartão e vai para a conta."""
    global metodo_pagamento, popup_visivel, popup_tipo, estado_atual, scroll_conta_y
    metodo_pagamento = "cartao"
    popup_visivel = False
    popup_tipo = None
    estado_atual = "conta"
    scroll_conta_y = 0
    criar_botoes()
    criar_conta_scrollbar()

def cancelar_popup_pagamento():
    """Cancela o pop-up de pagamento e volta ao pedido."""
    global popup_visivel, popup_tipo
    popup_visivel = False
    popup_tipo = None

def finalizar_pedido_ui():
    """Valida o pedido e abre o pop-up de pagamento se há itens."""
    global popup_visivel, popup_tipo
    if pedido:  # Só finalizar se há itens no pedido
        abrir_popup_pagamento()

# ================================
# FUNÇÕES AUXILIARES DE DESENHO
# ================================

def desenhar_item_com_preco(tela, x_esquerda, x_direita, y, texto_item, preco, 
                            cor_texto=COR_TEXTO, cor_preco=COR_TEXTO_SECUNDARIO,
                            fonte_item=FONTE_ITEM, fonte_preco=FONTE_PRECO):
    """
    Função auxiliar que desenha um item com seu preço.
    Coloca o texto do item à esquerda e o preço à direita.
    """
    # Desenhar nome/descrição do item
    item_surf = fonte_item.render(texto_item, True, cor_texto)
    tela.blit(item_surf, (x_esquerda, y))
    
    # Desenhar preço à direita
    preco_surf = fonte_preco.render(preco, True, cor_preco)
    preco_rect = preco_surf.get_rect()
    preco_rect.right = x_direita
    preco_rect.top = y
    tela.blit(preco_surf, preco_rect)

def desenhar_categoria(tela, x, y, categoria_nome, cor=COR_TEXTO_SECUNDARIO):
    """
    Função auxiliar que desenha um cabeçalho de categoria.
    """
    cat_surf = FONTE_CATEGORIA.render(categoria_nome.upper(), True, cor)
    tela.blit(cat_surf, (x, y))
    # Linha separadora sob a categoria
    pygame.draw.line(tela, (100, 100, 100), (x, y + 40), (x + 300, y + 40), 2)

def aplicar_area_clipping(tela, x, y, largura, altura):
    """
    Aplica uma área de recorte (clipping) retangular para limitar o desenho.
    Útil para implementar scroll sem desenhar fora dos limites.
    """
    clip_rect = pygame.Rect(x, y, largura, altura)
    tela.set_clip(clip_rect)
    return clip_rect

def remover_area_clipping(tela):
    """Remove a área de clipping, permitindo desenho em toda a tela."""
    tela.set_clip(None)

# ================================
# FUNÇÕES DE DESENHO PRINCIPAL
# ================================

def desenhar_moldura(tela):
    """Desenha uma moldura decorativa de madeira ao redor da tela."""
    # Desenhar borda exterior
    pygame.draw.rect(tela, COR_BORDA, (0, 0, LARGURA, ALTURA), 15)
    
    # Desenhar cantos decorativos para simular textura de madeira
    tamanho_canto = 40
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (10, 10, tamanho_canto, 10))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (10, 10, 10, tamanho_canto))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (LARGURA-50, 10, tamanho_canto, 10))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (LARGURA-20, 10, 10, tamanho_canto))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (10, ALTURA-20, tamanho_canto, 10))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (10, ALTURA-50, 10, tamanho_canto))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (LARGURA-50, ALTURA-20, tamanho_canto, 10))
    pygame.draw.rect(tela, COR_BOTAO_HOVER, (LARGURA-20, ALTURA-50, 10, tamanho_canto))

def desenhar_cabecalho(tela, titulo):
    """
    Desenha o cabeçalho da tela com fundo escuro e título.
    
    Args:
        tela: Surface do PyGame onde desenhar
        titulo: Texto a mostrar como título
    """
    # Desenhar fundo do cabeçalho
    pygame.draw.rect(tela, (40, 35, 30), (0, 0, LARGURA, 100))
    
    # Desenhar título centrado
    titulo_surf = FONTE_TITULO.render(titulo, True, COR_DESTAQUE)
    titulo_rect = titulo_surf.get_rect(center=(LARGURA//2, 50))
    tela.blit(titulo_surf, titulo_rect)
    
    # Desenhar linha separadora bajo o cabeçalho
    pygame.draw.line(tela, COR_TEXTO_SECUNDARIO, (100, 90), (LARGURA-100, 90), 3)

def desenhar_menu(tela, eventos):
    """
    Desenha o menu completo com todas as categorias e itens com scroll.
    Processa também eventos de scroll (roda do mouse e arrastamento).
    """
    global scroll_y
    
    # Atualizar scroll baseado na entrada do utilizador
    if scrollbar:
        scroll_y = scrollbar.atualizar(pygame.mouse.get_pos(), eventos)
    
    # Aplicar clipping para não desenhar fora do limite
    aplicar_area_clipping(tela, 50, 120, LARGURA - 100, ALTURA - 230)
    
    y = 120 - scroll_y
    categoria_atual = None
    
    # Desenhar cada item do menu
    for item_obj in itens_menu_obj:
        # Atualizar estado de seleção
        item_obj.selecionado = (item_selecionado == item_obj.index)
        
        # Desenhar cabeçalho de categoria se mudou
        if categoria_atual != item_obj.categoria:
            categoria_atual = item_obj.categoria
            # Desenhar apenas se estiver visível
            if y + 50 > 120 and y < ALTURA - 80:
                desenhar_categoria(tela, 100, y, categoria_atual)
            y += 50
            
            # Desenhar linha separadora sob a categoria
            if y - scroll_y - 10 > 120 and y - scroll_y - 10 < ALTURA - 80:
                pygame.draw.line(tela, (100, 100, 100), (100, y-10), (LARGURA-140, y-10), 2)
        
        # Desenhar item se estiver visível na tela
        if y > 120 - 45 and y < ALTURA - 80:
            item_obj.desenhar(tela, 120, y)
        
        y += 45
    
    # Remover clipping e desenhar scrollbar
    remover_area_clipping(tela)
    
    if scrollbar and scrollbar.scroll_max > 0:
        scrollbar.desenhar(tela)

def desenhar_pedido(tela, eventos):
    """
    Desenha a lista do pedido atual com scroll.
    Permite selecionar itens para remover.
    Mostra também o total no final da lista.
    """
    global scroll_pedido_y, itens_pedido_obj
    
    # Atualizar scroll baseado na entrada do utilizador
    if scrollbar_pedido:
        scroll_pedido_y = scrollbar_pedido.atualizar(pygame.mouse.get_pos(), eventos)
    
    # Aplicar clipping para limitar desenho
    aplicar_area_clipping(tela, 50, 120, LARGURA - 100, ALTURA - 230)
    
    y = 120 - scroll_pedido_y
    
    # Desenhar título da seção
    pedido_surf = FONTE_CATEGORIA.render("SEU PEDIDO", True, COR_DESTAQUE)
    tela.blit(pedido_surf, (LARGURA//2 - pedido_surf.get_width()//2, y))
    y += 60
    
    if not pedido:
        # Mostrar mensagem se pedido vazio
        vazio_surf = FONTE_ITEM.render("O pedido está vazio.", True, COR_TEXTO_SECUNDARIO)
        tela.blit(vazio_surf, (LARGURA//2 - vazio_surf.get_width()//2, y))
        y += 80
    else:
        categoria_atual = None
        itens_desenhados = 0
        total_itens = len(itens_pedido_obj)
        
        # Desenhar cada item do pedido
        for i, item_obj in enumerate(itens_pedido_obj):
            nome = item_obj['nome']
            preco = item_obj['preco']
            categoria = item_obj['categoria']
            quantidade = item_obj['quantidade']
            
            # Desenhar cabeçalho de categoria se mudou
            if categoria != categoria_atual:
                categoria_atual = categoria
                cat_surf = FONTE_CATEGORIA.render(categoria.upper(), True, COR_TEXTO_SECUNDARIO)
                if y + 50 > 120 and y < ALTURA - 80:
                    tela.blit(cat_surf, (150, y))
                y += 50
            
            # Desenhar item se estiver visível
            if y > 120 - 45 and y < ALTURA - 80:
                # Determinar cor baseada em seleção
                cor = COR_DESTAQUE if item_pedido_selecionado == i else COR_TEXTO
                
                # Desenhar quantidade e nome do item
                item_texto = f"{quantidade}x {nome}"
                item_surf = FONTE_ITEM.render(item_texto, True, cor)
                tela.blit(item_surf, (170, y))
                
                # Desenhar preço total do item (quantidade * preço unitário)
                total_item = preco * quantidade
                preco_texto = f"{total_item:.2f}€"
                desenhar_item_com_preco(tela, 170, LARGURA - 150, y, "", preco_texto, 
                                       cor, COR_TEXTO_SECUNDARIO)
                
                # Guardar retângulo para deteção de clique
                item_obj['rect'] = pygame.Rect(160, y-5, LARGURA - 180, 40)
                
                # Desenhar retângulo de seleção se item está selecionado
                if item_pedido_selecionado == i:
                    pygame.draw.rect(tela, (255, 255, 255, 50), item_obj['rect'], 2, border_radius=5)
            
            y += 45
            itens_desenhados += 1
            
            # Se é o último item, adicionar linha separadora e total
            if i == total_itens - 1:
                # Espaço antes da linha
                if y > 120 - 20 and y < ALTURA - 80:
                    y += 20
                    pygame.draw.line(tela, COR_TEXTO, (150, y), (LARGURA-150, y), 2)
                    y += 30
                    
                    # Desenhar total
                    total = calcular_total_pedido()
                    total_texto = f"TOTAL: {total:.2f}€"
                    total_surf = FONTE_CATEGORIA.render(total_texto, True, COR_DESTAQUE)
                    total_rect = total_surf.get_rect()
                    total_rect.right = LARGURA - 150
                    total_rect.top = y
                    
                    if y > 120 - 30 and y < ALTURA - 80:
                        tela.blit(total_surf, total_rect)
            
            # Verificar se chegou ao limite de tela
            if y > ALTURA - 80 + scroll_pedido_y:
                if itens_desenhados < total_itens:
                    # Mostrar indicador de mais itens
                    mais_surf = FONTE_ITEM.render("... mais itens (faça scroll para ver o total)", 
                                                  True, COR_TEXTO_SECUNDARIO)
                    tela.blit(mais_surf, (LARGURA//2 - mais_surf.get_width()//2, ALTURA - 120))
                break
    
    # Remover clipping e desenhar scrollbar
    remover_area_clipping(tela)
    
    if scrollbar_pedido and scrollbar_pedido.scroll_max > 0:
        scrollbar_pedido.desenhar(tela)

def desenhar_popup(tela):
    """
    Desenha um pop-up modal genérico que se adapta ao tipo de popup.
    Tipos suportados: "remover" (quantidade de itens), "pagamento" (escolha método)
    
    Retorna um dicionário com os retângulos dos botões para deteção de clique.
    """
    global quantidade_a_remover, popup_tipo
    
    # Desenhar fundo semi-transparente para escurecer a tela atrás
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # 150 = nível de transparência
    tela.blit(overlay, (0, 0))
    
    # Dimensões base do pop-up
    popup_largura = 550
    popup_altura = 380
    popup_x = (LARGURA - popup_largura) // 2
    popup_y = (ALTURA - popup_altura) // 2
    
    # ========================
    # POP-UP DE REMOÇÃO DE ITENS
    # ========================
    if popup_tipo == "remover":
        # Desenhar fundo do pop-up com borda
        pygame.draw.rect(tela, COR_POPUP_FUNDO, (popup_x, popup_y, popup_largura, popup_altura), border_radius=15)
        pygame.draw.rect(tela, COR_POPUP_BORDA, (popup_x, popup_y, popup_largura, popup_altura), 3, border_radius=15)
        
        # Desenhar título
        titulo = "Quantos itens pretende remover?"
        titulo_surf = FONTE_POPUP.render(titulo, True, COR_POPUP_TEXTO)
        titulo_x = popup_x + (popup_largura - titulo_surf.get_width()) // 2
        titulo_y = popup_y + 30
        tela.blit(titulo_surf, (titulo_x, titulo_y))
        
        # Informação do item a remover
        if item_para_remover:
            # Desenhar nome do item
            item_texto = f"{item_para_remover['nome']}"
            item_surf = FONTE_POPUP_PEQUENA.render(item_texto, True, COR_POPUP_TEXTO)
            item_x = popup_x + (popup_largura - item_surf.get_width()) // 2
            tela.blit(item_surf, (item_x, popup_y + 80))
            
            # Desenhar quantidade disponível no pedido
            quantidade_texto = f"Quantidade no pedido: {item_para_remover['quantidade']}"
            quantidade_surf = FONTE_POPUP_PEQUENA.render(quantidade_texto, True, COR_TEXTO_SECUNDARIO)
            quantidade_x = popup_x + (popup_largura - quantidade_surf.get_width()) // 2
            tela.blit(quantidade_surf, (quantidade_x, popup_y + 120))
        
        # Rótulo para a quantidade a remover
        qtd_texto = f"Quantidade a remover:"
        qtd_surf = FONTE_POPUP_PEQUENA.render(qtd_texto, True, COR_POPUP_TEXTO)
        qtd_x = popup_x + (popup_largura - qtd_surf.get_width()) // 2
        tela.blit(qtd_surf, (qtd_x, popup_y + 180))
        
        # Desenhar valor da quantidade (grande e destacado)
        valor_qtd_texto = f"{quantidade_a_remover}"
        valor_qtd_surf = FONTE_CATEGORIA.render(valor_qtd_texto, True, COR_DESTAQUE)
        valor_qtd_x = popup_x + (popup_largura - valor_qtd_surf.get_width()) // 2
        tela.blit(valor_qtd_surf, (valor_qtd_x, popup_y + 210))
        
        # Criar botões para controlar a quantidade (- e +)
        btn_tamanho = 50
        espacamento_btns = 80
        
        # Botão "-" (diminuir quantidade)
        menos_x = valor_qtd_x - espacamento_btns - btn_tamanho//2
        menos_y = popup_y + 210 + valor_qtd_surf.get_height()//2 - btn_tamanho//2
        menos_rect = pygame.Rect(menos_x, menos_y, btn_tamanho, btn_tamanho)
        
        # Botão "+" (aumentar quantidade)
        mais_x = valor_qtd_x + espacamento_btns - btn_tamanho//2
        mais_y = popup_y + 210 + valor_qtd_surf.get_height()//2 - btn_tamanho//2
        mais_rect = pygame.Rect(mais_x, mais_y, btn_tamanho, btn_tamanho)
        
        # Desenhar os botões - e +
        pygame.draw.rect(tela, COR_BOTAO, menos_rect, border_radius=25)
        pygame.draw.rect(tela, COR_BOTAO, mais_rect, border_radius=25)
        
        # Desenhar símbolos nos botões
        menos_text = FONTE_BOTAO.render("-", True, COR_TEXTO)
        mais_text = FONTE_BOTAO.render("+", True, COR_TEXTO)
        
        tela.blit(menos_text, (menos_rect.centerx - menos_text.get_width()//2, 
                               menos_rect.centery - menos_text.get_height()//2))
        tela.blit(mais_text, (mais_rect.centerx - mais_text.get_width()//2, 
                              mais_rect.centery - mais_text.get_height()//2))
        
        # Criar botões de ação (Cancelar e Confirmar)
        btn_altura = 50
        btn_largura = 180
        espacamento = 40
        
        # Botão Cancelar (à esquerda)
        cancelar_btn = pygame.Rect(popup_x + espacamento, 
                                   popup_y + popup_altura - btn_altura - 30, 
                                   btn_largura, btn_altura)
        
        # Botão Confirmar (à direita)
        confirmar_btn = pygame.Rect(popup_x + popup_largura - btn_largura - espacamento, 
                                    popup_y + popup_altura - btn_altura - 30, 
                                    btn_largura, btn_altura)
        
        # Desenhar os botões de ação
        pygame.draw.rect(tela, COR_BOTAO, cancelar_btn, border_radius=10)
        pygame.draw.rect(tela, COR_BOTAO_HOVER, confirmar_btn, border_radius=10)
        
        # Desenhar texto dos botões
        cancelar_text = FONTE_BOTAO.render("Cancelar", True, COR_TEXTO)
        confirmar_text = FONTE_BOTAO.render("Confirmar", True, COR_TEXTO)
        
        tela.blit(cancelar_text, (cancelar_btn.centerx - cancelar_text.get_width()//2, 
                                  cancelar_btn.centery - cancelar_text.get_height()//2))
        tela.blit(confirmar_text, (confirmar_btn.centerx - confirmar_text.get_width()//2, 
                                   confirmar_btn.centery - confirmar_text.get_height()//2))
        
        # Retornar dicionário com botões do pop-up remover
        return {
            'menos': menos_rect,
            'mais': mais_rect,
            'cancelar': cancelar_btn,
            'confirmar': confirmar_btn
        }
    
    # ========================
    # POP-UP DE ESCOLHA DE PAGAMENTO
    # ========================
    elif popup_tipo == "pagamento":
        # Ajustar altura do pop-up para pagamento
        popup_altura = 320
        popup_y = (ALTURA - popup_altura) // 2
        
        # Desenhar fundo do pop-up com borda
        pygame.draw.rect(tela, COR_POPUP_FUNDO, (popup_x, popup_y, popup_largura, popup_altura), border_radius=15)
        pygame.draw.rect(tela, COR_POPUP_BORDA, (popup_x, popup_y, popup_largura, popup_altura), 3, border_radius=15)
        
        # Desenhar título
        titulo = "Escolha o método de pagamento"
        titulo_surf = FONTE_POPUP.render(titulo, True, COR_POPUP_TEXTO)
        titulo_x = popup_x + (popup_largura - titulo_surf.get_width()) // 2
        titulo_y = popup_y + 30
        tela.blit(titulo_surf, (titulo_x, titulo_y))
        
        # Botão para pagamento em numerário
        btn_altura = 60
        btn_largura = 200
        espacamento_vertical = 20
        
        # Posição dos botões (verticalmente centrados)
        y_botoes = popup_y + 100
        
        # Botão Numerário (esquerda)
        numerario_btn = pygame.Rect(
            popup_x + (popup_largura // 2 - btn_largura - espacamento_vertical // 2),
            y_botoes,
            btn_largura,
            btn_altura
        )
        
        # Botão Cartão (direita)
        cartao_btn = pygame.Rect(
            popup_x + (popup_largura // 2 + espacamento_vertical // 2),
            y_botoes,
            btn_largura,
            btn_altura
        )
        
        # Desenhar botões
        pygame.draw.rect(tela, COR_BOTAO, numerario_btn, border_radius=10)
        pygame.draw.rect(tela, COR_BOTAO, cartao_btn, border_radius=10)
        
        # Desenhar texto dos botões
        numerario_text = FONTE_BOTAO.render("Numerário", True, COR_TEXTO)
        cartao_text = FONTE_BOTAO.render("Cartão", True, COR_TEXTO)
        
        tela.blit(numerario_text, (numerario_btn.centerx - numerario_text.get_width()//2,
                                   numerario_btn.centery - numerario_text.get_height()//2))
        tela.blit(cartao_text, (cartao_btn.centerx - cartao_text.get_width()//2,
                               cartao_btn.centery - cartao_text.get_height()//2))
        
        # Botão Cancelar (na base)
        cancelar_btn = pygame.Rect(
            popup_x + (popup_largura - btn_largura) // 2,
            popup_y + popup_altura - btn_altura - 30,
            btn_largura,
            btn_altura
        )
        
        # Desenhar botão cancelar
        pygame.draw.rect(tela, (80, 80, 80), cancelar_btn, border_radius=10)
        cancelar_text = FONTE_BOTAO.render("Cancelar", True, COR_TEXTO)
        tela.blit(cancelar_text, (cancelar_btn.centerx - cancelar_text.get_width()//2,
                                 cancelar_btn.centery - cancelar_text.get_height()//2))
        
        # Retornar dicionário com botões do pop-up pagamento
        return {
            'numerario': numerario_btn,
            'cartao': cartao_btn,
            'cancelar': cancelar_btn
        }
    
    return {}

def desenhar_conta(tela, eventos):
    """
    Desenha a conta final com todos os itens e o valor total a pagar.
    Inclui scroll para visualizar itens se houver muitos.
    """
    global scroll_conta_y
    
    # Atualizar scroll baseado na entrada do utilizador
    if scrollbar_conta:
        scroll_conta_y = scrollbar_conta.atualizar(pygame.mouse.get_pos(), eventos)
    
    # Aplicar clipping para limitar desenho
    aplicar_area_clipping(tela, 50, 120, LARGURA - 100, ALTURA - 230)
    
    y = 120 - scroll_conta_y
    
    # Desenhar título da conta
    conta_surf = FONTE_TITULO.render("CONTA FINAL", True, COR_DESTAQUE)
    tela.blit(conta_surf, (LARGURA//2 - conta_surf.get_width()//2, y))
    y += 80
    
    if pedido:
        itens_agrupados = agrupar_itens_pedido()
        total = 0
        total_itens = len(itens_agrupados)
        
        # Desenhar cada item da conta
        for idx, (nome, preco, categoria, quantidade) in enumerate(itens_agrupados):
            # Calcular total do item (antes do if para sempre ter valor)
            total_item = preco * quantidade
            
            # Desenhar item se estiver visível
            if y > 120 - 45 and y < ALTURA - 80:
                # Preparar textos
                item_texto = f"{quantidade}x {nome}"
                preco_texto = f"{total_item:.2f}€"
                
                # Desenhar nome e preço do item
                item_surf = FONTE_ITEM.render(item_texto, True, COR_TEXTO)
                tela.blit(item_surf, (200, y))
                
                preco_surf = FONTE_PRECO.render(preco_texto, True, COR_TEXTO_SECUNDARIO)
                preco_rect = preco_surf.get_rect()
                preco_rect.right = LARGURA - 200
                preco_rect.top = y
                tela.blit(preco_surf, preco_rect)
            
            # Adicionar ao total geral
            total += total_item
            y += 45
            
            # Se é o último item, adicionar linha separadora e total
            if idx == total_itens - 1:
                # Desenhar linha separadora se visível
                if y > 120 - 30 and y < ALTURA - 80:
                    y += 30
                    pygame.draw.line(tela, COR_DESTAQUE, (200, y), (LARGURA-200, y), 3)
                    y += 50
                    
                    # Desenhar total a pagar
                    total_texto = f"TOTAL A PAGAR: {total:.2f}€"
                    total_surf = FONTE_CATEGORIA.render(total_texto, True, COR_DESTAQUE)
                    if y > 120 - 50 and y < ALTURA - 80:
                        tela.blit(total_surf, (LARGURA//2 - total_surf.get_width()//2, y))
                        y += 60
                        
                        # Desenhar método de pagamento escolhido
                        if metodo_pagamento:
                            metodo_texto = "Pagamento em Numerário" if metodo_pagamento == "numerario" else "Pagamento em Cartão"
                            metodo_surf = FONTE_POPUP.render(metodo_texto, True, COR_TEXTO_SECUNDARIO)
                            if y > 120 - 50 and y < ALTURA - 80:
                                tela.blit(metodo_surf, (LARGURA//2 - metodo_surf.get_width()//2, y))
                                y += 50
                        
                        # Desenhar mensagem de agradecimento
                        obrigado_surf = FONTE_ITEM.render("Obrigado! Volte sempre!", True, COR_TEXTO_SECUNDARIO)
                        if y > 120 - 60 and y < ALTURA - 80:
                            tela.blit(obrigado_surf, (LARGURA//2 - obrigado_surf.get_width()//2, y))
    
    # Remover clipping e desenhar scrollbar
    remover_area_clipping(tela)
    
    if scrollbar_conta and scrollbar_conta.scroll_max > 0:
        scrollbar_conta.desenhar(tela)

def desenhar_rodape(tela):
    """
    Desenha informações no rodapé da tela.
    O conteúdo varia dependendo do estado atual da aplicação.
    """
    y = ALTURA - 40
    
    if estado_atual == "menu":
        # No menu, mostrar quantidade de itens no pedido
        qtd_texto = f"Itens no pedido: {len(pedido)}"
        qtd_surf = FONTE_PEDIDO.render(qtd_texto, True, COR_TEXTO_SECUNDARIO)
        tela.blit(qtd_surf, (LARGURA - 250, y))
        
        # Mostrar instruções (dinâmicas baseado em seleção)
        if item_selecionado is not None:
            instr_texto = "Item Selecionado. Clique em \"Adicionar\" para adicionar."
        else:
            instr_texto = "Clique em um item para selecionar • Use a roda do mouse para scroll"
        instr_surf = FONTE_PEDIDO.render(instr_texto, True, COR_TEXTO_SECUNDARIO)
        tela.blit(instr_surf, (50, y))
    
    elif estado_atual == "pedido":
        # No pedido, mostrar instruções sobre seleção de itens
        if item_pedido_selecionado is not None:
            instr_texto = "Item selecionado. Clique em 'Remover' para remover."
            instr_surf = FONTE_PEDIDO.render(instr_texto, True, COR_TEXTO_SECUNDARIO)
            tela.blit(instr_surf, (50, y))
        else:
            instr_texto = "Clique em um item do pedido para selecioná-lo"
            instr_surf = FONTE_PEDIDO.render(instr_texto, True, COR_TEXTO_SECUNDARIO)
            tela.blit(instr_surf, (50, y))

# ================================
# REDIMENSIONAMENTO E LOOP PRINCIPAL
# ================================

def redimensionar_tela(nova_largura, nova_altura):
    """
    Redimensiona a tela e atualiza todos os elementos da interface.
    Chamado quando o utilizador redimensiona a janela.
    """
    global LARGURA, ALTURA, TELA, scrollbar, scrollbar_pedido, scrollbar_conta
    LARGURA = nova_largura
    ALTURA = nova_altura
    # Recriar a surface do PyGame com novo tamanho
    TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    # Recriar todos os elementos para se adaptarem ao novo tamanho
    criar_botoes()
    criar_itens_menu()
    if estado_atual == "pedido":
        criar_itens_pedido()
    elif estado_atual == "conta":
        criar_conta_scrollbar()

def main():
    """
    Loop principal da aplicação.
    Processa eventos, atualiza estado e desenha a interface.
    """
    global item_selecionado, estado_atual, scroll_y, LARGURA, ALTURA
    global item_pedido_selecionado, quantidade_a_remover, scroll_pedido_y, scroll_conta_y
    
    # Inicializar elementos da interface
    criar_itens_menu()
    criar_botoes()
    
    # Clock para controlar frame rate (60 FPS)
    clock = pygame.time.Clock()
    
    # Dicionário para guardar retângulos dos botões do pop-up
    popup_botoes = {}
    
    while True:
        pos_mouse = pygame.mouse.get_pos()
        
        # Coletar todos os eventos do PyGame
        eventos = []
        for event in pygame.event.get():
            eventos.append(event)
            
            if event.type == pygame.QUIT:
                # Utilizador fecha a janela
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.VIDEORESIZE:
                # Utilizador redimensiona a janela
                redimensionar_tela(event.w, event.h)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    # Se pop-up está visível, processar cliques nele primeiro
                    if popup_visivel:
                        # ===== POP-UP DE REMOÇÃO =====
                        if popup_tipo == "remover":
                            if 'menos' in popup_botoes and popup_botoes['menos'].collidepoint(pos_mouse):
                                # Botão para diminuir quantidade
                                if quantidade_a_remover > 1:
                                    quantidade_a_remover -= 1
                            elif 'mais' in popup_botoes and popup_botoes['mais'].collidepoint(pos_mouse):
                                # Botão para aumentar quantidade
                                if item_para_remover and quantidade_a_remover < item_para_remover['quantidade']:
                                    quantidade_a_remover += 1
                            elif 'cancelar' in popup_botoes and popup_botoes['cancelar'].collidepoint(pos_mouse):
                                # Botão para cancelar a remoção
                                cancelar_remocao()
                            elif 'confirmar' in popup_botoes and popup_botoes['confirmar'].collidepoint(pos_mouse):
                                # Botão para confirmar a remoção
                                confirmar_remocao()
                        
                        # ===== POP-UP DE PAGAMENTO =====
                        elif popup_tipo == "pagamento":
                            if 'numerario' in popup_botoes and popup_botoes['numerario'].collidepoint(pos_mouse):
                                # Botão pagamento em numerário
                                confirmar_pagamento_numerario()
                            elif 'cartao' in popup_botoes and popup_botoes['cartao'].collidepoint(pos_mouse):
                                # Botão pagamento em cartão
                                confirmar_pagamento_cartao()
                            elif 'cancelar' in popup_botoes and popup_botoes['cancelar'].collidepoint(pos_mouse):
                                # Botão para cancelar (voltar ao pedido)
                                cancelar_popup_pagamento()
                        
                        # Não processar mais cliques se o pop-up está aberto
                        continue
                    
                    # Verificar clique nos botões principais
                    for botao in botoes:
                        if botao.verificar_clique(pos_mouse):
                            break
                    
                    # Verificar clique nos itens do menu (apenas no estado "menu")
                    if estado_atual == "menu":
                        mouse_y_ajustado = pos_mouse[1] + scroll_y
                        y = 120
                        categoria_atual = None
                        item_index = 0
                        
                        # Procurar qual item foi clicado
                        for nome, preco, categoria in menu:
                            if categoria != categoria_atual:
                                categoria_atual = categoria
                                y += 50
                            
                            item_rect = pygame.Rect(100, y, LARGURA - 200, 40)
                            item_rect_na_tela = pygame.Rect(100, y - scroll_y, LARGURA - 200, 40)
                            
                            # Verificar se o item está visível e foi clicado
                            if (item_rect_na_tela.top < ALTURA - 100 and 
                                item_rect_na_tela.bottom > 120):
                                
                                if item_rect_na_tela.collidepoint(pos_mouse):
                                    item_selecionado = item_index
                                    break
                            
                            y += 45
                            item_index += 1
                    
                    # Verificar clique nos itens do pedido (apenas no estado "pedido")
                    elif estado_atual == "pedido":
                        # Procurar qual item do pedido foi clicado
                        for i, item_obj in enumerate(itens_pedido_obj):
                            if item_obj['rect'] and item_obj['rect'].collidepoint(pos_mouse):
                                # Toggle selection (selecionar ou deselecionar)
                                if item_pedido_selecionado == i:
                                    item_pedido_selecionado = None  # Deselecionar
                                else:
                                    item_pedido_selecionado = i  # Selecionar novo item
                                break
        
        # Atualizar estado visual dos botões (hover effect)
        for botao in botoes:
            botao.atualizar(pos_mouse)
        
        # ===== DESENHO DA INTERFACE =====
        # Limpar a tela
        TELA.fill(COR_FUNDO)
        # Desenhar moldura decorativa
        desenhar_moldura(TELA)
        
        # Desenhar conteúdo específico baseado no estado atual
        if estado_atual == "menu":
            # Mostrar menu completo com categorias e itens
            desenhar_cabecalho(TELA, "RESTAURANTE ITALIANO - MENU DO DIA")
            desenhar_menu(TELA, eventos)
        elif estado_atual == "pedido":
            # Mostrar pedido atual do cliente
            desenhar_cabecalho(TELA, "SEU PEDIDO")
            desenhar_pedido(TELA, eventos)
        elif estado_atual == "conta":
            # Mostrar conta final a pagar
            desenhar_cabecalho(TELA, "OBRIGADO PELA VISITA!")
            desenhar_conta(TELA, eventos)
        
        # Desenhar os botões de ação
        for botao in botoes:
            botao.desenhar(TELA)
        
        # Desenhar informações no rodapé
        desenhar_rodape(TELA)
        
        # Desenhar pop-up de confirmação se estiver visível
        if popup_visivel:
            popup_botoes = desenhar_popup(TELA)
        
        # Atualizar a tela para mostrar o desenho
        pygame.display.flip()
        # Controlar velocidade (60 FPS)
        clock.tick(60)

# ================================
# PONTO DE ENTRADA DA APLICAÇÃO
# ================================

if __name__ == "__main__":
    main()