import streamlit as st
import plotly.express as px
import pandas as pd

CORES_PADRAO = ['#FF7500', '#c1c6c8', '#086FF3']

def render_kpi_total(valor):
    st.metric(label="", value=valor)

def render_grafico_donut(df, coluna, titulo_hover, hole=0.5):
    fig = px.pie(df, names=coluna, hole=hole, color_discrete_sequence=CORES_PADRAO)
    fig.update_traces(
        textinfo='value+percent',
        textposition='outside',
        hovertemplate=f"<b>{titulo_hover}:</b> %{{label}}<br><b>Total:</b> %{{value}}<extra></extra>"
    )
    fig.update_layout(showlegend=True, margin=dict(t=30, b=0, l=0, r=0), height=350)
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
        showlegend=False, # Garante que não haverá legenda lateral
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura, 
        margin=dict(t=10, b=10, l=10, r=10)
    )
    # Se os nomes no eixo X forem muito longos, rotacione-os:
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

def render_grafico_ranking(df, eixo_x, eixo_y, altura=350):
    fig = px.bar(df, x=eixo_x, y=eixo_y, orientation='h', color_discrete_sequence=[CORES_PADRAO[0]])
    fig.update_layout(xaxis_title=None, yaxis_title=None, height=altura, 
                      yaxis={'categoryorder':'total ascending'}, margin=dict(t=10, b=10, l=10, r=10))
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True)

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
    
    fig = px.line(df_final, x='mes', y='total', color='ano', markers=True, color_discrete_sequence=CORES_PADRAO)
    fig.update_xaxes(categoryorder='array', categoryarray=list(meses_map.values()))
    fig.update_yaxes(dtick=1)
    
    # Legenda horizontal no topo para não espremer o gráfico lateralmente
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura
    )
    st.plotly_chart(fig, use_container_width=True)

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

    fig = px.bar(df_plot, x=eixo_x, y=eixo_y, color_discrete_sequence=[CORES_PADRAO[0]])
    
    fig.update_xaxes(
        rangeslider_visible=False,
        showgrid=False, 
        type='category', 
        tickangle=45,
        categoryorder='total ascending',
        fixedrange=True
    )
    
    fig.update_yaxes(fixedrange=True)

    fig.update_layout(
        xaxis_title=None, 
        yaxis_title=None, 
        height=altura, 
        showlegend=False,
        margin=dict(t=10, b=80, l=40, r=10),
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