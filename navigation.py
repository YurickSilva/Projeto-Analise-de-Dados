import streamlit_antd_components as sac
from auth.authorization import usuario_tem_acesso

# Cria o menu que será usado no app.py
def build_menu():
    menu = [
        sac.MenuItem("Home", icon="house"),
    ]

    if usuario_tem_acesso("controladoria"):
        menu.append(
            sac.MenuItem(
                "Controladoria", 
                icon="graph-up",
                children=[
                    sac.MenuItem(
                        "DRE",
                        icon="graph-down",
                        children=[
                            sac.MenuItem("Receita")
                        ]
                    )
                ]
                )
        )

    if usuario_tem_acesso("ti"):
        menu.append(
            sac.MenuItem(
                "TI",
                icon="pc-display",
                children=[
                    sac.MenuItem(
                        "TI Global",
                        icon="diagram-3",
                        children=[
                            sac.MenuItem("Atendimentos"),
                            sac.MenuItem("Clientes"),
                            sac.MenuItem("Tempo Decorrido"),
                            sac.MenuItem("Tickets Abertos"),
                            sac.MenuItem("Tickets Geral"),
                            sac.MenuItem("Tickets Técnicos"),
                        ],
                    ),
                ],
            )
        )

    if usuario_tem_acesso("admin"):
        menu.append(
            sac.MenuItem(
                "Administração",
                icon="gear",
                children=[
                    sac.MenuItem("Usuários"),
                ],
            )
        )

    return menu

def get_menu_index(menu_list, target_label):
    """Retorna o índice plano do item no sac.menu"""
    flat_list = []
    def flatten(items):
        for item in items:
            flat_list.append(item.label)
            if item.children:
                flatten(item.children)
    
    flatten(menu_list)
    try:
        return flat_list.index(target_label)
    except ValueError:
        return 0