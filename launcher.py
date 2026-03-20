import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import time

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(application_path)

PYTHON_VERSION = "3.12.3"
PYTHON_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

ENV_DIR = ".env_dashboard"
PYTHON_EXE = os.path.join(ENV_DIR, "python.exe")

def print_msg(msg):
    print(f"\n>>> {msg}\n" + "-"*60)

def setup_portable_python():
    # Verifica se a versao mudou — se sim, recria o ambiente
    version_file = os.path.join(ENV_DIR, ".python_version")
    if os.path.exists(PYTHON_EXE):
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                installed_version = f.read().strip()
            if installed_version == PYTHON_VERSION:
                return  # Versao correta, prossegue
        # Versao diferente ou arquivo nao existe — recria
        print_msg(f"Versao do Python mudou para {PYTHON_VERSION}. Recriando ambiente...")
        shutil.rmtree(ENV_DIR, ignore_errors=True)

    print_msg("Configurando motor independente emulando ambiente Python...")
    os.makedirs(ENV_DIR, exist_ok=True)
    
    zip_path = os.path.join(ENV_DIR, "python_embed.zip")
    urllib.request.urlretrieve(PYTHON_URL, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(ENV_DIR)
        
    os.remove(zip_path)
    
    # Enable site-packages in embedded python (so pip works)
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
                    
    # Install pip
    print_msg("Baixando e instalando gerenciador de pacotes (pip)...")
    pip_script = os.path.join(ENV_DIR, "get-pip.py")
    urllib.request.urlretrieve(GET_PIP_URL, pip_script)
    subprocess.run([PYTHON_EXE, pip_script], check=True)
    os.remove(pip_script)

    # Salva a versao instalada para verificacao futura
    with open(version_file, "w") as f:
        f.write(PYTHON_VERSION)

def main():
    print_msg("INICIANDO DASHBOARD O TIMAO AUTOMATIZADO")
    
    try:
        # 1. Setup Python Portable
        setup_portable_python()
        
        # 2. Install Requirements
        if os.path.exists("requirements.txt"):
            print_msg("Instalando/Verificando dependencias do projeto...")
            subprocess.run([PYTHON_EXE, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            
        # 3. Create Mocks if missing
        mock_file = os.path.join("Mock", "staging", "Tiflux", "Tiflux_tb_Clientes_MOCK.csv")
        if not os.path.exists(mock_file):
            print_msg("Primeira execucao: Gerando base de dados sintetica. Isso pode levar alguns segundos...")
            subprocess.run([PYTHON_EXE, "Mock/gerar_mock.py"], check=True)
        else:
            print_msg("Base de dados encontrada. Pulando etapa de geracao de Mock.")
            
        # 4. Run Streamlit
        print_msg("Iniciando o Dashboard! O seu navegador sera aberto em instantes...")
        subprocess.run([PYTHON_EXE, "-m", "streamlit", "run", "app.py"])
        
    except Exception as e:
        print_msg(f"OCORREU UM ERRO DURANTE A EXECUCAO:\n{e}")
        input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()
