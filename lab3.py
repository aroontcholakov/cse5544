import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

df_data = pd.read_csv(r'https://raw.githubusercontent.com/aroontcholakov/cse5544/5bff17de181cf117ac0dcfea158ea56aff1dca6a/CSE5544.Lab1.ClimateData.csv', sep=',')
df_data = df_data.drop(columns=['Non-OECD Economies'])
df_data = df_data[df_data['Country\\year'].apply(lambda x: 'OECD' not in x and 'European Union' not in x)]
cols = df_data.columns.drop('Country\\year')
df_data[cols] = df_data[cols].apply(pd.to_numeric, errors='coerce')
data = pd.melt(df_data, id_vars=['Country\year'], var_name='year')
data = data.rename(columns={'Country\year': 'Country'})

st.title('Lab 3: Climate Analysis')


heatmap = alt.Chart(data).mark_rect().encode(
    alt.X('year:O'),
    alt.Y('Country:N', sort='ascending'),
    alt.Color('value:Q', scale=alt.Scale(scheme='inferno')),
    tooltip=['value']
).properties(
    title={
        "text":['CO2 Emissions for Countries (1990-2019)'],
        "subtitle":["Including Countries with both OECD and Non-OECD Economies"]
    }
).configure_title(
    fontSize = 24,
    font='Times New Roman',
    anchor='start',
)

st.altair_chart(heatmap, use_container_width=False)

st.write("The title tells us the type of emissions that were recorded, the years the data was taken, and who the data is from while the subtitle adds some information on the types of countries that were included. The heatmap itself shows each country and year and the color is encoded to the value of the emissions. The inferno color map is much more effective than the color map below because it has greater variation in luminance and the hues are not too similar from one end of the color map to the other. The sinebow color map, which I used below, has red on both sides of the color map so small and large values of emissions could be mapped to the same color. The tooltip pop up shows the value of the CO2 emissions for a more detailed look into the data for a specific country at a specific year.")

scatterplot = alt.Chart(data).mark_circle().encode(
    alt.X('year:O'),
    alt.Y('value:Q', axis=alt.Axis(title='Emissions', labels=False), sort='descending'),
    alt.Color('value:Q', scale=alt.Scale(scheme='sinebow')),
    alt.Size('Country:N', legend=None),
    opacity='value:Q',
    tooltip=['Country']
).properties(
    title='Emissions from 1990 to 2019'
)

st.altair_chart(scatterplot, use_container_width=True)

st.write("The scatterplot has a cyclical color map, reversed Y-axis with no labels, and the size corresponding to Country name. What the color legend does not show is values close to 0 are also mapped to red, so the high values and low values are both red is confusing. I included all the data that is present in the heatmap above, but with the y-axis is reversed so the higher emission values, like 12,000,000, are closer to the x-axis and smaller values are further away. The size is encoded to the name of the Country and the legend is disabled, so it appears that the countries at the top have a larger mark size and higher position which is conventionally associated with bigger values, but that is not the case. When hovering over the points, the tooltip box only shows the country name which is not helpful in reading the graph when an axis is not labeled. The opacity is the emission value which lets the larger marks bleed into one another, making the individual data points harder to read. Lastly, the title is not very descriptive of the chart's information.")
