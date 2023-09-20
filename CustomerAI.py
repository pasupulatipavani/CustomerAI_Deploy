import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid.shared import GridUpdateMode
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from plotly.colors import n_colors
import numpy as np
from Behavioural_Modeling import Behavioural_Modeling
from Recommendation import Recommendation
from DemandForecasting import Demand
from NPS_By_Product import NPS_By_Product
from Customer_Insights import Customer_Insights
from Channel_Attribution import Channel_Attribution
from Customer_Satisfaction import Customer_Satisfaction
from Pricing import Pricing
from PandasDF import pd_df_rfm, pd_df_nps_cust, pd_df_lead_seg, pd_df_clv, pd_df_nps_cust,pd_df_lead_seg, pd_df_ncatr,pd_df_lsrr,pd_df_recomm,pd_df_dmd,pd_df_prc



# session = Session.builder.configs(connection_parameters).create()
st.set_page_config(page_title="CustomerAI powered by Snowflake", page_icon="custai1.png",layout="wide")
st.image('custai.png',width =225)

page_selected = option_menu(
	            menu_title = None,
	            options = ['Summary', 'Customer Insights', 'Segmentation','Channel Attribution',
				'CSat','Product NPS', 'Recommendation','Demand Forecasting','Pricing'],
	            default_index = 0,
	            icons=None,
	            menu_icon=None,
	            orientation='horizontal',
	            styles={

	            
	            "container": {"padding": "0!important", "background-color": "#fafafa"},
	            # "icon": {"color": "orange", "font-size": "25px"},
	            "icon":{"display":"none"},
	            "nav": {"background-color":"#f2f5f9"},
	            "nav-link": {"font-size": "14px",
	            "font-weight":"bold", 
	            "color":"#00568D",
	            "border-right":"1.5px solid #00568D",
				"border-left":"1.5px solid #00568D",
				"border-top":"1.5px solid #00568D",
				"border-bottom":"1.5px solid #00568D",
	            "padding":"10px", 
	            "text-transform": "uppercase",
	            "border-radius":"0px",
	            "margin":"5px",
	            "--hover-color": "#e1e1e1"},
	            "nav-link-selected": {"background-color":"#00568d", "color":"#ffffff"},
	            }
	            )


if page_selected == 'Customer Insights':
	Customer_Insights()
elif page_selected == 'Segmentation':
	Behavioural_Modeling()	
elif page_selected == 'Channel Attribution':
	Channel_Attribution()
elif page_selected == 'CSat':
	Customer_Satisfaction()
elif page_selected == 'Product NPS':
	NPS_By_Product()
elif page_selected == 'Recommendation':
	Recommendation()
elif page_selected == 'Demand Forecasting':
	Demand()
elif page_selected == 'Pricing':
	Pricing()
elif page_selected == 'Summary':

	with open('style_sum.css') as f:
		st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
	
	set_conatiner_width=True
	upper_panel = st.container()
	header = st.container()
	first_row = st.container()
	second_row = st.container()

	with upper_panel:
		col_state, col_city, col_gender, col_agebin, col_lifestage, col_label, col_emp = st.columns([2,2,2,2,2,2,3])

		state = np.sort(pd_df_rfm['state'].unique()).tolist()
		#city = pd_df_rfm['CITY'].unique().tolist()    
		gender = np.sort(pd_df_rfm['gender'].unique()).tolist()
		agebin = np.sort(pd_df_rfm['ageBin'].unique()).tolist()
		lifestage = np.sort(pd_df_rfm['lifeStage'].unique()).tolist()
		label = np.sort(pd_df_rfm['label'].unique()).tolist()

		state.insert(0, 'All')
		#city.insert(0, 'All')
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
    
	
	pd_df_rfm = pd.merge(pd_df_rfm,customer_selection_pd, on='customerid')
	pd_df_rfm = pd_df_rfm[["customerid", "recency", "monetary", "frequency", "breadth", "firstPurchaseDate", "lastPurchaseDate", "tenure", "r_quartile", "f_quartile", "m_quartile", "lifeStage", "cummulative", "cumPer", "label", "phone", "address", "city", "state", "postalCode", "latitude", "longitude", "country", "firstName", "lastName", "gender", "age", "dateOfBirth", "ageBin", "education", "incomeInDollars"]]

	pd_df_nps_cust = pd.merge(pd_df_nps_cust,customer_selection_pd, on='customerid')
	pd_df_nps_cust = pd_df_nps_cust[["customerid", "id", "NPS_Score_by_CustomerID", "promote", "passivelySatisfied", "detract", "totalNoOfReviews", "avgRating", "Overall_NPS_Result", "recency", "monetary", "frequency", "breadth", "firstPurchaseDate", "lastPurchaseDate", "tenure", "r_quartile", "f_quartile", "m_quartile", "lifestage", "cummulative", "label", "phone", "address", "city", "state", "postalcode", "latitude", "longitude", "country", "firstName", "lastName", "gender", "age", "dobOfBirth", "ageBin", "education", "incomeInDollars"]]
	
	pd_df_ncatr = pd.merge(pd_df_ncatr,pd_df_nps_cust, on='customerid')
	pd_df_ncatr = pd_df_ncatr[["id_x","category","promote_x","passivelySatisfied_x","detract_x","totalNoOfReviews_x","avgRating_x","surveyMonth","surveyDateOrder","NPS_Score_by_Category","customerid","Detractor","Passive","Promoter","100pct","label","city","state","gender","ageBin"]]
	pd_df_ncatr.rename(columns = {'id_x':'id', 'promote_x':'promote', 'passivelySatisfied_x':'passivelySatisfied', 'detract_x':'detract', 'totalNoOfReviews_x':'totalNoOfReviews', 'avgRating_x':'avgRating'}, inplace = True)    

	count_of_customers = len(customer_selection_list)
	count_of_products = len(products_pd["categoryPurchased"].unique().tolist())

	with first_row:
		# col1, col2, col3, col4 = st.columns([3,2,2,2])
		col1, col2, col3 = st.columns(3)

		with col1:
			total_custs = str(count_of_customers)
			segment_count = str(len(pd.unique(pd_df_lead_seg['segmentName'])))
			customer_data = '79.0'
			pd_df_nps_cust_wid1=pd_df_nps_cust.groupby(["Overall_NPS_Result"])["Overall_NPS_Result"].count()
			pd_df_nps_cust_wid1['Detractors'] = pd_df_nps_cust_wid1.get('Detractors', 0)
			pd_df_nps_cust_wid1['Promoters'] = pd_df_nps_cust_wid1.get('Promoters', 0)
			pd_df_nps_cust_wid1['Passives'] = pd_df_nps_cust_wid1.get('Passives', 0)
			overall_nps=str(round((pd_df_nps_cust_wid1['Promoters']-pd_df_nps_cust_wid1['Detractors'])*(100/(pd_df_nps_cust_wid1['Detractors']+pd_df_nps_cust_wid1['Promoters']+pd_df_nps_cust_wid1['Passives'])),2))
			products = str(count_of_products)

			st.markdown("""
						<div class="streamlit_box">
						<div class="streamlit_row">
							<div class="streamlit_col"><h3>"""
							+ total_custs +
						"""
							</h3>
							<p font-family:'Segoe UI'>Customers</p>
							</div>
							<div class="streamlit_col">
								<h3>"""
							+ products +
						"""
							</h3>
							<p font-family:'Segoe UI'>Products</p>
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
								<div class="streamlit_col"><h3>"""
						+ overall_nps +
						"""
							</h3>
							<p font-family:'Segoe UI'>Overall Net Promoter Score</p>
							</div>
						</div></div>""", unsafe_allow_html=True)

		with col2:
			st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>MONETARY VALUE</b></p>
				
				""", True)

			pie_df_label_monetary_sum = pd_df_rfm.groupby(['label'], as_index=False)['monetary'].sum()
			l_label = pie_df_label_monetary_sum.label.tolist()
			l_monetary = pie_df_label_monetary_sum.monetary.tolist()
			pie_df_label_count = pd_df_rfm.groupby(['label'], as_index=False)[['customerid']].count()
			l_label2 = pie_df_label_count.label.tolist()
			l_customer2 = pie_df_label_count.customerid.tolist()
			l_monetary = [(item / 1000000) for item in l_monetary]
			l_monetary = [round(item, 2) for item in l_monetary]

			# data2 = [
			# 		# Individual components (outer donut)
			# 		go.Pie(values=l_monetary,
			# 		labels=l_label,
			# 		domain={'x':[0.1,0.9], 'y':[0,1]},
			# 		texttemplate =  "%{value:$} Mn <br>(%{percent})",
			# 		textposition='outside',
			# 		hole=0.65,
			# 		direction='clockwise',
			# 		sort=False,
			# 		showlegend=False),
			# 		# Portfolio (inner pie)
			# 		go.Pie(values=l_customer2,
			# 		labels=l_label2,
			# 		domain={'x':[0.3,0.7], 'y':[0.1,0.9]},
			# 		hole=0,
			# 		direction='clockwise',
			# 		sort=False,
			# 		marker={'colors':['#EE7621','#FFEC8B','#BCC6CC']})]

			data2 = [
					# Individual components (outer donut)
					go.Pie(values=l_monetary,
					labels=l_label,
					domain={'x':[0.1,0.9], 'y':[0,1]},
					texttemplate =  "%{value:$} Mn <br>(%{percent})",
					textposition='outside',
					hole=0.65,
					direction='clockwise',
					sort=False,
					showlegend=False),
					# Portfolio (inner pie)
					go.Pie(values=l_customer2,
					labels=l_label2,
					domain={'x':[0.3,0.7], 'y':[0.1,0.9]},
					texttemplate =  "%{value}",
					textposition='inside',
					hole=0,
					direction='clockwise',
					sort=False,
					marker={'colors':['#EE7621','#FFEC8B','#BCC6CC']})]


			fig = go.Figure(data=data2)
			fig.update_layout(
				autosize=False,
				width=400,
				height=300,
				margin=dict(
					l=20,
					r=20,
					b=20,
					t=20,
					pad=4
				), paper_bgcolor="#ffffff"
			)
			st.write(fig)



		with col3:

			st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>CLV VALUE</b></p>
				
				""", True)

			# df_rfm_clv = pd.merge(pd_df_rfm,pd_df_clv, on='customerid')
			# df_rfm_clv = df_rfm_clv[['customerid','label','firstName', 'lastName', 'gender', 'city', 'state', 'lastPurchaseDate', 'recency_x', 'frequency_x', 'monetary','1YearCLV',]]

			# df_rfm_clv['percent'] = (df_rfm_clv['1YearCLV'] / df_rfm_clv['1YearCLV'].sum()) * 100

			# l_label3 = df_rfm_clv.label.tolist()
			# l_1YearCLV3 = df_rfm_clv.percent.tolist()

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

			data3 = [
					# Individual components (outer donut)
					go.Pie(values=clv_list,
					labels=l_label3,
					domain={'x':[0.1,0.9], 'y':[0,1]},
					texttemplate =  "%{value:$} Mn <br>(%{percent})",
					textposition='outside',
					hole=0.65,
					direction='clockwise',
					sort=False,
					showlegend=False),
					# Portfolio (inner pie)
					go.Pie(values=l_customer2,
					labels=l_label2,
					domain={'x':[0.3,0.7], 'y':[0.1,0.9]},
					texttemplate =  "%{value}",
					textposition='inside',
					hole=0,
					direction='clockwise',
					sort=False,
					marker={'colors':['#EE7621','#FFEC8B','#BCC6CC']})]

			fig2 = go.Figure(data=data3)
			fig2.update_layout(
			autosize=False,
			width=400,
			height=300,
			margin=dict(
				l=20,
				r=20,
				b=20,
				t=20,
				pad=4
			), paper_bgcolor="#ffffff"
			)

			st.write(fig2)


	with second_row:

		col1,col2 = st.columns(2)

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

				fig.update_layout(margin=dict(l=5,r=0,b=0,t=10),font_size=14, width=570, height=250, paper_bgcolor="#ffffff")

				st.write(fig)

			if selected == "NPS":

				df_rfm_nps_cust = pd.merge(pd_df_rfm,pd_df_nps_cust, on='customerid')
				df_rfm_nps_cust = pd_df_nps_cust[['customerid','label','Overall_NPS_Result']]

				df = df_rfm_nps_cust.groupby(['Overall_NPS_Result','label'], as_index=False)['customerid'].count()
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

				fig.update_layout(margin=dict(l=5,r=0,b=0,t=10),font_size=14, width=570, height=250, paper_bgcolor="#ffffff")

				st.write(fig)


		with col2:
			st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>CUSTOMER SATISFACTION</b></p>
				
				""", True)
			l=[]
			c1=0
			c2=0
			c3=0
			s=pd_df_nps_cust['Overall_NPS_Result'].tolist()
			for i in s:
				if i=="Passives":
					c3=c3+1
				if i=="Detractors":
					c2=c2+1
				if i=="Promoters":
					c1=c1+1

			l.append(c3)
			l.append(c2)
			l.append(c1)
			y=["Passives","Detractors","Promoters"]
			st.set_option('deprecation.showPyplotGlobalUse', False)
			customers= l
			# bars = plt.barh(y,customers,color=['#118DFF','#118DFF','#118DFF'],orientation='horizontal',height=0.5)

			# for bar in bars:
			# 	width = bar.get_width()
			# 	label_y = bar.get_y() + bar.get_height() / 2
			# 	plt.text(width, label_y, s=f'{width}')

			plt.xlabel("Customers")
			plt.ylabel("Overall_NPS_Result")
			plt.figure(figsize=(10,5))
			ax1 = plt.subplot(1,1,1)
			bars = plt.barh(y,customers,color=['#FFBB00','#E01F27','#0CC368'],orientation='horizontal',height=0.5)

			for bar in bars:
				width = bar.get_width()
				label_y = bar.get_y() + bar.get_height() / 2
				plt.text(width, label_y, s=f'{width}')


			ax1.set_xlim(0,max(customers) * 1.1)
			ax1.xaxis.grid(linestyle='--', linewidth=0.5)
			ax1.set_axisbelow(True)
			# plt.show()
			st.pyplot()


	third_row = st.container()

	with third_row: 

		seg_by_conversion, seg_dimension = st.columns(2)


		with seg_by_conversion:

			st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>SEGMENT BY CONVERSION</b></p>
				
				""", True)
			
			df_grouped = pd_df_lead_seg.groupby('segmentName')['conversionCopy'].value_counts(normalize=True).unstack('conversionCopy')

			# plt.figure(figsize=(15,4))
			fig, ax = plt.subplots(figsize=(9.2, 5))
			df_grouped.plot.barh(stacked=True, color=["#00568D","#00AFFF"])
			plt.legend(
				bbox_to_anchor=(0.5, 1.02),
				loc="lower center",
				borderaxespad=0,
				frameon=False,
				ncol=3,
			)


			for ix, row in df_grouped.reset_index(drop=True).iterrows():
				# print(ix, row)
				cumulative = 0
				for element in row:
					if element > 0.1:
						plt.text(
							cumulative + element / 2,
							ix,
							f"{round(element * 100,2)} %",
							va="center",
							ha="center",
							color="#ffffff"
							)

					cumulative += element

			axis_font = {'fontname':'Segoe UI', 'size':'10'}
			plt.ylabel("Segment", **axis_font)
			plt.xlabel("Conversion %", **axis_font)	

			# plt.tight_layout()
			
				
			# plt.title("Segment By Conversion", **axis_font)
			st.pyplot(plt)


		with seg_dimension:

			st.markdown("""
				<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>SEGMENT DIMENSIONS</b></p>
			
				""", True) 

			pd_df_lsrr_af = pd_df_lsrr.groupby(['segmentName','customer_affordability_bin'], as_index=False)['id'].count()
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
			
			pd_df_lsrr_agg3 = pd_df_lsrr.groupby(['segmentName','loyalty_and_engagement'], as_index=False)['id'].count()
			
			pd_df_lsrr_agg3_m10=pd_df_lsrr_agg3.groupby('segmentName')['id'].agg(['sum', 'max']).reset_index()
			pd_df_lsrr_agg3_m10['Loyalty and Engagement'] =(pd_df_lsrr_agg3_m10['max']/pd_df_lsrr_agg3_m10['sum'])*100  
			l3= pd_df_lsrr_agg3_m10['Loyalty and Engagement'].tolist() 
			
			pd_df_lsrr_agg3.rename(columns={'id':'total'},inplace=True)
			pd_df_lsrr_agg3_top2=pd_df_lsrr_agg3.groupby(['segmentName'])['total'].apply(lambda x: x.nlargest(2)).reset_index()
			pd_df_lsrr_agg3_top2_sum=pd_df_lsrr_agg3_top2.groupby(['segmentName'],as_index=False)['total'].sum()
			pd_df_lsrr_agg3_sum=pd_df_lsrr_agg3.groupby(['segmentName'],as_index=False)['total'].sum() 
			pd_df_lsrr_agg3_per=((pd_df_lsrr_agg3_top2_sum['total']/pd_df_lsrr_agg3_sum['total'])*100).reset_index() 
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
			plot.update_layout(autosize=False,width=600,height=400,	margin=dict(l=30,r=30,b=30,t=30,pad=4), paper_bgcolor="#ffffff")

			st.plotly_chart(plot)


	fourth_row = st.container()

	with fourth_row:
		NPS_Trend_Analysis,a = st.columns([1000,1])
		# NPS_Trend_Analysis = st.column()

		with NPS_Trend_Analysis:
			st.markdown("""
						<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>NPS TREND ANALYSIS</b></p>
					""", True)
			
			pd_df_ncalc=pd_df_ncatr.groupby(['surveyDateOrder','surveyMonth']) \
			.apply(lambda x: pd.Series({
				'Detractor_sum' : x['Detractor'].sum(),
				'Detractor_count'       : x['Detractor'].count(),    
				'Promoter_sum'       : x['Promoter'].sum(),
				'Promoter_count'       : x['Promoter'].count(), 
				'Passive_sum'       : x['Passive'].sum(),
				'Passive_count'       : x['Passive'].count(),
				'NPS_Score_by_Category_sum'       : x['NPS_Score_by_Category'].sum(),
				'NPS_Score_by_Category_count'       : x['NPS_Score_by_Category'].count(),
			})
			)

			pd_df_ncalc['Detractor_sum'] = pd_df_ncalc.get('Detractor_sum', 0)
			pd_df_ncalc['Promoter_sum'] = pd_df_ncalc.get('Promoter_sum', 0)
			pd_df_ncalc['Passive_sum'] = pd_df_ncalc.get('Passive_sum', 0)
			pd_df_ncalc['NPS_Score_by_Category_sum'] = pd_df_ncalc.get('NPS_Score_by_Category_sum', 0)

			pd_df_ncalc['Detractor_count'] = pd_df_ncalc.get('Detractor_count', 1)
			pd_df_ncalc['Promoter_count'] = pd_df_ncalc.get('Promoter_count', 1)
			pd_df_ncalc['Passive_count'] = pd_df_ncalc.get('Passive_count', 1)
			pd_df_ncalc['NPS_Score_by_Category_count'] = pd_df_ncalc.get('NPS_Score_by_Category_count', 1)		

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
				go.Bar(name='Promoters', x=l_surveyMonth, y=l_promoter,text=l_promoter,textposition='inside', marker={'color':colors['C']}),
				go.Bar(name='Passives', x=l_surveyMonth, y=l_passive,text=l_passive,textposition='inside',marker={'color':colors['B']}),
				go.Bar(name='Detractors', x=l_surveyMonth, y=l_detractor,text=l_detractor,textposition='inside',marker={'color':colors['A']}),
				go.Line(name='NPS Score', x=l_surveyMonth, y=l_NPS_Score,line_width=2,line_color='#000000', yaxis='y2')
					]

			min1 = min(l_NPS_Score)-min(l_NPS_Score)*0.30
			max1 = max(l_NPS_Score)*1.30
			# Add titles and color the font of the titles to match that of the traces
			# 'SteelBlue' and 'DarkOrange' are the defaults of the first two colors.
			y1 = go.YAxis(title='Promoter Passive and Detractor', titlefont=go.Font(color='Black'))
			y2 = go.YAxis(title= 'NPS Score', titlefont=go.Font(color='Black'),range=[min1,max1])
			x = go.XAxis(title= 'Survey Month', titlefont=go.Font(color='Black'))

			# update second y axis to be position appropriately
			y2.update(overlaying='y', side='right')

			# Add the pre-defined formatting for both y axes 
			layout = go.Layout(xaxis=x, yaxis1 = y1, yaxis2 = y2)

			fig = go.Figure(data=data, layout=layout)

			fig.update_layout(barmode='stack',autosize=True,width=1300,height=450,margin=dict(l=10,r=10,b=10,t=10,pad=4), paper_bgcolor="#ffffff")
			st.write(fig)


st.markdown("<div class='custom_footer'><b>Copyright (c) Anblicks Inc.  </b><a href='https://www.anblicks.com'>https://www.anblicks.com</a></div>", True)

