import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd
import dash
from dash.dependencies import Input, Output, State


pg = pd.read_csv('pg.csv', engine='python')
spell_list = pd.read_csv('Spells.csv', engine='python')





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

# -------------------------------------------------------------------------------------------------------------------
#       LAYOUT      LAYOUT      LAYOUT      LAYOUT      LAYOUT      LAYOUT      LAYOUT      LAYOUT      LAYOUT
# -------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='STATUS', value='tab1'),
        dcc.Tab(label='MAGIE', value='tab2'),
        dcc.Tab(label='INVENTARIO', value='tab3'),
    ]),
    html.Div(id='tabs-content')
])

status = html.Div([
    daq.Tank(
        id='hp',
        min=0,
        value=5,
        max=10
    ),
    daq.NumericInput(
        id='damage',
        min=0,
        value=5,
        max=10
    ),
    html.Button('Damage', id='hit'),
    html.Button('Heal', id='heal')
])

magie = html.Div([
    dcc.Dropdown(options=[{'label': i, 'value': i} for i in pg['nome']], id='spell_list_pg'),
    dcc.Checklist(id='canrips_check', persistence=True),
    dcc.Checklist(id='spell1_check', persistence=True),
    dcc.Checklist(id='spell2_check', persistence=True),
    dcc.Checklist(id='spell3_check', persistence=True),
    dcc.Checklist(id='spell4_check', persistence=True),
    dcc.Checklist(id='spell5_check', persistence=True),
    dcc.Checklist(id='spell6_check', persistence=True),
    dcc.Checklist(id='spell7_check', persistence=True),
    dcc.Checklist(id='spell8_check', persistence=True),
    dcc.Checklist(id='spell9_check', persistence=True),
])

inventario = html.Div([
    dash_table.DataTable(
        id='inventario',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True
    ),
    html.Button('Add Row', id='new_row', n_clicks=0),
])


# -------------------------------------------------------------------------------------------------------------------
#       CALLBACKS       CALLBACKS       CALLBACKS       CALLBACKS       CALLBACKS       CALLBACKS
# -------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('inventario', 'data'),
    [Input('new_row', 'n_clicks')],
    [State('inventario', 'data'),
     State('inventario', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback([
    [Output('canrips_check', 'options')] +
    [Output('spell{}_check'.format(i), 'options') for i in range(10)],
    [Input('spell_list_pg', 'value')]
])
def load_spell_list(sel_pg):
    classe = pg.loc[(pg.nome == sel_pg), 'classe']
    archetipo = pg.loc[(pg.nome == sel_pg), 'archetipo']
    #FARE UN MERGING DI PIù DATABESE PER CAPIRE QUALI SPELL APPARTENGONO AD UN ARCHETIPO O AD UNA CLASSE
    #O IMPOSTARE VARIABILI DICOTOMICHE
    spells_c = spell_list[(classe in spell_list.Classes), :]




@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab1':
        return status
    elif tab == 'tab3':
        return inventario
    else:
        return magie


# -------------------------------------------------------------------------------------------------------------------
#       MAIN        MAIN        MAIN        MAIN        MAIN        MAIN        MAIN        MAIN        MAIN
# -------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
