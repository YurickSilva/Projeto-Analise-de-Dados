# Demonstração Análise de Dados

Dashboard de análise de dados desenvolvido com Streamlit para monitoramento de métricas comerciais e operacionais, focado em BI (Business Intelligence).

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Versão](https://img.shields.io/badge/Versão-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualização-3F4F75?logo=plotly&logoColor=white)
![YAML](https://img.shields.io/badge/Config-YAML-CB171E?logo=yaml&logoColor=white)
![BCrypt](https://img.shields.io/badge/Segurança-BCrypt-black?logo=security&logoColor=white)
![LGPD](https://img.shields.io/badge/Compliance-LGPD-blue)

---

## 🚀 Como Rodar o Projeto

Para proteger dados sensíveis, cumprir as diretrizes da **LGPD** e respeitar os limites de armazenamento do GitHub, este repositório **não contém** os bancos de dados reais e nem os arquivos `.csv`. Os dados de demonstração são gerados automaticamente na primeira execução.

Existem **duas formas** de rodar o projeto:

### Opção 1 — Executável Automático (Recomendado para qualquer usuário)

> Esta é a forma mais simples. Não precisa ter Python instalado no computador.

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/YurickSilva/Projeto-Analise-de-Dados.git
    cd Projeto-Analise-de-Dados
    ```

2. **Compile o executável** (necessita [Python](https://www.python.org/downloads/) e [PyInstaller](https://pyinstaller.org/)):
    ```bash
    pip install pyinstaller
    python -m PyInstaller Iniciar_Dashboard.spec
    move dist\Iniciar_Dashboard.exe .\Iniciar_Dashboard.exe
    ```

3. **Execute o `Iniciar_Dashboard.exe`** que estará na raiz do projeto.

O executável fará **tudo automaticamente**:
- ✅ **Extrai** os arquivos do projeto para uma pasta chamada `Dashboard_Projeto` ao lado do `.exe`.
- ✅ **Configura** um Python 3.12 portátil dentro dessa pasta.
- ✅ **Instala** todas as dependências do `requirements.txt`.
- ✅ **Gera** a base de dados sintética (Mock) na primeira execução.
- ✅ **Inicia** o Dashboard no navegador.

> **Requisitos:** Windows 64-bit com acesso à internet (apenas na primeira execução).

### Opção 2 — Execução Manual (Para desenvolvedores)

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/YurickSilva/Projeto-Analise-de-Dados.git
    cd Projeto-Analise-de-Dados
    ```

2. **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Gere os dados fictícios (Mock):**
    ```bash
    python Mock/gerar_mock.py
    ```
    > Este script cria automaticamente a estrutura de pastas `Mock/staging/Tiflux/` e popula os arquivos `.csv` mockados (Clientes, Tickets, Apontamentos e Valores Extras). Pode levar alguns segundos.

4. **Inicie o Dashboard:**
    ```bash
    streamlit run app.py
    ```

---

## 🔑 Login de Teste

Na primeira execução, o sistema cria automaticamente as credenciais de teste:

- **Usuário**: `loginpadrao`
- **Senha**: `senha1234`

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| **Streamlit** | Frontend e interface web |
| **Streamlit Authenticator** | Autenticação (Cookies + Hash BCrypt) |
| **Pandas / NumPy** | Análise e manipulação de dados |
| **Plotly** | Gráficos interativos |
| **Folium** | Mapas interativos |
| **AgGrid** | Tabelas com seleção e ordenação |
| **Faker** | Geração de dados sintéticos (LGPD) |
| **PyYAML** | Configuração de usuários |
| **Loguru** | Sistema de logging |

---

## 💡 Funcionalidades

### 🔐 Autenticação e Segurança
- **Auto-Geração de Configuração**: O sistema verifica a existência do arquivo `users.yaml`. Caso ausente, gera um ambiente de teste seguro automaticamente.
- **Persistência**: Sistema de login com persistência via cookies.
- **Controle de Acesso**: Workspaces restritos por permissões de usuário (Roles).

### 📊 Workspaces Disponíveis
- **Home**: Visão geral e boas-vindas.
- **TI Global**: Monitoramento completo de atendimentos via integração **Tiflux**, incluindo métricas de tickets, performance de técnicos e SLA.

---

## 📂 Estrutura do Projeto

```text
├── app.py                           # Ponto de entrada da aplicação
├── launcher.py                      # Lançador automático (compila para .exe)
├── Iniciar_Dashboard.spec           # Receita PyInstaller para gerar o .exe
├── navigation.py                    # Construção dinâmica do menu
├── router.py                        # Roteamento de páginas
├── requirements.txt                 # Dependências do projeto
│
├── auth/                            # Sistema de autenticação e autorização
│   ├── authenticator.py             # Login, registro e hash de senhas
│   └── authorization.py             # Controle de acesso por workspace
│
├── components/                      # Componentes reutilizáveis da UI
│   ├── cards.py                     # Componentes KPI (métricas)
│   ├── filters.py                   # Filtros (período, multiselect, hierárquico)
│   ├── graphs.py                    # Gráficos (linhas, barras, donut, área)
│   ├── maps.py                      # Mapas interativos (Folium)
│   └── tables.py                    # Tabelas com seleção (AgGrid)
│
├── datasets/                        # Loaders e abstrações de dados
│   ├── loader.py                    # Carregador genérico de CSVs
│   └── tiflux.py                    # Loader específico para dados Tiflux
│
├── metrics/                         # Lógica de negócio e KPIs
│   ├── base.py                      # Cálculos base e utilitários
│   ├── agg.py                       # Funções de agregação
│   ├── ti.py                        # Métricas de TI e tickets
│   └── interatividade.py            # Gerenciamento de seleções de usuário
│
├── workspaces/                      # Páginas e módulos do dashboard
│   ├── home.py                      # Página inicial
│   ├── admin.py                     # Painel administrativo
│   └── TI_Global/                   # Workspace de monitoramento TI
│
├── services/                        # Serviços de backend
│   └── users_service.py             # CRUD de usuários
│
├── utils/                           # Utilitários gerais
│   ├── logger.py                    # Sistema de logging
│   ├── security.py                  # Funções de segurança
│   └── styles.py                    # Estilos CSS globais
│
├── Mock/                            # Ambiente de demonstração
│   ├── gerar_mock.py                # Gerador de dados fictícios
│   └── mockuser.py                  # Gerador de credenciais de teste
│
├── config/                          # Configurações (não versionado)
│   └── users.yaml                   # Credenciais de usuários (gerado automaticamente)
│
├── visual/                          # Ativos visuais (logos, imagens)
│
└── Dashboard_Projeto/               # Pasta gerada pelo .exe (não versionada)
    ├── .env_dashboard/              # Python portátil
    └── (Arquivos do projeto extraídos)
```

---

## 🔧 Detalhes dos Módulos Principais

### Auth (`auth/`)
- **authenticator.py**: Gerencia login, registro de novos usuários e validações
- **authorization.py**: Controla permissões de acesso por workspace

### Components (`components/`)

Componentes reutilizáveis em toda a aplicação:

- **cards.py**: KPI cards com valores formatados
- **filters.py**: Filtros de período, multiselect e seleção hierárquica
- **graphs.py**: Gráficos Plotly (linhas, barras, donuts, áreas)
- **maps.py**: Mapas Folium com interatividade
- **tables.py**: Tabelas AgGrid com seleção múltipla

### Datasets (`datasets/`)

Camada de abstração para carregamento de dados:

- **loader.py**: Carregador genérico de CSVs
- **tiflux.py**: Processamento específico de dados Tiflux

### Metrics (`metrics/`)

Lógica de cálculo de métricas:

- **base.py**: Funções base de cálculo
- **ti.py**: KPIs de TI (tickets, SLA, atendimentos)
- **interatividade.py**: Gerencia seleções do usuário durante navegação

### Workspaces (`workspaces/`)

Módulos de dashboard por departamento:

- **Home**: Boas-vindas e resumo de acesso
- **TI_Global**: Dashboards de TI

### Utils (`utils/`)

- **logger.py**: Sistema de logging centralizado
- **styles.py**: CSS global (backgrounds, logos, temas)
- **security.py**: Funções de segurança

---

## 📊 Fluxo de Dados

```
app.py → login() → navigation.py → router.py → workspace.render()
                                             ↓
                                    datasets (loader)
                                             ↓
                                        metrics
                                             ↓
                                       components
                                             ↓
                                           pages
```

---

## ⚙️ Como Funciona o Executável (`launcher.py`)

O arquivo `launcher.py` é o coração do sistema de auto-inicialização. Quando compilado para `.exe` com PyInstaller, ele:

1. **Detecta o diretório de execução** — Garante que sempre rode na pasta correta.
2. **Extrai o Projeto** — Copia os arquivos-fonte internos para a pasta `Dashboard_Projeto/` ao lado do `.exe`.
3. **Baixa o Python 3.12 Embarcável** — Um Python portátil (~15MB) que não precisa de instalação.
4. **Instala o pip** — Gerenciador de pacotes para o Python portátil.
5. **Instala as dependências** — Lê o `requirements.txt` e instala tudo automaticamente.
6. **Gera os dados Mock** — Se for a primeira execução, gera a base sintética.
7. **Inicia o Streamlit** — Abre o dashboard no navegador padrão.

> **Controle de versão inteligente:** O `launcher.py` salva um arquivo `.python_version` dentro da pasta `.env_dashboard`. Se a versão configurada mudar, ele recria o ambiente automaticamente.

---

## 📝 Configuração de Usuários

O arquivo `config/users.yaml` é gerado automaticamente na primeira execução com a seguinte estrutura:

```yaml
cookie:
  expiry_days: 30
  key: plataforma-bi-key-v2
  name: plataforma_bi

credentials:
  usernames:
    usuario1:
      name: Nome do Usuário
      password: $2b$12$hashbcrypt...
      role: user
      workspaces:
        - home
        - ti
```

### Roles Disponíveis

- **admin**: Acesso total (wildcard `*`)
- **user**: Acesso restrito por workspace

---

## 🚀 Desenvolvimento

### Adicionar Novo Workspace

1. Criar pasta em `workspaces/novo_workspace/`
2. Criar arquivo `novo_modulo.py` com função `render()`
3. Importar em `router.py`
4. Adicionar ao menu em `navigation.py`

### Adicionar Novo Componente

1. Criar função em `components/novo_componente.py`
2. Importar em páginas conforme necessário

### Adicionar Novo Loader de Dados

1. Criar classe em `datasets/novo_loader.py`
2. Herdar de estrutura base em `loader.py`

---

## 📋 Checklist de Primeiro Acesso

- [ ] Clonar o repositório
- [ ] Compilar o `.exe` ou criar ambiente virtual manualmente
- [ ] Executar o sistema (`.exe` ou `streamlit run app.py`)
- [ ] Fazer login com credenciais de teste (`loginpadrao` / `senha1234`)
- [ ] Explorar workspaces disponíveis

---

## 📄 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `requirements.txt` | Dependências do projeto |
| `launcher.py` | Lançador automático do dashboard |
| `Iniciar_Dashboard.spec` | Receita para compilar o `.exe` |
| `config/users.yaml` | Credenciais (não versionado no GitHub) |
| `.gitignore` | Protege arquivos sensíveis |

---

## 🤝 Contribuindo

Para adicionar novas funcionalidades:

1. Crie um branch
2. Adicione dados/lógica em `datasets/` e `metrics/`
3. Crie componentes em `components/`
4. Integre em um workspace
5. Faça teste local
6. Commit com mensagem clara

---

## 📞 Suporte

Para dúvidas sobre estrutura ou funcionamento, consulte:

- Arquivos `.py` na raiz (app.py, router.py, navigation.py)
- Docstrings nas funções principais
- Arquivos de log em `logs/`
