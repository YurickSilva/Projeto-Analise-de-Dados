import pandas as pd
from pathlib import Path
import time
import os
from utils.logger import setup_logger

logger = setup_logger("datasets")

# Raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_csv(sistema: str, tabela: str) -> pd.DataFrame:
    # Lógica de prioridade: 
    # 1. Tenta carregar da pasta Mock (para o GitHub/Testes)
    # 2. Se não existir, tenta carregar da pasta data/staging real
    
    mock_path = PROJECT_ROOT / "Mock" / "data" / "staging" / sistema / f"{tabela}.csv"
    real_path = PROJECT_ROOT / "data" / "staging" / sistema / f"{tabela}.csv"

    if mock_path.exists():
        path = mock_path
        logger.info(f"Utilizando dados de MOCK (Fictícios) | path={path}")
    else:
        path = real_path
        logger.info(f"Utilizando dados REAIS | path={path}")

    inicio = time.time()
    logger.info(f"Iniciando carga | sistema={sistema} | tabela={tabela}")

    if not path.exists():
        logger.error(f"Arquivo não encontrado em nenhum dos caminhos: {path}")
        raise FileNotFoundError(f"CSV não encontrado: {tabela}.csv")

    # Adicionamos low_memory=False para evitar warnings em colunas mistas
    df = pd.read_csv(path, low_memory=False)

    duracao = round(time.time() - inicio, 3)
    logger.info(
        f"Carga concluída | sistema={sistema} | tabela={tabela} "
        f"| linhas={len(df)} | colunas={len(df.columns)} | tempo={duracao}s"
    )

    return df