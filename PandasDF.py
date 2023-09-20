from snowflake.snowpark.session import Session
from Config import connection_parameters
import pandas as pd


session = Session.builder.configs(connection_parameters).create()

snow_df_rfm = session.table('VW_RFM_RESULT')
snow_df_clv = session.table('VW_CLV_RESULT')
snow_df_nps_cat = session.table('VW_NPS_CATEGORY_RESULT')
snow_df_nps_cust = session.table('VW_NPS_CUSTOMER_RESULT')
snow_df_lead_seg = session.table('VW_LEAD_SEGMENTATION_RETAIL_RESULT')
snow_df_ncatr = session.table('VW_NPS_CATEGORY_RESULT_SLIT')
snow_df_lsrr = session.table('VW_LEAD_SEGMENTATION_RETAIL_RESULT')
snow_df_recomm = session.table('VW_RECOMMENDATION_RESULT')
snow_df_ctmtr = session.table('VW_CHANNEL_TRANS_MATRIX_TRANSPOSED_RESULT')
snow_df_cir = session.table('VW_CHANNEL_IMPORTANCE_RESULTS')
snow_df_bestpath = session.table('CUSTOMERAI_DB.MAIN.VW_CHANNEL_DISPLAY_BESTPATH')
snow_df_bestpath1 = session.table('CUSTOMERAI_DB.MAIN.VW_CHANNEL_DISPLAY_BESTPATH1')
snow_df_importance = session.table('CUSTOMERAI_DB.MAIN.VW_CHANNEL_IMPORTANCE_RESULTS')
snow_df_leastpath = session.table('CUSTOMERAI_DB.MAIN.VW_CHANNEL_DISPLAY_LEAST_PATH')
snow_df_q_matrix_csv = session.table('CUSTOMERAI_DB.MAIN.VW_CHANNEL_DISPLAY_MATRIX')
# snow_df_salesai_bestpath1 = session.table('CUSTOMERAI_DB.MAIN.vw_salesai_bestpath1')
snow_df_salesai_incompletepath = session.table('CUSTOMERAI_DB.MAIN.VW_CHANNEL_DISPLAY_INCOMPLETE_PATH')
snow_df_dmd=session.table('CUSTOMERAI_DB.MAIN.VW_DEMAND_FORECAST_PREDICTION')
snow_df_prc=session.table('CUSTOMERAI_DB.MAIN.VW_PRICING_PREDICTION')


npc = session.sql('SELECT _C0,MEMBERSHIP, EMAIL, CUSTOMER_SERVICE, WEBSITE, SOCIAL_MEDIA, STORE, EVENT_FORM FROM CUSTOMERAI_DB.MAIN.CHANNEL_DISPLAY_MATRIX')
npc_df = npc.toPandas()

# Converting Snowpark DataFrames to Pandas DataFrames for Streamlit
pd_df_rfm = snow_df_rfm.to_pandas()
pd_df_clv = snow_df_clv.to_pandas()
pd_df_nps_cat = snow_df_nps_cat.to_pandas()
pd_df_nps_cust = snow_df_nps_cust.to_pandas()
pd_df_lead_seg = snow_df_lead_seg.to_pandas()
pd_df_ncatr = snow_df_ncatr.to_pandas()
pd_df_lsrr= snow_df_lsrr.to_pandas()
pd_df_recomm = snow_df_recomm.to_pandas()
pd_df_ctmtr = snow_df_ctmtr.to_pandas()
pd_df_cir = snow_df_cir.to_pandas()
pd_df_bestpath = snow_df_bestpath.to_pandas()
pd_df_bestpath1 = snow_df_bestpath1.to_pandas()
pd_df_importance = snow_df_importance.to_pandas()
pd_df_leastpath = snow_df_leastpath.to_pandas()
pd_df_q_matrix_csv = snow_df_q_matrix_csv.to_pandas()
pd_df_salesai_bestpath1 = snow_df_bestpath1.to_pandas()
pd_df_salesai_incompletepath = snow_df_salesai_incompletepath.to_pandas()
pd_df_dmd = snow_df_dmd.to_pandas()
pd_df_prc=snow_df_prc.to_pandas()

pd_df_rfm['customerid']=  pd_df_rfm['customerid'].astype(str).astype(int)

pd_df_recomm.rename(columns = {'customerId':'customerid'}, inplace = True)
pd_df_ncatr.rename(columns = {'customerId':'customerid'}, inplace = True)

pd_df_recomm['customerid']=  pd_df_recomm['customerid'].astype(str).astype(int)

npc_df[['MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']] = npc_df[
['MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']].astype(float)
npc_df[['MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']] = npc_df[[
'MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']] * 100
npc_df[['MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']] = npc_df[
['MEMBERSHIP', 'EMAIL', 'CUSTOMER_SERVICE', 'WEBSITE', 'SOCIAL_MEDIA', 'STORE', 'EVENT_FORM']].astype(int)

