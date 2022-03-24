from utils import dashboard_utils
from dashboard2 import *

import plotly.graph_objects as go
from bokeh.models import Div
import plotly.express as px
import streamlit as st 
import screening_main
import altair as alt
import pandas as pd
import numpy as np
import webbrowser
import time
import json
import glob
import os


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link#.split('=')[1]
    per = '%'
#     return st.button(str(text),on_click='Clicked')
#     return f'<a href="{link}">{text}{per}</a>'
    return f'<button name="subject" type="submit" value="{text}">{text}{per}</button>'
#     return f'<button onclick="alert({text}{per})">{text}</button>'




st.set_page_config(page_title = 'Auto Recruitment Dashboard', page_icon='💹')

st.markdown(f"<h1 style='text-align: center; color: gray;'>AI Recruitment</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'>This application is a Recruitment dashboard</p>", unsafe_allow_html=True)

ph = st.empty()
with ph.container():
    if st.button('Upload File'):
        js = "window.location.href = 'http://127.0.0.1:5000/'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
        
path_to_dashboard_jsons = './dashboard_json/*.json'
if not glob.glob(path_to_dashboard_jsons):
     st.info('Please upload Json files!')
else:
    job_descriptions = dashboard_utils.get_job_descriptions_title(path_to_dashboard_jsons)    
    df = dashboard_utils.make_df_for_dashboard(job_descriptions)
    placeholder = st.empty()
    with placeholder.container():            
#         df = df.append([df]*15,ignore_index=True)
        profile_name = dashboard_utils.make_table(df)
        
#     st.balloons()
    with st.spinner('In Progress...'):
        if profile_name:
            ph.empty()
            placeholder.empty()
            app_main(profile_name)


    
# dataframe = make_df_for_dashboard(job_descriptions)

# # link is the column with hyperlinks
# for col in list(dataframe.columns)[1:]:
#     dataframe[col] = dataframe[col].apply(make_clickable)
    
# dataframe_html = dataframe.to_html(escape=False)

# st.markdown(f"<h3 style='text-align: left; color: blue;'>LinkedIn Acivity Similarity to Job Description</h3>", unsafe_allow_html=True)
# # st.header("Statistics")
# st.write( dataframe_html, unsafe_allow_html=True)
   


