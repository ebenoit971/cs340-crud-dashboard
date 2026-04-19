#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash  # Enables Dash app execution inside Jupyter notebooks
import dash_leaflet as dl  # For map rendering
from dash import dcc, html, dash_table  # Dash core components and HTML utilities
from dash.dependencies import Input, Output  # For callback dependencies
import plotly.express as px  # For chart plotting
import base64  # For encoding image data
import numpy as np
import pandas as pd  # Data manipulation
import matplotlib.pyplot as plt
from IPython.display import HTML  # For displaying external link in notebook
from aac_crud_module import AnimalShelter  # Import your CRUD module

###########################
# Data Manipulation / Model
###########################

username = "aacuser"
password = "AACpass123"

# Instantiate CRUD class to interact with MongoDB
db = AnimalShelter(username, password)

# Load initial dataset into a pandas DataFrame
df = pd.DataFrame.from_records(db.read({}))
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

#########################
# Dashboard Layout / View
#########################

# Create Dash app instance
app = JupyterDash(__name__)

# Encode logo image
image_filename = "Grazioso Salvare Logo.png"
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# App layout
app.layout = html.Div([
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height': '100px'})),
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.Center(html.H4("Edward Benoit")),
    html.Hr(),

    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Water Rescue', 'value': 'water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'wilderness'},
            {'label': 'Disaster or Individual Tracking', 'value': 'disaster'},
            {'label': 'Reset', 'value': 'reset'}
        ],
        value='reset',
        labelStyle={'display': 'inline-block', 'margin': '10px'}
    ),
    html.Hr(),

    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ] + [{"name": "View Location", "id": "view_location", "presentation": "markdown"}],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        sort_action="native",
        filter_action="native",
    ),

    html.Br(),
    html.Hr(),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(id='graph-id', className='col s12 m6'),
        html.Div(id='map-id', className='col s12 m6')
    ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(Output('datatable-id', 'data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    if filter_type == 'water':
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif filter_type == 'wilderness':
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
    elif filter_type == 'disaster':
        query = {
            "animal_type": "Dog",
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }
    else:
        query = {}

    df_filtered = pd.DataFrame.from_records(db.read(query))
    if '_id' in df_filtered.columns:
        df_filtered.drop(columns=['_id'], inplace=True)

    # Set simple "View" label to prevent link navigation
    df_filtered['view_location'] = 'View'

    return df_filtered.to_dict('records')

# Pie chart callback
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):
    if viewData is None or len(viewData) == 0:
        return [html.Div()]

    dff = pd.DataFrame.from_dict(viewData)
    fig = px.pie(dff, names='breed', title='Breed Distribution')
    return [dcc.Graph(figure=fig)]

# Highlight columns
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns or []]

# Updated map callback — shows map on "View Location" click
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "active_cell"),
     Input('datatable-id', "data")]
)
def update_map(active_cell, table_data):
    if not active_cell or not table_data:
        return [html.Div("Click 'View' in the table to display a map.")]

    row = active_cell.get("row")
    col = active_cell.get("column_id")

    if col != "view_location":
        return [html.Div()]

    try:
        dff = pd.DataFrame(table_data)
        lat = float(dff.iloc[row].get('location_lat', 'nan'))
        lon = float(dff.iloc[row].get('location_long', 'nan'))

        if pd.isna(lat) or pd.isna(lon):
            raise ValueError("Missing coordinates.")

        return [
            dl.Map(style={'width': '1000px', 'height': '500px'}, center=[lat, lon], zoom=13, children=[
                dl.TileLayer(),
                dl.Marker(position=[lat, lon], children=[
                    dl.Tooltip(dff.iloc[row].get('breed', '')),
                    dl.Popup([
                        html.H4("Animal Name"),
                        html.P(dff.iloc[row].get('name', 'Unknown'))
                    ])
                ])
            ])
        ]
    except Exception as e:
        return [html.Div(f"Error displaying map: {e}")]

#######################
# Run App (toggle mode)
#######################

RUN_INLINE = False  # Toggle between inline and browser

if RUN_INLINE:
    app.run_server(mode='inline', debug=True, port=8050)
else:
    display(HTML("<a href='http://localhost:8050' target='_blank'>Click here to open the dashboard</a>"))
    app.run_server(mode='external', debug=True, port=8050)



# In[ ]:


