from utils import dashboard_utils
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

def app_main(selected_profile_name):
    
    home, upload = st.sidebar.columns(2)
    
    with home:
        if st.button('Home'):
            js = "window.location.href = 'http://localhost:8501/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
    with upload:
        if st.button('Upload Files'):
            js = "window.location.href = 'http://127.0.0.1:5000/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)

#     st.sidebar.title("AI Recruitment")
    st.sidebar.markdown(f"<h1 style='text-align: left; color: gray; border-bottom: 1px solid gray; display: block;'>AI Recruitment</h1>", unsafe_allow_html=True)

    st.sidebar.markdown("This application is a Recruitment dashboard")
    st.markdown("<hr/>", unsafe_allow_html=True)

    # side bar for selecting job description
    st.sidebar.markdown(f"<h1 style='text-align: left; color: gray; border-bottom: 1px solid gray; display: block;'>Job Description</h1>", unsafe_allow_html=True)

    path_to_dashboard_jsons = './dashboard_json/*.json'
    job_descriptions = dashboard_utils.get_job_descriptions_title(path_to_dashboard_jsons)
    # job_descriptions.insert(0,'Select a Job Description')
    if job_descriptions:
        jd_select_box = st.sidebar.selectbox('Job Description', job_descriptions, key='1')
    else:
        jd_select_box = st.sidebar.selectbox('Job Description', job_descriptions, key='1')

    jd_select_box = '' if jd_select_box == 'Select a Job Description' else jd_select_box    
    if not jd_select_box:
            st.markdown(f"<h6 style='text-align: center; color: gray;'>Please Select a Job Description!</h1>", unsafe_allow_html=True)


    #load json file of prediction model
    try:
        if jd_select_box:
            data = dashboard_utils.read_json(path_to_dashboard_jsons.rsplit('/',1)[0]+'/'+jd_select_box+'.json')
        else:
            data = {}
    except:
        data = {}



#     st.sidebar.title("Profiles")
    st.sidebar.markdown(f"<h1 style='text-align: left; color: gray; border-bottom: 1px solid gray; display: block;'>Profiles</h1>", unsafe_allow_html=True)

    profiles_name = dashboard_utils.get_profile_names(data)
    profiles_name.remove(selected_profile_name)
    profiles_name.insert(0,selected_profile_name)
    if profiles_name:
        select = st.sidebar.selectbox('User', profiles_name, key='1')
    else:
        select = st.sidebar.selectbox('User', profiles_name, key='1')

    select = '' if select == 'Select a Name' else select
    if select:
        profile_data = dashboard_utils.search_profile_by_name(select,data)
        personality = dashboard_utils.profile_personality(profile_data)
        total_exp, company_exp = dashboard_utils.experience_details(profile_data)
        activity = dashboard_utils.activity_similar(profile_data)
        profile_similarity_with_jd = dashboard_utils.profile_similarity_with_jd(profile_data)

        contact_info = dashboard_utils.get_contact_info(profile_data)

        all_profile_exp = dashboard_utils.all_profiles_experience(data)

        # if st.sidebar.button("All Profiles Experience"):
        #     dashboard_utils.bt_all_profiles_experience(all_profile_exp)
        # else:
        #     st.markdown(f"## Job Description : {jd_select_box}")
        #     st.markdown("<hr/>", unsafe_allow_html=True)

            

        #     if contact_info:
        #         st.markdown(f"### {select.split()[0]}'s Contact Info.")

        #         n_cols = len(contact_info.keys())
        #         col_labels = list(contact_info.keys())
        #         for key,val in contact_info.items():
        #             st.caption(key +':')
        #             st.caption(val)

        #     else:
        #         st.markdown(f"### {select.split()[0]}'s Contact Info.")
        #         st.markdown("Contact information not mentioned") 
        #     st.markdown("<hr/>", unsafe_allow_html=True)
            
        #     if profile_similarity_with_jd:
        #         st.markdown(f"### {select.split()[0]}'s Skills Similarity with Job Description")
        #         st.markdown(f"<h6 style='text-align: center; color: blue;'>Similarity of Skills : {round(profile_similarity_with_jd*100)}%</h1>", unsafe_allow_html=True)
        #     else:
        #         st.markdown(f"### {select.split()[0]}'s Skills Similarity with Job Description")
        #         st.markdown("No similarity found!") 
        #     st.markdown("<hr/>", unsafe_allow_html=True)
            
        #     if activity:
        #         st.markdown(f"### Similar LinkedIn Activities According to the Job Description")
        #         st.markdown(f"<h6 style='text-align: center; color: blue;'>Similarity of Activities : {round(activity*100)}%</h1>", unsafe_allow_html=True)
        #     else:
        #         st.markdown(f"### Similar LinkedIn Activities According to the Job Description")
        #         st.markdown("No similar activity found!") 
        #     st.markdown("<hr/>", unsafe_allow_html=True)
            
        #     # dashboard flow
        #     dashboard_utils.bt_experience_details(company_exp,total_exp)
        #     dashboard_utils.bt_profile_personality(personality,select)
        #     dashboard_utils.graph_working_domains_and_skills_in_linkedin(profile_data)

        #     dashboard_utils.graph_working_domains_and_skills_from_resume(profile_data)


        #     dashboard_utils.graph_working_domains_and_skills_from_experience(profile_data)
        #     dashboard_utils.graph_working_domains_and_skills_from_jd(profile_data)
        #     dashboard_utils.graph_common_resume_jd_skills(profile_data)
        #     dashboard_utils.graph_common_linkedin_jd_skills(profile_data)
        #     dashboard_utils.graph_union_linkedin_resume_skills(profile_data)

        if st.sidebar.button("All Profiles Experience"):
            dashboard_utils.bt_all_profiles_experience(all_profile_exp)
        else:
            st.markdown(f"## Job Description : {jd_select_box}")
            st.markdown("<hr/>", unsafe_allow_html=True)

            if contact_info:
                st.markdown(f"### {select.split()[0]}'s Contact Info.")

                n_cols = len(contact_info.keys())
                col_labels = list(contact_info.keys())
                for key,val in contact_info.items():
                    st.caption(key +':')
                    st.caption(val)

            else:
                st.markdown(f"### {select.split()[0]}'s Contact Info.")
                st.markdown("Contact information not mentioned") 
            st.markdown("<hr/>", unsafe_allow_html=True)
            
            if profile_similarity_with_jd:
                st.markdown(f"### {select}'s Skills Similarity with Job Description")
                st.markdown(f"<h6 style='text-align: center; color: gray;'>Similarity of Person's Skills : {round(profile_similarity_with_jd*100)}%</h1>", unsafe_allow_html=True)
            else:
                st.markdown(f"### {select}'s Skills Similarity with Job Description")
                st.markdown("No similarity found!") 
            st.markdown("<hr/>", unsafe_allow_html=True)
            
            if activity:
                st.markdown(f"### Similar LinkedIn Activities According to the Job Description")
                st.markdown(f"<h6 style='text-align: center; color: gray;'>Similarity of Activities : {round(activity*100)}%</h1>", unsafe_allow_html=True)
            else:
                st.markdown(f"### Similar LinkedIn Activities According to the Job Description")
                st.markdown("No similar activity found!") 
            st.markdown("<hr/>", unsafe_allow_html=True)
            
            # dashboard flow
            dashboard_utils.bt_experience_details(company_exp,total_exp)
            dashboard_utils.bt_profile_personality(personality)
            dashboard_utils.graph_working_domains_and_skills_in_linkedin(profile_data)

            dashboard_utils.graph_working_domains_and_skills_from_resume(profile_data)
            dashboard_utils.graph_working_domains_and_skills_from_experience(profile_data)
            dashboard_utils.graph_working_domains_and_skills_from_jd(profile_data)
            dashboard_utils.graph_common_resume_jd_skills(profile_data)
            dashboard_utils.graph_common_linkedin_jd_skills(profile_data)
            dashboard_utils.graph_union_linkedin_resume_skills(profile_data)


        
        
        
