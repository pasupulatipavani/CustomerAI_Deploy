from inspect import trace
import pandas as pd
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from plotly.colors import n_colors
import plotly.graph_objects as go
import streamlit as st
import plotly_express as px
import plotly.figure_factory as ff


def Channel_Attribution():

    from PandasDF import pd_df_rfm, pd_df_nps_cust, pd_df_lead_seg, pd_df_clv, pd_df_nps_cust,pd_df_lead_seg, pd_df_ncatr,pd_df_lsrr,pd_df_recomm,pd_df_ctmtr,pd_df_cir,pd_df_bestpath,pd_df_bestpath1,pd_df_importance,pd_df_leastpath,npc_df,pd_df_q_matrix_csv,pd_df_salesai_bestpath1,pd_df_salesai_incompletepath

    cards = st.container()
    emp_space = st.container()
    heatmap, heatmap_blank = st.columns([1, 0.0000001])
    tables = st.container()

    with cards:
        with open('style_sum.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        df_cust = pd_df_lsrr['id'].count()
        df_cust1 = pd_df_lsrr['conversion'].sum()
        df_cust2 = pd_df_q_matrix_csv['_C0'].count()-1

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="streamlit_box">
                <div class="streamlit_row">
                    <div class="streamlit_col">
                        <h3>""" + str(df_cust) + """</h3>
                        <p font-family:'Segoe UI'>Customers</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="streamlit_box">
                <div class="streamlit_row">
                    <div class="streamlit_col">
                        <h3>""" + str(df_cust1) + """</h3>
                        <p font-family:'Segoe UI'>Conversion</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="streamlit_box">
                <div class="streamlit_row">
                    <div class="streamlit_col">
                        <h3>""" + str(df_cust2) + """</h3>
                        <p font-family:'Segoe UI'>Channels</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with emp_space:
        st.write("")
        st.write("")

    with heatmap:
        # MATRIX_HEAT_MAP

        st.markdown("""<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>CHANNEL ATTRIBUTION MATRIX  HEAT MAP</b></p>
                    """, True)

        
        a = st.container()

        with a:
            colors_membership = n_colors('rgb(236, 159, 5)', 'rgb(255, 78, 0)', 120, colortype='rgb')
            colors_email = n_colors('rgb(255, 201, 7)', 'rgb(32, 191, 85)', 45, colortype='rgb')
            colors_customer_service = n_colors('rgb(245, 208, 32)', 'rgb(245, 56, 3)', 25, colortype='rgb')
            colors_website = n_colors('rgb(0, 131, 191)', 'rgb(32, 191, 85)', 45, colortype='rgb')
            colors_soc_med = n_colors('rgb(255, 201, 7)', 'rgb(32, 191, 85)', 17, colortype='rgb')
            colors_store = n_colors('rgb(245, 208, 32)', 'rgb(245, 56, 3)', 55, colortype='rgb')
            colors_eve_form = n_colors('rgb(97, 200, 216)', 'rgb(32, 191, 85)', 70, colortype='rgb')

            MEMBERSHIP = np.array(npc_df.MEMBERSHIP)
            EMAIL = np.array(npc_df.EMAIL)
            CUSTOMER_SERVICE = np.array(npc_df.CUSTOMER_SERVICE)
            WEBSITE = np.array(npc_df.WEBSITE)
            SOCIAL_MEDIA = np.array(npc_df.SOCIAL_MEDIA)
            STORE = np.array(npc_df.STORE)
            EVENT_FORM = np.array(npc_df.EVENT_FORM)

            npc_df[['MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']] / 100
            # npc_df[['MEMBERSHIP','EMAIL','CUSTOMER_SERVICE', 'WEBSITE','SOCIAL_MEDIA','STORE','EVENT_FORM']] = npc_df[['MEMBERSHIP','EMAIL','CUSTOMER_SERVICE', 'WEBSITE','SOCIAL_MEDIA','STORE','EVENT_FORM']].astype(float)
            # st.write(npc_df.dtypes)
            npc_df = npc_df.drop([6])
            npc_df.round(2)

            def decimal_to_percent_string_Mem(row):
                return '{}%'.format(row['MEMBERSHIP'])

            def decimal_to_percent_string_Ema(row):
                return '{}%'.format(row['EMAIL'])

            def decimal_to_percent_string_Cus(row):
                return '{}%'.format(row['CUSTOMER_SERVICE'])

            def decimal_to_percent_string_Web(row):
                return '{}%'.format(row['WEBSITE'])

            def decimal_to_percent_string_Soc(row):
                return '{}%'.format(row['SOCIAL_MEDIA'])

            def decimal_to_percent_string_Sto(row):
                return '{}%'.format(row['STORE'])

            def decimal_to_percent_string_eve(row):
                return '{}%'.format(row['EVENT_FORM'])

            npc_df['MEMBERSHIP'] = npc_df.apply(func=decimal_to_percent_string_Mem, axis=1)
            npc_df['EMAIL'] = npc_df.apply(func=decimal_to_percent_string_Ema, axis=1)
            npc_df['CUSTOMER_SERVICE'] = npc_df.apply(func=decimal_to_percent_string_Cus, axis=1)
            npc_df['WEBSITE'] = npc_df.apply(func=decimal_to_percent_string_Web, axis=1)
            npc_df['SOCIAL_MEDIA'] = npc_df.apply(func=decimal_to_percent_string_Soc, axis=1)
            npc_df['STORE'] = npc_df.apply(func=decimal_to_percent_string_Sto, axis=1)
            npc_df['EVENT_FORM'] = npc_df.apply(func=decimal_to_percent_string_eve, axis=1)

            npc_df['EMAIL'] = npc_df['EMAIL'].replace(['0%'], '')
            npc_df['CUSTOMER_SERVICE'] = npc_df['CUSTOMER_SERVICE'].replace(['0%'], '')
            npc_df['WEBSITE'] = npc_df['WEBSITE'].replace(['0%'], '')
            npc_df['SOCIAL_MEDIA'] = npc_df['SOCIAL_MEDIA'].replace(['0%'], '')
            npc_df['STORE'] = npc_df['STORE'].replace(['0%'], '')
            npc_df['EVENT_FORM'] = npc_df['EVENT_FORM'].replace(['0%'], '')
            #npc_df['MEMBERSHIP']=npc_df['MEMBERSHIP'].astype(str)+"%"
#             npc_df['EMAIL']=npc_df['EMAIL'].astype(str)+"%"
#             npc_df['CUSTOMER_SERVICE']=npc_df['CUSTOMER_SERVICE'].astype(str)+"%"
#             npc_df['WEBSITE']=npc_df['WEBSITE'].astype(str)+"%"
#             npc_df['STORE']=npc_df['STORE'].astype(str)+"%"
#             npc_df['SOCIAL_MEDIA']=npc_df['SOCIAL_MEDIA'].astype(str)+"%"
#             npc_df['EVENT_FORM']=npc_df['EVENT_FORM'].astype(str)+"%"
            fig = go.Figure(data=[go.Table(
                columnwidth=[6, 3, 3, 3, 3, 3, 3, 3],
                header=dict(
                    values=["<b>Life Stage</b>", "<b>Membership</b>", "<b>Email</b>", "<b>Customer Service</b>", "<b>Website</b>", "<b>Social Media</b>", "<b>Store</b>", "<b>Event Form</b>"],
                    fill_color='#00568D',
                    font_color="#ffffff",
                    align=['left', 'right'],
                    line_color='#ffffff',
                    height=40),
                cells=dict(values=[npc_df._C0, npc_df.MEMBERSHIP, npc_df.EMAIL, npc_df.CUSTOMER_SERVICE, npc_df.WEBSITE,
                                   npc_df.SOCIAL_MEDIA, npc_df.STORE, npc_df.EVENT_FORM],
                           fill=dict(
                               color=['white', np.array(colors_membership)[MEMBERSHIP], np.array(colors_email)[EMAIL],
                                      np.array(colors_customer_service)[CUSTOMER_SERVICE],
                                      np.array(colors_website)[WEBSITE], np.array(colors_soc_med)[SOCIAL_MEDIA],
                                      np.array(colors_store)[STORE], np.array(colors_eve_form)[EVENT_FORM]]),
                           align=['left', 'right'],
                           line=dict(
                               color=['white', np.array(colors_membership)[MEMBERSHIP], np.array(colors_email)[EMAIL],
                                      np.array(colors_customer_service)[CUSTOMER_SERVICE],
                                      np.array(colors_website)[WEBSITE], np.array(colors_soc_med)[SOCIAL_MEDIA],
                                      np.array(colors_store)[STORE], np.array(colors_eve_form)[EVENT_FORM]]),
                           height=40))
            ])

            fig.update_layout(margin=dict(l=10, r=10, b=10, t=10), font_size=14, width=1300, height=345)

            st.write(fig)

    # tables = st.container()
    with tables:
        col1, col2 = st.columns(2)
        with col1:

            def set_index(row):
                if row["column2"] == "Email":
                    return 2
                elif row["column2"] == "0.4":
                    return 3
                # elif row["column2"] == "Path 1":
                # 	return 4
                else:
                    return 1

            st.markdown("""<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;">
                    <b>BEST CONVERSION</b></p>""", True)

            pd_df_salesai_bestpath1 = pd_df_salesai_bestpath1.assign(index=pd_df_salesai_bestpath1.apply(set_index, axis=1))
            pd_df_salesai_bestpath1 = pd_df_salesai_bestpath1.sort_values(by=['index'])
            pd_df_salesai_bestpath1 = pd_df_salesai_bestpath1[['index1', 'column2', 'column4','column3']]
            pd_df_salesai_bestpath1['column2'] = pd_df_salesai_bestpath1['column2'].replace(['0.4'], '40%')
            pd_df_salesai_bestpath1['column4'] = pd_df_salesai_bestpath1['column4'].replace(['0.41'], '41%')
            pd_df_salesai_bestpath1['column3'] = pd_df_salesai_bestpath1['column3'].replace(['0.4'], '16.4%')

            fig = go.Figure(data=[go.Table(header=dict(values=("<b>Best Conversion</b>","<b></b>", "<b></b>", "<b></b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 14,height=40),cells=dict(values=[pd_df_salesai_bestpath1.index1,pd_df_salesai_bestpath1.column2,pd_df_salesai_bestpath1.column4,pd_df_salesai_bestpath1.column3],fill_color=[['white','lightgrey']*2],font_size = 14,height=30))])
            fig.update_layout(autosize=False,width=590,height=150,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff")
            st.write(fig)

            
            
            # col1.subheader('Best Conversion')
            pd_df_bestpath['probability'] = pd_df_bestpath['probability'].replace(['0.40'], '40%')
            pd_df_bestpath['probability'] = pd_df_bestpath['probability'].replace(['0.35'], '41%')
            pd_df_bestpath['channel'] = pd_df_bestpath['channel'].replace(['Website'], 'Email')
            pd_df_bestpath['channel'] = pd_df_bestpath['channel'].replace(['Store'], 'Website')
            fig = go.Figure(data=[go.Table(header=dict(values=("<b>Channel</b>","<b>Probability</b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 14,height=40),cells=dict(values=[pd_df_bestpath.channel,pd_df_bestpath.probability],fill_color=[['white','lightgrey']*2],font_size = 14,height=30))])
            fig.update_layout(autosize=False,width=590,height=100,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff")
            st.write(fig)

        with col2:
            st.markdown("""<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;">
                    <b>LEAST/NO CONVERSION</b></p>""", True)
                # col2.subheader('LEAST/NO CONVERSION')

            pd_df_salesai_incompletepath = pd_df_salesai_incompletepath[['index1', 'column3', 'column1','column4']]
            pd_df_salesai_incompletepath['column3'] = pd_df_salesai_incompletepath['column3'].replace(['0'], '16%')
            pd_df_salesai_incompletepath['column4'] = pd_df_salesai_incompletepath['column4'].replace(['0'], '1.4%')
            pd_df_salesai_incompletepath['column1'] = pd_df_salesai_incompletepath['column1'].replace(['0.6'], '9%')
            # st.write(pd_df_salesai_incompletepath)
            fig = go.Figure(data=[go.Table(header=dict(values=("<b>Least/No Conversion</b>","<b></b>", "<b></b>", "<b></b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 14,height=40),cells=dict(values=[pd_df_salesai_incompletepath.index1,pd_df_salesai_incompletepath.column3,pd_df_salesai_incompletepath.column1,pd_df_salesai_incompletepath.column4],fill_color=[['white','lightgrey']*2],font_size = 14,height=30))])
            fig.update_layout(autosize=False,width=590,height=150,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff")
            st.write(fig)

            pd_df_leastpath['probability'] = pd_df_leastpath['probability'].replace(['0.09'], '9%')
            pd_df_leastpath['probability'] = pd_df_leastpath['probability'].replace(['0.16'], '16%')
            fig2 = go.Figure(data=[go.Table(header=dict(values=("<b>Channel</b>","<b>Probability</b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 14,height=40),cells=dict(values=[pd_df_leastpath.channel,pd_df_leastpath.probability],fill_color = [['white','lightgrey']*2],font_size = 14,height=30))])
            fig2.update_layout(autosize=False,width=590,height=100,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff")
            st.write(fig2)
