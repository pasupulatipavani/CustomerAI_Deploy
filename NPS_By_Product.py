from inspect import trace
import pandas as pd
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
#import plotly.graph_objects as px
import common as com


def NPS_By_Product():
    
    from PandasDF import pd_df_rfm, pd_df_nps_cust, pd_df_lead_seg, pd_df_clv, pd_df_nps_cust,pd_df_lead_seg, pd_df_ncatr,pd_df_lsrr,pd_df_recomm
    
    pd_df_ncatr = pd.merge(pd_df_ncatr,pd_df_nps_cust, on='customerid')
    pd_df_ncatr = pd_df_ncatr[["id_x","category","promote_x","passivelySatisfied_x","detract_x","totalNoOfReviews_x","avgRating_x","surveyMonth","surveyDateOrder","NPS_Score_by_Category","customerid","Detractor","Passive","Promoter","100pct","label","city","state","gender","ageBin"]]
    pd_df_ncatr.rename(columns = {'id_x':'id', 'promote_x':'promote', 'passivelySatisfied_x':'passivelySatisfied', 'detract_x':'detract', 'totalNoOfReviews_x':'totalNoOfReviews', 'avgRating_x':'avgRating'}, inplace = True)    
    
    #FILTERS
    with open('style_sum.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    upper_panel = st.container()
    with upper_panel:
    
        col_state, col_city, col_gender, col_agebin, col_label,col_category,col_emp= st.columns([2,2,2,2,2,2,3])
    
        state = np.sort(pd_df_ncatr['state'].unique()).tolist()
        gender = np.sort(pd_df_ncatr['gender'].unique()).tolist()
        agebin = np.sort(pd_df_ncatr['ageBin'].unique()).tolist()
        label = np.sort(pd_df_ncatr['label'].unique()).tolist()
        category = np.sort(pd_df_ncatr['category'].unique()).tolist()

        state.insert(0, 'All')
        gender.insert(0, 'All')
        agebin.insert(0, 'All')
        label.insert(0, 'All')
        category.insert(0, 'All')

    state_selection = col_state.selectbox('State', state,index=0)
    if state_selection == 'All':    
        state_selection = state
        #Created a Dependency City Filter in the bottom
        city = np.sort(pd_df_ncatr['city'].unique()).tolist()  
        city.insert(0, 'All')  

    else:
        #state_selection.append('Dummy')
        state_selection=[state_selection]
        pd_df_ncatr_city= pd_df_ncatr.loc[(pd_df_ncatr["state"].isin(state_selection)),['city']]
        city=np.sort(pd_df_ncatr_city['city'].unique()).tolist()
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

    label_selection = col_label.selectbox('Monetary Bin', label,index=0)
    if label_selection == 'All':    
        label_selection = label
    else:
        #label_selection.append('Dummy') 
        label_selection=[label_selection]

    category_selection = col_category.selectbox('Product Category', category,index=0)
    if category_selection == 'All':    
        category_selection = category
    else:
        #category_selection.append('Dummy')
        category_selection=[category_selection]

    ID_selection_pd = pd_df_ncatr.loc[(pd_df_ncatr['state'].isin(state_selection)) & (pd_df_ncatr['city'].isin(city_selection)) & (pd_df_ncatr['gender'].isin(gender_selection)) & (pd_df_ncatr['ageBin'].isin(agebin_selection)) & (pd_df_ncatr['label'].isin(label_selection)) & (pd_df_ncatr['category'].isin(category_selection)),["id"]]
    ID_selection_list = ID_selection_pd["id"].unique().astype(str).tolist()

    pd_df_ncatr = pd.merge(pd_df_ncatr,ID_selection_pd, on='id')
    pd_df_ncatr = pd_df_ncatr[["id","category","promote","passivelySatisfied","detract","totalNoOfReviews","avgRating","surveyMonth","surveyDateOrder","NPS_Score_by_Category","customerid","Detractor","Passive","Promoter","100pct","label","city","state","gender","ageBin"]]


    #####################################################################################################################################################################################
    # NPS Trend Analysis
    #####################################################################################################################################################################################

    col_nps_trend_analysis, col_nps_trend_analysis_blank = st.columns([1, 0.0000001])
    with col_nps_trend_analysis:
        com.set_header("NPS TREND ANALYSIS")

        pd_df_ncalc=pd_df_ncatr.groupby(['surveyDateOrder','surveyMonth']) \
        .apply(lambda x: pd.Series({
            'Detractor_sum'       : x['Detractor'].sum(),
            'Detractor_count'       : x['Detractor'].count(),
            'Promoter_sum'       : x['Promoter'].sum(),
            'Promoter_count'       : x['Promoter'].count(),
            'Passive_sum'       : x['Passive'].sum(),
            'Passive_count'       : x['Passive'].count(),
            'NPS_Score_by_Category_sum'       : x['NPS_Score_by_Category'].sum(),
            'NPS_Score_by_Category_count'       : x['NPS_Score_by_Category'].count(),
        })
        )
        pd_df_ncalc['Detractor']=pd_df_ncalc['Detractor_sum']/pd_df_ncalc['Detractor_count']
        pd_df_ncalc['Promoter']=pd_df_ncalc['Promoter_sum']/pd_df_ncalc['Promoter_count']
        pd_df_ncalc['Passive']=pd_df_ncalc['Passive_sum']/pd_df_ncalc['Passive_count']
        pd_df_ncalc['NPS_Score']=pd_df_ncalc['NPS_Score_by_Category_sum']/pd_df_ncalc['NPS_Score_by_Category_count']
        #pd_df_ncalc.columns = pd_df_ncalc.columns.get_level_values(0)
        #pd_df_ncalc.columns = [' '.join(col).strip() for col in pd_df_ncalc.columns.values]
        pd_df_ncalc=pd_df_ncalc.reset_index(1)
        pd_df_ncalc.columns = pd_df_ncalc.columns.to_flat_index()
        pd_df_ncalc=pd_df_ncalc[['surveyMonth','Detractor','Promoter','Passive','NPS_Score']].round({'Detractor': 2, 'Promoter': 2, 'Passive': 2, 'NPS_Score': 2})
        l_surveyMonth = pd_df_ncalc.surveyMonth.tolist()
        l_detractor=pd_df_ncalc.Detractor.tolist()
        l_promoter=pd_df_ncalc.Promoter.tolist()
        l_passive=pd_df_ncalc.Passive.tolist()
        l_NPS_Score=pd_df_ncalc.NPS_Score.tolist()

        colors = {'A': '#E01F27',
                'B': '#FFBB00',
                'C':"#0CC368"}


        data=[
                    go.Bar(name='Promoters', x=l_surveyMonth, y=l_promoter,text=l_promoter,textposition='inside',marker={'color':colors['C']}),
                    go.Bar(name='Passives', x=l_surveyMonth, y=l_passive,text=l_passive,textposition='inside',marker={'color':colors['B']}),
                    go.Bar(name='Detractors', x=l_surveyMonth, y=l_detractor,text=l_detractor,textposition='inside',marker={'color':colors['A']}),
                    go.Line(name='NPS Score', x=l_surveyMonth, y=l_NPS_Score,line_width=2,line_color='#000000', yaxis='y2')
                ]

        min1 = min(l_NPS_Score)-min(l_NPS_Score)*0.30
        max1 = max(l_NPS_Score)*1.30
        # Add titles and color the font of the titles to match that of the traces
        # 'SteelBlue' and 'DarkOrange' are the defaults of the first two colors.
        y1 = go.YAxis(title='Promoters Passives and Detractors', titlefont=go.Font(color='Black'))
        y2 = go.YAxis(title= 'NPS Score', titlefont=go.Font(color='Black'),range=[min1,max1])
        x = go.XAxis(title= 'Survey Month', titlefont=go.Font(color='Black'))

        # update second y axis to be position appropriately
        y2.update(overlaying='y', side='right')

        # Add the pre-defined formatting for both y axes
        layout = go.Layout(xaxis=x, yaxis1 = y1, yaxis2 = y2)

        fig = go.Figure(data=data, layout=layout)

        fig.update_layout(barmode='stack',autosize=True,width=1300,height=500,margin=dict(l=10,r=10,b=10,t=10,pad=4), paper_bgcolor="#ffffff")
        st.write(fig)

    #####################################################################################################################################################################################
    # Survey Trend By Product Category
    #####################################################################################################################################################################################

    col_survey_trend, col_survey_trend_blank = st.columns([1, 0.0000001])
    with col_survey_trend:
        com.set_header("SURVEY TREND BY PRODUCT CATEGORY")

        pd_df_ncalc1=pd_df_ncatr.groupby(['surveyDateOrder','surveyMonth']) \
        .apply(lambda x: pd.Series({
            'Detractor_sum'       : x['Detractor'].sum(),
            'Detractor_count'       : x['Detractor'].count(),
            'Promoter_sum'       : x['Promoter'].sum(),
            'Promoter_count'       : x['Promoter'].count(),
            'Passive_sum'       : x['Passive'].sum(),
            'Passive_count'       : x['Passive'].count(),
            'NPS_Score_by_Category_sum'       : x['NPS_Score_by_Category'].sum(),
            'NPS_Score_by_Category_count'       : x['NPS_Score_by_Category'].count(),
        })
        )
        pd_df_ncalc1['Detractor']=pd_df_ncalc1['Detractor_sum']/pd_df_ncalc1['Detractor_count']
        pd_df_ncalc1['Promoter']=pd_df_ncalc1['Promoter_sum']/pd_df_ncalc1['Promoter_count']
        pd_df_ncalc1['Passive']=pd_df_ncalc1['Passive_sum']/pd_df_ncalc1['Passive_count']
        pd_df_ncalc1['NPS_Score']=pd_df_ncalc1['NPS_Score_by_Category_sum']
        #pd_df_ncalc.columns = pd_df_ncalc.columns.get_level_values(0)
        #pd_df_ncalc.columns = [' '.join(col).strip() for col in pd_df_ncalc.columns.values]
        pd_df_ncalc1=pd_df_ncalc1.reset_index(1)
        pd_df_ncalc1.columns = pd_df_ncalc1.columns.to_flat_index()
        pd_df_ncalc1=pd_df_ncalc1[['surveyMonth','Detractor','Promoter','Passive','NPS_Score']].round({'Detractor': 2, 'Promoter': 2, 'Passive': 2, 'NPS_Score': 2})
        l_surveyMonth1 = pd_df_ncalc1.surveyMonth.tolist()
        l_detractor1=pd_df_ncalc1.Detractor.tolist()
        l_promoter1=pd_df_ncalc1.Promoter.tolist()
        l_passive1=pd_df_ncalc1.Passive.tolist()
        l_NPS_Score1=pd_df_ncalc1.NPS_Score.tolist()


        colors = {'A': '#E01F27',
                'B': '#FFBB00',
                'C':"#0CC368"}

        data=[
                    go.Bar(name='Promoters', x=l_surveyMonth1, y=l_promoter1,text=l_promoter1,textposition='inside',marker={'color':colors['C']}),
                    go.Bar(name='Passives', x=l_surveyMonth1, y=l_passive1,text=l_passive1,textposition='inside',marker={'color':colors['B']}),
                    go.Bar(name='Detractors', x=l_surveyMonth1, y=l_detractor1,text=l_detractor1,textposition='inside',marker={'color':colors['A']}),
                    go.Line(name='NPS Score', x=l_surveyMonth1, y=l_NPS_Score1,line_width=2,line_color='#000000', yaxis='y2')
                ]

        min1 = min(l_NPS_Score1)-min(l_NPS_Score1)*0.30
        max1 = max(l_NPS_Score1)*1.30
        # Add titles and color the font of the titles to match that of the traces
        # 'SteelBlue' and 'DarkOrange' are the defaults of the first two colors.
        y1 = go.YAxis(title='Promoters Passives and Detractors', titlefont=go.Font(color='Black'))
        y2 = go.YAxis(title= 'NPS Score', titlefont=go.Font(color='Black'),range=[min1,max1])
        x = go.XAxis(title= 'Survey Month', titlefont=go.Font(color='Black'))

        # update second y axis to be position appropriately
        y2.update(overlaying='y', side='right')

        # Add the pre-defined formatting for both y axes
        layout = go.Layout(xaxis=x, yaxis1 = y1, yaxis2 = y2)

        fig1 = go.Figure(data=data, layout=layout)

        fig1.update_layout(barmode='stack',autosize=True,width=1300,height=500,margin=dict(l=10,r=10,b=10,t=10,pad=4), paper_bgcolor="#ffffff")
        st.write(fig1)

    #####################################################################################################################################################################################
    # NPS By Product Category
    #####################################################################################################################################################################################

    col_nps_by_product_category, col_nps_by_product_category_blank = st.columns([1, 0.0000001])

    with col_nps_by_product_category:
        com.set_header("NPS BY PRODUCT CATEGORY")

        pd_df_ncalc2=pd_df_ncatr.groupby('category')['NPS_Score_by_Category'].agg(['sum', 'count']).reset_index()
        pd_df_ncalc2.rename(columns = {'category':'Category'}, inplace = True)
        pd_df_ncalc2['NPS Score']=pd_df_ncalc2['sum']/pd_df_ncalc2['count']
        pd_df_ncalc2=pd_df_ncalc2[['Category','NPS Score']].round({'NPS_Score': 2}).sort_values(by='NPS Score', ascending=False)

        fig4 = px.bar(pd_df_ncalc2, y='NPS Score', x='Category', text_auto='.2s')
        fig4.update_traces(textfont_size=20, textangle=0, textposition="inside",marker_color='#e66c37')
        # Add range slider
        fig4.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([dict(step="all")])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="category"
            )
        )
        fig4.update_layout(autosize=True,width=1300,height=600,margin=dict(l=10,r=10,b=10,t=10,pad=4), paper_bgcolor="#ffffff")
        st.plotly_chart(fig4)
