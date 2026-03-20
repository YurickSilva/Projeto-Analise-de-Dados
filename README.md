# Demonstração Análise de Dados

Dashboard de análise de dados desenvolvido com Streamlit para monitoramento de métricas comerciais e operacionais, focado em BI (Business Intelligence).

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Versão](https://img.shields.io/badge/Versão-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualização-3F4F75?logo=plotly&logoColor=white)
![YAML](https://img.shields.io/badge/Config-YAML-CB171E?logo=yaml&logoColor=white)
![BCrypt](https://img.shields.io/badge/Segurança-BCrypt-black?logo=security&logoColor=white)
![LGPD](https://img.shields.io/badge/Compliance-LGPD-blue)
---

## 🚀 Como Visualizar o Projeto (Dados de Demonstração)

Para proteger dados sensíveis, cumprir as diretrizes da **LGPD** e respeitar os limites de armazenamento do GitHub, este repositório **não contém** os bancos de dados reais e nem os arquivos de dados `.csv` de demonstração (que são extensos e excedem o limite de tamanho do GitHub).

O projeto utiliza um sistema de **Auto-Inicialização** e um script gerador de mock para facilitar o teste por recrutadores e desenvolvedores localmente.

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Gere os dados fictícios (Mock):**
    Como os arquivos de dados de demonstração não estão no GitHub devido ao seu tamanho, você precisará gerar a base de dados sintética localmente para que os gráficos e tabelas do dashboard funcionem. Execute o comando abaixo:
    ```bash
    python Mock/gerar_mock.py
    ```
    > **Atenção:** Este script criará automaticamente a estrutura de pastas `mock/staging/Tiflux/` e vai popular os arquivos `.csv` mockados (Clientes, Tickets, Apontamentos e Valores Extras) necessários para rodar a aplicação. Tenha paciência, pois a geração da base contendo milhares de registros pode levar alguns segundos.

3.  **Inicie o Dashboard:**
    ```bash
    streamlit run app.py
    ```
    *Nota: No primeiro acesso, o sistema detectará a ausência do arquivo de configuração e criará automaticamente as credenciais de teste abaixo.*

---

## 🔑 Login de Teste
- **Usuário**: `loginpadrao`
- **Senha**: `senha1234`

---

## 🛠️ Tecnologias

- **Frontend**: Streamlit 1.54
- **Autenticação**: Streamlit Authenticator (Cookies + Hash BCrypt)
- **Análise de Dados**: Pandas, NumPy
- **Visualização**: Plotly, Folium (Mapas)
- **Componentes UI**: Streamlit Antd Components
- **Dados Sintéticos**: Faker (Engenharia de dados sintéticos)

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
├── navigation.py                    # Construção dinâmica do menu
├── router.py                        # Roteamento de páginas
├── requirements.txt                 # Dependências do projeto
│
├── auth/                            # Sistema de autenticação e autorização
│   ├── authenticator.py             # Login, registro e hash de senhas
│   ├── authorization.py             # Controle de acesso por workspace
│   └── __init__.py
│
├── components/                      # Componentes reutilizáveis da UI
│   ├── cards.py                     # Componentes KPI (métricas)
│   ├── filters.py                   # Filtros (período, multiselect, hierárquico)
│   ├── graphs.py                    # Gráficos (linhas, barras, donut, área)
│   ├── maps.py                      # Mapas interativos (Folium)
│   ├── tables.py                    # Tabelas com seleção (AgGrid)
│   └── __init__.py
│
├── datasets/                        # Loaders e abstrações de dados
│   ├── loader.py                    # Carregador genérico de CSVs
│   ├── tiflux.py                    # Loader específico para dados Tiflux
│   └── __init__.py
│
├── metrics/                         # Lógica de negócio e KPIs
│   ├── base.py                      # Cálculos base e utilitários
│   ├── ti.py                        # Métricas de TI e tickets
│   ├── interatividade.py            # Gerenciamento de seleções de usuário
│   └── __init__.py
│
├── workspaces/                      # Páginas e módulos do dashboard
│   ├── home.py                      # Página inicial
│   ├── admin.py                     # Painel administrativo
│   ├── TI_Global/
│   │   ├── paginas.py               # Páginas do Workspace de Ti_Global
│   │   └── __init__.py
│   └── __init__.py
│
├── utils/                           # Utilitários gerais
│   ├── logger.py                    # Sistema de logging
│   ├── security.py                  # Funções de segurança
│   ├── styles.py                    # Estilos CSS globais
│   └── __init__.py
│
├── config/                          # Configurações
│   └── users.yaml                   # Credenciais de usuários (gerado automaticamente)
│
│
├── logs/                            # Arquivos de log (gerados automaticamente)
│
│
├── visual/                          # Ativos visuais
│
├── Mock/                            # Ambiente de demonstração (opcional)
│   ├── gerar_mock.py                    # Gerador de dados fictícios
│   ├── mockuser.py                  # Gerador de credenciais de teste
│   ├── data/                        # Dados sintéticos(Seguindo LGPD)
│   └── staging/                     # Dados em estágio
│       └── Tiflux/                  # Dados Tiflux (CSVs)
│           ├── Tiflux_tb_Apontamentos_MOCK.csv
│           ├── Tiflux_tb_Clientes_MOCK.csv
│           └── Tiflux_tb_Tickets_MOCK.csv
│
├── venv_bi/                         # Ambiente virtual Python
│
└── README.md                        # Este arquivo
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

## 📋 Checklist de Primeiro Acesso

- [ ] Instalar dependências: `pip install -r requirements.txt`
- [ ] Gerar dados fictícios localmente (Obrigatório!): `python Mock/gerar_mock.py`
- [ ] Executar app: `streamlit run app.py`
- [ ] Fazer login com credenciais de teste
- [ ] Explorar workspaces disponíveis

---

## 📄 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `requirements.txt` | Dependências do projeto |
| `config/users.yaml` | Credenciais (não é postado no GitHub) |
| `.gitignore` | Protege arquivos sensíveis |
| `mock/staging/` | Dados de entrada do projeto |
| `logs/` | Registros de execução |

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
