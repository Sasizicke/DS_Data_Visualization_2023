# Data Sources: https://www.who.int/data/gho/data/themes/air-pollution/who-air-quality-database/2022, https://www.kaggle.com/code/abmsayem/impact-of-air-pollution-on-human-health/input?select=death-rates-from-air-pollution.csv & https://ourworldindata.org/grapher/PM25-air-pollution

import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import folium
import branca.colormap as cm
import geopandas as gpd
import numpy as np

APP_TITLE = 'Worldwide particulate matter pollution and related death rates'
APP_SUB_TITLE = 'Data Sources: https://www.who.int/data/gho/data/themes/air-pollution/who-air-quality-database/2022, https://www.kaggle.com/code/abmsayem/impact-of-air-pollution-on-human-health/input?select=death-rates-from-air-pollution.csv & https://ourworldindata.org/grapher/PM25-air-pollution'

def display_map_type_filter():
    return st.sidebar.radio('Map Type', ['PM10 (μg/m3) pollution', 'PM2.5 (μg/m3) pollution', 'PM2.5 pollution related death rates (per 100,000)'])

def display_time_filters(df):
    df=df.dropna()
    year_list = list(df['Year'].unique())
    year_list.sort()
    year = st.slider('Select the year', min_value=int(min(year_list)),max_value=int(max(year_list)), step=1)
    return year
    
def display_map(df, year, map_type):
    df = df[(df['Year'] == year)]
    table = df.dropna()
   
   
    pm_m = folium.Map(min_zoom=1, location=(45, 5), zoom_start=2, tiles='cartodb positron', overley=False)

    if map_type == 'PM10 (μg/m3) pollution':
    
        table_pm10 = table[['PM10']]
        table_pm10 = table_pm10.dropna()
    
        try:
            max_colour10 = max(table_pm10['PM10'])
            min_colour10 = min(table_pm10['PM10'])
        except:
            return
    
        pm_10 = folium.Choropleth(
                geo_data="http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson",
                data=table,
                columns=['Code', 'PM10'],
                key_on= "feature.properties.iso_a3",
                fill_color='Reds', #See Brewer pakettes: https://en.wikipedia.org/wiki/Cynthia_Brewer#Brewer_palettes
                nan_fill_color="Gray",
                fill_opacity=0.8,
                line_opacity=0.25,
                legend_name='PM10 (μg/m3) pollution', #title of the legend
                highlight=True,
                line_color='black')
        pm_10.geojson.add_to(pm_m)

        table['Year']= table['Year'].apply(lambda x: str(round(x)))
        
        folium.features.GeoJson(
                    data=table,
                    name='PM10 (μg/m3) pollution',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.3},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Country',
                                'Year',
                                'PM10'
                               ],
                        aliases=['Country: ',
                                'Year: ',
                                'PM10: '
                                ],
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=1200,),
                            highlight_function=lambda x: {'weight':1,'fillColor':'grey'},
                        ).add_to(pm_m)

       
        cmap10 = cm.linear.Reds_09.scale(min_colour10, max_colour10)
        cmap10.add_to(pm_m)
        cmap10.caption = 'PM10 (μg/m3) pollution'
        st.bar_chart(data=table, x='Country', y='PM10')
        
    elif map_type == 'PM2.5 (μg/m3) pollution':
    
    
        table_pm25 = table[['PM2.5']]
        table_pm25 = table_pm25.dropna()
    
        try:
            max_colour25 = max(table_pm25['PM2.5'])
            min_colour25 = min(table_pm25['PM2.5'])
        except:
            return
    
        pm_25 = folium.Choropleth(
                geo_data="http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson",
                data=table,
                columns=['Code', 'PM2.5'],
                key_on= "feature.properties.iso_a3",
                fill_color='Reds', #See Brewer pakettes: https://en.wikipedia.org/wiki/Cynthia_Brewer#Brewer_palettes
                nan_fill_color="Gray",
                fill_opacity=0.8,
                line_opacity=0.25,
                legend_name='PM2.5 pollution', #title of the legend
                highlight=True,
                line_color='black')
        pm_25.geojson.add_to(pm_m)
        
        table['Year']= table['Year'].apply(lambda x: str(round(x)))
        
        folium.features.GeoJson(
                    data=table,
                    name='PM2.5 (μg/m3) pollution',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.3},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Country',
                                'Year',
                                'PM2.5'
                               ],
                        aliases=['Country: ',
                                'Year: ',
                                'PM2.5: '
                                ],
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=1200,),
                            highlight_function=lambda x: {'weight':1,'fillColor':'grey'},
                        ).add_to(pm_m)


        cmap25 = cm.linear.Reds_09.scale(min_colour25, max_colour25)
        cmap25.add_to(pm_m)
        cmap25.caption = 'PM2.5 (μg/m3) pollution'
        #table['pm25'] = table['PM2.5'] #change name so st can work with it
        #t10 = table.sort_values('pm25')['Country'].head(10)
        #st.bar_chart(data=t10, x='Country', y='pm25') #too many countries
        
        
    else:
    
    
        table_pm_d = table[['PMDeaths']]
        table_pm_d = table_pm_d.dropna()
    
        try:
            max_colourd = max(table_pm_d['PMDeaths'])
            min_colourd = min(table_pm_d['PMDeaths'])
        except:
            return
            
            
        pm_d = folium.Choropleth(
                geo_data="http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson",
                data=table,
                columns=['Code', 'PMDeaths'],
                key_on= "feature.properties.iso_a3",
                fill_color='Reds', #See Brewer pakettes: https://en.wikipedia.org/wiki/Cynthia_Brewer#Brewer_palettes
                nan_fill_color="Gray",
                fill_opacity=0.8,
                line_opacity=0.25,
                legend_name='PM2.5 pollution related death rates (riskfactor) per 100,000 individuals', #title of the legend
                highlight=True,
                line_color='black')
        pm_d.geojson.add_to(pm_m)
        
        table['Year']= table['Year'].apply(lambda x: str(round(x)))
        
        folium.features.GeoJson(
                    data=table,
                    name='PM2.5 pollution related death rates (riskfactor) per 100,000 individuals',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.3},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Country',
                                'Year',
                                'PMDeaths'
                               ],
                        aliases=['Country: ',
                                'Year: ',
                                'PMDeaths: '
                                ],
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=1200,),
                            highlight_function=lambda x: {'weight':1,'fillColor':'grey'},
                        ).add_to(pm_m)

        table_pm_d = table[['PMDeaths']]
        table_pm_d = table_pm_d.dropna()
        max_colourd = max(table_pm_d['PMDeaths'])
        min_colourd = min(table_pm_d['PMDeaths'])
        cmapd = cm.linear.Reds_09.scale(min_colourd, max_colourd)
        cmapd.add_to(pm_m)
        cmapd.caption = 'PM2.5 pollution related death rates (riskfactor) per 100,000 individuals'
        #st.bar_chart(data=table, x='Country', y='PMDeaths') #too many countries
        
        
    st_map = st_folium(pm_m, width=1200)
    


def display_pollution_facts(df, year, map_type, metric, title):
    df = df[(df['Year'] == year)]
    df = df.dropna()
    
    if map_type == 'PM10 (μg/m3) pollution':
        m_type = 'PM10'
    elif map_type == 'PM2.5 (μg/m3) pollution':
        m_type = 'PM2.5'
    else:
        m_type = 'PMDeaths'
    
    if metric == 'min_t':
        try:
            total = round(min(df[m_type]),2)
        except:
            total = 'No data for this year'
    elif metric == 'avg_t':
        total = round(df[m_type].median(),2)
    elif metric == 'max_t':
        try:
            total = round(max(df[m_type]),2)
        except:
            total = 'No data for this year'
    elif metric == 'min_c':
        try:
            low = min(df[m_type])
            df = df["Country"][df[m_type] == low]
            total = df.iloc[0]      
        except:
            total = 'No data for this year'
    else:
        try:
            high = max(df[m_type])
            df = df["Country"][df[m_type] == high]
            total = df.iloc[0]
        except:
            total = 'No data for this year'
    st.metric(title, str(total))
    
    
    
def main():
    st.set_page_config(APP_TITLE,layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.loc[world['name'] == 'France', 'iso_a3'] = 'FRA'
    world.loc[world['name'] == 'Norway', 'iso_a3'] = 'NOR'
    world.loc[world['name'] == 'Somaliland', 'iso_a3'] = 'SOM'
    world.loc[world['name'] == 'Kosovo', 'iso_a3'] = 'RKS'
   
    #Display Filters and Map
    map_type = display_map_type_filter()
    
    if map_type == 'PM10 (μg/m3) pollution':
        df = world.merge(pd.read_csv('who_aap_2021_v9_11august2022_clean.csv'), how="left", left_on=['iso_a3'], right_on=['Code'])
        df.loc[df['Country'] == 'France', 'Code'] = 'FRA'
        df.loc[df['Country'] == 'Norway', 'Code'] = 'NOR'
        df.loc[df['Country'] == 'Somaliland', 'Code'] = 'SOM'
        df.loc[df['Country'] == 'Kosovo', 'Code'] = 'RKS'
    elif map_type == 'PM2.5 (μg/m3) pollution':
        df = world.merge(pd.read_csv('PM25-air-pollution.csv'), how="left", left_on=['iso_a3'], right_on=['Code'])
        df.loc[df['Country'] == 'France', 'Code'] = 'FRA'
        df.loc[df['Country'] == 'Norway', 'Code'] = 'NOR'
        df.loc[df['Country'] == 'Somaliland', 'Code'] = 'SOM'
        df.loc[df['Country'] == 'Kosovo', 'Code'] = 'RKS'
    else:
        df = world.merge(pd.read_csv('death-rates-from-air-pollution_clean.csv'), left_on=['iso_a3'], right_on=['Code'])
        df.loc[df['Country'] == 'France', 'Code'] = 'FRA'
        df.loc[df['Country'] == 'Norway', 'Code'] = 'NOR'
        df.loc[df['Country'] == 'Somaliland', 'Code'] = 'SOM'
        df.loc[df['Country'] == 'Kosovo', 'Code'] = 'RKS'
    
    #Extract Year
    year = display_time_filters(df)
    
    #Create Map
    display_map(df, year, map_type)
    
    #Display Metrics
    st.subheader(f'{map_type} facts')

    col1, col2, col3 = st.columns(3)
    with col1:
        display_pollution_facts(df, year, map_type, 'avg_t', f'Median of {map_type}')
    with col2:
        display_pollution_facts(df, year, map_type, 'min_t', f'Min {map_type}')
    with col3:
        display_pollution_facts(df, year, map_type, 'max_t',  f'Max {map_type}')     
        
    col1_1, col1_2= st.columns(2)
    with col1_1:
        display_pollution_facts(df, year, map_type, 'min_c', f'Country with lowest {map_type}')
    with col1_2:
        display_pollution_facts(df, year, map_type, 'max_c', f'Country with highest {map_type}')


if __name__ == "__main__":
    main()