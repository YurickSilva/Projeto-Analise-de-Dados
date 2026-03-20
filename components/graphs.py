import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.io as pio
import streamlit.components.v1 as components

CORES_PADRAO = ['#FF7500', '#c1c6c8', '#086FF3', '#FFA400','#00DBFF', '#118DFF']

def render_kpi_total(valor):
    st.metric(label="", value=valor)

def render_grafico_donut(df, coluna, titulo_hover, hole=0.5, show_legend=True, text_info='value+percent', text_position='outside', margin=None):
    fig = px.pie(df, names=coluna, hole=hole, color_discrete_sequence=CORES_PADRAO)
    fig.update_traces(
        textinfo=text_info,
        textposition=text_position,
        hovertemplate=f"<b>{titulo_hover}:</b> %{{label}}<br><b>Total:</b> %{{value}}<extra></extra>"
    )
    if margin is None:
        margin = dict(t=30, b=0, l=0, r=0)
    fig.update_layout(showlegend=show_legend, margin=margin, height=350)
    st.plotly_chart(fig, use_container_width=True)

def render_grafico_area_acumulada(df, col_eixo_x, col_contagem):
    
    df_acum = df.groupby(col_eixo_x).size().reset_index(name=col_contagem)
    df_acum['acumulado'] = df_acum[col_contagem].cumsum()
    
    fig = px.area(
        df_acum, 
        x=col_eixo_x, 
        y='acumulado', 
        markers=True, 
        text='acumulado',
        color_discrete_sequence=[CORES_PADRAO[0]]
    )
    
    fig.update_traces(
        textposition='top center', 
        texttemplate='%{text}',    
        hovertext=df_acum['acumulado'],
        cliponaxis=False 
    )
    
    max_valor = df_acum['acumulado'].max() if not df_acum.empty else 10

    fig.update_layout(
        xaxis_type='category', 
        margin=dict(l=40, r=40, t=50, b=40), 
        showlegend=False, 
        height=350,
        yaxis=dict(
            nticks=5,           
            dtick=None,         
            rangemode="tozero",
            range=[0, max_valor * 1.2] 
        )
    )
    
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
    
    st.plotly_chart(fig, use_container_width=True)

def render_grafico_barras(df, eixo_x, eixo_y, altura=350, categorias_fixas=None):
    df_plot = df.copy()
    if categorias_fixas:
        esqueleto = pd.DataFrame({eixo_x: categorias_fixas})
        df_plot = pd.merge(esqueleto, df_plot, on=eixo_x, how='left').fillna(0)

    fig = px.bar(df_plot, x=eixo_x, y=eixo_y, color_discrete_sequence=[CORES_PADRAO[0]])
    
    fig.update_layout(
        showlegend=False,
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura, 
        margin=dict(t=10, b=10, l=10, r=10)
    )
    fig.update_xaxes(tickangle=45) 
    st.plotly_chart(fig, use_container_width=True)

def render_grafico_linha(df, eixo_x, eixo_y, altura=300, show_legend=True):
    fig = px.line(df, x=eixo_x, y=eixo_y, markers=True, 
                  text=eixo_y,
                  color_discrete_sequence=[CORES_PADRAO[0]])
    
    fig.update_traces(
        textposition="top center",
        texttemplate='%{text}'
    )
    
    fig.update_xaxes(rangeslider_visible=False, showgrid=False)
    
    fig.update_layout(
        xaxis_type='category', 
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura, 
        showlegend=show_legend,
        # Aumentamos um pouco a margem superior (t) para o número não cortar no teto
        margin=dict(t=30, b=50, l=30, r=20),
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_grafico_donut_sla(df, coluna_status):
    fig = px.pie(df, names=coluna_status, hole=0.6, color=coluna_status,
                 color_discrete_map={'Sim': '#FF7500', 'Não': '#c1c6c8'})
    fig.update_layout(height=300, margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

def render_grafico_ranking(
    df,
    eixo_x,
    eixo_y,
    altura=350,
    *,
    scroll=True,
    scroll_altura=380,
    altura_por_item=32,
    altura_max=20000,
):
    # eixo_x = valores, eixo_y = nomes (responsável)
    fig = px.bar(df, x=eixo_x, y=eixo_y, orientation='h', text=eixo_x)
    
    # 1. Pintamos todas as barras com a mesma cor manualmente nos traces
    fig.update_traces(
        marker_color=CORES_PADRAO[0], 
        showlegend=False, # Mata a legenda do dado
        textposition="outside",
        cliponaxis=False
    )
    
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura, 
        showlegend=False, # Mata a legenda do layout
        # 2. Mata a escala de cores (Colorbar)
        coloraxis_showscale=False,
        yaxis={'categoryorder':'total ascending'}, 
        margin=dict(t=10, b=10, l=10, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(visible=False) # Esconde o eixo X já que temos os números nas barras
    # Garantir que os nomes (eixo Y) não fiquem cortados
    fig.update_yaxes(automargin=True, ticksuffix="  ")

    # --- Lista rolável (quando há muitos itens) ---
    if scroll:
        try:
            n_itens = int(len(df)) if df is not None else 0
            altura_conteudo = min(altura_max, max(scroll_altura, (n_itens * altura_por_item) + 80))
            fig.update_layout(height=altura_conteudo)

            # Margem esquerda dinâmica para caber rótulos longos
            if df is not None and eixo_y in df.columns:
                max_chars = int(df[eixo_y].astype(str).str.len().max() or 0)
                # ~7px por caractere (ajuste prático) com limites para não “explodir” o layout
                margem_l = max(110, min(420, 10 + (max_chars * 7)))
                fig.update_layout(margin=dict(t=10, b=10, l=margem_l, r=40))

            html = pio.to_html(
                fig,
                include_plotlyjs="cdn",
                full_html=False,
                config={"displayModeBar": False, "responsive": True},
            )
            # O iframe do components.html fica com altura fixa; o conteúdo maior vira scroll.
            components.html(html, height=scroll_altura, scrolling=True)
            return
        except Exception:
            # fallback (caso ambiente bloqueie components/html)
            pass

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_grafico_evolucao_mensal(df, col_data, altura=350):
    df_temp = df.copy()
    df_temp['ano'] = pd.to_datetime(df_temp[col_data]).dt.year
    df_temp['mes_num'] = pd.to_datetime(df_temp[col_data]).dt.month
    
    anos = df_temp['ano'].unique()
    meses_map = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 
                 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    
    esqueleto = pd.MultiIndex.from_product([anos, range(1, 13)], names=['ano', 'mes_num']).to_frame(index=False)
    df_contagem = df_temp.groupby(['ano', 'mes_num']).size().reset_index(name='total')
    df_final = pd.merge(esqueleto, df_contagem, on=['ano', 'mes_num'], how='left').fillna(0)
    
    df_final['mes'] = df_final['mes_num'].map(meses_map)
    df_final['ano'] = df_final['ano'].astype(str)
    
    fig = px.line(df_final, x='mes', y='total', color='ano', markers=True, 
                  text='total', color_discrete_sequence=CORES_PADRAO)
    
    # 1. FORÇAR desativação de legenda em cada linha individualmente
    # Se você quer esconder totalmente: showlegend=False
    # Se você quer apenas que ela não ocupe espaço lateral:
    fig.update_traces(textposition="top center", showlegend=True) 

    fig.update_layout(
        xaxis_type='category',
        xaxis_title=None,
        yaxis_title=None,
        height=altura,
        # 2. Configuração de legenda que NÃO ocupa espaço lateral
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title=None
        ),
        # 3. MATAR qualquer barra de cores ou escala lateral
        coloraxis_showscale=False,
        showlegend=True, 
        margin=dict(t=50, b=20, l=30, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # 4. Remover barra de ferramentas que causa bugs de redimensionamento
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_grafico_sazonal_comparativo(df_final, eixo_x, eixo_cor, altura=350, ordem_x=None):
    fig = px.line(df_final, x=eixo_x, y='total', color=eixo_cor, markers=True, color_discrete_sequence=CORES_PADRAO)
    if ordem_x:
        fig.update_xaxes(categoryorder='array', categoryarray=ordem_x)
    fig.update_layout(xaxis_title=None, yaxis_title=None, height=altura, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

def render_grafico_linha_simples(df, eixo_x, eixo_y, altura=300):
    fig = px.line(df, x=eixo_x, y=eixo_y, markers=True, color_discrete_sequence=[CORES_PADRAO[0]])
    fig.update_xaxes(type='category')
    fig.update_layout(xaxis_title=None, yaxis_title=None, height=altura, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
def render_grafico_barras_ranking(df, eixo_x, eixo_y, altura=350, categorias_fixas=None, show_legend=True):
    df_plot = df.copy()
    
    if categorias_fixas:
        esqueleto = pd.DataFrame({eixo_x: categorias_fixas})
        df_plot = pd.merge(esqueleto, df_plot, on=eixo_x, how='left').fillna(0)

    # Criamos o gráfico
    fig = px.bar(df_plot, x=eixo_x, y=eixo_y, color_discrete_sequence=[CORES_PADRAO[0]])
    
    # --- A SOLUÇÃO DE FORÇA BRUTA ---
    
    # 1. Limpeza Radical dos Eixos
    fig.update_xaxes(
        rangeslider_visible=False, # Desativa a barra cinza de zoom
        showgrid=False, 
        type='category', 
        tickangle=45,
        categoryorder='total ascending',
        fixedrange=True # Impede que o usuário dê zoom e "estrague" a visualização
    )
    
    fig.update_yaxes(fixedrange=True) # Trava o zoom vertical também

    # 2. Configurações de Layout (Remoção total de margens residuais)
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura, 
        showlegend=False, # Forçamos False aqui dentro
        margin=dict(t=10, b=80, l=40, r=10), # 'b=80' dá espaço para nomes grandes de mesas
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.2 # Espaço entre as barras para não ficarem coladas
    )
    
    # 3. Forçar remoção de legenda em cada barra individualmente
    fig.update_traces(showlegend=False)
    
    # 4. Renderização limpa
    st.plotly_chart(
        fig, 
        use_container_width=True, 
        config={
            'displayModeBar': False,  # Remove a barra de ícones do topo
            'staticPlot': False,
            'responsive': True
        }
    )