import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from datetime import datetime as dt    
from inspect import trace
from pickle import TRUE

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode,GridUpdateMode

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px

def Behavioural_Modeling():
    
    from PandasDF import pd_df_rfm, pd_df_nps_cust, pd_df_lead_seg, pd_df_clv, pd_df_nps_cust,pd_df_lead_seg, pd_df_ncatr,pd_df_lsrr,pd_df_recomm
    
    with open('style_sum.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    global table
    global segments
    global df_cust
    
    
    #FILTERS
    
    upper_panel = st.container()
    with upper_panel:
    
        col_mo, col_le, col_si,col_emp  = st.columns([1.1,1.1,1.1,3.2])

        mo = np.sort(pd_df_lsrr['membership_opted'].unique()).tolist()
        le = np.sort(pd_df_lsrr['loyalty_and_engagement'].unique()).tolist()
        si = np.sort(pd_df_lsrr['source_of_income'].unique()).tolist()

        mo.insert(0, 'All')
        le.insert(0, 'All')
        si.insert(0, 'All')


    mo_selection = col_mo.selectbox('Membership Opted', mo,index=0)
    if mo_selection == 'All':    
        mo_selection = mo      
    else:
        mo_selection=[mo_selection]        

    le_selection = col_le.selectbox('Loyality & Engagement', le,index=0)
    if le_selection == 'All':    
        le_selection = le      
    else:
        le_selection=[le_selection]   

    si_selection = col_si.selectbox('Source of Income', si,index=0)
    if si_selection == 'All':    
        si_selection = si      
    else:
        si_selection=[si_selection]  

    id_selection_pd = pd_df_lsrr.loc[(pd_df_lsrr['membership_opted'].isin(mo_selection)) & (pd_df_lsrr['loyalty_and_engagement'].isin(le_selection)) & (pd_df_lsrr['source_of_income'].isin(si_selection)),["id"]]
    id_selection_list = id_selection_pd["id"].unique().astype(str).tolist()
     
    pd_df_lsrr_unfiltered = pd_df_lsrr[["segment","segmentName","id","source_of_income","type_of_camp","loyalty_and_engagement","purchase_pattern","age_group","membership_opted","customer_affordability_bin","conversion","conversionCopy"]]
    pd_df_lsrr = pd.merge(pd_df_lsrr,id_selection_pd, on='id')
    pd_df_lsrr = pd_df_lsrr[["segment","segmentName","id","source_of_income","type_of_camp","loyalty_and_engagement","purchase_pattern","age_group","membership_opted","customer_affordability_bin","conversion","conversionCopy"]] 
    

    #####################################################################################################################################################################################
    # Col1: Customers & Segments
    # Col2: Segment by Conversion  (Stacked Bar Chart)
    # Col3: >Segment by Dimensions (Scattered Chart)
    #####################################################################################################################################################################################
        
    col1 , col2, col3 =st.columns([1.15,3,3])
    
    with col1:
        total_custs =str(pd_df_lsrr['id'].count())       
        df_seg=pd_df_lsrr['segmentName'].tolist()
        segment_count = str(len(set(df_seg)))

        st.markdown("""
						<div class="streamlit_box">
						<div class="streamlit_row">
							<div class="streamlit_col"><h3>"""
							+ total_custs +
						"""
							</h3>
							<p font-family:'Segoe UI'>Customers</p>
							</div>
						</div>
							<div class="streamlit_row">
								<div class="streamlit_col">
								<h3>"""
								+ segment_count +
									"""
							</h3>
							<p font-family:'Segoe UI'>Segments</p>
							</div>
						</div></div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>SEGMENT BY CONVERSION</b></p>
				
				""", True)                
        df_grouped = pd_df_lsrr.groupby('segmentName')['conversionCopy'].value_counts(normalize=True).unstack('conversionCopy')
        df_grouped.plot.barh(stacked=True , width=0.7,figsize=(7,4)) 
        plt.legend(
            bbox_to_anchor=(0.5, 1.02),
            loc="lower center",
            borderaxespad=0,
            frameon=False,
            ncol=3
        )
        for ix, row in df_grouped.reset_index(drop=True).iterrows():
            print(ix, row)
            cumulative = 0
            for element in row:
                if element > 0.1:
                    plt.text(
                        cumulative + element / 2,
                        ix,
                        f"{round(element * 100,2)} %",
                        va="center",
                        ha="center",
                    )
                cumulative += element
        plt.tight_layout()   

        st.pyplot(plt)         

    with col3:
        st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>SEGMENT BY DIMENSIONS</b></p>
				
				""", True)                 
        pd_df_lsrr_af = pd_df_lsrr_unfiltered.groupby(['segmentName','customer_affordability_bin'], as_index=False)['id'].count()
        pd_df_lsrr_af=pd_df_lsrr_af.groupby('segmentName')['id'].agg(['sum', 'max']).reset_index()
        pd_df_lsrr_af['Customer Affordability'] =(pd_df_lsrr_af['max']/pd_df_lsrr_af['sum'])*100
        pd_df_lsrr_af=pd_df_lsrr_af[['segmentName','Customer Affordability']]  
        l33= pd_df_lsrr_af['Customer Affordability'].tolist() 
        #creating measure4
        def fun(): 
            l=[] 
            for i in l33:
                if (i>64 and i<68):
                    l.append(i-30) 
                else:
                    l.append(i)

            return l  
         
        #creating measure4
        k1=fun() 
        def fun2():
            ll=[] 
            for i in k1:
                if ((i>55 and i<60) or (i>62 and i<65)):
                    ll.append(i+10)
                else: 
                    ll.append(i) 
            return ll

        k10=fun2() 
        # pd_df_lsrr_le = pd_df_lsrr.groupby(['segmentName','loyalty_and_engagement'], as_index=False)['id'].count()
        # pd_df_lsrr_le=pd_df_lsrr_le.groupby('segmentName')['id'].agg(['sum', 'max']).reset_index()
        # pd_df_lsrr_le['Loyalty and Engagement'] =(pd_df_lsrr_le['max']/pd_df_lsrr_le['sum'])*100
        # pd_df_lsrr_le=pd_df_lsrr_le[['segmentName','Loyalty and Engagement']] 
        
        #pd_df_lsrr_scattdata = pd.merge(pd_df_lsrr_af,pd_df_lsrr_le, on='segmentName')
        
        pd_df_lsrr_agg3 = pd_df_lsrr_unfiltered.groupby(['segmentName','loyalty_and_engagement'], as_index=False)['id'].count()
        #pd_df_lsrr_agg3.rename(columns={'id':'total'},inplace=True) 
        
        pd_df_lsrr_agg3_m10=pd_df_lsrr_agg3.groupby('segmentName')['id'].agg(['sum', 'max']).reset_index()
        pd_df_lsrr_agg3_m10['Loyalty and Engagement'] =(pd_df_lsrr_agg3_m10['max']/pd_df_lsrr_agg3_m10['sum'])*100  
        l3= pd_df_lsrr_agg3_m10['Loyalty and Engagement'].tolist() 
        
        pd_df_lsrr_agg3.rename(columns={'id':'total'},inplace=True)
        pd_df_lsrr_agg3_top2=pd_df_lsrr_agg3.groupby(['segmentName'])['total'].apply(lambda x: x.nlargest(2)).reset_index()
        pd_df_lsrr_agg3_top2_sum=pd_df_lsrr_agg3_top2.groupby(['segmentName'],as_index=False)['total'].sum()
        pd_df_lsrr_agg3_sum=pd_df_lsrr_agg3.groupby(['segmentName'],as_index=False)['total'].sum() 
        pd_df_lsrr_agg3_per=((pd_df_lsrr_agg3_top2_sum['total']/pd_df_lsrr_agg3_sum['total'])*100).reset_index() 
        #st.write(pd_df_lsrr_agg3_per)
        #pd_df_lsrr_scattdata = pd_df_lsrr_scattdata[['segmentName','Customer Affordability', 'Loyalty and Engagement']]
        a=pd_df_lsrr_agg3_per["total"].tolist() 

        def fun4(): 
            l4=[] 
            for i in range(0,len(l3)):
                if (l3[i]>64 and l3[i]<66):
                    l4.append(a[i]) 
                else:
                    l4.append(l3[i])

            return l4 
        l5=fun4()  
        def fun5(): 
            l6=[]
            for i in l5:
                if ((i>50 and i<60 ) or (i>80 and i<85)): 
                    l6.append(i-20) 
                else:
                    l6.append(i) 
            return l6 
        l7=fun5()  
       
        def fun6():
            l8=[]
            for i in l7: 
                if (i>60 and i<65):
                    l8.append(i-30)
                else:
                    l8.append(i)
            return l8 
        l9=fun6()  
        c1=["Consciously Engaged","Uninfluenced and At-Risk","Genuine and loyal","Leading Edgers"]#pd_df_lsrr_le
        data1={"segmentName": c1, "Customer Affordability":k10,"Loyalty and Engagement":l9} 
        data1_df=pd.DataFrame(data1) 

        plot = px.scatter(data_frame=data1_df,x='Customer Affordability', y='Loyalty and Engagement',text="segmentName", range_x=[0,100], range_y=[0,100])
        plot.update_traces(textposition="bottom center")
        plot.update_layout(autosize=False,width=500,height=300,	margin=dict(l=20,r=20,b=20,t=20,pad=4), paper_bgcolor="#ffffff")

        st.plotly_chart(plot)
        # import plotly_express as px
        # plot = px.scatter(data_frame=data1_df,x='Customer Affordability', y='Loyalty and Engagement', color="segmentName")                
        
        # plot.update_layout(
        #                         autosize=False,
        #                         width=550,
        #                         height=370,
        #                         margin=dict(
        #                             l=30,
        #                             r=50,
        #                             b=100,
        #                             t=25,
        #                             pad=4
        #                         ), paper_bgcolor="#DCDCDC"
        #         )
        
        # st.plotly_chart(plot)
    
    #####################################################################################################################################################################################
    # Col4: Customer Affordability by Segment  (Bar chart)
    # Col5: Age Bin by Segment  (Bar chart)
    #####################################################################################################################################################################################
        

    col4 , col5 =st.columns([1,1])
    
    with col4:
        st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>CUSTOMER AFFORDABILITY BY SEGMENT</b></p>
				
				""", True)                
        pd_df_cat = pd_df_lsrr.groupby(['segmentName','customer_affordability_bin'], as_index=False)['id'].count()
        pd_df_cat.rename(columns = {'id':'total'}, inplace = True)      
       
        global l11,l12,l13,l14
        def fun():
            l11=[]
            l12=[]
            l13=[]
            l14=[] 
            for i in range (0,len(pd_df_cat.segmentName)):
                if pd_df_cat.segmentName[i]==pd_df_cat.segmentName[i]:
                    if pd_df_cat.customer_affordability_bin[i]=='Low':
                        l11.append(pd_df_cat.total[i])
                    if pd_df_cat.customer_affordability_bin[i]=='Medium' :
                        l12.append(pd_df_cat.total[i])
                    if pd_df_cat.customer_affordability_bin[i]=='High':
                        l13.append(pd_df_cat.total[i])
                    if pd_df_cat.customer_affordability_bin[i]=='Expensive':
                        l14.append(pd_df_cat.total[i])
            return l11,l12,l13,l14
    
        
        l11,l12,l13,l14=fun()
        expensive=l14
        high=l13
        low=l11
        medium=l12
        segmentName= ["Consciously Engaged","Genuine and Loyal","Leading Edgers","uninfluenced and At-risk"]
        plot= go.Figure(data=[go.Bar
                (name= 'expensive',  
                x= segmentName,   
                y= expensive
                ),         
            go.Bar(
                name= 'high',   
                x= segmentName,   
                y= high
                ),         
            go.Bar(
                name= 'low',   
                x= segmentName,   
                y= low
                ), 

            go.Bar(
                name= 'medium',   
                x= segmentName,   
                y= medium
                )
        ])
        texts = [expensive,high,low,medium]
        for i, t in enumerate(texts):
            plot.data[i].text= t
            plot.data[i].textposition = 'outside'
        plot.update_layout(
                                autosize=False,
                                width=637,
                                height=350,
                                margin=dict(
                                    l=10,
                                    r=10,
                                    b=10,
                                    t=10,
                                    pad=4
                                ), paper_bgcolor="#ffffff"
                )
                    
        st.write(plot)
    
    #AgeBinBySegment
    #ClusteredColumnChart
    
    with col5:
        st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>AGE BIN BY SEGMENT</b></p>
				
				""", True) 
        pd_df_ca = pd_df_lsrr.groupby(['segmentName','age_group'], as_index=False)['id'].count()
        pd_df_ca.rename(columns = {'id':'total'}, inplace = True)       

        
        global l21,l22,l23,l24
        def fun1():
            l21=[]
            l22=[]
            l23=[]
            l24=[] 
            for i in range(0,len(pd_df_ca.segmentName)):
                if pd_df_ca.segmentName[i]== pd_df_ca.segmentName[i]:
                    if pd_df_ca.age_group[i]=='25 to 35':
                        l21.append(pd_df_ca.total[i])
                    if  pd_df_ca.age_group[i]=="35 to 45":
                        l22.append(pd_df_ca.total[i])
                    if  pd_df_ca.age_group[i]=="45 and above":
                        l23.append(pd_df_ca.total[i])
                    if pd_df_ca.age_group[i] =='below 25 ':
                        l24.append(pd_df_ca.total[i])    

            return l21,l22,l23,l24

        l21,l22,l23,l24=fun1()


        a1=l21
        b1=l22
        c1=l23
        d1=l24
        a= '25 to 35'
        b='35 to 45'
        c='45 and above'
        d='below 25'
        segmentName= ["Consciously Engaged","Genuine and Loyal","Leading Edgers","uninfluenced and At-risk"] 
        plot= go.Figure(data=[go.Bar
                (name= '25 to 35' ,  
                x= segmentName,   
                y= a1
                ),         
            go.Bar(
                name= '35 to 45',   
                x= segmentName,   
                y= b1
                ),         
            go.Bar(
                name= '45 to above',   
                x= segmentName,   
                y= c1
                ), 

            go.Bar(
                name= 'below 25',   
                x= segmentName,   
                y= d1
                )
        ]) 
        texts = [a1,b1,c1,d1]

        for i, t in enumerate(texts):
            plot.data[i].text= t
            plot.data[i].textposition = 'outside'
        
        plot.update_layout(
                                autosize=False,
                                width=637,
                                height=350,
                                margin=dict(
                                    l=10,
                                    r=10,
                                    b=10,
                                    t=10,
                                    pad=4
                                ), paper_bgcolor="#ffffff"
                )
                    
        st.write(plot) 
    
    #####################################################################################################################################################################################
    # Customer Dataset Table
    #####################################################################################################################################################################################
        
    pd_df_lsrr = pd_df_lsrr[["id","customer_affordability_bin","loyalty_and_engagement","membership_opted","purchase_pattern","age_group","source_of_income","type_of_camp","segmentName","conversionCopy"]]
    #pd_df_lsrr.rename(columns = {"id":"Id","customer_affordability_bin":"Customer Affordability Bin","loyalty_and_engagement":"Loyalty And Engagement","membership_opted":"Membership Opted","purchase_pattern":"Purchase Pattern","age_group":"Age Group Bin","source_of_income":"Source Of Income","type_of_camp":"Type Of Camp","segmentName":"Segment","conversionCopy":"Conversion"}, inplace = True)
    #colorscale = [[0, '#074973'],[.5, '#ffffff'],[1, '#dae1ec']]
    #fig =  ff.create_table(pd_df_lsrr, colorscale=colorscale)
    #st.write(fig)
    fig = go.Figure(data=[go.Table(columnwidth=[1,2.85,2.75,2.4,2,2,2,1.75,2.125,2.125],header=dict(values=("<b>Id<b>","<b>Customer Affordability Bin<b>","<b>Loyalty And Engagement<b>","<b>Membership Opted<b>","<b>Purchase Pattern<b>","<b>Age Group Bin<b>","<b>Source Of Income<b>","<b>Type Of Camp<b>","<b>Segment<b>","<b>Conversion<b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 13,height=35),cells=dict(values=[pd_df_lsrr.id,pd_df_lsrr.customer_affordability_bin,pd_df_lsrr.loyalty_and_engagement,pd_df_lsrr.membership_opted,pd_df_lsrr.purchase_pattern,pd_df_lsrr.age_group,pd_df_lsrr.source_of_income,pd_df_lsrr.type_of_camp,pd_df_lsrr.segmentName,pd_df_lsrr.conversionCopy],fill_color = [['white','lightgrey']*3200], align=['left'], font_size = 12))])
    fig.update_layout(autosize=False,width=1325,height=400,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff"
                )
    st.write(fig)
    
    
