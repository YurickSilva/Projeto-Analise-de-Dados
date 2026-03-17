import pandas as pd
from pathlib import Path
import time
from utils.logger import setup_logger

logger = setup_logger("datasets")

# raiz do projeto (plataforma_bi/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "data"

def load_csv(sistema: str, tabela: str) -> pd.DataFrame:
    path = BASE_PATH / "staging" / sistema / f"{tabela}.csv"

    inicio = time.time()
    logger.info(f"Iniciando carga | sistema={sistema} | tabela={tabela} | path={path}")

    if not path.exists():
        logger.error(f"Arquivo não encontrado: {path}")
        raise FileNotFoundError(f"CSV não encontrado: {path}")

    df = pd.read_csv(path)

    duracao = round(time.time() - inicio, 3)
    logger.info(
        f"Carga concluída | sistema={sistema} | tabela={tabela} "
        f"| linhas={len(df)} | colunas={len(df.columns)} | tempo={duracao}s"
    )

    return df