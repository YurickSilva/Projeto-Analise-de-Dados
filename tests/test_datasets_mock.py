import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

# Agora os imports devem funcionar
from datasets.tiflux import tickets, clientes, apontamentos, valores_extras
import os

print("\n--- Testando Carregamento de Dados Mock ---")
try:
    df_tickets = tickets()
    print(f"SUCESSO: Tickets carregados com sucesso: {len(df_tickets)} linhas")
except Exception as e:
    print(f"ERRO: Erro ao carregar Tickets: {e}")

try:
    df_clientes = clientes()
    print(f"SUCESSO: Clientes carregados com sucesso: {len(df_clientes)} linhas")
except Exception as e:
    print(f"ERRO: Erro ao carregar Clientes: {e}")

try:
    df_apontamentos = apontamentos()
    print(f"SUCESSO: Apontamentos carregados com sucesso: {len(df_apontamentos)} linhas")
except Exception as e:
    print(f"ERRO: Erro ao carregar Apontamentos: {e}")

try:
    df_valores_extras = valores_extras()
    print(f"SUCESSO: Valores extras carregados com sucesso: {len(df_valores_extras)} linhas")
except Exception as e:
    print(f"ERRO: Erro ao carregar Valores extras: {e}")
print("--- Fim do Teste ---\n")
