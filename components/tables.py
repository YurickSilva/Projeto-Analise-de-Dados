from st_aggrid import AgGrid, GridOptionsBuilder, AgGridTheme, ColumnsAutoSizeMode, GridUpdateMode, DataReturnMode

def render_tabela_generica(df, mapeamento_nomes=None, colunas_ocultas=None, colunas_wrap=None, altura=400):
    """
    Renderiza uma tabela AgGrid padronizada para o sistema.
    Possui seleção múltipla por clique, estilo zebrado e filtros automáticos.
    Configurada para auto-ajuste de largura de colunas baseado no conteúdo.
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # --- CONFIGURAÇÃO PADRÃO DE COLUNAS (Essencial para o Auto-Size) ---
    gb.configure_default_column(
        resizable=True,      # Permite redimensionar (obrigatório para auto-size funcionar)
        filterable=True, 
        sortable=True,
        minWidth=100,        # Impede que colunas fiquem invisíveis
        wrapHeaderText=True, # Permite que o título da coluna quebre linha
        autoHeaderHeight=True
    )
    
    # --- CONFIGURAÇÃO DE SELEÇÃO ---
    gb.configure_selection(
        selection_mode='multiple',      
        use_checkbox=False,             
        header_checkbox=True,           
        suppressRowDeselection=False,   
        suppressRowClickSelection=False 
    )
    
    # --- CONFIGURAÇÕES DE INTERAÇÃO E VISUAL ---
    gb.configure_grid_options(
        enableRangeSelection=True,
        rowMultiSelectWithClick=True,   # Clique simples marca/desmarca (Toggle)
        suppressCellSelection=True,     # Remove o retângulo de foco azul das células
        rowHeight=35                    # Altura fixa para manter o padrão visual
    )
    
    # --- MAPEAMENTO DE COLUNAS E VISIBILIDADE ---
    if mapeamento_nomes:
        for col in df.columns:
            if col in mapeamento_nomes:
                gb.configure_column(col, headerName=mapeamento_nomes[col])
            else:
                # Oculta colunas não listadas no mapeamento
                gb.configure_column(col, hide=True)

    # Ocultação forçada de colunas específicas
    if colunas_ocultas:
        for col in colunas_ocultas:
            gb.configure_column(col, hide=True)

    # Configuração de texto longo (Wrap)
    if colunas_wrap:
        for col in colunas_wrap:
            gb.configure_column(col, wrapText=True, autoHeight=True)

    # --- REGRAS DE ESTILO (ZEBRADO) ---
    gb.configure_grid_options(
        rowClassRules={
            'ag-row-even': 'node.rowIndex % 2 === 0', 
            'ag-row-odd': 'node.rowIndex % 2 !== 0'
        }
    )
    
    # Customização via CSS
    custom_css = {
        ".ag-row-odd": {"background-color": "rgba(208, 209, 211, 1) !important"},
        ".ag-header": {"border-bottom": "2px solid #fe5000 !important"}
    }
    
    return AgGrid(
        df, 
        gridOptions=gb.build(), 
        theme=AgGridTheme.ALPINE, 
        height=altura,
        custom_css=custom_css,
        # 🟢 MODO DE AUTO-AJUSTE PELO CONTEÚDO
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED
    )
    
def tabela(df, mapeamento_nomes=None, colunas_ocultas=None):
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Se passarmos um mapeamento, configuramos as colunas desejadas
    # e podemos ocultar TODAS as outras que não estão no mapeamento
    if mapeamento_nomes:
        for col in df.columns:
            if col in mapeamento_nomes:
                gb.configure_column(col, headerName=mapeamento_nomes[col])
            else:
                # Se a coluna não está no mapeamento e não foi explicitamente pedida, ocultamos
                gb.configure_column(col, hide=True)

    # Força a ocultação de colunas específicas passadas na lista (como Latitude/Longitude)
    if colunas_ocultas:
        for col in colunas_ocultas:
            gb.configure_column(col, hide=True)

    # Configurações de Design
    gb.configure_grid_options(
        rowSelection='single',
        rowClassRules={
            'ag-row-even': 'node.rowIndex % 2 === 0',
            'ag-row-odd': 'node.rowIndex % 2 !== 0',
        }
    )
    
    custom_css = {
        ".ag-row-odd": {"background-color": "rgba(208, 209, 211, 1) !important"},
        ".ag-header": {"border-bottom": "2px solid #fe5000 !important"}
    }
    
    return AgGrid(
        df, 
        gridOptions=gb.build(), 
        theme=AgGridTheme.ALPINE, 
        custom_css=custom_css,
        update_mode='selection_changed',
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )