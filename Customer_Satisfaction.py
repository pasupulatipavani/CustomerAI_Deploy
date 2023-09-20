import common
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import plotly.express as px
import plotly.graph_objects as go
import datetime

def Customer_Satisfaction():

    from PandasDF import pd_df_rfm, pd_df_clv, pd_df_nps_cust,pd_df_recomm

    with open('style_sum.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    upper_panel = st.container()
    header = st.container()
    table_lifestage_label = st.container()
    pie_charts = st.container()
    dataset = st.container()

    with upper_panel:
        col_state, col_city, col_gender, col_agebin, col_lifestage, col_label, col_emp = st.columns([2,2,2,2,2,2,3])

        state = np.sort(pd_df_rfm['state'].unique()).tolist()
        gender = np.sort(pd_df_rfm['gender'].unique()).tolist()
        agebin = np.sort(pd_df_rfm['ageBin'].unique()).tolist()
        lifestage = np.sort(pd_df_rfm['lifeStage'].unique()).tolist()
        label = np.sort(pd_df_rfm['label'].unique()).tolist()

        state.insert(0, 'All')
        gender.insert(0, 'All')
        agebin.insert(0, 'All')
        lifestage.insert(0, 'All')
        label.insert(0, 'All')

    state_selection = col_state.selectbox('State', state,index=0)
    if state_selection == 'All':    
        state_selection = state
        #Created a Dependency City Filter in the bottom
        city = np.sort(pd_df_rfm['city'].unique()).tolist()  
        city.insert(0, 'All')  

    else:
        #state_selection.append('Dummy')
        state_selection=[state_selection]
        pd_rfm_city= pd_df_rfm.loc[(pd_df_rfm["state"].isin(state_selection)),['city']]
        city=np.sort(pd_rfm_city['city'].unique()).tolist()
        city.insert(0, 'All')
        

    city_selection = col_city.selectbox('City', city,index=0)
    if city_selection == 'All':    
        city_selection = city 
    else:
        #city_selection.append('Dummy')
        city_selection=[city_selection]

    gender_selection = col_gender.selectbox('Gender', gender,index=0)
    if gender_selection == 'All':    
        gender_selection = gender      
    else:
        #gender_selection.append('Dummy')
        gender_selection=[gender_selection]

    agebin_selection = col_agebin.selectbox('Age Bin', agebin,index=0)
    if agebin_selection == 'All':    
        agebin_selection = agebin
    else:
        #agebin_selection.append('Dummy')
        agebin_selection=[agebin_selection]

    lifestage_selection = col_lifestage.selectbox('Life Stage', lifestage,index=0)
    if lifestage_selection == 'All':    
        lifestage_selection = lifestage
    else:
        #lifestage_selection.append('Dummy') 
        lifestage_selection=[lifestage_selection]

    label_selection = col_label.selectbox('Monetary Bin', label,index=0)
    if label_selection == 'All':    
        label_selection = label
    else:
        #label_selection.append('Dummy')
        label_selection=[label_selection]

    customer_selection_pd = pd_df_rfm.loc[(pd_df_rfm['state'].isin(state_selection)) & (pd_df_rfm['city'].isin(city_selection)) & (pd_df_rfm['gender'].isin(gender_selection)) & (pd_df_rfm['ageBin'].isin(agebin_selection)) & (pd_df_rfm['lifeStage'].isin(lifestage_selection)) & (pd_df_rfm['label'].isin(label_selection)),["customerid"]]
    #customer_selection_pd = pd_df_rfm.loc[(pd_df_rfm['STATE'].isin(state)) & (pd_df_rfm['CITY'].isin(city)) & (pd_df_rfm['GENDER'].isin(gender)) & (pd_df_rfm['AGEBIN'].isin(agebin)) & (pd_df_rfm['LIFESTAGE'].isin(lifestage)) & (pd_df_rfm['LABEL'].isin(label)),["CUSTOMERID"]]

    customer_selection_list = customer_selection_pd["customerid"].unique().astype(str).tolist()
    
    pd_df_recomm['customerid']=  pd_df_recomm['customerid'].astype(str)
    products_pd = pd_df_recomm.loc[(pd_df_recomm["customerid"].isin(customer_selection_list)),['categoryPurchased']]

    count_of_customers = len(customer_selection_list)
    count_of_products = len(products_pd["categoryPurchased"].unique().tolist())

    customer_statistics = st.container()
    with customer_statistics:

        # Row A
        c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.1, 1.7])

        with c1:
            st.markdown("""
                        <div class="streamlit_box">
                            <div class="streamlit_row">
                                <div class="streamlit_col">
                                    <h3>""" + str(count_of_customers) + """</h3>
                                    <p font-family:'Segoe UI'>Customers</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
                        <div class="streamlit_box">
                            <div class="streamlit_row">
                                <div class="streamlit_col">
                                    <h3>""" + str(count_of_products) + """</h3>
                                    <p font-family:'Segoe UI'>Products</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        with c3:
            pd_df_nps_cust_wid = pd.merge(pd_df_nps_cust, customer_selection_pd, on='customerid')
            
            pd_df_nps_cust_wid1=pd_df_nps_cust.groupby(["Overall_NPS_Result"])["Overall_NPS_Result"].count()
            pd_df_nps_cust_wid1['detract'] = pd_df_nps_cust_wid1.get('detract', 0)
            pd_df_nps_cust_wid1['promote'] = pd_df_nps_cust_wid1.get('promote', 0)
            pd_df_nps_cust_wid1['passive'] = pd_df_nps_cust_wid1.get('passive', 0)
            overall_nps=str(round((pd_df_nps_cust_wid1['promote']-pd_df_nps_cust_wid1['detract'])*(100/(pd_df_nps_cust_wid1['detract']+pd_df_nps_cust_wid1['promote']+pd_df_nps_cust_wid1['passive'])),2))
			


            st.markdown("""
                        <div class="streamlit_box">
                            <div class="streamlit_row">
                                <div class="streamlit_col">
                                    <h3>""" + str(overall_nps) + """</h3>
                                    <p font-family:'Segoe UI'>Overall Net Promoter Score</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # fig = px.pie(pd_df_nps_cust, names='OVERALL_NPS_RESULT', values='CUSTOMERID')
            # c4.write(fig)

        with c4:
            #st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            #st.subheader("Overall NPS Result by CustomerID")
            pd_df_nps_cust_wid2=pd_df_nps_cust_wid.groupby(['Overall_NPS_Result']) .apply(lambda x: pd.Series({'CUSTOMER_COUNT' : x['customerid'].count()}))
            pd_df_nps_cust_wid2=pd_df_nps_cust_wid2.reset_index(0)
            pd_df_nps_cust_wid2.rename(columns = {'Overall_NPS_Result':'Overall_NPS_Result', 'CUSTOMER_COUNT':'Count of Customers'}, inplace = True)
            fig = px.pie(pd_df_nps_cust_wid2, names='Overall_NPS_Result', values='Count of Customers', hole = 0.65, color='Overall_NPS_Result',
                    color_discrete_map={'promote':'#0CC368',
                                        'detract':'#E01F27',
                                        'passive':'#FFBB00'})
            fig.update_layout(
                        autosize=True,
                        width=350,
                        height=300,
                        margin=dict(
                            l=20,
                            r=5,
                            b=10,
                            t=10,
                            pad=4
                        ), paper_bgcolor="#ffffff",)

            st.write(fig)
    
    dataset = st.container()
    
    with dataset:

        col_table, col_table_blank = st.columns([1, 0.0000001])

        with col_table:

            inner = pd.merge(pd_df_rfm,customer_selection_pd, on='customerid')
            inner = inner[['customerid','firstName', 'lastName', 'gender', 'city', 'state', 'lastPurchaseDate','recency', 'frequency','monetary']]
            inner = pd.merge(inner,pd_df_clv, on='customerid')
            inner = inner[['customerid','firstName', 'lastName', 'gender', 'city', 'state', 'lastPurchaseDate','recency_x', 'frequency_x','monetary','1YearCLV']]


            inner.rename(columns = {'recency_x':'recency', 'frequency_x':'frequency'}, inplace = True)

            inner = pd.merge(inner, pd_df_nps_cust, on='customerid')
            inner = inner[['customerid','firstName_x', 'lastName_x', 'gender_x', 'city_x', 'state_x', 'lastPurchaseDate_x', 'recency_x', 'frequency_x', 'monetary_x','1YearCLV','avgRating','Overall_NPS_Result']]
            
            inner['1YearCLV'] = inner['1YearCLV'].round(decimals = 2)
            inner['lastPurchaseDate_x'] = inner['lastPurchaseDate_x'].dt.strftime("%m/%d/%Y")
            inner['monetary_x'] = '$'+inner['monetary_x'].astype(str)
            inner['1YearCLV'] = '$'+inner['1YearCLV'].astype(str)
            
            inner.rename(columns = {'customerid':'Customerid', 'firstName_x':'firstName', 'lastName_x':'lastName', 'gender_x':'gender', 'city_x':'city', 'state_x':'state', 'lastPurchaseDate_x':'lastPurchaseDate', 'recency_x':'recency', 'frequency_x':'frequency', 'monetary_x':'Income', '1YearCLV':'OneYearCLV', 'avgRating':'avgRating', 'Overall_NPS_Result':'Overall_NPS_Result'}, inplace = True)

            st.markdown("""<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;">
                    <b>CUSTOMER LIST</b></p>""", True)
                # col2.subheader('Least/No Conversion')
            fig2 = go.Figure(data=[go.Table(columnwidth=[3,2.5,2.5,1.5,3,1.5,4,2,2,2,2,2.5,3.5],header=dict(values=("<b>Customer Id</b>", "<b>First Name</b>", "<b>Last Name</b>", "<b>Gender</b>", "<b>City</b>", "<b>State</b>", "<b>Last Purchase Date</b>", "<b>Recency</b>", "<b>Frequency</b>", "<b>Income</b>", "<b>1YearCLV</b>", "<b>Rating</b>", "<b>Overall NPS Result</b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 14,height=40),cells=dict(values=[inner.Customerid, inner.firstName, inner.lastName, inner.gender, inner.city, inner.state, inner.lastPurchaseDate, inner.recency, inner.frequency, inner.Income, inner.OneYearCLV, inner.avgRating, inner.Overall_NPS_Result], fill_color = [['white','lightgrey']*2600], align=['left','left','left','left','left','left','left','right','right','right','right','right','left'], font_size = 13,height=30))])
            fig2.update_layout(autosize=False,width=1300,height=400,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff"        )
            st.write(fig2)
            
