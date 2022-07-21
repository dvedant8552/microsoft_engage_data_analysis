# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:03:27 2022

@author: vsd85
"""

import streamlit as st
import pandas as pd
import numpy as np
import typing_extensions

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set_style('darkgrid')
matplotlib.rcParams['font.size']=6
matplotlib.rcParams['figure.figsize']=[6,3]
matplotlib.rcParams['figure.facecolor']='#00000000'



st.set_page_config(page_title=("individual analysis"),page_icon=":bar_chart:",layout="wide")


car=pd.read_csv('final_dataframe.csv')




st.sidebar.header("Select the company")


make=st.sidebar.selectbox("", car.Make.unique())

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            #background-color: white;
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)







st.title(":bar_chart:Analysis of "+make+" company")
st.markdown("***")

car=pd.read_csv('final_dataframe.csv')

company_df=car[car.Make==make]

lc,rc=st.columns(2)
with lc:
    st.subheader("Total Revenue")
    st.subheader(f"{round(company_df.Total_revenue.sum(),2):,} Billion Rs")
    
with rc :
    st.subheader("Total Sales")
    st.subheader(f"{round(company_df.sale_quantity.sum(),2):,} thousand units")

st.markdown("***")
# adding analysis points

list_of_basis=["Model wise Sales","Body Type wise sales", "Month wise sales","Popular specification combinations I","Price and Fuel Type wise sales","Popular specification combination II","Others"]
st.sidebar.header("Select the Basis")
basis=st.sidebar.radio("",list_of_basis)



  
def quant_vs_model(x) :
    model=car[car.Make==x]
    model_wise_sale=model.groupby('Model')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False)
    
    sns.set(font_scale=1.5)
    plt.xticks(rotation=75)
    plt.title(x +' : Sales for different models')
    
    sns.barplot(model_wise_sale.sale_quantity.index,model_wise_sale.sale_quantity)
    plt.ylabel('Units sold (in Thousands)')
 
def revenue_vs_model(x):
    model=car[car.Make==x]
    model_wise_sale=model.groupby('Model')[['Total_revenue']].sum().sort_values('Total_revenue',ascending=False)
    
    plt.figure(figsize=(12,6))
    sns.set(font_scale=1.5)
    plt.xticks(rotation=75)
    plt.title(x + ': Revenue generated for different models')
    sns.barplot(model_wise_sale.Total_revenue.index,model_wise_sale.Total_revenue)
    plt.ylabel('Revenue (in Billion Rupees)')
 
def body_vs_quant(x):
    model=car[car.Make==x]
    body_wise_sale=model.groupby('Body_Type')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False)
    plt.figure(figsize=(12,6))
    sns.barplot(x=body_wise_sale.sale_quantity, y=body_wise_sale.index)
    plt.title(x +' : Sales for different Car Body Types')
    plt.ylabel('Body Type');
    plt.xlabel('Units Sold (in Thousands)');
    plt.legend(np.round(body_wise_sale.sale_quantity,2));
    
def body_vs_revenue(make):
    model=car[car.Make==make]
    body_wise_sale=model.groupby('Body_Type')[['Total_revenue']].sum().sort_values('Total_revenue',ascending=False)
    plt.figure(figsize=(12,6))
    sns.barplot(x=body_wise_sale.Total_revenue, y=body_wise_sale.index)
    plt.title(make + ': Total revenue generated for different car body types')
    plt.ylabel('Body Types');
    plt.xlabel('Total revenue generated (in Billions)')
    plt.legend(np.round(body_wise_sale.Total_revenue,2));

def fuel_type_vs_model(make) :
    model=car[car.Make==make]
    f=model['Fuel_Type'].value_counts()
    y = np.array(f)
    x=np.array(f.index)
    percent = 100.*y/y.sum()
    plt.pie(y,startangle=90, radius=1.2)
    plt.title(make+ ' : Composition of various fuel consuming cars')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=16)




def month_vs_quant(x):
    model=car[car.Make==x]
    month_wise_sale=model.groupby('sale_month')[['sale_quantity']].sum()
    plt.figure(figsize=(12,6))
    sns.barplot(x=month_wise_sale.index, y=month_wise_sale.sale_quantity)
    plt.title(x + ' : Monthwise sales distribution')
    plt.ylabel('Units sold (in Thousands)');
    plt.xlabel('Month')

def month_vs_revenue(x):
    model=car[car.Make==x]
    month_wise_sale=model.groupby('sale_month')[['Total_revenue']].sum()
    plt.figure(figsize=(12,6))
    sns.barplot(x=month_wise_sale.index, y=month_wise_sale.Total_revenue)
    plt.title(x + ' : Monthwise distribution of generated revenue')
    plt.ylabel('Revenue (in Billion Rupees)');
    plt.xlabel('Month')

    
def emission_norm_vs_model(make) :
    model=car[car.Make==make]
    f=model['Emission_Norm'].value_counts()
    y = np.array(f)
    x=np.array(f.index)
    percent = 100.*y/y.sum()
    plt.pie(y,startangle=90, radius=1.2)
    plt.title(make + ' : Composition of various Emission Norm Types')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=16)

def emissionnorm_vs_sale(make) :
    model=car[car.Make==make]
    fin=model.groupby('Emission_Norm')[['sale_quantity']].sum()
    y = np.array(fin['sale_quantity'])
    x=np.array(fin.index)
    percent = 100.*y/y.sum()
    plt.pie(y,startangle=90, radius=1.2)
    plt.title(make + ' : Composition of Sales for different Emission Norms')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(patches, labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=16)

def sale_quantity_vs_price(make) :
    pd.options.mode.chained_assignment = None
    model=car[car.Make==make]
    mx=model['Ex_Showroom_Price'].max()
    plt.figure(figsize=(12,17))
    sns.set(font_scale=4)
    mx=max(mx,6)
    model['Price_Range']=pd.cut(x=model['Ex_Showroom_Price'], bins=[0,1.5,5,mx+2], labels=['Low Price Range','Medium Price Range','High Price Range'])
    fin=model.groupby('Price_Range')[['sale_quantity']].sum()   
    y = np.array(fin['sale_quantity'])
    x=np.array(fin.index)
    percent = 100.*y/y.sum()
    plt.pie(y,startangle=90, radius=1.2)
    plt.title( make + ' : Composition of Sales for different price segments')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=30)

def fueltype_vs_sale(make) :
    model=car[car.Make==make]
    fin=model.groupby('Fuel_Type')[['sale_quantity']].sum()
    plt.figure(figsize=(10,3))
    y = np.array(fin['sale_quantity'])
    x=np.array(fin.index)
    percent = 100.*y/y.sum()
    sns.set(font_scale=1)
    plt.pie(y,startangle=90, radius=1.2)
    plt.title(make + ' : Distribution of Sales for different fuel types')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=10)


def type_vs_sale(make) :
    model=car[car.Make==make]
    fin=model.groupby('Type')[['sale_quantity']].sum()
    y = np.array(fin['sale_quantity'])
    x=np.array(fin.index)
    percent = 100.*y/y.sum()
    plt.pie(y,startangle=90, radius=1.3)
    plt.title(make + ' : Composition of Sales for different transmission types')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=16)


def type_vs_model(make) :
    model=car[car.Make==make]
    y = np.array(model['Type'].value_counts())
    x=np.array(model['Type'].unique())
    plt.figure(figsize=(6,3))
    percent = 100.*y/y.sum()
    plt.pie(y,startangle=90, radius=1.3)
    plt.title(make + ' : Composition of different transmission types cars')
        
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    plt.legend(labels, loc='best',bbox_to_anchor=(0, 1.), fontsize=16)


def popular_specification_type_emission_fueltype(make) :
    model=car[car.Make==make]
    df=model[['sale_quantity']]
    df['specification']=model['Type']+" "+model['Emission_Norm']+ " "+model['Fuel_Type']
    df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
    plt.figure(figsize=(11,11.5))
    sns.barplot(x=df.sale_quantity, y=df.index)
    plt.title(make + ' : Salewise top popular specification(Transmission, Emission Norm, Fuel)')
    plt.xlabel('Units Sold (in Thousands)');
    plt.ylabel(None)
    plt.legend(np.round(df.sale_quantity,2));



def popular_specification_mileage_bodytype(make):
    model=car[car.Make==make].copy()
    
    condition=model.ARAI_Certified_Mileage.isna()
    model=model[~condition]
    model=model.reset_index(drop=True)
    
    df=model[['sale_quantity']]
    df['mileage']=pd.cut(x=model['ARAI_Certified_Mileage'], bins=[0,12,24,40], labels=['Low Mileage','Medium mileage','High Mileage'])
    df['mileage']=df.mileage.astype(str)
    df['specification']=df['mileage']+" "+model['Body_Type']
    
    df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
    plt.figure(figsize=(11,12))
    sns.set(font_scale=2)
    sns.barplot(x=df.sale_quantity, y=df.index)
    plt.title(make +' : Salewise top popular specifications (Mileage and Car Body Type) ')
    
    plt.ylabel(None);
    plt.xlabel('Units sold (in Thousands)')
    plt.legend(np.round(df.sale_quantity,2),fontsize=20);
   

def popular_specification_price_fueltype(make):
    model=car[car.Make==make]
    df=model[['sale_quantity']]
    mx=model.Ex_Showroom_Price.max()
    mx=max(mx,8)
    sns.set(font_scale=2)
    df['price_range']=pd.cut(x=model['Ex_Showroom_Price'], bins=[0,2,5,mx+2], labels=['Low Price','Medium Price','High Price'])
    df['price_range']=df.price_range.astype(str)
    df['specification']=df['price_range']+" "+model['Fuel_Type']
    
    df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
    plt.figure(figsize=(12,10))
    sns.barplot(x=df.sale_quantity, y=df.index)
    plt.title(make + ' : Salewise Top Popular Specifications(Price range and Fuel type)')
    plt.ylabel(None);
    plt.xlabel('Units sold (in Thousands) ')
    plt.legend(np.round(df.sale_quantity,2),fontsize=20);
    
def popular_specification_type_fueltype_bodytype(make):
    model=car[car.Make==make]
    df=model[['sale_quantity']]
    df['specification']=model['Type']+" "+model['Fuel_Type']+ " "+model['Body_Type']
    df=df.groupby('specification')[['sale_quantity']].sum().sort_values('sale_quantity',ascending=False).head(10)
    sns.set(font_scale=2)
    plt.figure(figsize=(12,11.5))
    sns.barplot(x=df.sale_quantity, y=df.index)
    plt.title(make + ' : Salewise Top Popular Specifications(Transmission, Fuel and Body type)')
    plt.ylabel(None);
    plt.xlabel('Units sold (in Thousands) ')
    plt.legend(np.round(df.sale_quantity,2),fontsize=20);
    
    

st.set_option('deprecation.showPyplotGlobalUse', False)


if basis=='Model wise Sales':
    lc,rc=st.columns(2)
    with lc:
        revenue_vs_model(make)
        st.pyplot()      
    with rc :
        quant_vs_model(make)
        st.pyplot()
        
if basis=='Body Type wise sales':
    lc,rc=st.columns(2)
    with lc:
        body_vs_quant(make)
        st.pyplot()      
    with rc :
        body_vs_revenue(make)
        st.pyplot()
        
if basis=='Month wise sales':
    lc,rc=st.columns(2)
    with lc:
        month_vs_quant(make)
        st.pyplot()      
    with rc :
        month_vs_revenue(make)
        st.pyplot()

if basis=='Popular specification combinations I':
    lc,rc=st.columns(2)
    with lc:
        popular_specification_type_emission_fueltype(make)
        
        st.pyplot()      
    with rc :
        popular_specification_mileage_bodytype(make)
        st.pyplot()
    st.markdown("***")
    st.markdown("**Low Mileage Range : Below 12 km/Litre**")
    st.markdown("**Medium Mileage Range : Between 12 and 24 km/Litre**")
    st.markdown("**High Mileage Range : Above 24 km/Litre**")
        
if basis=='Price and Fuel Type wise sales':
    lc,rc=st.columns(2)
    with lc:
        sale_quantity_vs_price(make)
        st.pyplot()      
    with rc :
        fueltype_vs_sale(make)
        st.pyplot()
    st.markdown("***")
    st.markdown("**Low Price Range : Below 1.5 Million Rs**")
    st.markdown("**Medium Price Range : Between 1.5 Million and 6 Million Rs** ")
    st.markdown("**High Price Range : Above 6 Million Rs** ")
if basis=='Popular specification combination II':
    lc,rc=st.columns(2)
    with lc:
        popular_specification_price_fueltype(make)
        st.pyplot()      
    with rc :
        popular_specification_type_fueltype_bodytype(make)
        st.pyplot()
    st.markdown("***")
    st.markdown("**Low Price Range : Below 1.5 Million Rs**")
    st.markdown("**Medium Price Range : Between 1.5 Million and 6 Million Rs** ")
    st.markdown("**High Price Range : Above 6 Million Rs** ")
        
if basis=='Others':
    lc,rc=st.columns(2)
    with lc:
        fuel_type_vs_model(make)
        st.pyplot()      
    with rc :
        emission_norm_vs_model(make)
        st.pyplot()
    st.markdown("***")    
    lc,rc=st.columns(2)
    with lc:
        type_vs_model(make)
        st.pyplot()      
    with rc :
        type_vs_sale(make)
        st.pyplot()
        
    
        
        

       


    
        
    
