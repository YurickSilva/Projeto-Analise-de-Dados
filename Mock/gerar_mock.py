import pandas as pd
import numpy as np
from faker import Faker
import random
import unicodedata
from datetime import datetime, timedelta

# Inicializa o Faker
fake = Faker('pt_BR')

# --- 1. FUNÇÃO DE LIMPEZA DIRETA (REMOVER ACENTOS) ---
def limpar_texto(texto):
    if not isinstance(texto, str):
        return texto
    mapa = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ç': 'c', 'ñ': 'n', 'Á': 'A', 'À': 'A', 'Â': 'A', 
        'Ã': 'A', 'Ä': 'A', 'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E', 'Í': 'I', 'Ì': 'I', 'Î': 'I', 
        'Ï': 'I', 'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ú': 'U', 'Ù': 'U', 'Û': 'U', 
        'Ü': 'U', 'Ç': 'C', 'Ñ': 'N'
    }
    for acento, sem_acento in mapa.items():
        texto = texto.replace(acento, sem_acento)
    return texto

# --- 2. LISTAS DE COERÊNCIA E CONFIGURAÇÃO ---
LISTA_LOCALIDADES = [
    {"cep": "99010-000", "cidade": "Passo Fundo", "estado": "RS", "lat": -28.2628, "long": -52.4067},
    {"cep": "88010-000", "cidade": "Florianopolis", "estado": "SC", "lat": -27.5948, "long": -48.5482},
    {"cep": "01001-000", "cidade": "Sao Paulo", "estado": "SP", "lat": -23.5505, "long": -46.6333},
    {"cep": "20010-000", "cidade": "Rio de Janeiro", "estado": "RJ", "lat": -22.9068, "long": -43.1729},
    {"cep": "30110-000", "cidade": "Belo Horizonte", "estado": "MG", "lat": -19.9167, "long": -43.9345},
    {"cep": "70040-000", "cidade": "Brasilia", "estado": "DF", "lat": -15.7942, "long": -47.8822},
    {"cep": "40010-000", "cidade": "Salvador", "estado": "BA", "lat": -12.9714, "long": -38.5014},
    {"cep": "80010-000", "cidade": "Curitiba", "estado": "PR", "lat": -25.4284, "long": -49.2733},
    {"cep": "90010-000", "cidade": "Porto Alegre", "estado": "RS", "lat": -30.0346, "long": -51.2177},
    {"cep": "60010-000", "cidade": "Fortaleza", "estado": "CE", "lat": -3.7172, "long": -38.5433},
    {"cep": "50010-000", "cidade": "Recife", "estado": "PE", "lat": -8.0578, "long": -34.8829},
    {"cep": "69005-000", "cidade": "Manaus", "estado": "AM", "lat": -3.1190, "long": -60.0217},
    {"cep": "66010-000", "cidade": "Belem", "estado": "PA", "lat": -1.4550, "long": -48.4902},
    {"cep": "74003-010", "cidade": "Goiania", "estado": "GO", "lat": -16.6869, "long": -49.2648},
    {"cep": "29010-000", "cidade": "Vitoria", "estado": "ES", "lat": -20.3155, "long": -40.3128},
    {"cep": "58010-000", "cidade": "Joao Pessoa", "estado": "PB", "lat": -7.1195, "long": -34.8450},
    {"cep": "57010-000", "cidade": "Maceio", "estado": "AL", "lat": -9.6658, "long": -35.7350},
    {"cep": "65010-000", "cidade": "Sao Luis", "estado": "MA", "lat": -2.5307, "long": -44.3068},
    {"cep": "79002-000", "cidade": "Campo Grande", "estado": "MS", "lat": -20.4697, "long": -54.6201},
    {"cep": "78005-000", "cidade": "Cuiaba", "estado": "MT", "lat": -15.6014, "long": -56.0978},
    {"cep": "64000-000", "cidade": "Teresina", "estado": "PI", "lat": -5.0920, "long": -42.8034},
    {"cep": "59010-000", "cidade": "Natal", "estado": "RN", "lat": -5.7945, "long": -35.2110},
    {"cep": "49010-000", "cidade": "Aracaju", "estado": "SE", "lat": -10.9472, "long": -37.0731},
    {"cep": "76801-000", "cidade": "Porto Velho", "estado": "RO", "lat": -8.7612, "long": -63.9039},
    {"cep": "69900-000", "cidade": "Rio Branco", "estado": "AC", "lat": -9.9754, "long": -67.8106},
    {"cep": "68900-000", "cidade": "Macapa", "estado": "AP", "lat": 0.0340, "long": -51.0694},
    {"cep": "69301-000", "cidade": "Boa Vista", "estado": "RR", "lat": 2.8235, "long": -60.6758},
    {"cep": "77001-000", "cidade": "Palmas", "estado": "TO", "lat": -10.1844, "long": -48.3336},
    {"cep": "13010-000", "cidade": "Campinas", "estado": "SP", "lat": -22.9099, "long": -47.0626},
    {"cep": "11010-000", "cidade": "Santos", "estado": "SP", "lat": -23.9608, "long": -46.3330},
    {"cep": "24020-000", "cidade": "Niteroi", "estado": "RJ", "lat": -22.8859, "long": -43.1153},
    {"cep": "89010-000", "cidade": "Blumenau", "estado": "SC", "lat": -26.9165, "long": -49.0717},
    {"cep": "89201-000", "cidade": "Joinville", "estado": "SC", "lat": -26.3044, "long": -48.8464},
    {"cep": "95010-000", "cidade": "Caxias do Sul", "estado": "RS", "lat": -29.1678, "long": -51.1794},
    {"cep": "96010-000", "cidade": "Pelotas", "estado": "RS", "lat": -31.7654, "long": -52.3376},
    {"cep": "86010-000", "cidade": "Londrina", "estado": "PR", "lat": -23.3103, "long": -51.1628},
    {"cep": "87013-000", "cidade": "Maringa", "estado": "PR", "lat": -23.4209, "long": -51.9331},
    {"cep": "38400-000", "cidade": "Uberlandia", "estado": "MG", "lat": -18.9113, "long": -48.2622},
    {"cep": "36010-000", "cidade": "Juiz de Fora", "estado": "MG", "lat": -21.7665, "long": -43.3502},
    {"cep": "12209-000", "cidade": "Sao Jose dos Campos", "estado": "SP", "lat": -23.1791, "long": -45.8872},
    {"cep": "14010-000", "cidade": "Ribeirao Preto", "estado": "SP", "lat": -21.1704, "long": -47.8103},
    {"cep": "15010-000", "cidade": "Sao Jose do Rio Preto", "estado": "SP", "lat": -20.8113, "long": -49.3758},
    {"cep": "18010-000", "cidade": "Sorocaba", "estado": "SP", "lat": -23.5015, "long": -47.4521},
    {"cep": "44001-000", "cidade": "Feira de Santana", "estado": "BA", "lat": -12.2733, "long": -38.9556},
    {"cep": "58400-000", "cidade": "Campina Grande", "estado": "PB", "lat": -7.2241, "long": -35.8774},
    {"cep": "63010-000", "cidade": "Juazeiro do Norte", "estado": "CE", "lat": -7.2114, "long": -39.3134},
    {"cep": "62010-000", "cidade": "Sobral", "estado": "CE", "lat": -3.6858, "long": -40.3497},
    {"cep": "56302-000", "cidade": "Petrolina", "estado": "PE", "lat": -9.3982, "long": -40.5008},
    {"cep": "55002-000", "cidade": "Caruaru", "estado": "PE", "lat": -8.2844, "long": -35.9700},
    {"cep": "39400-000", "cidade": "Montes Claros", "estado": "MG", "lat": -16.7350, "long": -43.8617}
]

LISTA_NEGOCIO = [
    {"setor": "Varejo", "grupo": "Vendas Diretas"},
    {"setor": "Industria", "grupo": "Manufatura Sul"},
    {"setor": "Servicos", "grupo": "Tecnologia"},
    {"setor": "Contabil", "grupo": "Escritorios Associados"}
]

OPCOES_HORAS = [0.0, 10.0, 20.0, 40.0, 80.0]
OPCOES_TICKETS = [0, 5, 10, 20, 50]
MESA = ["Help-Desk","Ativacao","On Site SSP","On Site TI","Infraestrutura","Labin","Telefonia"]

LISTA_SERVICOS = [
    {"cat": "Hardware", "item": "Substituicao de Fonte de Alimentacao"}, {"cat": "Hardware", "item": "Reparo de Placa Mae"},
    {"cat": "Hardware", "item": "Instalacao de Nobreak"}, {"cat": "Hardware", "item": "Montagem de Rack de Servidores"},
    {"cat": "Redes", "item": "Configuracao de Link de Internet"}, {"cat": "Redes", "item": "Configuracao de VLAN"},
    {"cat": "Software", "item": "Atualizacao de Firmware"}, {"cat": "Software", "item": "Correcao de Bug em Script"},
    {"cat": "Seguranca", "item": "Implementacao de MFA Autenticacao"}, {"cat": "Cloud", "item": "Provisionamento de Instancia AWS"}
]

# --- NOVA LISTA PARA VALORES EXTRAS (BASEADA NO SEU CSV) ---
TIPOS_EXTRAS = [
    {"tipo": "Deslocamento", "desc": "KM rodado para atendimento", "unitario": 1.55},
    {"tipo": "Almoco", "desc": "Reembolso de alimentacao", "unitario": 35.0},
    {"tipo": "Pedagio", "desc": "Pedagio via Sem Parar", "unitario": 12.50},
    {"tipo": "Hospedagem", "desc": "Pernoite em hotel p/ projeto", "unitario": 250.0},
    {"tipo": "Diversos", "desc": "Material miudo de instalacao", "unitario": 15.0}
]

def gerar_mock_final(n_clientes=400, n_tickets=30000, valor_hora=150.0):
    tecnicos_ficticios = [limpar_texto(fake.name()) for _ in range(10)]
    
    # --- 3. CADASTROS BASE ---
    clientes_base = []
    for _ in range(n_clientes):
        local = random.choice(LISTA_LOCALIDADES)
        negocio = random.choice(LISTA_NEGOCIO)
        nome_empresa = limpar_texto(fake.company())
        dominio = nome_empresa.lower().replace(" ", "").replace(",", "")[:10] + ".com.br"
        solicitantes = [{"nome": limpar_texto(fake.name()), "email": f"{fake.name().lower().replace(' ', '.')}@{dominio}"} for _ in range(random.randint(5, 20))]

        clientes_base.append({
            "id": random.randint(100000, 900000), "nome": nome_empresa, "razao": nome_empresa.upper() + " LTDA",
            "cep": local["cep"], "cidade": local["cidade"].upper(), "estado": local["estado"],
            "lat": local["lat"], "long": local["long"], "setor": negocio["setor"], "grupo": negocio["grupo"],
            "fmh_help": random.choice(OPCOES_HORAS), "fm_ssp": random.choice(OPCOES_TICKETS),
            "fm_help": random.choice(OPCOES_TICKETS), "fm_labin": random.choice(OPCOES_TICKETS),
            "fm_tel": random.choice(OPCOES_TICKETS), "fm_site": random.choice(OPCOES_TICKETS),
            "fmh_site": random.choice(OPCOES_HORAS), "fmh_ssp": random.choice(OPCOES_HORAS),
            "solicitantes": solicitantes
        })

    n_heavy_users = max(1, int(n_clientes * 0.2))
    pesos = [80 if i < n_heavy_users else (20 / (n_clientes - n_heavy_users)) for i in range(n_clientes)]

    # --- 4. TABELA CLIENTES ---
    df_clientes = pd.DataFrame([{
        "Id_cliente": c['id'], "Cliente": c['nome'], "Razao_social": c['razao'], "Situacao": random.choice(["Ativo", "Inativo"]),
        "Criado_em": fake.date_time_between(start_date='-3y').strftime('%Y-%m-%d %H:%M:%S.%f'),
        "Atualizado_em": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "Tipo_de_contrato": random.choice(['Chamado','Horas','Eqpto/Colab']),
        "Contrato": random.choice(["Sim", "Não", "Rescindido"]), "FMH_Help_Desk": c['fmh_help'], "FM_On_Site_SSP": c['fm_ssp'],
        "FM_Help_Desk": c['fm_help'], "FM_LABIN": c['fm_labin'], "FM_Telefonia": c['fm_tel'], "FM_On_Site_Ti": c['fm_site'],
        "FMH_On_site_Ti": c['fmh_site'], "FMH_On_site_SSP": c['fmh_ssp'], "Grupo_cliente": c['grupo'], "Setor": c['setor'],
        "CEP": c['cep'], "Cidade": c['cidade'], "Estado": c['estado']
    } for c in clientes_base])

    # --- 5. GERAÇÃO DE TICKETS, APONTAMENTOS E EXTRAS ---
    tickets_data = []
    apontamentos_data = []
    extras_data = []
    id_ap_counter = 200000
    id_ex_counter = 300000

    for i in range(n_tickets):
        c = random.choices(clientes_base, weights=pesos, k=1)[0]
        solicitante = random.choice(c['solicitantes'])
        servico = random.choice(LISTA_SERVICOS)
        id_t = 80000 + i
        mesa_atual = random.choice(MESA)
        tecnico_resp = random.choice(tecnicos_ficticios)
        
        criado_dt = fake.date_time_between(start_date='-45d', end_date='now')
        data_1_ap = criado_dt + timedelta(minutes=random.randint(5, 60))
        data_fec = data_1_ap + timedelta(hours=random.randint(1, 72))
        
        # --- APONTAMENTOS ---
        duracao_total_ticket = 0.0
        qtd_apontamentos = random.randint(3, 7)
        for _ in range(qtd_apontamentos):
            duracao_min = float(random.randint(15, 120))
            duracao_total_ticket += duracao_min
            valor_sessao = round((duracao_min / 60) * valor_hora, 2)
            
            apontamentos_data.append({
                "Id_apontamento": id_ap_counter, "Id_ticket": id_t,
                "Desc_apontamento": limpar_texto(fake.sentence()), "Cliente": c['nome'],
                "Mesa": mesa_atual, "Tecnico": random.choice(tecnicos_ficticios),
                "Solicitado_por": solicitante['nome'], "Servico_avulso": random.choice(["Sim", "Nao"]),
                "Assistencia": random.choice(["Remoto", "Interno", "Presencial"]), "Garantia": random.choice([True, False]),
                "Duracao": duracao_min, "Data_apontamento": data_1_ap.strftime('%Y-%m-%d %H:%M:%S'),
                "Data_encerramento": data_fec.strftime('%Y-%m-%d %H:%M:%S'),
                "Valor_apontamento": valor_sessao, "Latitude": c['lat'], "Longitude": c['long']
            })
            id_ap_counter += 1

        # --- LÓGICA DE VALORES EXTRAS (Nova Adição) ---
        if "On Site" in mesa_atual and random.random() < 0.4:
            for _ in range(random.randint(1, 3)):
                ex = random.choice(TIPOS_EXTRAS)
                qtd = random.randint(1, 100) if ex['tipo'] == "Deslocamento" else 1
                valorizacao = round(qtd * ex['unitario'], 2)
                
                extras_data.append({
                    "Id_ticket": id_t,
                    "Mesa": mesa_atual,
                    "Data_apontamento": criado_dt.strftime('%Y-%m-%d %H:%M:%S'),
                    "Responsavel": tecnico_resp,
                    "Valor_extra": ex['tipo'],
                    "Desc_valorizacao": ex['desc'],
                    "Quantidade": float(qtd),
                    "Valor_unitario": ex['unitario'],
                    "Valorizacao_extra": valorizacao,
                    "Custo_Interno": random.choice(["Sim", "Não"]),
                    "Id_valorizacao": id_ex_counter
                })
                id_ex_counter += 1

        # --- TICKETS ---
        tickets_data.append({
            "Id_ticket": id_t, "Id_cliente": c['id'], "Cliente": c['nome'],
            "Desc_ticket": limpar_texto(fake.sentence(nb_words=5)), "Situacao": "Fechado",
            "Mesa": mesa_atual, "Responsavel": tecnico_resp,
            "Solicitado_por": solicitante['nome'], "Email_responsavel": solicitante['email'],
            "Ultima_resposta": random.choice(["Cliente", "Interno", "Nenhum"]),
            "Nome_estagio": "Fechado", "Prioridade": random.choice(["Baixa", "Media", "Alta"]),
            "Catalogo_de_Servicos": servico["cat"], "Item": servico["item"],
            "Criado_em": criado_dt.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "Data_1o_apontamento": data_1_ap.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "Fechado_em": data_fec.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "Avaliacao": float(random.randint(1, 5)),
            "SLA_atendido": random.choice(["Sim", "Não", "Sem SLA"]),
            "Duracao_apontada": duracao_total_ticket,
            "Tempo_total_fechamento": round(duracao_total_ticket / 60, 4),
            "Link_chamado": f"https://app.tiflux.com/v/tickets/{id_t}/basic_info"
        })

    return df_clientes, pd.DataFrame(tickets_data), pd.DataFrame(apontamentos_data), pd.DataFrame(extras_data)

# --- EXECUÇÃO ---
df_c, df_t, df_a, df_e = gerar_mock_final()

# Salvando os arquivos
df_c.to_csv("Tiflux_tb_Clientes_MOCK.csv", index=False, encoding='utf-8-sig')
df_t.to_csv("Tiflux_tb_Tickets_MOCK.csv", index=False, encoding='utf-8-sig')
df_a.to_csv("Tiflux_tb_Apontamentos_MOCK.csv", index=False, encoding='utf-8-sig')
df_e.to_csv("Tiflux_tb_Valores_Extras_MOCK.csv", index=False, encoding='utf-8-sig')

print(f"Sucesso!")
print(f"- Tickets: {len(df_t)}")
print(f"- Apontamentos: {len(df_a)}")
print(f"- Valores Extras: {len(df_e)}")