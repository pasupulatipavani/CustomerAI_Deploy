import streamlit as st
import numpy as np
from snowflake.snowpark.session import Session
import pandas
from Config import connection_parameters 
import random

def Recommendation():

    from PandasDF import pd_df_recomm

    with open('style_sum.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    prods = st.container()

    with prods:
        col1, col3 = st.columns([2.1,1.1])
        prods1 = np.sort(pd_df_recomm['categoryPurchased'].unique()).tolist()
        prods2 = prods1.copy()
        prods3 = prods1.copy()
        
        # col1.write(" ")
        # col1.write(" ")
        # col1.markdown("""
        #         <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>Product1</b></p>
                
        #         """, True)
        # col1.write(" ") 
        # col1.write(" ")  
        # col1.markdown("""
        #     <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>Product2</b></p>

        #     """, True)
        # col1.write(" ")
        # col1.write(" ")
        # col1.markdown("""
        #     <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>Product3</b></p>

        #     """, True) 
            

        prod1_selection = col1.selectbox('Select Product 1 ', prods1,index=0)
        prods2.remove(prod1_selection)
        prods3.remove(prod1_selection)
        prod2_selection = col1.selectbox('Select Product 2 ', prods2,index=0)
        prods3.remove(prod2_selection)
        prod3_selection = col1.selectbox('Select Product 3 ', prods3,index=0)
        INPUT_PRODUCT=prod1_selection+','+prod2_selection+','+prod3_selection
        
        
        session = Session.builder.configs(connection_parameters).create()
       
        k=session.call('CUSTOMERAI.MAIN.SP_RECOMMENDER',INPUT_PRODUCT)
        col3.markdown("""
                <p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;"><b>Recommendated Product
                </b></p>
                
                """, True)
       
        #col3.write(k)
        st.write("")
        col3.markdown("""
                        <div class="recomm_prod">
                            <h4>""" +str(k) + """</h4>
                            """, unsafe_allow_html=True)
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ") 
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ") 
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ")
        st.write("                                    ") 
        
        
        
        return 0




