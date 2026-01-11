# 🍝 Sistema de Menu Interativo - Restaurante Italiano

## 📋 Descrição do Projeto

O **Sistema de Menu Interativo** é uma aplicação gráfica desenvolvida em **PyGame** que simula um sistema completo de gestão de pedidos para um restaurante italiano. A aplicação oferece uma interface intuitiva e responsiva que permite aos clientes visualizar o menu, adicionar/remover itens e finalizar pedidos, gerando uma conta final com detalhes de todos os itens.

Este é um projeto educacional que demonstra conceitos avançados de programação em Python, incluindo programação orientada a objetos, gestão de estado, design de interfaces gráficas e padrões de interação com o utilizador.

---

## 🎯 Funcionalidades Principais

### Menu
- ✅ Visualização organizada do menu por categorias (Entradas, Especialidades, Pastas, Pizza, Bebidas, Sobremesas)
- ✅ Preços claramente visíveis para cada item
- ✅ Sistema de scroll para navegação fluida
- ✅ Seleção de itens para adicionar ao pedido
- ✅ Interface responsiva que se adapta ao tamanho da tela

### Gestão de Pedidos
- ✅ Adição rápida de itens ao pedido
- ✅ Visualização clara de todos os itens adicionados com quantidades
- ✅ Remoção flexível de itens (com confirmação para múltiplas unidades)
- ✅ Limpeza total do pedido
- ✅ Cálculo automático do total

### Conta Final
- ✅ Apresentação profissional de todos os itens do pedido
- ✅ Agrupamento inteligente de itens iguais
- ✅ Cálculo preciso do total a pagar
- ✅ **Escolha de método de pagamento** (Numerário ou Cartão)
- ✅ **Exibição do método de pagamento escolhido** na conta final
- ✅ Opção para iniciar um novo pedido

---

## 🛠️ Tecnologias e Dependências

### Linguagem
- **Python 3.x** - Linguagem de programação utilizada

### Bibliotecas Principais

| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| **PyGame** | 2.x+ | Rendering gráfico, gestão de eventos e interface gráfica |
| **sys** | Built-in | Funções e parâmetros do sistema |
| **os** | Built-in | Operações com o sistema de ficheiros |

### Requisitos do Sistema
- Resolução mínima recomendada: 1024x768
- Suporte a janelas redimensionáveis
- Python 3.7 ou superior
- PyGame instalado

---

## 📚 Conceitos e Padrões de Programação Utilizados

### 1. **Programação Orientada a Objetos (POO)**
- Implementação de **3 classes principais** para modelar componentes da interface
- Classes: `Botao`, `ItemMenu`, `Scrollbar`
- **Encapsulamento** de dados e métodos relacionados
- **Reutilização** de código através de herança de padrões
- **Modularização** para facilitar manutenção

### 2. **Gestão de Estado**
- Sistema de **estados finitos** global (`"menu"`, `"pedido"`, `"conta"`)
- **Variáveis de estado** para rastrear seleções, posições de scroll e modo pop-up
- **Transições suaves** entre diferentes vistas da aplicação
- Lógica clara de mudança de estado

### 3. **Padrão Responsivo**
- Interface **adaptável a diferentes resoluções** de tela
- **Recálculo dinâmico** de posições e tamanhos de elementos
- **Clipping (viewport)** para renderizar apenas o conteúdo visível (eficiência)
- Mantém proporções ao redimensionar janela

### 4. **Padrão de Evento-Ação (Event Loop)**
- **Loop de eventos principal** que processa entrada do utilizador em tempo real
- **Callbacks** associados a botões para executar ações
- **Detecção de colisões** usando rectangles para determinar cliques
- Tratamento de múltiplos tipos de eventos (mouse, teclado, janela)

### 5. **Agregação e Transformação de Dados**
- **Estruturas de dados imutáveis** (tuplas) para menu
- **Estruturas de dados mutáveis** (listas) para pedido
- **Agrupamento dinâmico** de itens iguais com contagem
- **Cálculos automáticos** baseados em dados estruturados

### 6. **Interface Modal Genérica**
- **Pop-up modal reutilizável** com suporte para múltiplos tipos
- **Overlay semi-transparente** que escurece fundo e bloqueia interação
- **Dois tipos implementados:**
  - **Pop-up de Remoção:** Controles +/- para ajustar quantidade
  - **Pop-up de Pagamento:** Botões para escolher método de pagamento
- **Impede operações acidentais** com confirmações

---

## 🔧 Arquitetura Técnica

### Estrutura de Dados

```python
# Menu (tuplas imutáveis para segurança - não pode ser modificado acidentalmente)
menu = (
    ("Bruschetta al Pomodoro", 5.50, "Entradas"),
    ("Spaghetti alla Carbonara", 13.00, "Pastas"),
    # ... mais itens
)

# Pedido (lista mutável - pode-se adicionar/remover itens)
pedido = [
    ("Pasta", 13.00, "Pastas"),      # primeira unidade
    ("Pasta", 13.00, "Pastas"),      # segunda unidade
    ("Pizza", 9.00, "Pizza"),
]

# Itens do Pedido Agrupados (para visualização)
itens_agrupados = [
    ("Pasta", 13.00, "Pastas", 2),   # 2 unidades
    ("Pizza", 9.00, "Pizza", 1),     # 1 unidade
]
```

### Fluxo de Execução

```
┌──────────────────────┐
│  INICIALIZAÇÃO       │
│  PyGame + Variáveis  │
│  + Objetos da UI     │
└───────────┬──────────┘
            │
    ┌───────▼──────────────────────┐
    │  LOOP PRINCIPAL (60 FPS)     │
    │  pygame.time.Clock()         │
    └───────┬──────────────────────┘
            │
    ┌───────▼────────────────────────┐
    │ 1. PROCESSAR EVENTOS           │
    │    • Mouse clicks              │
    │    • Keyboard input            │
    │    • Window resizing           │
    │    • Wheel scroll              │
    └───────┬────────────────────────┘
            │
    ┌───────▼────────────────────────┐
    │ 2. ATUALIZAR ESTADO            │
    │    • Scroll positions          │
    │    • Button hover effects      │
    │    • Seleções                  │
    │    • Scroll da scrollbar       │
    └───────┬────────────────────────┘
            │
    ┌───────▼────────────────────────┐
    │ 3. LIMPAR TELA                 │
    │    pygame.display.fill()       │
    └───────┬────────────────────────┘
            │
    ┌───────▼────────────────────────┐
    │ 4. DESENHAR INTERFACE          │
    │    • Moldura decorativa        │
    │    • Cabeçalho                 │
    │    • Conteúdo (por estado)     │
    │    • Botões                    │
    │    • Rodapé                    │
    │    • Pop-ups (se necessário)   │
    └───────┬────────────────────────┘
            │
    ┌───────▼────────────────────────┐
    │ 5. ATUALIZAR DISPLAY           │
    │    pygame.display.flip()       │
    │    pygame.display.update()     │
    └───────┬────────────────────────┘
            │
            │  Repetir 60 vezes por segundo
            └────────────────────────────▶
```

---

## 🎨 Componentes de Interface

### Classe `Botao`
Representa botões interativos com **efeito hover**.

**Atributos principais:**
- `rect` - Retângulo que define posição e tamanho do botão
- `texto` - String exibida no botão
- `acao` - Função callback executada ao clicar
- `cor_atual` - Cor dinâmica que muda com mouse over
- `cor_normal`, `cor_hover` - Cores pré-definidas

**Métodos principais:**
- `desenhar(tela)` - Renderiza o botão com cantos arredondados e borda
- `verificar_clique(pos)` - Detecta cliques e executa callback
- `atualizar(pos_mouse)` - Muda cor baseado em hover

### Classe `ItemMenu`
Representa um **item do menu** com funcionalidades de seleção.

**Atributos principais:**
- `nome`, `preco`, `categoria` - Dados do item
- `selecionado` - Boolean que indica se está selecionado
- `rect` - Retângulo clicável do item

**Métodos principais:**
- `desenhar(tela, x, y)` - Renderiza item com preço alinhado à direita
- Detecção automática de cliques através do `rect`

### Classe `Scrollbar`
Implementa **scrollbar vertical personalizada** com suporte completo.

**Atributos principais:**
- `scroll_y` - Posição atual de scroll em pixels
- `scroll_max` - Limite máximo de scroll permitido
- `arrastando` - Boolean indicando se thumb está sendo arrastado
- `hover` - Boolean indicando se mouse está sobre scrollbar
- `altura`, `conteudo_altura` - Dimensões para cálculos

**Métodos principais:**
- `atualizar(pos_mouse, eventos)` - Processa eventos (roda, clique, arrastar)
- `desenhar(tela)` - Renderiza scrollbar com thumb e background

**Funcionalidades:**
- Detecção de roda do mouse
- Arrastamento do thumb
- Cliques na barra de scroll
- Thumb redimensionado dinamicamente

---

## 🔑 Funções Principais do Projeto

### Gestão de Estado e Navegação
| Função | Descrição | Impacto |
|--------|-----------|---------|
| `mudar_para_menu()` | Transição para vista do menu | Reseta seleção, scroll |
| `mudar_para_pedido()` | Transição para visualização do pedido | Agrega itens, recria botões |
| `mudar_para_conta()` | Transição para conta final | Calcula total |
| `novo_pedido()` | Limpa pedido e volta ao menu | Reseta tudo |
| `criar_botoes()` | Cria botões contextuais baseado em estado | Interface dinâmica |

### Operações com Pedidos
| Função | Descrição | Parâmetros |
|--------|-----------|------------|
| `adicionar_item_ui()` | Adiciona item selecionado ao pedido | Nenhum (usa global) |
| `remover_item_pedido()` | Remove quantidade específica de um item | `item_info`, `quantidade` |
| `iniciar_remocao()` | Abre diálogo de confirmação | Nenhum (usa global) |
| `confirmar_remocao()` | Confirma remoção com quantidade do pop-up | Nenhum (usa global) |
| `cancelar_remocao()` | Cancela operação e fecha pop-up | Nenhum |
| `limpar_pedido()` | Limpa todos os itens do pedido | Nenhum |
| `agrupar_itens_pedido()` | Agrupa items iguais e conta quantidades | Retorna lista agrupada |
| `calcular_total_pedido()` | Retorna valor total do pedido | Retorna float |

### Cálculos e Dimensionamento
| Função | Descrição | Retorna |
|--------|-----------|---------|
| `calcular_altura_conteudo_menu()` | Dimensiona scrollbar do menu | int (pixels) |
| `calcular_altura_conteudo_pedido()` | Dimensiona scrollbar do pedido | int (pixels) |
| `calcular_altura_conteudo_conta()` | Dimensiona scrollbar da conta | int (pixels) |

### Renderização de Interface (Principais)
| Função | Descrição | Responsabilidade |
|--------|-----------|------------------|
| `desenhar_moldura()` | Moldura decorativa de madeira | Aspecto visual |
| `desenhar_cabecalho()` | Cabeçalho com título | Navegação visual |
| `desenhar_menu()` | Menu com scroll responsivo | Visualização menu |
| `desenhar_pedido()` | Visualização do pedido | Visualização pedido |
| `desenhar_conta()` | Conta final com total | Visualização conta |
| `desenhar_popup()` | **Pop-up modal genérico** (remover/pagamento) | **Confirmação de ações** |
| `desenhar_rodape()` | Informações contextuais | UX feedback |

### Auxiliares de Desenho (Reutilizáveis)
| Função | Descrição | Uso |
|--------|-----------|-----|
| `desenhar_item_com_preco()` | Helper para desenhar item + preço alinhado | Menu, pedido, conta |
| `desenhar_categoria()` | Helper para cabeçalho de categoria | Organização visual |
| `aplicar_area_clipping()` | Define viewport para scroll | Menu, pedido, conta |
| `remover_area_clipping()` | Remove limitações de desenho | Após clipping |

### Loop Principal e Controle
| Função | Descrição | Frequência |
|--------|-----------|------------|
| `main()` | Loop principal (60 FPS) | Executa sempre |
| `redimensionar_tela()` | Adapta interface a novo tamanho | Ao redimensionar |

---

## 🎯 Lógica Principal do Código

### 1. Ciclo de Renderização (60 FPS)

A aplicação funciona com um **loop principal** que se executa 60 vezes por segundo, garantindo fluidez e responsividade:

```python
clock = pygame.time.Clock()
while True:
    # Processar eventos de entrada
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            quit()
        # ... outros eventos
    
    # Atualizar scroll e estado
    scroll_y = scrollbar.atualizar(...)
    
    # Limpar tela
    TELA.fill(COR_FUNDO)
    
    # Desenhar camadas (back to front)
    desenhar_moldura(TELA)
    desenhar_cabecalho(TELA, "Menu")
    
    # Desenhar conteúdo baseado em estado
    if estado_atual == "menu":
        desenhar_menu(TELA, eventos)
    elif estado_atual == "pedido":
        desenhar_pedido(TELA, eventos)
    # ... etc
    
    # Desenhar botões interativos
    for botao in botoes:
        botao.desenhar(TELA)
        botao.verificar_clique(mouse_pos)
    
    # Atualizar display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS
```

### 2. Sistema de Scroll Inteligente

O scroll implementa 3 técnicas para melhor performance:

**a) Viewport Clipping (Recorte de Área)**
```python
# Define área de desenho - fora desta área não desenha
clip_rect = pygame.Rect(50, 120, LARGURA - 100, ALTURA - 230)
TELA.set_clip(clip_rect)

# Desenha conteúdo (desenhado apenas dentro do clip)
y = 120 - scroll_y
for item in itens:
    desenhar_item(TELA, x, y)
    y += altura_item

# Remove clipping
TELA.set_clip(None)
```

**b) Scrollbar Dinâmica**
- Tamanho do thumb = (altura disponível² / altura conteúdo)
- Ajusta-se automaticamente ao conteúdo
- Suporta arrastamento, cliques e roda do mouse

**c) Múltiplas Entradas**
- Roda do mouse: scroll incrementado
- Clique na barra: scroll para posição
- Arrastar thumb: scroll contínuo

### 3. Gestão de Pedido com Agrupamento

O pedido usa uma estrutura **simples mas inteligente**:

```python
# Estrutura interna (lista de tuplas repetidas)
pedido = [
    ("Pasta", 13.00, "Pastas"),  # unidade 1
    ("Pasta", 13.00, "Pastas"),  # unidade 2
    ("Pizza", 9.00, "Pizza"),    # unidade 1
]

# Função que agrupa para visualização
def agrupar_itens_pedido():
    contagem = {}
    for item in pedido:
        chave = item
        contagem[chave] = contagem.get(chave, 0) + 1
    
    # Retorna lista com quantidades
    return [
        ("Pasta", 13.00, "Pastas", 2),   # 2 unidades
        ("Pizza", 9.00, "Pizza", 1),     # 1 unidade
    ]

# Renderiza usando itens agrupados
for nome, preco, categoria, quantidade in agrupar_itens_pedido():
    texto = f"{nome} x{quantidade}"
    # Desenha...
```

**Vantagens:**
- Simples adicionar (append), remover (filter)
- Visualização clara com contagens
- Fácil calcular totais

### 4. Pop-up Modal com Overlay

A remoção de múltiplos itens usa um **padrão modal robusto**:

```python
if popup_visivel:
    # 1. Desenhar overlay semi-transparente
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # 150 = 59% transparência
    TELA.blit(overlay, (0, 0))
    
    # 2. Desenhar pop-up box
    popup_rect = pygame.Rect((x, y), (largura, altura))
    pygame.draw.rect(TELA, COR_POPUP, popup_rect)
    pygame.draw.rect(TELA, COR_POPUP_BORDA, popup_rect, 3)
    
    # 3. Desenhar conteúdo (título, item, quantity)
    desenhar_titulo(...)
    desenhar_quantidade(...)
    desenhar_botoes(...)
    
    # 4. Processar cliques apenas no pop-up
    if mouse_clique:
        if btn_menos.collidepoint(mouse_pos):
            quantidade_a_remover -= 1
        elif btn_mais.collidepoint(mouse_pos):
            quantidade_a_remover += 1
        # ... etc
```

### 5. Responsividade Dinâmica

Todos os elementos recalculam ao redimensionar:

```python
def redimensionar_tela(nova_largura, nova_altura):
    global LARGURA, ALTURA, TELA
    
    # Atualizar dimensões globais
    LARGURA = nova_largura
    ALTURA = nova_altura
    
    # Recriar surface do PyGame
    TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    
    # Recalcular tudo dinamicamente
    criar_botoes()           # Botões recentram-se
    criar_itens_menu()       # Scrollbar recalcula
    criar_itens_pedido()     # Conteúdo reposiciona
    criar_conta_scrollbar()  # Conta recalcula
```

**Cálculos responsivos:**
```python
# Botões centram-se dinamicamente
botao_largura = min(200, LARGURA // 6 - 20)
espacamento = (LARGURA - (4 * botao_largura)) // 5

# Scroll reserva espaço proporcionalmente
scrollbar_x = LARGURA - 40
scrollbar_altura = ALTURA - 230
```

---

## 🚀 Como Usar

### Instalação

1. **Clonar ou descarregar o projeto**
```bash
cd /Volumes/Bau/exercicios_materiaIPNautica/projeto_menu
```

2. **Criar ambiente virtual (opcional mas recomendado)**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows
```

3. **Instalar PyGame**
```bash
pip install pygame
```

### Execução

**Opção 1: Executar script shell (recomendado)**
```bash
./executar.sh
```

**Opção 2: Executar diretamente com Python**
```bash
python menu_restaurante.py
```

**Opção 3: Linha de comando interativa**
```bash
python3 -c "from menu_restaurante import main; main()"
```

### Controles de Utilizador

| Ação | Método | Resultado |
|------|--------|-----------|
| **Selecionar item** | Clicar no item no menu | Item fica destacado em amarelo |
| **Adicionar ao pedido** | Clicar botão "Adicionar" | Item adicionado, seleção mantida |
| **Ver pedido** | Clicar botão "Ver Pedido" | Muda para tela de pedido |
| **Remover item** | Selecionar item + clicar "Remover" | Abre pop-up se múltiplas unidades |
| **Ajustar quantidade** | Clicar +/- no pop-up | Altera quantidade a remover |
| **Confirmar remoção** | Clicar "Confirmar" | Remove quantidade especificada |
| **Finalizar pedido** | Clicar "Finalizar" | **Abre pop-up de pagamento** |
| **Escolher pagamento** | Clicar "Numerário" ou "Cartão" | **Define método e vai para conta** |
| **Scroll no menu** | Roda do mouse ou arrastar scrollbar | Navegação vertical |
| **Redimensionar janela** | Arrastar canto da janela | Interface adapta-se |
| **Novo pedido** | Clicar "Novo Pedido" (na conta) | Volta ao menu |
| **Sair do programa** | **Clicar botão "Sair"** (menu ou conta) | **Fecha a aplicação** |

---

## 📊 Estrutura de Ficheiros

```
projeto_menu/
├── menu_restaurante.py      # Aplicação principal (1300+ linhas de código)
│                             # Inclui: 3 classes, 30+ funções, comentários
├── executar.sh              # Script bash para inicialização automática
└── README.md                # Este ficheiro (documentação completa)
```

---

## 💡 Destaques Técnicos

### Eficiência
- ✅ **Viewport Clipping** - Apenas conteúdo visível é renderizado
- ✅ **Cálculos lazy** - Alturas recalculadas apenas quando necessário
- ✅ **Reutilização de objetos** - Mesmas listas de botões/itens são reutilizadas
- ✅ **60 FPS constante** - Mesmo com muitos itens no menu

### Robustez
- ✅ **Validações claras** - Verifica se item está selecionado antes de adicionar
- ✅ **Tratamento de edge cases** - Pedido vazio, quantidade zero, etc
- ✅ **Proteção de índices** - Nenhuma operação acessa índice inválido
- ✅ **Estados consistentes** - Nunca deixa estado inconsistente

### Experiência do Utilizador
- ✅ **Feedback visual** - Hover effects em botões e itens
- ✅ **Confirmações** - Pop-ups para operações irreversíveis
- ✅ **Transições suaves** - Mudanças de estado claras
- ✅ **Responsividade** - Responde imediatamente a input

### Manutenibilidade
- ✅ **Código bem comentado** - Cada seção bem documentada
- ✅ **Funções focadas** - Cada função tem responsabilidade única
- ✅ **Separação de responsabilidades** - UI, lógica, dados bem separados
- ✅ **Paleta centralizada** - Todas as cores em constantes globais
- ✅ **Fontes gerenciadas** - Todas as fontes em constantes globais
- ✅ **Nomes descritivos** - Variáveis e funções claramente nomeadas

---

## 🎓 Conceitos Aprendidos e Demonstrados

Este projeto é um **case study completo** da aplicação prática de conceitos:

### Programação
1. **POO Avançada** - 3 classes com múltiplos métodos e atributos
2. **Gestão de Eventos** - Input do utilizador em tempo real (60x/seg)
3. **Renderização Gráfica** - Desenho de UI complexa com PyGame
4. **Estruturas de Dados** - Listas, tuplas, dicionários com propósitos específicos
5. **Algoritmos** - Sorting, grouping, busca, cálculos dinâmicos

### Design e UX
6. **UI/UX Design** - Interface intuitiva, responsiva e acessível
7. **Padrões de Design** - Callback pattern, state pattern, modal pattern
8. **Feedback visual** - Hover effects, seleção, destaque

### Performance
9. **Otimização** - Rendering eficiente com clipping
10. **Responsividade** - 60 FPS constante mesmo com scroll

---

## 📝 Notas de Desenvolvimento

- A aplicação foi desenvolvida com **foco em educação** e demonstração de conceitos avançados
- O menu é uma **amostra fictícia** de um restaurante italiano real
- O sistema é **facilmente extensível** - basta adicionar itens à tupla `menu`
- **Sem dependências externas** além do PyGame (Python puro)
- Código bem organizado em **11 seções principais**
- Cada componente é **independente e reutilizável**

### Funcionalidades Recentes (v1.1)
- ✅ **Sistema de Pop-up Genérico** - Uma única função `desenhar_popup()` reutilizável
- ✅ **Pop-up de Pagamento** - Escolha entre Numerário ou Cartão/Débito
- ✅ **Exibição de Método Pagamento** - Mostra escolha na conta final
- ✅ **Melhor Organização de Código** - Suporta fácil adição de novos tipos de popup
- ✅ **Botão Sair** - Permite fechar a aplicação a partir do menu ou conta final

### Possíveis Extensões
- Adicionar persistência (guardar pedidos em BD)
- Sistema de autenticação de utilizadores
- Histórico de pedidos
- Recomendações baseadas em histórico
- Integração com sistema de pagamento real
- Modo de administrador para editar menu
- Impressão de conta
- Novos tipos de popup (confirmação genérica, etc)

---

## 👨‍💻 Autor e Contexto

Projeto desenvolvido como **exercício prático de programação em Python**, focado em:
- ✅ Desenvolvimento de interfaces gráficas avançadas
- ✅ Aplicação de padrões de programação profissionais
- ✅ Boas práticas de código e documentação
- ✅ Conceitos de UX/UI
- ✅ Otimização e performance

---

## 📄 Licença

Este projeto é fornecido **para fins educacionais**.

---

**Última atualização:** Janeiro 2026  
**Status:** ✅ Completo e Totalmente Funcional  
**Versão:** 1.1 - Com Sistema de Pop-ups Genérico
