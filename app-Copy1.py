from utils.dashboard_utils import *
import plotly.graph_objects as go
from bokeh.models import Div
import plotly.express as px
import streamlit as st 
import screening_main
import altair as alt
import pandas as pd
import numpy as np
import webbrowser
import json
import glob
import os


st.set_page_config(page_title = 'Auto Recruitment Dashboard', layout='wide', page_icon='💹')

st.markdown(f"<h1 style='text-align: center; color: red;'>Auto Recruitment</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'>This application is a Recruitment dashboard</p>", unsafe_allow_html=True)


if st.sidebar.button('Home'):
    js = "window.location.href = 'http://github.com'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
    
    
st.sidebar.title("Auto Recruitment")
st.sidebar.markdown("This application is a Recruitment dashboard:")
st.markdown("<hr/>", unsafe_allow_html=True)



# side bar for selecting job description
st.sidebar.title("Job Description")
path_to_jds = './job_descriptions/*'
job_descriptions = get_job_descriptions_title(path_to_jds)
# job_descriptions.insert(0,'Select a Job Description')
if job_descriptions:
    jd_select_box = st.sidebar.selectbox('Job Description', job_descriptions, key='1')
else:
    jd_select_box = st.sidebar.selectbox('Job Description', job_descriptions, key='1')
    
    
    
jd_select_box = '' if jd_select_box == 'Select a Job Description' else jd_select_box
if jd_select_box:
    selected_job_description = read_selected_job_description(jd_select_box,path_to_jds)
    model_predictions = screening_main.main_fun(selected_job_description,jd_select_box)
else:
    st.markdown(f"<h6 style='text-align: center; color: blue;'>Please Select a Job Description!</h1>", unsafe_allow_html=True)
    
        
#load json file of prediction model
try:
    if model_predictions:
        data = read_json('./dashboard_json/dashboard_test.json')
    else:
        data = {}
except:
    data = {}

    
    
st.sidebar.title("Profiles")
profiles_name = get_profile_names(data)
# profiles_name.insert(0,'Select a Name')
if profiles_name:
    select = st.sidebar.selectbox('User', profiles_name, key='1')
else:
    select = st.sidebar.selectbox('User', profiles_name, key='1')


    
select = '' if select == 'Select a Name' else select
if select:
    profile_data = search_profile_by_name(select,data)
    scores, skills = working_domains(profile_data)
    jd_matched_skills = JD_matched_skills(profile_data)
    resume_linkedin_matched_skills = resume_linkedin_matched_skills(profile_data)
    total_exp, company_exp = experience_details(profile_data)
    skills_from_experience = skills_from_experience(profile_data)
    personality = profile_personality(profile_data)
    activity = activity_similar(profile_data)
    skills_from_linkedin = skills_from_linkedin(profile_data)
    all_profile_exp = all_profiles_experience(data)

    if st.sidebar.button("All Profiles Experience"):
        bt_all_profiles_experience(all_profile_exp)
    else:
        if activity:
            st.markdown("## Similar Activities According to the Job Description")
            st.markdown(f"<h6 style='text-align: center; color: blue;'>Similarity of Activities : {round(activity, 2)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown("## Similar Activities According to the Job Description")
            st.markdown("No similar activity found!") 
        st.markdown("<hr/>", unsafe_allow_html=True)

    #     if st.sidebar.button("Working Domain"):
    #         bt_working_domain(scores)
    #     if st.sidebar.button("Experience"):
    #         bt_experience_details(company_exp,total_exp)
    #     if st.sidebar.button("JD Matched Skills"):
    #         bt_JD_matched_skills(jd_matched_skills)
    #     if st.sidebar.button("Resume/Linkedin Skills"):
    #         bt_resume_linkedin_matched_skills(resume_linkedin_matched_skills)
    #     if st.sidebar.button("Skills from Experience"):
    #         bt_skills_from_experience(skills_from_experience)
    #     if st.sidebar.button("Personality"):
    #         bt_profile_personality(personality)


        # dashboard flow

        bt_working_domain(scores)
        bt_experience_details(company_exp,total_exp)
        bt_JD_matched_skills(jd_matched_skills)
        bt_resume_linkedin_matched_skills(resume_linkedin_matched_skills)
        bt_skills_from_experience(skills_from_experience)
        bt_profile_personality(personality)

        
        
        
