
from utils.dashboard_utils import *
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 
import screening_main
import altair as alt
import pandas as pd
import numpy as np
import textract
import json
import glob
import os

from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure
from bokeh.plotting import curdoc
from bokeh.layouts import column


def read_json(json_path):
    try:
        """
            input (str) : path of json file
            output (json): return a json file
        """
        # Opening JSON file
        f = open(json_path,"r")

        # returns JSON object as
        # a dictionary
        data = json.load(f)
        return data
    except: 
        return ''
    
def extract_text_from_document(filename):
    try:
        """
            input (str) : path of the document
            output (str) : return all the text foung in doucment
        """
        text = textract.process(filename)
        lower_case_string =  str(text.decode('utf-8')).lower()
        return lower_case_string
    except:
        return ''

def read_file(txt_file):
    try:
        text = extract_text_from_document(txt_file)        
        return text
    except:
        return ''
    
def read_selected_job_description(path_to_jd):
    try:
        my_jd = read_file(path_to_jd)
        return my_jd
    except:
        return ''


def get_contact_info(profile_data):
    try:
        contact_info = profile_data['my_contact_info']
        return contact_info
    except:
        return {}
            
def get_profile_names(data):
    p_names = []
    try:
        for p in data.keys():
            p_names.append(data[p]['Name'])
    except:
        pass
    return p_names

def get_job_descriptions_title(path_to_jds):
    try:
        jds = glob.glob(path_to_jds)
        titles = [os.path.basename(jd).split('.')[0] for jd in jds]
        return titles
    except:
        return []
    
def working_domains(data):
    try:
        name = data['Name']
        domain = data['Working_Domain']
        scores = domain['Scores']
        skills = domain['Skills']
        return scores, skills
    except:
        return {}, {}
        
def search_profile_by_name(name,data):
    try:
        for key in data.keys():
            profile = data[key]
            if profile['Name'].lower() == name.lower():
                return profile
        return ''
    except:
        return ''
    
def JD_matched_skills(profile_data):
    try:
        skills = profile_data['JD matched skills']
        return skills
    except:
        return {}
    
def resume_linkedin_matched_skills(profile_data):
    try:
        skills = profile_data['Resume linkedin matched skills']
        return skills
    except:
        return {}
    
def experience_details(profile_data):
    try:
        experience = profile_data['Experience Details']
        total_exp = experience[-1]
        company_exp = experience[0]
        return total_exp, company_exp
    except:
        return 0,  {}
    
def exp_in_int(score_df):
    try:
        expp = list(score_df['Experience'])
        exp_ind = []
        for ind, i in enumerate(expp):
            i = i.replace('Full-time','').strip(' .·')
            
            if 'yr' in i and 'mo' in i:
                years = int(i.split('yr')[0].strip())
                months = int(i.split('yr')[-1].strip('mos '))
                years = years + months/12
                exp_ind.append(round(years,2))
            elif 'yr' in i:
                years = int(i.split('yr')[0].strip())
                exp_ind.append(round(years,2))
            else:
                months = int(i.strip('mos '))
                years = months/12
                exp_ind.append(round(years,2))

        return exp_ind
    except:
        print('=======>>>>>>>>>>> inexceptipn ')
        return []
    
def skills_from_experience(profile_data):
    try:
        skills = profile_data['Skills from Experience']
        return skills
    except:
        return {}
    
def profile_personality(profile_data):
    try:
        personality = profile_data['personality']
        return personality
    except:
        return []

def activity_similar(profile_data):
    try:
        activity  = profile_data['activity_similar']
        return activity
    except:
        return 0
    
def profile_similarity_with_jd(profile_data):
    try:
        skills_similarity  = profile_data['skills_similarity_with_jd']
        return skills_similarity
    except:
        return 0
    
def all_profiles_experience(data):
    profile_exp = {}
    try:
        for key in data.keys():
            try:
                name = data[key]['Name']
                exp = data[key]['Experience Details']
                total_exp = exp[-1]
                profile_exp[name] = total_exp
            except:
                pass
    except Exception as e:
        pass
    return profile_exp


def skills_from_linkedin(profile_data):
    try:
        skills  = profile_data['skills from linkedin']
        return skills
    except:
        return []
    
def get_parent_character(d):
    characters = []
    parents = []
    for key in d.keys():
        characters.extend(d[key])
        parents.extend([key]*len(d[key]))

    characters.extend(list(d.keys()))
    parents.extend(['Skills']*len(d.keys()))
    
    return characters, parents

    
def graph_working_domains_and_skills_from_experience(profile_data):
    st.markdown("### Working Domains and Skills from Experience")
    if profile_data['working_domains_and_skills_from_experience']:   
        d = profile_data['working_domains_and_skills_from_experience']

        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    else:
        st.markdown("Skills and Domains not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)

def graph_working_domains_and_skills_from_resume(profile_data):
    st.markdown("### Working Domains and Skills from Resume")
    if profile_data['working_domains_and_skills_from_resume']:   
        d = profile_data['working_domains_and_skills_from_resume']
  
        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    else:
        st.markdown("Skills and Domains not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
def graph_working_domains_and_skills_from_jd(profile_data):
    st.markdown("### Working Domains and Skills from Job Description")
    if profile_data['working_domains_and_skills_from_jd']:   
        d = profile_data['working_domains_and_skills_from_jd']
        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    else:
        st.markdown("Skills and Domains not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    
def graph_union_linkedin_resume_skills(profile_data):
    st.markdown("### Union of Resume/LinkedIn Working Domains and Skills")
    if profile_data['union_linkedin_resume_skills']:   
        d = profile_data['union_linkedin_resume_skills']
        # print('\n\n ---->>>> unioon\n',d)
        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    else:
        st.markdown("Skills and Domains not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    
def graph_common_resume_jd_skills(profile_data):
    st.markdown("### Common Resume/JD Working Domains and Skills")
#     if profile_data['common_resume_jd_skills']:   
#         d = profile_data['common_resume_jd_skills']
#         df = pd.DataFrame(d)
#         if len(df)<1:
#             st.markdown("Skills and Domains not found!")
#         else: 
#             fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
#             st.plotly_chart(fig)
#     else:
#         st.markdown("Skills and Domains not found!")

    if profile_data['common_resume_jd_skills'].get('s1'):
        st.markdown("Skills and Domains not found from Resume OR Resume not Found!")
    elif profile_data['common_resume_jd_skills'].get('s2'):
        st.markdown("Skills and Domains not found from JD!")
    else:   
        d = profile_data['common_resume_jd_skills']
        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    st.markdown("<hr/>", unsafe_allow_html=True)
    
def graph_common_linkedin_jd_skills(profile_data):
    st.markdown("### Common LinkedIn/JD Working Domains and Skills")
    if profile_data['common_linkedin_jd_skills']:   
        d = profile_data['common_linkedin_jd_skills']
        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    else:
        st.markdown("Skills and Domains not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)



def graph_working_domains_and_skills_in_linkedin(profile_data):
    st.markdown("### Working Domains and Skills Mentioned in LinkedIn")
    if profile_data['domains_and_skills_from_linkedin']:   
        d = profile_data['domains_and_skills_from_linkedin']
        
        df = pd.DataFrame(d)
        if len(df)<1:
            st.markdown("Skills and Domains not found!")
        else: 
            fig = px.sunburst(df, path=['Parent', 'Role', 'Skills', 'Aliases'])
            st.plotly_chart(fig)
    else:
        st.markdown("Skills and Domains not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)



def bt_all_profiles_experience(profile_exp):
    st.markdown("### Experience Comparison")
    if profile_exp:            
        score_df = pd.DataFrame(profile_exp.items(),columns = ['Name','Experience'])         
        score_df = score_df.sort_values('Experience')
        fig = px.bar(score_df,x='Name',y='Experience',color="Experience", title="Experience Comparison",height=600)
        st.plotly_chart(fig)                
    else:
        st.markdown("Experience not found!")
    st.markdown("<hr/>", unsafe_allow_html=True)
    


def bt_working_domain(scores):
    st.markdown("## Working Domain & Score")
    if scores:            
        score_df = pd.DataFrame(scores.items(),columns = ['domain','score']) 
        fig = px.pie(score_df, values='score', names='domain', title='Working Domain Score')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    else:
        st.markdown("Working Domains not Found!")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
def bt_experience_details(company_exp,total_exp,profile_data):
    st.markdown("## Experience Details")
    if company_exp:
        st.markdown(f"<h1 style='text-align: center; color: gray;'>Total Experience Above: {total_exp} years</h1>", unsafe_allow_html=True)
        score_df = pd.DataFrame(company_exp.items(),columns = ['Company','Experience']) 

        mylist = exp_in_int(score_df)
        se = pd.Series(mylist)
        score_df['Total Experience (Years)'] = se.values
        score_df = score_df.sort_values('Total Experience (Years)')
        fig = px.bar(score_df,x='Company',y='Total Experience (Years)',color="Experience", title="Experience Details",height=600)
        st.plotly_chart(fig)

        table_for_company_exp(profile_data)
    else:
        st.markdown("Experience not Found!")
    st.markdown("<hr/>", unsafe_allow_html=True)

def bt_JD_matched_skills(jd_matched_skills):
    st.markdown("## Skills Matched with Job Description") 
    if jd_matched_skills:
        score_df = pd.DataFrame(jd_matched_skills.items(),columns = ['skill','score']) 
        fig = px.pie(score_df, values='score', names='skill', title='JD skills & Score')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    else:
        st.markdown("No skill matched with Job Description!")
    st.markdown("<hr/>", unsafe_allow_html=True)

def bt_resume_linkedin_matched_skills(resume_linkedin_matched_skills):
    st.markdown("### Resume Linkedin Matched Skills & Score")
    if resume_linkedin_matched_skills:
        score_df = pd.DataFrame(resume_linkedin_matched_skills.items(),columns = ['skills','score']) 
        fig = px.pie(score_df, values='score', names='skills', title='Resume Linkedin Matched Skills & Score')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    else:
        st.markdown("Skills mentioned in linkedin not matched with resume's skills!")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
def bt_skills_from_experience(skills_from_experience):
    st.markdown("### Skills & Scores From Experience")
    if skills_from_experience:
        score_df = pd.DataFrame(skills_from_experience.items(),columns = ['skills','score']) 
        fig = px.pie(score_df, values='score', names='skills', title='Skills & Scores From Experience')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    else:
        st.markdown("Skills not matched with Experience")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
def bt_profile_personality(personality):
    st.markdown("### Personality of Person")
    if personality:
        p_types = ['Extraversion','Neuroticism','Agreeableness', 'Conscientiousness', 'Openness']    
        rr = [1]*len(p_types)
        personality_df = pd.DataFrame(list(zip(p_types, personality,rr)),
               columns =['Type', 'value','r'])

        fig = px.line_polar(personality_df, r= personality, theta='Type', line_close=True)
        st.plotly_chart(fig)
    else:
        st.markdown("Personality of Person not found!") 
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    
def make_df_for_dashboard(job_descriptions):
    df_list = []
    for jd_title in job_descriptions:
        data = read_json('./dashboard_json/'+jd_title+'.json')
        name_list = []
        activity_list = []
        jd_skills_similarity = []
        for profile in data.keys():
            activity = data[profile]['activity_similar']*100
            name = data[profile]['Name']
            similarity = data[profile]['skills_similarity_with_jd']
            
#             print(name,' :: ',similarity,'\n')
            name_list.append(name)
            activity_list.append(int(activity))
            jd_skills_similarity.append(round(similarity*100,1))
#         table = pd.DataFrame({'Name':name_list,jd_title:activity_list,'Skills_JD':jd_skills_similarity})
        table = pd.DataFrame({'Name':name_list,jd_title:jd_skills_similarity})
        df_list.append(table)
    df = df_list[0]
    for dfs in df_list[1:]:
        df = pd.merge(df, dfs) 
    return df


def make_table(df):
    st.subheader("Profile's Similarity According to Job Description")
    cds = ColumnDataSource(df)
    columns = []
    df_clmns = list(df.columns)
    for clm in df_clmns:
        if clm == 'Name':
            columns.append(TableColumn(field=clm, title=clm, formatter=HTMLTemplateFormatter(template='<p><%= value %></p>')))
        else:
            columns.append(TableColumn(field=clm, title=clm, formatter=HTMLTemplateFormatter(template='<p><%= value %>%</p>')))
    
    
    source_code = """
            document.dispatchEvent(
            new CustomEvent("INDEX_SELECT", {detail: {data: source.selected.indices}})
            )
            """  
#     source_code = """
#             var grid = document.getElementsByClassName('grid-canvas')[0].children;

#             var row = '';
#             var col = '';

#             for (var i=0,max=grid.length;i<max;i++){
#                 if (grid[i].outerHTML.includes('active')){
#                     row=i;
#                     for (var j=0,jmax=grid[i].children.length;j<jmax;j++){
#                         if(grid[i].children[j].outerHTML.includes('active')){col=j}
#                     }
#                 }
#             }

#             console.log('row',row);
#             console.log('col',col);

#             cb_obj.selected['1d'].indices = [];
#             """
    
    # define events
    cds.selected.js_on_change(
    "indices",
    CustomJS(
            args=dict(source=cds),
            code=source_code ))
    p = DataTable(source=cds, columns=columns, css_classes=["my_table"])
    result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=True, debounce_time=0, )
    if result:
        print(result)
        if result.get("INDEX_SELECT"):
            profile_name = df.iloc[result.get("INDEX_SELECT")["data"][0]]['Name']
            return profile_name
    return ''


def table_for_company_exp(profile_data):
    company_and_exp_dict = profile_data['company_and_exp_dict']
    company_dict = {}
    for c_key in company_and_exp_dict.keys():
        my_skills_list = []
        exp_skills = company_and_exp_dict[c_key]['Skills']
        for k in exp_skills.keys():
            my_skills_list.append(exp_skills[k])

        my_skills_list = list(set(my_skills_list))
        company_dict[c_key.replace('Full-time','').strip('· ')] = my_skills_list
        

    min_length = 1000

    df = pd.DataFrame({k:pd.Series(v[:min_length]) for k,v in company_dict.items()})
    df.fillna('', inplace=True)
    st.dataframe(df)
    
    
