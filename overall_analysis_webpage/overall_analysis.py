# -*- coding: utf-8 -*-
"""
Created on Sat May 28 00:37:08 2022

@author: vsd85
"""
# Overall Analysis 

import streamlit as st
import pandas as pd
import numpy as np
 
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set_style('darkgrid')
matplotlib.rcParams['font.size']=6
matplotlib.rcParams['figure.figsize']=[6,3]
matplotlib.rcParams['figure.facecolor']='#00000000'

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
            
st.set_page_config(page_title=("overall analysis"),page_icon=":bar_chart:",layout="wide")
st.markdown(hide_st_style, unsafe_allow_html=True)


st.set_option('deprecation.showPyplotGlobalUse', False)
car=pd.read_csv('final_dataframe.csv')

st.sidebar.header("Select The Basis")

st.title(":bar_chart:Overall Analysis of Automotive Industry")
st.markdown("***")
list_of_basis=["Top Ten Companies by Sale and Revenue","Price Wise Total Sales", "Body Type wise Sales","Month wise Sales","Popular specification combinations I","Fuel Type Distribution","Popular specification combinations II","Emission Norm Type Distribution", "Transmission Type Distribution"]
    
basis=st.sidebar.radio("",list_of_basis)


if basis=="Top Ten Companies by Sale and Revenue" :
    lc,rc=st.columns(2)
    with lc :
        make_wise_sale=car.groupby('Make')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
        plt.figure(figsize=(12,8))
        sns.set(font_scale = 1.5)

        plt.title('Total Sales for Top Ten Companies', fontsize=20)
        sns.barplot(make_wise_sale.sale_quantity,make_wise_sale.sale_quantity.index)
        plt.xlabel('Units sold (in Thousands)');
        plt.ylabel('Company');
        
        st.pyplot()
    
    with rc :
        make_wise_revenue=car.groupby('Make')[['Total_revenue']].sum().sort_values('Total_revenue',ascending=False).head(10)
        plt.figure(figsize=(12,8))
        sns.set(font_scale = 1.5)
        plt.title('Total Revenue Generated for Car Companies', fontsize=20)
        sns.barplot(make_wise_revenue.Total_revenue,make_wise_revenue.index)
        plt.xlabel('Total Revenue Generated (in Billion Rupees)');
        plt.ylabel('Company');
        
        st.pyplot()
        
if basis=="Price Wise Total Sales" :
    lc,rc=st.columns(2)
    with lc :
        sns.set(font_scale=1.5)

        plt.figure(figsize=(12, 6))
        sns.scatterplot(x='Ex_Showroom_Price', 
                        y='sale_quantity', 
                        s=100,hue='Type',
                        data=car).set(title='Pricewise Total Sales');
        plt.xlabel('Ex Showroom Price(in Million Rupees)');
        plt.ylabel('Units Sold (in Thousands)');
        
        
        st.pyplot()
    
    with rc :
        mx=car['Ex_Showroom_Price'].max()
        car['Price_Range']=pd.cut(x=car['Ex_Showroom_Price'], bins=[0,1.5,5,mx+2e7], labels=['Low Price Range','Medium Price Range','High Price Range'])
        fin=car.groupby('Price_Range')[['sale_quantity']].sum()   
        y = []
        y = np.array(fin['sale_quantity'])
        x=np.array(fin.index)
        percent = 100.*y/y.sum()
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title('Overall Price wise Total Sales')
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=16);
        st.pyplot()
    st.markdown("***")
    st.markdown("**Low Price Range : Below 1.5 Million Rs**")
    st.markdown("**Medium Price Range : Between 1.5 Million and 6 Million Rs** ")
    st.markdown("**High Price Range : Above 6 Million Rs** ")

if basis=="Body Type wise Sales" :
    lc,rc=st.columns(2)
    with lc :
        body_wise_sale=car.groupby('Body_Type')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(7)
        plt.figure(figsize=(12,8))
        sns.barplot(x=body_wise_sale.sale_quantity, y=body_wise_sale.index)
        plt.title('Overall Sales for Different Body Types')
        plt.xlabel('Units sold(in thousands)');
       
        
        st.pyplot()
    
    with rc :
        
        body_wise_sale=car.groupby('Body_Type')[['Total_revenue']].sum().sort_values('Total_revenue',ascending=False).head(7)
        plt.figure(figsize=(12,8))
        sns.barplot(x=body_wise_sale.Total_revenue, y=body_wise_sale.index)
        plt.title('Overall: Revenue for Different Body Types')
        plt.ylabel('Body Type');
        plt.xlabel('Total Revenue in Billion Rupees');
        st.pyplot()
        
    
    
if basis=="Month wise Sales" :
    lc,rc=st.columns(2)
    with lc :
        
        month_wise_sale=car.groupby('sale_month')[['sale_quantity']].sum()
        plt.figure(figsize=(12,6))
        sns.barplot(x=month_wise_sale.index, y=month_wise_sale.sale_quantity)
        plt.title('Overall : Monthwise Sales')
        plt.xlabel('Month');
        plt.ylabel('Units sold(in thousands)');
       
        
        st.pyplot()
    
    with rc :
        
        month_wise_sale=car.groupby('sale_month')[['Total_revenue']].sum()
        plt.figure(figsize=(12,6))
        sns.barplot(x=month_wise_sale.index, y=month_wise_sale.Total_revenue)
        plt.title('Overall : Monthwise Revenue Generated')
        plt.ylabel('Revenue(in Billion Rupees)');
        plt.xlabel('Month');
        
        
        
        st.pyplot()


if basis=="Fuel Type Distribution" :
    lc,rc=st.columns(2)
    with lc :
        f=car['Fuel_Type'].value_counts()
        y = np.array(f)
        x=np.array(f.index)
        percent = 100.*y/y.sum()
        plt.figure(figsize=(12,6))
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title('Composition of Number of Various Fuel Consuming Cars', fontsize=16)
                
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=12);
        
        st.pyplot()
    
    with rc :
        y = []
        fin=car.groupby('Fuel_Type')[['sale_quantity']].sum()
        y = np.array(fin['sale_quantity'])
        plt.figure(figsize=(10,5))
        x=np.array(fin.index)
        percent = 100.*y/y.sum()
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title(' Fuel Type wise Total Sales', fontsize=12)
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=10);
        st.pyplot()
        
        
        


if basis=="Emission Norm Type Distribution" :
    lc,rc=st.columns(2)
    with lc :
        f=car['Emission_Norm'].value_counts()
        y = np.array(f)
        x=np.array(f.index)
        percent = 100.*y/y.sum()
        plt.figure(figsize=(12,12))
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title('Composition of Number of Various Emission Norm Types of Cars')
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=30);
        st.pyplot()
    
    with rc :
        y = []
        fin=car.groupby('Emission_Norm')[['sale_quantity']].sum()
        y = np.array(fin['sale_quantity'])
        x=np.array(fin.index)
        percent = 100.*y/y.sum()
        plt.figure(figsize=(12,10))
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title('Emission Norm wise Distribution of Sales')
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=30);
        
        
        
        
        
        
        st.pyplot()
        
        
if basis=="Transmission Type Distribution" :
    lc,rc=st.columns(2)
    with lc :
        y = []
        fin=car.groupby('Type')[['sale_quantity']].sum()
        y = np.array(fin['sale_quantity'])
        plt.figure(figsize=(12,8))
        x=np.array(fin.index)
        percent = 100.*y/y.sum()
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title('Total Sales Distribution for Different Transmission Types')
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=16);
        
      
       
        
        st.pyplot()
    
    with rc :
        f=car['Type'].value_counts()
        y = np.array(f)
        plt.figure(figsize=(12,8))
        x=np.array(f.index)
        percent = 100.*y/y.sum()
        patches, texts = plt.pie(y,startangle=90, radius=1.2)
        plt.title('Composition of Number of Various Transmission Types of Cars')
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]
        plt.legend(patches, labels, loc='best',bbox_to_anchor=(-0.1, 1.), fontsize=16);
        
        
        
        
        
        st.pyplot()
        
        
if basis=="Popular specification combinations I" :
    lc,rc=st.columns(2)
    with lc :
        
        df=car[['sale_quantity']]
        pd.options.mode.chained_assignment = None
        df['specification']=car['Type']+" "+car['Emission_Norm']+ " "+car['Fuel_Type']
        df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
        plt.figure(figsize=(12,10))
        sns.set(font_scale=1.5)
        sns.barplot(x=df.sale_quantity, y=df.index)
        plt.title('Overall : Salewise Top Popular Specifications (Transmission, Emission Norm, and Fuel Type)')
        plt.ylabel(None);
        plt.xlabel('Units sold(in thousands)')
        plt.legend(np.round(df.sale_quantity,2));
        
      
       
        
        st.pyplot()
    
    with rc :
        
        car_copy=car.copy()
        condition=car_copy.ARAI_Certified_Mileage.isna()
        car_copy=car_copy[~condition]
        car_copy=car_copy.reset_index(drop=True)
        
        
        df=car_copy[['sale_quantity']]
        df['mileage']=pd.cut(x=car_copy['ARAI_Certified_Mileage'], bins=[0,12,24,50], labels=['Low Mileage','Medium mileage','High Mileage'])
        df['mileage']=df.mileage.astype(str)
        df['specification']=df['mileage']+" "+car_copy['Body_Type']
            
        df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
        plt.figure(figsize=(18,15))
        sns.set(font_scale=2)
        sns.barplot(x=df.sale_quantity, y=df.index)
        plt.title('Overall : Salewise Top Popular Specifications (Mileage and Body Type)')
        plt.ylabel(None);
        plt.xlabel('Units sold(in thousands)');
        plt.legend(np.round(df.sale_quantity,2),fontsize=20);
        
        st.pyplot()
                        
        
        
        
        
        
    st.markdown("***")
    st.markdown("**Low Mileage Range : Below 12 km/Litre**")
    st.markdown("**Medium Mileage Range : Between 12 and 24 km/Litre**")
    st.markdown("**High Mileage Range : Above 24 km/Litre**")
        

if basis=="Popular specification combinations II" :
    lc,rc=st.columns(2)
    with lc :
        df=car[['sale_quantity']]
        df['price_range']=pd.cut(x=car['Ex_Showroom_Price'], bins=[0,2e6,5e6,car.Ex_Showroom_Price.max()+2e7], labels=['Low Price','Medium Price','High Price'])
        df['price_range']=df.price_range.astype(str)
        df['specification']=df['price_range']+" "+car['Fuel_Type']
        df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
        plt.figure(figsize=(12,10))
        sns.barplot(x=df.sale_quantity, y=df.index)
        plt.title('Overall : Salewise top Popular specifications (Price Range and Fuel Type)')
        plt.ylabel(None);
        plt.xlabel('Units sold (in Thousands)')
        plt.legend(np.round(df.sale_quantity,2),fontsize=20, loc='lower right');
        
        st.pyplot()
    
    with rc :
         
         df=car[['sale_quantity']]
         df['specification']=car['Type']+" "+car['Fuel_Type']+ " "+car['Body_Type']
         df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
         sns.set(font_scale=2)
         plt.figure(figsize=(12,10.5))
         sns.barplot(x=df.sale_quantity, y=df.index)
         plt.title('Overall: Salewise Top Popular Specifications(Transmission, Fuel and Body type)')
         plt.ylabel(None);
         plt.xlabel('Units sold (in Thousands) ')
         plt.legend(np.round(df.sale_quantity,2),fontsize=20);
        
        
         st.pyplot()
         
    st.markdown("***")
    st.markdown("**Low Price Range : Below 1.5 Million Rs**")
    st.markdown("**Medium Price Range : Between 1.5 Million and 6 Million Rs** ")
    st.markdown("**High Price Range : Above 6 Million Rs** ")
        


    
    

        
        
        
   
    

    
    
    
    
    
