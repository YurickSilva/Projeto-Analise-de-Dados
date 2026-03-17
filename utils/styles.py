import streamlit as st
import base64

def get_base64_image(image_path):
    """Converte a imagem local para base64 para uso no CSS."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_global_ui(logo_path):
    """Aplica o CSS global: Logo Sidebar, Fundo com Marca d'Água e Transparências."""
    logo_b64 = get_base64_image(logo_path)
    
    st.markdown(f"""
        <style>
        
            [data-testid="stSidebarHeader"] img {{
                max-width: 100% !important;
                height: auto !important;
                min-height: 120px !important;
                object-fit: contain;
            }}
            
            [data-testid="stAppViewContainer"]::after {{
                content: "";
                position: fixed; /* Fica fixa na tela mesmo ao rolar */
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                
                /* Configurações da Imagem */
                background-image: url("data:image/png;base64,{logo_b64}");
                background-repeat: no-repeat;
                background-position: center;
                background-size: 800px; /* Ajuste o tamanho da logo aqui */
                
                opacity: 0.05; 
                
                /* ESSENCIAL: Permite clicar nos elementos que estão atrás da logo */
                pointer-events: none; 
                
                /* Coloca na frente de quase tudo */
                z-index: 9999;
            }}

            [data-testid="stSidebarNavItems"] span {{
                font-size: 18px !important;
                font-weight: 500 !important;
                color: #333333 !important;
            }}
            [data-testid="stSidebarNavItems"] [aria-current="page"] span {{
                color: #fe5000 !important;
                font-weight: bold !important;
            }}
            
            [data-testid="stSidebarNavItems"] span {{
                font-size: 18px !important;
                font-weight: 500 !important;
                color: #333333 !important;
            }}

            [data-testid="stSidebarNavItems"] [aria-current="page"] span {{
                color: #fe5000 !important;
                font-weight: bold !important;
            }}

        </style>
    """, unsafe_allow_html=True)
    
    
    
def render_page_title(title_text):
    st.markdown(
        f"""
        <h1 style='text-align: center; color: #fe5000; margin-bottom: 30px; margin-top: -60px'>
            {title_text}
        </h1>
        """, 
        unsafe_allow_html=True
    )
    
    
def apply_metric_style():
    st.markdown("""
        <style>
        /* 1. Centraliza o título do Expander */
        .streamlit-expanderHeader {
            text-align: center;
            justify-content: center;
        }

        [data-testid="stMetric"] {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 100%;
        }

        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            display: flex;
            justify-content: center;
            width: 100%;
        }


        [data-testid="stMetricValue"] {
            color: #FF7500 !important;
            font-size: 3rem !important; /* Aumenta um pouco o destaque */
        }
        </style>
        """, unsafe_allow_html=True)
    
def apply_right_panel_style():
    st.markdown("""
        <style>
        .right-panel {
            background-color: rgba(255,255,255,0.85);
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 0 12px rgba(0,0,0,0.05);
            position: sticky;
            top: 80px;
        }
        </style>
    """, unsafe_allow_html=True)
    