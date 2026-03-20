import streamlit_antd_components as sac
from auth.authorization import usuario_tem_acesso

def build_menu():
    menu = [
        sac.MenuItem("Home", icon="house"),
    ]

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
                            sac.MenuItem("Clientes"),
                            sac.MenuItem("Tickets Geral"),
                            sac.MenuItem("Tickets Tempo"),
                            sac.MenuItem("Tickets Clientes"),
                            sac.MenuItem("Tickets Técnicos"),
                            sac.MenuItem("Tickets Abertos"),
                            sac.MenuItem("Tempo Decorrido"),
                            sac.MenuItem("Atendimentos"),
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