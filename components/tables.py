from st_aggrid import AgGrid, GridOptionsBuilder, AgGridTheme, ColumnsAutoSizeMode, GridUpdateMode, DataReturnMode

def render_tabela_generica(df, mapeamento_nomes=None, colunas_ocultas=None, colunas_wrap=None, altura=400):
    gb = GridOptionsBuilder.from_dataframe(df)
    
    gb.configure_default_column(
        resizable=True,
        filterable=True, 
        sortable=True,
        minWidth=100,
        wrapHeaderText=True,
        autoHeaderHeight=True
    )
    
    gb.configure_selection(
        selection_mode='multiple',      
        use_checkbox=False,             
        header_checkbox=True,           
        suppressRowDeselection=False,   
        suppressRowClickSelection=False 
    )
    
    gb.configure_grid_options(
        enableRangeSelection=True,
        rowMultiSelectWithClick=True,
        suppressCellSelection=True,
        rowHeight=35
    )
    
    if mapeamento_nomes:
        for col in df.columns:
            if col in mapeamento_nomes:
                gb.configure_column(col, headerName=mapeamento_nomes[col])
            else:
                gb.configure_column(col, hide=True)

    if colunas_ocultas:
        for col in colunas_ocultas:
            gb.configure_column(col, hide=True)

    if colunas_wrap:
        for col in colunas_wrap:
            gb.configure_column(col, wrapText=True, autoHeight=True)

    gb.configure_grid_options(
        rowClassRules={
            'ag-row-even': 'node.rowIndex % 2 === 0', 
            'ag-row-odd': 'node.rowIndex % 2 !== 0'
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
        height=altura,
        custom_css=custom_css,
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
                gb.configure_column(col, hide=True)

    if colunas_ocultas:
        for col in colunas_ocultas:
            gb.configure_column(col, hide=True)

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