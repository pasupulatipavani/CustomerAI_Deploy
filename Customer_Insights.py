import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid.shared import GridUpdateMode
from plotly.colors import n_colors
import plotly.graph_objects as go
import numpy as np
from decimal import *


def Customer_Insights():

    from PandasDF import pd_df_rfm, pd_df_nps_cust, pd_df_lead_seg, pd_df_clv, pd_df_nps_cust,pd_df_lead_seg, pd_df_ncatr,pd_df_lsrr,pd_df_recomm

    with open('style_sum.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    upper_panel = st.container()
    header = st.container()
    table_lifestage_label = st.container()
    pie_charts = st.container()

    lifestage_clv_nps = st.container()
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
        state_selection=[state_selection]
        pd_rfm_city= pd_df_rfm.loc[(pd_df_rfm["state"].isin(state_selection)),['city']]
        city=np.sort(pd_rfm_city['city'].unique()).tolist()
        city.insert(0, 'All')
        

    city_selection = col_city.selectbox('City', city,index=0)
    if city_selection == 'All':    
        city_selection = city 
    else:
        city_selection=[city_selection]

    gender_selection = col_gender.selectbox('Gender', gender,index=0)
    if gender_selection == 'All':    
        gender_selection = gender      
    else:
        gender_selection=[gender_selection]

    agebin_selection = col_agebin.selectbox('Age Bin', agebin,index=0)
    if agebin_selection == 'All':    
        agebin_selection = agebin
    else:
        agebin_selection=[agebin_selection]

    lifestage_selection = col_lifestage.selectbox('Life Stage', lifestage,index=0)
    if lifestage_selection == 'All':    
        lifestage_selection = lifestage
    else:
        lifestage_selection=[lifestage_selection]

    label_selection = col_label.selectbox('Monetary Bin', label,index=0)
    if label_selection == 'All':    
        label_selection = label
    else:
        label_selection=[label_selection]

    customer_selection_pd = pd_df_rfm.loc[(pd_df_rfm['state'].isin(state_selection)) & (pd_df_rfm['city'].isin(city_selection)) & (pd_df_rfm['gender'].isin(gender_selection)) & (pd_df_rfm['ageBin'].isin(agebin_selection)) & (pd_df_rfm['lifeStage'].isin(lifestage_selection)) & (pd_df_rfm['label'].isin(label_selection)),["customerid"]]
    
    customer_selection_list = customer_selection_pd["customerid"].unique().astype(str).tolist()
     

    pd_df_rfm = pd.merge(pd_df_rfm,customer_selection_pd, on='customerid')
    pd_df_rfm = pd_df_rfm[['customerid','firstName', 'lastName', 'gender', 'city', 'state', 'lastPurchaseDate','recency', 'frequency','monetary','lifeStage','label','incomeInDollars']]


    # For keeping some space between upper pannel and "lifestage_clv_nps" container.
    emp_space = st.container()
    with lifestage_clv_nps:
        col1, col2, col3 = st.columns([1.6, 1.2, 1.2])

        with col1:
                # st.subheader("Count of customers by Label and Lifestage")
                # Putting the menu in this columns 
            st.markdown("""
                <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>CUSTOMER INSIGHTS</b></p>
                
                """, True)


            selected = option_menu(
                menu_title = None,
                options = ['Life Stage', 'CLV', 'NPS'],
                default_index = 0,
                icons=None,
                menu_icon=None,
                orientation='horizontal',
                styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                # "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "12px", "text-align": "center", "margin":"0px", "--hover-color": "#118dff"},
                "nav-link-selected": {"background-color": "#118dff"},
                }
                )

            

            if selected == "Life Stage":
                df_rfm_clv = pd.merge(pd_df_rfm,pd_df_clv, on='customerid')
                df_rfm_clv = df_rfm_clv[['customerid','lifeStage','label','CLVbins', 'lastName', 'gender', 'city', 'state', 'lastPurchaseDate', 'recency_x', 'frequency_x', 'monetary','1YearCLV',]]
                
                # Latest Agg table matching with PBI.
                pd_df_rfm_agg_lifestage = pd_df_rfm.groupby(['lifeStage','label'], as_index=False)['customerid'].count()
                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.pivot(index='lifeStage', columns='label', values='customerid',)
                pd_df_rfm_agg_lifestage['Gold'] = pd_df_rfm_agg_lifestage.get('Gold', 0)
                pd_df_rfm_agg_lifestage['Silver'] = pd_df_rfm_agg_lifestage.get('Silver', 0)
                pd_df_rfm_agg_lifestage['Bronze'] = pd_df_rfm_agg_lifestage .get('Bronze', 0)

                pd_df_rfm_agg_lifestage['Gold'].fillna(0,inplace=True)
                pd_df_rfm_agg_lifestage['Silver'].fillna(0,inplace=True)
                pd_df_rfm_agg_lifestage['Bronze'].fillna(0,inplace=True)

                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.reset_index()

                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage[['lifeStage','Gold','Silver','Bronze']]

                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.fillna(0)
                pd_df_rfm_agg_lifestage['A'] = pd_df_rfm_agg_lifestage['Gold']
                pd_df_rfm_agg_lifestage['B'] = pd_df_rfm_agg_lifestage['Silver']
                pd_df_rfm_agg_lifestage['C'] = pd_df_rfm_agg_lifestage['Bronze']

                pd_df_rfm_agg_lifestage[list("ABC")] = pd_df_rfm_agg_lifestage[list("ABC")].astype(int)
                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.drop(columns=['Gold', 'Silver','Bronze'])

                pd_df_rfm_agg_lifestage['Gold'] = pd_df_rfm_agg_lifestage['A']
                pd_df_rfm_agg_lifestage['Silver'] = pd_df_rfm_agg_lifestage['B']
                pd_df_rfm_agg_lifestage['Bronze'] = pd_df_rfm_agg_lifestage['C']
                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.drop(columns=['A', 'B','C'])


                # # Older version in which RFM and CLV were together.
                # pd_df_lifestage_agg = df_rfm_clv.groupby(['lifeStage','label'], as_index=False)['customerid'].count()
                # pd_df_lifestage_agg = pd_df_lifestage_agg.pivot(index='lifeStage', columns='label', values='customerid',)
                # pd_df_lifestage_agg['Gold'] = pd_df_lifestage_agg.get('Gold', 0)
                # pd_df_lifestage_agg['Silver'] = pd_df_lifestage_agg.get('Silver', 0)
                # pd_df_lifestage_agg['Bronze'] = pd_df_lifestage_agg.get('Bronze', 0)

                # pd_df_lifestage_agg['Gold'].fillna(0,inplace=True)
                # pd_df_lifestage_agg['Silver'].fillna(0,inplace=True)
                # pd_df_lifestage_agg['Bronze'].fillna(0,inplace=True)
                
                # pd_df_lifestage_agg = pd_df_lifestage_agg.reset_index()

                # # col1.dataframe(pd_df_lifestage_agg, width=400)
                # pd_df_lifestage_agg = pd_df_lifestage_agg[['lifeStage','Gold','Silver','Bronze']]

                # pd_df_lifestage_agg = pd_df_lifestage_agg.fillna(0)
                # pd_df_lifestage_agg['A'] = pd_df_lifestage_agg['Gold']
                # pd_df_lifestage_agg['B'] = pd_df_lifestage_agg['Silver']
                # pd_df_lifestage_agg['C'] = pd_df_lifestage_agg['Bronze']

                # pd_df_lifestage_agg[list("ABC")] = pd_df_lifestage_agg[list("ABC")].astype(int)
                # pd_df_lifestage_agg = pd_df_lifestage_agg.drop(columns=['Gold', 'Silver','Bronze'])

                # pd_df_lifestage_agg['Gold'] = pd_df_lifestage_agg['A']
                # pd_df_lifestage_agg['Silver'] = pd_df_lifestage_agg['B']
                # pd_df_lifestage_agg['Bronze'] = pd_df_lifestage_agg['C']
                # pd_df_lifestage_agg = pd_df_lifestage_agg.drop(columns=['A', 'B','C'])

                # st.write(pd_df_lifestage_agg)

                colors = n_colors('rgb(255, 255, 255)', 'rgb(0, 131, 191)', 2060, colortype='rgb')
                a = np.array(pd_df_rfm_agg_lifestage.Gold)
                b = np.array(pd_df_rfm_agg_lifestage.Silver)
                c = np.array(pd_df_rfm_agg_lifestage.Bronze)
                
                def set_index(row):
                    if row["lifeStage"] == "Active Customer":
                        return 2
                    elif row["lifeStage"] == "Lapsed Customer":
                        return 3
                    elif row["lifeStage"] == "Lost Customer":
                        return 4
                    else:
                        return 1

                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.assign(index=pd_df_rfm_agg_lifestage.apply(set_index, axis=1))
                pd_df_rfm_agg_lifestage = pd_df_rfm_agg_lifestage.sort_values(by=['index'])

                # fig = go.Figure(data=pd_df_lifestage_agg)
                fig = go.Figure(data=[go.Table(
                columnwidth=[5,3,3,3],    
                header=dict(values=["<b>Life Stage</b>", "<b>Gold</b>", "<b>Silver</b>", "<b>Bronze</b>"],
                            fill_color='#ffffff',
                            align=['left','right'],
                            line_color='gray',
                            height=30),
                cells=dict(values=[pd_df_rfm_agg_lifestage.lifeStage,pd_df_rfm_agg_lifestage.Gold, pd_df_rfm_agg_lifestage.Silver, pd_df_rfm_agg_lifestage.Bronze],
                        fill = dict(color = ['white', np.array(colors)[a],np.array(colors)[b], np.array(colors)[c]]),
                        align=['left','right'],
                        line_color='gray',
                        height=30))
                ])

                fig.update_layout(margin=dict(l=5,r=0,b=0,t=10),font_size=14, width=500, height=250, paper_bgcolor="#ffffff")

                # st.write(pd_df_rfm_agg_lifestage)
                
                st.write(fig)
            
            if selected == "CLV":
                df_rfm_clv = pd.merge(pd_df_rfm,pd_df_clv, on='customerid')
                df_rfm_clv = df_rfm_clv[['customerid','lifeStage','label','CLVbins', 'lastName', 'gender', 'city', 'state', 'lastPurchaseDate', 'recency_x', 'frequency_x', 'monetary','1YearCLV',]]

                df = df_rfm_clv.groupby(['CLVbins','label'], as_index=False)['customerid'].count()
                df = df.pivot(index='CLVbins', columns='label', values='customerid',)
                df['Gold'] = df.get('Gold', 0)
                df['Silver'] = df.get('Silver', 0)
                df['Bronze'] = df.get('Bronze', 0) 
                
                df['Gold'].fillna(0,inplace=True)
                df['Silver'].fillna(0,inplace=True)
                df['Bronze'].fillna(0,inplace=True)				
                
                df = df.reset_index() 
                df = df[['CLVbins','Gold','Silver','Bronze']]


                df = df.fillna(0)
                df['A'] = df['Gold']
                df['B'] = df['Silver']
                df['C'] = df['Bronze']
                df[list("ABC")] = df[list("ABC")].astype(int)
                df = df.drop(columns=['Gold', 'Silver','Bronze'])

                df['Gold'] = df['A']
                df['Silver'] = df['B']
                df['Bronze'] = df['C']
                df = df.drop(columns=['A', 'B','C'])

                colors = n_colors('rgb(255, 255, 255)', 'rgb(0, 131, 191)', 1800, colortype='rgb')
                a = np.array(df.Gold)
                b = np.array(df.Silver)
                c = np.array(df.Bronze)


                fig = go.Figure(data=[go.Table(
                        columnwidth=[5,3,3,3],    
                        header=dict(values=["<b>CLVbins</b>", "<b>Gold</b>", "<b>Silver</b>", "<b>Bronze</b>"],
                                    fill_color='#ffffff',
                                    align=['left','right'],
                                    line_color='gray',
                                    height=30),
                        cells=dict(values=[df.CLVbins,df.Gold, df.Silver, df.Bronze],
                                # fill_color='#ffffff',
                                fill = dict(color = ['white', np.array(colors)[a],np.array(colors)[b], np.array(colors)[c]]),
                                align=['left','right'],
                                line_color='gray',
                                height=30))
                        ])

                fig.update_layout(margin=dict(l=5,r=0,b=0,t=10),font_size=14, width=500, height=250, paper_bgcolor="#ffffff")

                st.write(fig)

            if selected == "NPS":

                df_rfm_nps_cust = pd.merge(pd_df_clv,pd_df_nps_cust, on='customerid')
                df_rfm_nps_cust = pd_df_nps_cust[['customerid','label','Overall_NPS_Result']]

                df = df_rfm_nps_cust.groupby(['Overall_NPS_Result','label'], as_index=False)['customerid'].count()
                # st.write(df)
                df = df.pivot(index='Overall_NPS_Result', columns='label', values='customerid',)
                df['Gold'] = df.get('Gold', 0)
                df['Silver'] = df.get('Silver', 0)
                df['Bronze'] = df.get('Bronze', 0) 
                
                df['Gold'].fillna(0,inplace=True)
                df['Silver'].fillna(0,inplace=True)
                df['Bronze'].fillna(0,inplace=True)					
                df = df.reset_index()
                df = df[['Overall_NPS_Result','Gold','Silver','Bronze']]

                df = df.fillna(0)
                df['A'] = df['Gold']
                df['B'] = df['Silver']
                df['C'] = df['Bronze']
                df[list("ABC")] = df[list("ABC")].astype(int)
                df = df.drop(columns=['Gold', 'Silver','Bronze'])

                df['Gold'] = df['A']
                df['Silver'] = df['B']
                df['Bronze'] = df['C']
                df = df.drop(columns=['A', 'B','C'])

                colors = n_colors('rgb(255, 255, 255)', 'rgb(0, 131, 191)', 4000, colortype='rgb')
                a = np.array(df.Gold)
                b = np.array(df.Silver)
                c = np.array(df.Bronze)

                fig = go.Figure(data=[go.Table(
                columnwidth=[5,3,3,3],    
                header=dict(values=["<b>Overall_NPS_Result</b>", "<b>Gold</b>", "<b>Silver</b>", "<b>Bronze</b>"],
                            fill_color='#ffffff',
                            line_color='gray',
                            align=['left','right'],
                            height=30),
                cells=dict(values=[df.Overall_NPS_Result,df.Gold, df.Silver, df.Bronze],
                        # fill_color='#ffffff',
                        fill = dict(color = ['white', np.array(colors)[a],np.array(colors)[b], np.array(colors)[c]]),
                        line_color='gray',
                        align=['left','right'],
                        height=30))
                ])
                fig.update_layout(margin=dict(l=5,r=0,b=0,t=10),font_size=14, width=500, height=250, paper_bgcolor="#ffffff")

                st.write(fig)
    
        with col2:
            st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>MONETARY VALUE</b></p>
				
				""", True)
            pie_df_label_monetary_sum = pd_df_rfm.groupby(['label'], as_index=False)['monetary'].sum()
            l_label = pie_df_label_monetary_sum.label.tolist()
            l_monetary =pie_df_label_monetary_sum.monetary.tolist()  
            pie_df_label_count = pd_df_rfm.groupby(['label'], as_index=False)[['customerid']].count()
            #pie_df_label_count
            l_label2 = pie_df_label_count.label.tolist()
            l_customer2 = pie_df_label_count.customerid.tolist()
            l_monetary = [(item / 1000000) for item in l_monetary]
            l_monetary = [round(item, 2) for item in l_monetary]
            # l_monetary = [str(x) + " M" for x in l_monetary]
            # l_monetary = [str(s) + 'M' for s in l_monetary]   
            # st.write(l_monetary)

            # def human_format(num):
            #     # set decimal default options!
            #     getcontext().prec = 1
            #     getcontext().rounding = ROUND_DOWN
            #     _num = Decimal(num)
            #     num = float(f'{_num:.3g}')
            #     magnitude = 0
            #     while abs(num) >= 1000:
            #         magnitude += 1
            #         num /= 1000.0
            #     num = int(num * 10) / 10
            #     return f"{f'{num:f}'.rstrip('0').rstrip('.')}{['', 'k', 'M', 'B', 'T'][magnitude]}" 
            # l_monetary_1=[]
            # for  i in range(0,len(l_monetary)):
            #     l_monetary_1.append('%s'% human_format(l_monetary[i]))
            

            data2 = [# Portfolio (inner donut)
                    go.Pie(values=l_customer2, 
                    labels=l_label2,
                    domain={'x':[0.3,0.7], 'y':[0.1,0.9]},
                    textinfo='value',
                    hole=0,
                    direction='clockwise',
                    sort=False,
                    marker={'colors':['#EE7621','#FFEC8B','#BCC6CC']}),
                    # Individual components (outer donut)
                    go.Pie(values=l_monetary,
                    labels=l_label,
                    domain={'x':[0.1,0.9], 'y':[0,1]},
                    texttemplate =  "%{value:$} Mn <br>(%{percent})",
                    textposition='outside',
                    # textinfo='value+percent',
                    hole=0.65,
                    direction='clockwise',
                    sort=False,
                    showlegend=False)]

            fig = go.Figure(data=data2)
            fig.update_layout(
                            autosize=False,
                            width=385,
                            height=260,
                            margin=dict(
                                l=10,
                                r=10,
                                b=10,
                                t=10,
                                pad=4
                            ), paper_bgcolor="#ffffff"
            )


            st.write(fig)

        with col3:
            st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>CLV VALUE</b></p>
				
				""", True)
            df_rfm_clv2 = pd.merge(pd_df_rfm,pd_df_clv, on='customerid')
            df_rfm_clv2 = df_rfm_clv2[['customerid','lifeStage','label','CLVbins', 'firstName','lastName', 'gender', 'city', 'state', 'lastPurchaseDate', 'recency_x', 'frequency_x', 'monetary','1YearCLV',]]
            
            df_rfm_clv21 = df_rfm_clv2.groupby(['label'], as_index=False)['1YearCLV'].sum()
            df_rfm_clv21['PERCENT'] = ((df_rfm_clv21['1YearCLV'] / df_rfm_clv21['1YearCLV'].sum()) * 100)
            df_rfm_clv21['1YearCLV'] = df_rfm_clv21['1YearCLV'].round(decimals = 2) 
            l_label3 = df_rfm_clv21.label.tolist()
            l_1YearCLV3 = df_rfm_clv21.PERCENT.tolist()
            clv_list = df_rfm_clv21['1YearCLV'].tolist()
            clv_list = [(item / 1000000) for item in clv_list]
            clv_list = [round(item, 2) for item in clv_list]
            # st.write(clv_list)

            data3 = [# Portfolio (inner donut)
                    go.Pie(values=l_customer2,
                    labels=l_label2,
                    domain={'x':[0.3,0.7], 'y':[0.1,0.9]},
                    textinfo='value',
                    hole=0,
                    direction='clockwise',
                    sort=False,
                    marker={'colors':['#EE7621','#FFEC8B','#BCC6CC']}),
                    # Individual components (outer donut)
                    go.Pie(values=clv_list,
                    labels=l_label3,
                    domain={'x':[0.1,0.9], 'y':[0,1]},
                    texttemplate =  "%{value:$} Mn <br>(%{percent})",
                    textposition='outside',
                    # textinfo='value+percent',
                    # texttemplate = "%{value:$,~s} <br>(%{percent})",
                    hole=0.65,
                    direction='clockwise',
                    sort=False,
                    showlegend=False)]

            fig2 = go.Figure(data=data3)
            fig2.update_layout(
                        autosize=False,
                        width=385,
                        height=260,
                        margin=dict(
                            l=10,
                            r=10,
                            b=10,
                            t=10,
                            pad=4
                        ), paper_bgcolor="#ffffff"
            )
            st.write(fig2)

    
  

    with dataset:
        

    

        st.markdown("""<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;">
                    <b>CUSTOMER LIST</b></p>""", True)

        
        df_rfm_clv2.rename(columns = {'recency_x':'recency', 'frequency_x':'frequency'}, inplace = True)

        pd_df_rfm = pd.merge(df_rfm_clv2, pd_df_nps_cust, on='customerid')
        pd_df_rfm = pd_df_rfm[['customerid','firstName_x', 'lastName_x', 'gender_x', 'city_x', 'state_x', 'lifeStage','label_x', 'lastPurchaseDate_x', 'recency_x', 'frequency_x', 'monetary_x','1YearCLV','avgRating','Overall_NPS_Result']]
            
        pd_df_rfm['1YearCLV'] = pd_df_rfm['1YearCLV'].round(decimals = 2)
        pd_df_rfm['lastPurchaseDate_x'] = pd_df_rfm['lastPurchaseDate_x'].dt.strftime("%m/%d/%Y")
        pd_df_rfm['monetary_x'] = '$'+pd_df_rfm['monetary_x'].astype(str)
        pd_df_rfm['1YearCLV']=pd_df_rfm['1YearCLV'].round(decimals = 2)
        pd_df_rfm['1YearCLV'] = '$'+pd_df_rfm['1YearCLV'].astype(str)
            
        pd_df_rfm.rename(columns = {'customerid':'Customer Id', 'firstName_x':'First Name', 'lastName_x':'Last Name', 'gender_x':'Gender', 'city_x':'City', 'state_x':'State', 'lifeStage':'Life Stage','label_x':'Label', 'lastPurchaseDate_x':'Last Purchase Date', 'recency_x':'Recency', 'frequency_x':'Frequency', 'monetary_x':'Income', '1YearCLV':'1YearCLV', 'avgRating':'Avg Rating'}, inplace = True)

        gb = GridOptionsBuilder.from_dataframe(pd_df_rfm)
# 	gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)
        # gb.configure_column("LIFESTAGE", cellStyle=cellsytle_jscode)
        gb.configure_selection(selection_mode="select", use_checkbox=True)

        gridOptions = gb.build()

        custom_css={".ag-header-cell-text": {"color": "#ffffff !important;"},".ag-header": {"background-color": "#00568D !important;"}}

        data = AgGrid(
            pd_df_rfm,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,height=350, width='100%',
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            custom_css=custom_css)
        # st.markdown('div.ag-header{background-color: #000000;}', unsafe_allow_html=True)
        selected_rows = data["selected_rows"]
        
        selected_rows = pd.DataFrame(selected_rows)
        # selected_rows.reset_index(drop=True, inplace=True)
        # selected_rows.set_index('customerid')
        
        # st.write(selected_rows)
        if len(selected_rows) != 0:
            selected_rows["customerid"]=selected_rows["Customer Id"]
            pd_df_recomm['customerid']=  pd_df_recomm['customerid'].astype(str).astype(int)
            pd_rfm_recommendation = pd.merge(selected_rows,pd_df_recomm, on='customerid')
            selected_rows =  pd.merge(selected_rows,pd_df_rfm, on='Customer Id')

            selected_rows_1 = selected_rows[["Life Stage_x", "Label_x", "Frequency_x", "Recency_x", "Income_x", "1YearCLV_x"]]
            selected_rows = selected_rows[["Customer Id", "First Name_x","Last Name_x", "Gender_x", "State_x", "City_x"]]
            selected_rows.rename(columns = {'First Name_x':'First Name','Last Name_x':'Last Name','Gender_x':'Gender','State_x':'State','City_x':'City'}, inplace = True)               
            selected_rows_1.rename(columns = {'Life Stage_x':'Life Stage','Label_x':'ABC Bin','Frequency_x':'Frequency','Recency_x':'Recency','Income_x':'Monetary Value','1YearCLV_x':'Predicted CLV'}, inplace = True)               
            selected_rows = selected_rows.transpose().reset_index().rename(columns={'index':'Variable'})
            selected_rows_1 = selected_rows_1.transpose().reset_index().rename(columns={'index':'Variable'})
            selected_rows[0]=selected_rows[0].astype(str)
            selected_rows_1[0]=selected_rows_1[0].astype(str)
            selected_rows.rename(columns = {0:'Value'}, inplace = True)
            selected_rows_1.rename(columns = {0:'Value'}, inplace = True)





            col1,col2,col3,col4 = st.columns(4)
        # row1 = st.container()
        # with row1:
            # col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                    <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:18px;"><b>CUSTOMER DETAILS</b></p>
                    """, True)
                fig11 = go.Figure(data=[go.Table(header=dict(fill_color='lightgrey'),cells=dict(values=[selected_rows.Variable,selected_rows.Value],fill_color = [['white','lightgrey']*10],align=['left'],font_size = 14,height=30))])
                fig11.update_layout(autosize=False,width=300,height=250,margin=dict(l=10,r=0,b=10,t=0,pad=4), paper_bgcolor="#ffffff"        )
                st.write(fig11)
            with col2:
                st.markdown("""
                <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:18px;"><b>CUSTOMER PERSONA</b></p>
                """, True)
                fig22 = go.Figure(data=[go.Table(header=dict(fill_color='lightgrey'),cells=dict(values=[selected_rows_1.Variable,selected_rows_1.Value],fill_color = [['white','lightgrey']*10],align=['left'],font_size = 14,height=30))])
                fig22.update_layout(autosize=False,width=300,height=250,margin=dict(l=10,r=0,b=10,t=0,pad=4), paper_bgcolor="#ffffff"        )
                st.write(fig22)                
            with col3:
                st.markdown("""
                <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:18px;"><b>TOP PURCHASED</b></p>
                """, True)
                fig15 = go.Figure(data=[go.Table(header=dict(fill_color='lightgrey'),cells=dict(values=[pd_rfm_recommendation.categoryPurchased],fill_color = [['white','lightgrey']*10],align=['left'],font_size = 14,height=30))])
                fig15.update_layout(autosize=False,width=300,height=250,margin=dict(l=10,r=0,b=10,t=0,pad=4), paper_bgcolor="#ffffff"        )
                st.write(fig15)    
            with col4:
                st.markdown("""
                <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:18px;"><b>TOP RECOMMENDED</b></p>
                """, True)
                fig25 = go.Figure(data=[go.Table(header=dict(fill_color='lightgrey'),cells=dict(values=[pd_rfm_recommendation.categoryRecommended],fill_color = [['white','lightgrey']*10],align=['left'],font_size = 14,height=30))])
                fig25.update_layout(autosize=False,width=300,height=250,margin=dict(l=10,r=0,b=10,t=0,pad=4), paper_bgcolor="#ffffff"        )
                st.write(fig25)   

        else:
            st.write("")   
  

