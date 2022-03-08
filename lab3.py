import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

df_data = pd.read_csv('https://github.com/aroontcholakov/cse5544/blob/5bff17de181cf117ac0dcfea158ea56aff1dca6a/CSE5544.Lab1.ClimateData.csv', sep=',')
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
    size='value:Q',
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
# st.text("")


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

st.text("")
