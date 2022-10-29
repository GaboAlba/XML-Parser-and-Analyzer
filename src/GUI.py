from parse_xml import XmlParser
import streamlit as stl
import pandas as pd
from urllib.request import urlopen
import plotly.express as px
import json


# Defining cache in order to run faster after first load
@stl.cache
def load_data():
    with open(r"../UFO_Report_2022_original.xml", 'r') as f:
        parser = XmlParser()
        return parser.parse_data(f.read())


@stl.cache
def load_geo_info():
    with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') \
            as response:
        return json.load(response)


# Defining data dtructures
raw_data = load_data()
states = load_geo_info()
shape_list = raw_data["shape_list"]
state_list = raw_data["state_list"]
events = raw_data["events"]

stl.write("""
    
    # **Tarea Programada** 🚀
    
      Grupo: lambda
      
    - Steven Gerardo Montero Muñoz B85125
    - Gabriel Francisco Alba Romero C29896
    - Hansel Calderón Calvo B51323

""")

stl.title("UFO Sightings Analytics Tool")

stl.subheader("Events related to a specific state")
events_by_state_ind = events.set_index('event_state')
state_selection = stl.selectbox("Select a State", state_list)
stl.write(events_by_state_ind.loc[state_selection])

stl.subheader("Events related to a specific shape")
events_by_shape_ind = events.set_index('event_shape')
shape_selection = stl.selectbox("Select a Shape", shape_list)
stl.write(events_by_shape_ind.loc[shape_selection])

stl.subheader("Number of events by state")
events_state_histogram = pd.DataFrame.value_counts(events, "event_state")
stl.bar_chart(events_state_histogram)

stl.subheader("Number of events by shape")
events_shape_histogram = pd.DataFrame.value_counts(events, "event_shape")
stl.bar_chart(events_shape_histogram)


def add_state_id(state_name):
    for state_geo in states['features']:
        if state_geo['properties']['name'] == state_name.capitalize():
            return state_geo['id']
    return None


map_event_df = events.copy()
events_state_map_graph = pd.DataFrame.value_counts(map_event_df, "event_state", ).reset_index(name='total_events')
events_state_map_graph['state_id'] = events_state_map_graph['event_state'].map(add_state_id)
events_state_map_graph = events_state_map_graph[events_state_map_graph['state_id'].notnull()]
