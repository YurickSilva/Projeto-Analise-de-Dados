import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import time

# ─── Diretórios ───────────────────────────────────────────────
# Se estiver rodando como .exe (frozen), os arquivos empacotados
# ficam em sys._MEIPASS. Caso contrário, usa o diretório do script.
if getattr(sys, 'frozen', False):
    BUNDLED_DIR = sys._MEIPASS  # pasta temporaria onde o PyInstaller extrai os datas
    BASE_DIR = os.path.dirname(sys.executable)  # pasta onde o .exe está
else:
    BUNDLED_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = BUNDLED_DIR

PROJECT_DIR = os.path.join(BASE_DIR, "Dashboard_Projeto")

PYTHON_VERSION = "3.12.3"
PYTHON_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

ENV_DIR = os.path.join(PROJECT_DIR, ".env_dashboard")
PYTHON_EXE = os.path.join(ENV_DIR, "python.exe")

def print_msg(msg):
    print(f"\n>>> {msg}\n" + "-"*60)

# ─── Etapa 0: Extrair arquivos do projeto ──────────────────────
def extract_project_files():
    """Copia os arquivos empacotados pelo PyInstaller para a pasta do projeto."""
    if os.path.exists(os.path.join(PROJECT_DIR, "app.py")):
        print_msg("Arquivos do projeto ja existem. Pulando extracao.")
        return

    print_msg("Extraindo arquivos do projeto pela primeira vez...")
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Lista de arquivos e pastas que foram empacotados
    items_to_copy = [
        "app.py", "navigation.py", "router.py", "requirements.txt",
        "auth", "components", "datasets", "metrics",
        "workspaces", "services", "utils", "Mock", ".streamlit"
    ]

    for item in items_to_copy:
        src = os.path.join(BUNDLED_DIR, item)
        dst = os.path.join(PROJECT_DIR, item)
        if not os.path.exists(src):
            continue
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    print_msg("Arquivos extraidos com sucesso!")

# ─── Etapa 1: Setup Python Portable ───────────────────────────
def setup_portable_python():
    version_file = os.path.join(ENV_DIR, ".python_version")
    if os.path.exists(PYTHON_EXE):
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                installed_version = f.read().strip()
            if installed_version == PYTHON_VERSION:
                return
        print_msg(f"Versao do Python mudou para {PYTHON_VERSION}. Recriando ambiente...")
        shutil.rmtree(ENV_DIR, ignore_errors=True)

    print_msg("Baixando Python portatil (isso pode levar alguns minutos na primeira vez)...")
    os.makedirs(ENV_DIR, exist_ok=True)

    zip_path = os.path.join(ENV_DIR, "python_embed.zip")
    urllib.request.urlretrieve(PYTHON_URL, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(ENV_DIR)
    os.remove(zip_path)

    # Habilita site-packages no Python embedded (para o pip funcionar)
    pth_file = None
    for f in os.listdir(ENV_DIR):
        if f.startswith("python") and f.endswith("._pth"):
            pth_file = os.path.join(ENV_DIR, f)
            break

    if pth_file:
        with open(pth_file, "r") as f:
            lines = f.readlines()
        with open(pth_file, "w") as f:
            for line in lines:
                if line.strip() == "#import site":
                    f.write("import site\n")
                else:
                    f.write(line)

    # Instala o pip
    print_msg("Instalando gerenciador de pacotes (pip)...")
    pip_script = os.path.join(ENV_DIR, "get-pip.py")
    urllib.request.urlretrieve(GET_PIP_URL, pip_script)
    subprocess.run([PYTHON_EXE, pip_script], check=True)
    os.remove(pip_script)

    # Salva a versão instalada
    with open(version_file, "w") as f:
        f.write(PYTHON_VERSION)

# ─── Main ─────────────────────────────────────────────────────
def main():
    print_msg("INICIANDO DASHBOARD - ANALISE DE DADOS")
    print(f"    Diretorio do projeto: {PROJECT_DIR}")

    try:
        # 0. Extrair arquivos empacotados
        extract_project_files()

        # Muda o diretório de trabalho para a pasta do projeto
        os.chdir(PROJECT_DIR)

        # 1. Setup Python Portátil
        setup_portable_python()

        # 2. Instalar Dependências
        req_file = os.path.join(PROJECT_DIR, "requirements.txt")
        if os.path.exists(req_file):
            print_msg("Instalando/Verificando dependencias do projeto...")
            subprocess.run([PYTHON_EXE, "-m", "pip", "install", "-r", req_file], check=True)

        # 3. Gerar Mocks se necessário
        mock_file = os.path.join(PROJECT_DIR, "Mock", "staging", "Tiflux", "Tiflux_tb_Clientes_MOCK.csv")
        if not os.path.exists(mock_file):
            print_msg("Primeira execucao: Gerando base de dados sintetica...")
            mock_script = os.path.join(PROJECT_DIR, "Mock", "gerar_mock.py")
            subprocess.run([PYTHON_EXE, mock_script], check=True)
        else:
            print_msg("Base de dados encontrada. Pulando geracao de Mock.")

        # 4. Iniciar Streamlit
        print_msg("Iniciando o Dashboard! O navegador sera aberto em instantes...")
        subprocess.run([PYTHON_EXE, "-m", "streamlit", "run", os.path.join(PROJECT_DIR, "app.py")])

    except Exception as e:
        print_msg(f"OCORREU UM ERRO DURANTE A EXECUCAO:\n{e}")
        input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()
