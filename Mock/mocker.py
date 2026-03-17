import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker('pt_BR')

# Configurações de volume
NUM_CLIENTES = 30
NUM_TICKETS = 150
NUM_APONTAMENTOS = 400

def generate_tiflux_data():
    print("Iniciando geração de dados completos para o portfólio...")

    # --- 1. TABELA CLIENTES ---
    clientes_list = []
    for i in range(NUM_CLIENTES):
        id_cli = i + 1
        nome_fantasia = fake.company()
        clientes_list.append({
            "Id_cliente": id_cli, "Cliente": nome_fantasia, "Razao_social": f"{nome_fantasia} LTDA",
            "Situacao": random.choice(["Ativo", "Inativo"]), "Criado_em": fake.date_this_decade(),
            "Atualizado_em": datetime.now(), "Tipo_de_contrato": random.choice(["Mensal", "Anual"]),
            "Contrato": f"CTR-{random.randint(100, 999)}", "FMH_Help_Desk": random.randint(0, 1),
            "FM_On_Site_SSP": 0, "FM_Help_Desk": 1, "FM_LABIN": 0, "FM_Telefonia": 0,
            "FM_On_Site_Ti": random.randint(0, 1), "FMH_On_site_Ti": 0, "FMH_On_site_SSP": 0,
            "Grupo_cliente": random.choice(["Varejo", "Indústria", "Tecnologia"]),
            "Setor": "Geral", "CEP": fake.postcode(), "Cidade": fake.city(), "Estado": fake.state_abbr()
        })
    df_clientes = pd.DataFrame(clientes_list)

    # --- 2. TABELA TICKETS ---
    tickets_list = []
    tecnicos = [fake.name() for _ in range(5)] # Lista fixa de técnicos para consistência
    
    for i in range(NUM_TICKETS):
        id_tkt = 1000 + i
        cli = df_clientes.sample(1).iloc[0]
        data_criacao = fake.date_time_between(start_date='-1y', end_date='now')
        fechado = random.choice([True, True, False])
        
        tickets_list.append({
            "Id_ticket": id_tkt, "Id_cliente": cli["Id_cliente"], "Cliente": cli["Cliente"],
            "Desc_ticket": fake.sentence(), "Situacao": "Fechado" if fechado else "Aberto",
            "Mesa": random.choice(["Suporte N1", "Suporte N2"]), "Responsavel": random.choice(tecnicos),
            "Solicitado_por": fake.name(), "Email_responsavel": fake.email(), "Ultima_resposta": datetime.now(),
            "Nome_estagio": "Concluído" if fechado else "Em Atendimento", "Prioridade": random.choice(["Baixa", "Média", "Alta"]),
            "Catalogo_de_Servicos": "TI", "Item": "Suporte Técnico", "Criado_em": data_criacao,
            "Data_1o_apontamento": data_criacao + timedelta(minutes=random.randint(10, 60)),
            "Fechado_em": data_criacao + timedelta(hours=random.randint(1, 48)) if fechado else None,
            "Avaliacao": random.randint(3, 5) if fechado else None, "SLA_atendido": random.choice(["Sim", "Não"]),
            "Duracao_apontada": random.randint(30, 180), "Tempo_total_fechamento": random.randint(60, 500),
            "Link_chamado": f"https://tiflux.com/tkt/{id_tkt}"
        })
    df_tickets = pd.DataFrame(tickets_list)

    # --- 3. TABELA APONTAMENTOS ---
    apontamentos_list = []
    for i in range(NUM_APONTAMENTOS):
        tkt = df_tickets.sample(1).iloc[0]
        duracao_min = random.randint(15, 90)
        apontamentos_list.append({
            "Id_apontamento": 5000 + i, "Id_ticket": tkt["Id_ticket"], "Desc_apontamento": fake.text(max_nb_chars=50),
            "Cliente": tkt["Cliente"], "Mesa": tkt["Mesa"], "Tecnico": tkt["Responsavel"],
            "Solicitado_por": tkt["Solicitado_por"], "Servico_avulso": "Não", "Assistencia": "Não",
            "Garantia": "Não", "Duracao": str(timedelta(minutes=duracao_min)), 
            "Data_apontamento": fake.date_time_between(start_date=tkt["Criado_em"], end_date='now'),
            "Data_encerramento": datetime.now(), "Valor_apontamento": round(duracao_min * 1.2, 2),
            "Latitude": float(fake.latitude()), "Longitude": float(fake.longitude())
        })
    df_apontamentos = pd.DataFrame(apontamentos_list)

    # --- 4. TABELA VALORES EXTRAS (Para evitar o erro no tiflux.py) ---
    df_extras = pd.DataFrame(columns=["Id_ticket", "Campo", "Valor"]) # Tabela vazia mas com colunas

    # --- SALVAMENTO ---
    path = "data/staging/Tiflux/"
    os.makedirs(path, exist_ok=True)

    df_clientes.to_csv(f"{path}Tiflux_tb_Clientes.csv", index=False)
    df_tickets.to_csv(f"{path}Tiflux_tb_Tickets.csv", index=False)
    df_apontamentos.to_csv(f"{path}Tiflux_tb_Apontamentos.csv", index=False)
    df_extras.to_csv(f"{path}Tiflux_tb_Valores_extras.csv", index=False)

    print(f"✅ Sucesso! {NUM_TICKETS} Tickets gerados em: {path}")

if __name__ == "__main__":
    generate_tiflux_data()