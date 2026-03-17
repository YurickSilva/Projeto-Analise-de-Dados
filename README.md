# Demonstração Análise de Dados - Voyzer Dashboard

Dashboard de análise de dados desenvolvido com Streamlit para monitoramento de métricas comerciais e operacionais, focado em BI (Business Intelligence).

---

## 🚀 Como Visualizar o Projeto (Dados de Demonstração)

Para proteger dados sensíveis e cumprir as diretrizes da **LGPD**, este repositório não contém os bancos de dados reais. O projeto utiliza um sistema de **Auto-Inicialização** para facilitar o teste por recrutadores e desenvolvedores.

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Gere os dados fictícios:**
    Para que os gráficos e tabelas funcionem, você precisa gerar a base de dados sintética:
    ```bash
    python Mock/mocker.py
    ```

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
- **Controladoria**: Dashboards financeiros e análise de receita.
- **TI Global**: Monitoramento completo de atendimentos via integração **Tiflux**, incluindo métricas de tickets, performance de técnicos e SLA.

---

## 📂 Estrutura do Projeto

```text
├── app.py                # Ponto de entrada da aplicação
├── Mock/                 # Ambiente de demonstração
│   ├── mocker.py         # Gerador de dados fictícios (CSVs)
│   ├── mockuser.py       # Gerador automático de credenciais de teste
│   └── data/             # Pasta de destino dos CSVs sintéticos
├── auth/                 # Lógica de login e tratamento de YAML
├── components/           # Componentes modulares de interface
├── datasets/             # Camada de abstração e carga de dados (Loaders)
├── metrics/              # Lógica de negócio e cálculos de KPIs
├── workspaces/           # Páginas e módulos do dashboard
├── utils/                # Loggers e estilos globais
└── config/               # Armazena users.yaml (protegido via .gitignore)