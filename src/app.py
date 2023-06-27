# -*- coding: utf-8 -*-
"""
Created on Fri May 26 15:15:18 2023

@author: s5119521
"""
import glob
import dash
import random
import base64
import pandas as pd
import os
import pandas as pd
import dash_bootstrap_components as dbc
import json
import plotly.express as px
from pathlib import Path
from PIL import Image
import io
from io import BytesIO
from IPython.display import HTML
from dash import Dash, dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate

id_combinedactions = glob.glob("D:/ARI_BCR_ALL/Scenarios/HalveSedimentbudget/Dashboard_items/CA_img/*.jpg")
id_combinedactions = [x[:-4] for x in id_combinedactions]
id_hillslope = glob.glob("D:/ARI_BCR_ALL/Scenarios/HalveSedimentbudget/Dashboard_items/Hillslope_img/*.jpg")
id_hillslope = [x[:-4] for x in id_hillslope]
id_riverbank = glob.glob("D:/ARI_BCR_ALL/Scenarios/HalveSedimentbudget/Dashboard_items/Riverbank_img/*.jpg")
id_riverbank = [x[:-4] for x in id_riverbank]
id_wetland = glob.glob("D:/ARI_BCR_ALL/Scenarios/HalveSedimentbudget/Dashboard_items/Wetland_img/*.jpg")
id_wetland = [x[:-4] for x in id_wetland]
id_gully = glob.glob("D:/ARI_BCR_ALL/Scenarios/HalveSedimentbudget/Dashboard_items/Gully_img/*.jpg")
id_gully = [x[:-4] for x in id_gully]
df = pd.read_csv('summary_500.csv')
pd.set_option('display.max_colwidth', None)

img_uni = 'uni_logo.png'
with open(img_uni, 'rb') as f:
    encoded_image = base64.b64encode(f.read())


# In[ ]:


def get_thumbnail(path):
    i = Image.open(path)
    i.thumbnail((288, 694), Image.LANCZOS)
    return i

def image_base64(im):
    if isinstance(im, str):
        im = get_thumbnail(im)
    with BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'


# In[ ]:


df = df.iloc[:-67]

#Add Combined actions image
df['id_combinedactions'] = pd.Series(id_combinedactions,dtype="str")
df['file_combinedactions'] = df.id_combinedactions.map(lambda id_combinedactions: f'{id_combinedactions}.jpg')
df['Combined Actions'] = df.file_combinedactions.map(lambda f: get_thumbnail(f))

#Add Hillslope restoration action
df['id_hillslope'] = pd.Series(id_hillslope,dtype="str")
df['file_hillslope'] = df.id_hillslope.map(lambda id_hillslope: f'{id_hillslope}.jpg')
df['HillSlope Restoration'] = df.file_hillslope.map(lambda f: get_thumbnail(f))

#Add RiverBank Restoration action
df['id_riverbank'] = pd.Series(id_riverbank,dtype="str")
df['file_riverbank'] = df.id_riverbank.map(lambda id_riverbank: f'{id_riverbank}.jpg')
df['RiverBank Restoration'] = df.file_riverbank.map(lambda f: get_thumbnail(f))

#Add WetlandsEstablishment action
df['id_wetland'] = pd.Series(id_wetland,dtype="str")
df['file_wetland'] = df.id_wetland.map(lambda id_wetland: f'{id_wetland}.jpg')
df['Wetlands Establishment'] = df.file_wetland.map(lambda f: get_thumbnail(f))

#Add GullyRestoration action
df['id_gully'] = pd.Series(id_gully,dtype="str")
df['file_gully'] = df.id_gully.map(lambda id_gully: f'{id_gully}.jpg')
df['Gully Restoration'] = df.file_gully.map(lambda f: get_thumbnail(f))
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
    
    


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
server = app.server
dropdown_options = [{'label': k, 'value': k} for k in list(df.columns)[9:14]]
app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
        'height': '50px',
        'float': 'right',
        'top': '-40px',
        'left': '-10px'
    }),
    html.H4('Illustrations of trade-offs between the key objectives', style={'margin': '20px', 'display': 'flex'}),   
    html.Div([
        dcc.Graph(id='graph_scatter', figure={}, className="mb-4", style={'display': 'inline-block','margin-left': '20px'}),
        html.Div(id='hover-data' , style={
        'display': 'inline-block',
        'border': '1px solid black',
        'padding': '10px',
        'width': '400px',
        'height': '400px',
        'overflow': 'auto',
        'box-sizing': 'border-box', 'font-size': '20px',
    })
    ], style={'display': 'flex'}),
    html.Div([
        html.Img(id='click-data', style={
        'position': 'absolute',
        'top': '10px',
        'right': '10px',
        'display': 'inline-block',
        'float': 'right','margin-top': '60px',
            'margin-right': '170px'
    }, src='', width="288", height="694"),
        dcc.Dropdown(
            id='Dropdown',
            options=dropdown_options,
            placeholder="Types of management actions",
            value=dropdown_options[0]['value'],
            clearable=True,
    style={
        'float': 'right',
        'width': '60%',
        'display': 'inline-block',
        'position': 'relative',
        'top': '100%',
        'font-size': '20px',
        'margin-left': 'auto',
        'margin-right': '20px'
    }
        )
    ], style={'display': 'flex'}),
html.P('Implementation Cost ($):',style={'font-size': '20px'}),
dcc.Slider(
                id='slider-1',
    min=df[' Implementation Cost ($)'].min(), max=df[' Implementation Cost ($)'].max(),
    value=42876405,className="dbc", tooltip={'always_visible': False, 'placement': 'top'}),
html.P('Dissolved Nitrogen (t/yr):',style={'font-size': '20px'}),
dcc.Slider(
    id='slider-2',
    min=df[' Dissolved Nitrogen (t/yr)'].min(), max=df[' Dissolved Nitrogen (t/yr)'].max(),
    value=150,className="dbc",tooltip={'always_visible': False, 'placement': 'top'}),

html.P('Particulate Nitrogen (t/yr):',style={'font-size': '20px'}),
dcc.Slider(
    id='slider-3',
    min=df[' Particulate Nitrogen (t/yr)'].min(), max= df[' Particulate Nitrogen (t/yr)'].max(),
    value=213,className="dbc",tooltip={'always_visible': False, 'placement': 'top'}),
html.P('Opportunity Cost ($):',style={'font-size': '20px'}),
dcc.Slider(
    id='slider-4',
    min=df[' Opportunity Cost ($)'].min(), max= df[' Opportunity Cost ($)'].max(),
    value=3475684,className="dbc",tooltip={'always_visible': False, 'placement': 'top'}),
])

    


@app.callback(
   [Output('slider-2', 'value'),
   Output('slider-3','value'),
   Output('slider-4','value')],
   Input('slider-1', 'value')
   )


def update_sliders(slider1_value):
    slider2_value = 1846 * (slider1_value ** -0.14)
    slider3_value = 274 * (slider1_value ** -0.015)
    slider4_value = 0.0145 * (slider1_value ** 1.0946)
    return slider2_value, slider3_value, slider4_value
    raise PreventUpdate
    
@app.callback(
   Output('graph_scatter', 'figure'),
   [Input('slider-2', 'value'),
   Input('slider-3', 'value'),
   Input('slider-4','value'),
   ])
def update_bar_chart(slider2_value, slider3_value, slider4_value):
#    slider_1 = slider1_value
    slider_2 = slider2_value
    slider_4 = slider4_value
    slider_3 = slider3_value
    filtered_df = df[
        (df[' Particulate Nitrogen (t/yr)'] < slider_3) &
        (df[' Dissolved Nitrogen (t/yr)'] < slider_2) &
        (df[' Opportunity Cost ($)'] < slider_4)
    ]
#    print(slider_1)
    dff = dict(filtered_df)

    
    # Create scatter plot
    fig = px.scatter_3d(dff,
        x=' Opportunity Cost ($)',y=' Dissolved Nitrogen (t/yr)', 
        z=' Particulate Nitrogen (t/yr)',
        hover_name = dff['Number']
        ,custom_data=['Combined Actions','HillSlope Restoration','RiverBank Restoration','Wetlands Establishment','Gully Restoration'], height = 700, width = 700)

    fig.update_traces(marker_size=50)
    fig.update_traces(marker=dict(size=5,opacity=1,
                                  line=dict(width=2,
                                            color='darkSlateGrey')),
                      selector=dict(mode='markers'),surfacecolor="LightSteelBlue")
    fig.update_layout(
    margin=dict(l=0))
    return fig

@app.callback(
    Output('hover-data', 'children'),
    Input('graph_scatter', 'hoverData'),)

def update_hover_data(hover_data):
    if hover_data is None:
        return html.Div('Hover over the scatter plot to see data')
    else:
        # Get the selected data point and extract the relevant information
        point_data = hover_data['points'][0]
        x_value = point_data['x']
        y_value = point_data['y']
        z_value = point_data['z']

#        text = point_data['hover_name']

        # Create a list of paragraphs to display the information
        info_box = html.Div(
            [
                html.H5('Associated information'),
                html.P(f'Opportunity Cost ($): {x_value}'),
                html.P(f'Dissolved Nitrogen (t/yr): {y_value}'),
                html.P(f'Particulate Nitrogen (t/yr): {z_value}')
#                html.P(f'Text: {text}')
            ],
            className='info-box',
            style={'width': '200px', 'height': '200px'}
        )

        return info_box

#@app.callback(
#    Output('hover-data', 'children'),
#    Input('graph_scatter', 'hoverData'),
#)
#def display_hover_data(hoverData):
#    if hoverData is None:
#        return None
#    
#    hover_text = hoverData['points'][0]['hovertext']
#    return html.Pre(json.dumps(hover_text, indent=4), style = styles['pre'])


@app.callback(
    Output('click-data', 'src'),
    Input('Dropdown', 'value'),
    Input('graph_scatter', 'clickData'),
    )
def update_image(value, clickData):
    if clickData is None:
        return None
    if value == dropdown_options[0]['value']:
        return clickData['points'][0]['customdata'][0]
    elif value == dropdown_options[1]['value']:
        return clickData['points'][0]['customdata'][1]
    elif value == dropdown_options[2]['value']:
        return clickData['points'][0]['customdata'][2]
    elif value == dropdown_options[3]['value']:
        return clickData['points'][0]['customdata'][3]
    elif value == dropdown_options[4]['value']:
        return clickData['points'][0]['customdata'][4]
    
if __name__ == "__main__":
    app.run_server(debug=False)