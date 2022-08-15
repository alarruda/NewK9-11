from jupyter_plotly_dash import JupyterDash
import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import base64

from aarruda_CS340_mod5_CRUD import AnimalShelter

############
###############
# Implement performance advisor
############
###############

# View collections with slow queries
atlas performanceAdvisor namespaces list -o json

# Run performance advisor to suggest indexes
atlas performanceAdvisor suggestedIndexes list -o json

############
###############
# Data Manipulation / Model
##########
#################

# Assign username and password for user auth
username = "aacuser"
password = "1qaz!QAZ"
shelter = AnimalShelter(username, password)

# Class read returns cursor object
df = pd.DataFrame.from_records(shelter.read({}))

############
#############
# Dashboard Layout / View
#############
############

app = JupyterDash('SimpleExample')


# Add Grazioso Salvare�s logo

image_filename = 'Grazioso Salvare Logo.png' # replace with your own image

encoded_image = base64.b64encode(open(image_filename, 'rb').read())


# Place the HTML image tag and
# Include a unique identifier such as your name or date

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
    html.Center(html.B(html.H2('Caio De Morais'))),
    html.Hr(),
    html.Div(


# Interactive filtering options for radio buttons

className='row',
        style={'display': 'flex'},
        children=[
            html.Button(id='button-one',n_clicks=0, children= 'Water Rescue'),
            html.Button(id='button-two',n_clicks=0, children= 'Mountain or Wilderness Rescue'),
            html.Button(id='button-three',n_clicks=0, children='Disaster Rescue or Individual Tracking'),
            html.Button(id='button-four', n_clicks=0, children='reset')
        ]),
    
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),

# Interactive data table to make it user-friendly, set page size, and style

        page_size=100,
        style_table={'height':'400px','overflowY':'auto','overflowX':'auto'},
        style_header={
            'backgroundColor':'rgb(240,230,230)',
            'fontWeight':'bold'
        },
        style_data={
            'whiteSpace':'normal',
            'height':'auto'
        },


# Tooltips

tooltip ={i: {
    'value': i,
    'use_with': 'both'
    } 

for i in df.columns},
        tooltip_delay=0,
        tooltip_duration = None,
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        editable=False,
        column_selectable=True,
        row_selectable='single',
        row_deletable=False,
        selected_rows=[],
    ),
    
    html.Br(),
    html.Hr(),

    #This sets up the dashboard so that your chart and your geolocation chart are side-by-side

    html.Div(className='row',
             style={'display' : 'flex'},
             children=[
                 html.Div(
                     id='graph-id',
                     className='col s12 m6',
                 ),
                 
                 html.Div(
                     id='map-id',
                     className='col s12 m6',
                 )
             ])
])


###############
#########
# Interaction Between Components / Controller
#########
##############


@app.callback([Output('datatable-id','data')],
              [Input('button-one', 'n_clicks'),Input('button-two','n_clicks'),
               Input('button-three','n_clicks'),Input('button-four','n_clicks')])

def update_dashboard(button1,button2,button3,button4):
    # Filter interactive data table with MongoDB queries

    if (int(button1) >= 1):
        df = pd.Dataframe.from_records(shelter.read({'$and': [
            {'$or': [ {'breed':'Labrador Retriever Mix'}, {'breed':'Chesapeake Bay Retriever'},
                     {'breed':'Newfoundland'}]},
            {'sex_upon_outcome':'Intact Female'}, {'age_upon_outcome_in_weeks':{'$lte':26, 'gte':156}}]}))
        button2, button3, button4 = 0
    
    elif (int(button2)>= 1):
        df = pd.Dataframe.from_records(shelter.read({'$and': [
            {'$or': [ {'breed':'German Shepherd'}, {'breed':'Alaskan Malamute'},
                     {'breed':'Old English Sheepdog'},{'breed':'Siberian Husky'},{'breed':'Rottweiler'}]},
            {'sex_upon_outcome':'Intact Male'}, {'age_upon_outcome_in_weeks':{'$lte':26, 'gte':156}}]}))
        button1, button3, button4 = 0
    
    elif (int(button3)>=1):
        df = pd.Dataframe.from_records(shelter.read({'$and': [
            {'$or': [ {'breed':'Doberman Pinscher'}, {'breed':'German Sheperd'},
                     {'breed':'Golden Retriever'},{'breed':'Bloodhound'},{'breed':'Rottweiler'}]},
            {'sex_upon_outcome':'Intact Male'}, {'age_upon_outcome_in_weeks':{'$lte':20, 'gte':300}}]}))
        button1, button2, button4 = 0

    elif(int(button4)>=1):
        df = pd.Dataframe.from_records(shelter.read())
        button1, button2, button3 = 0
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
        data=df.to_dict('records')
        return data
    
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')
    ]
)

def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data")
    ]
)

def update_graphs(viewData):

# Chart database data   
    df = pd.DataFrame.from_dict(viewData)
    return [
        dcc.Graph(
            figure = px.pie(df, values=values, names=names, title='Percentage of breeds available')
        )

]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
     Input('datatable-id',"derived_viewport_selected_rows")
    ]
)
    
def update_map(viewData):
# Geolocation chart
    dff = pd.DataFrame.from_dict(viewData)

# Marker with tool tip and pop up
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[dff.loc[0,'location_lat'],dff.loc[0,'location_long']], zoom=15, children=[
        dl.TileLayer(id="base-layer-id"),
        dl.Marker(position=[dff.loc[0,'location_lat'],dff.loc[0,'location_long']], children=[
            dl.Tooltip(dff['breed']),
            dl.Popup([
                html.H1("Animal Name"),
                html.P(dff.loc[0,'name'])
            ])
        ])
    ])]